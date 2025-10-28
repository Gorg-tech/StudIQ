import os
import sys
import django
import json
import re

def setup_django():
    """
    Sets up the Django environment to allow the script to use the ORM.
    This needs to be called before importing any Django models.
    """
    # The script is in src/server/scraper/, the Django project root is src/server/
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(project_path)
    
    # The settings module is likely 'server.settings' if your project is named 'server'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

def populate_database():
    """
    Main function to read JSON files and populate the database.
    """
    # Import models after Django is set up
    from quizzes.models import Studiengang, Modul

    # Define paths to the JSON files within the scraper directory
    scraper_dir = os.path.dirname(__file__)
    programs_file_path = os.path.join(scraper_dir, 'htw_programs_with_modulux_details.json')
    modules_file_path = os.path.join(scraper_dir, 'htw_modules.json')

    # --- Step 1: Populate Studiengang ---
    print('--- Starting to populate Studiengang data ---')
    try:
        with open(programs_file_path, 'r', encoding='utf-8') as f:
            programs_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {programs_file_path}")
        return
    except json.JSONDecodeError:
        print(f"ERROR: Error decoding JSON from {programs_file_path}")
        return

    created_programs_count = 0
    updated_programs_count = 0
    for program in programs_data:
        details = program.get('details', {})
        program_id = details.get('Studiengangsnummer')
        
        if not program_id:
            print(f"WARNING: Skipping program due to missing 'Studiengangsnummer': {program.get('programName')}")
            continue

        program_name = details.get('Studiengang', program.get('programName', 'N/A'))
        
        # Clean up the name
        program_name = program_name.replace(program_id, '').strip()

        studiengang, created = Studiengang.objects.update_or_create(
            id=program_id,
            defaults={
                'name': program_name,
                'description': f"Abschluss: {details.get('Abschluss', 'N/A')}, Regelstudienzeit: {details.get('Regelstudienzeit', 'N/A')}",
                'modulux_url': program.get('moduluxLink', '')
            }
        )
        if created:
            created_programs_count += 1
        else:
            updated_programs_count += 1
    
    print(f'Finished Studiengang: {created_programs_count} created, {updated_programs_count} updated.')

    # --- Step 2: Populate Modul and link to Studiengang ---
    print('\n--- Starting to populate Modul data ---')
    try:
        with open(modules_file_path, 'r', encoding='utf-8') as f:
            modules_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {modules_file_path}")
        return
    except json.JSONDecodeError:
        print(f"ERROR: Error decoding JSON from {modules_file_path}")
        return

    # --- Filter for the latest version of each module ---
    latest_modules = {}
    for module_data in modules_data:
        module_number_raw = module_data.get('moduleNumber')
        if not module_number_raw:
            continue

        # Extract base ID (e.g., M175)
        id_match = re.search(r'([A-Z]\d+)', module_number_raw)
        if not id_match:
            continue
        base_id = id_match.group(1)

        # Extract version
        version_match = re.search(r'Version: (\d+)', module_number_raw)
        version = int(version_match.group(1)) if version_match else 1

        if base_id not in latest_modules or version > latest_modules[base_id]['version']:
            latest_modules[base_id] = {'version': version, 'data': module_data}

    created_modules_count = 0
    updated_modules_count = 0
    linked_relations_count = 0
    
    for base_id, module_info in latest_modules.items():
        module_data = module_info['data']
        module_id = base_id # Use the cleaned base ID

        # Extract credits as integer
        credits_str = module_data.get('credits', '0').split(' ')[0]
        try:
            credits = int(float(credits_str))
        except (ValueError, TypeError):
            credits = 0

        # Clean module name
        module_name = module_data.get('moduleName', 'N/A').split('\n')[0].strip()

        # Clean up responsible and examinations fields
        responsible_raw = module_data.get('responsible', 'N/A')
        responsible = ' '.join(responsible_raw.split())

        examinations_raw = module_data.get('examinations', 'N/A')
        examinations = ' '.join(examinations_raw.split())

        modul, created = Modul.objects.update_or_create(
            modulId=module_id,
            defaults={
                'name': module_name,
                'description': f"Verantwortlich: {responsible}\nPrüfungen: {examinations}",
                'credits': credits,
                'semester': 0, # Default
                'modulux_url': module_data.get('moduluxLink', '')
            }
        )
        if created:
            created_modules_count += 1
        else:
            updated_modules_count += 1

        # Link module to Studiengang
        curriculum_text = module_data.get('curriculum', '')
        # Find all program IDs (e.g., 'L32', 'W71') in the curriculum text
        program_ids_in_curriculum = re.findall(r'([A-Z]\d{2,3}) –', curriculum_text)
        
        for prog_id in set(program_ids_in_curriculum):
            try:
                studiengang_obj = Studiengang.objects.get(id=prog_id)
                modul.studiengang.add(studiengang_obj)
                linked_relations_count += 1
            except Studiengang.DoesNotExist:
                print(f"WARNING: Studiengang with ID '{prog_id}' not found for module '{module_id}'.")

    print(f'Finished Modul: {created_modules_count} created, {updated_modules_count} updated.')
    print(f'Created {linked_relations_count} links between modules and programs.')
    print('\nDatabase population complete.')


if __name__ == '__main__':
    print("Setting up Django environment...")
    setup_django()
    print("Starting database population...")
    populate_database()