import json
import time
import argparse  # Neu hinzugefügt für Kommandozeilenargumente
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class ModuluxScraper:
    def __init__(self, headless=True):
        """
        Initialisiert den ModuluxScraper
        
        Args:
            headless (bool): Browser im Headless-Modus starten
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        self.browser = webdriver.Chrome(options=options)
    
    def scrape_modulux(self, mode='both'):
        """
        Scrape Studiengänge und/oder deren Module aus der ModulX-Webseite
        
        Args:
            mode (str): 'programs' für nur Studiengänge, 'modules' für nur Module, 'both' für beides
        """
        try:
            if mode in ['programs', 'both']:
                print('Navigiere zur Modulux-Webseite für Studiengänge...')
                self.browser.get('https://apps.htw-dresden.de/modulux/frontend/studiengaenge')
                
                # Warte auf "Alle anzeigen" Button
                print('Warte auf "Alle anzeigen" Button...')
                wait = WebDriverWait(self.browser, 30)
                show_all_elements = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.tx-ezqueries-link.page-link.text-nowrap'))
                )
                
                # Finde und klicke "Alle anzeigen" Button
                for button in show_all_elements:
                    if "Alle anzeigen" in button.text:
                        print('Klicke "Alle anzeigen" Button...')
                        button.click()
                        break
                
                # Warte bis Tabelle vollständig geladen ist
                print('Warte auf vollständige Ladung der Tabelle...')
                wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 
                          'table.table.table-striped tbody tr.tx-ezqueries-list-row')) > 10)
                
                # Extrahiere Daten der Studiengänge
                print('Extrahiere Studiengangsdaten...')
                programs = self._extract_programs()
                print(f'Gefunden: {len(programs)} Studiengänge')
                
                if mode == 'programs':
                    # Speichere nur Studiengänge
                    with open('htw_programs.json', 'w', encoding='utf-8') as f:
                        json.dump(programs, f, ensure_ascii=False, indent=2)
                    print('Studiengangsdaten gespeichert in htw_programs.json')
                    return programs
            
            if mode in ['modules', 'both']:
                if mode == 'modules':
                    # Navigiere direkt zur Modulseite
                    print('Navigiere zur Modulux-Webseite für Module...')
                    self.browser.get('https://apps.htw-dresden.de/modulux/frontend/module')
                    
                    # Warte auf "Alle anzeigen" Button
                    print('Warte auf "Alle anzeigen" Button...')
                    wait = WebDriverWait(self.browser, 30)
                    show_all_elements = wait.until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.tx-ezqueries-link.page-link.text-nowrap'))
                    )
                    
                    # Finde und klicke "Alle anzeigen" Button
                    for button in show_all_elements:
                        if "Alle anzeigen" in button.text:
                            print('Klicke "Alle anzeigen" Button...')
                            button.click()
                            break
                    
                    # Warte bis Tabelle vollständig geladen ist
                    print('Warte auf vollständige Ladung der Tabelle...')
                    wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 
                              'table.table.table-striped tbody tr.tx-ezqueries-list-row')) > 10)
                    
                    # Extrahiere alle Module direkt
                    all_modules = self._extract_modules()
                    print(f'Gefunden: {len(all_modules)} Module')
                
                else:
                    # Für 'both' oder wenn Studiengänge bereits geladen, sammle Module aus Studiengängen
                    all_modules = []
                    # Besuche die Detailseite jedes Studiengangs und extrahiere Module
                    for i, program in enumerate(programs):
                        if program['moduluxLink']:
                            print(f'Verarbeite Studiengang {i+1}/{len(programs)}: {program["programName"]} für Module')
                            try:
                                self.browser.get(program['moduluxLink'])
                                modules = self._extract_modules()
                                # Füge Programm-Info zu jedem Modul hinzu
                                for module in modules:
                                    module['programName'] = program['programName']
                                    module['programNumber'] = program['programNumber']
                                all_modules.extend(modules)
                            except Exception as e:
                                print(f'Fehler bei Modulen für Studiengang {program["programName"]}:', str(e))
                
                # Speichere alle Module
                with open('htw_modules.json', 'w', encoding='utf-8') as f:
                    json.dump(all_modules, f, ensure_ascii=False, indent=2)
                print(f'Moduledaten gespeichert in htw_modules.json ({len(all_modules)} Module)')
                
                if mode == 'modules':
                    return all_modules
            
            if mode == 'both':
                # Besuche die Detailseite jedes Studiengangs für Details und Module
                for i, program in enumerate(programs):
                    if program['moduluxLink']:
                        print(f'Verarbeite Studiengang {i+1}/{len(programs)}: {program["programName"]}')
                        try:
                            self._get_program_details(program)
                        except Exception as e:
                            print(f'Fehler bei Studiengang {program["programName"]}:', str(e))
                            program['detailsError'] = str(e)
                
                # Speichere Ergebnisse
                with open('htw_programs_with_modulux_details.json', 'w', encoding='utf-8') as f:
                    json.dump(programs, f, ensure_ascii=False, indent=2)
                
                print('Daten gespeichert in htw_programs_with_modulux_details.json')
                return programs
            
        except Exception as e:
            print('Scraping fehlgeschlagen:', str(e))
            self.browser.save_screenshot('error.png')
            print('Screenshot gespeichert als error.png')
            raise
        finally:
            self.browser.quit()
            print('Browser geschlossen')
    
    def _extract_programs(self):
        """Extrahiert die Studiengangsdaten aus der Tabelle"""
        rows = self.browser.find_elements(By.CSS_SELECTOR, 'table.table.table-striped tbody tr.tx-ezqueries-list-row')
        print(f'Gefunden: {len(rows)} Zeilen in der Tabelle')
        
        programs = []
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, 'th, td')
            
            # Extrahiere Modulux-Link
            modulux_link_cell = row.find_element(By.CSS_SELECTOR, 'td.tx-ezqueries-list-data-stg_modulux_link_value')
            modulux_link = None
            try:
                link_element = modulux_link_cell.find_element(By.TAG_NAME, 'a')
                modulux_link = link_element.get_attribute('href')
            except:
                pass
            
            program = {
                'programNumber': cells[1].text.strip() if len(cells) > 1 else '',
                'programName': cells[2].text.strip() if len(cells) > 2 else '',
                'degree': cells[3].text.strip() if len(cells) > 3 else '',
                'firstEnrollment': cells[4].text.strip() if len(cells) > 4 else '',
                'status': cells[5].text.strip() if len(cells) > 5 else '',
                'moduluxLink': modulux_link or '',
                'details': {}
            }
            programs.append(program)
        
        return programs
    
    def _get_program_details(self, program):
        """Holt Detailinformationen und Module von der Modulux-Seite eines Studiengangs"""
        self.browser.get(program['moduluxLink'])
        
        # Warte auf Laden der Details
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tx-ezqueries-detail-rows')))
        
        # Extrahiere detaillierte Informationen
        rows = self.browser.find_elements(By.CSS_SELECTOR, '.tx-ezqueries-detail-row')
        details = {}
        
        for row in rows:
            try:
                label_element = row.find_element(By.CSS_SELECTOR, '.tx-ezqueries-detail-label')
                data_element = row.find_element(By.CSS_SELECTOR, '.tx-ezqueries-detail-data')
                
                label = label_element.text.strip()
                value = data_element.text.strip()
                
                # Bereinige den Wert
                value = ' '.join(value.split())
                
                # Spezialfall: E-Mail-Adressen
                if 'verantwortliche' in label.lower():
                    try:
                        email_link = data_element.find_element(By.CSS_SELECTOR, 'a[data-mailto-token]')
                        value = email_link.text.strip()
                    except:
                        pass
                
                # Spezialfall: Links in Ordnungen
                if label == 'Ordnungen':
                    links = data_element.find_elements(By.TAG_NAME, 'a')
                    link_data = []
                    
                    for link in links:
                        link_text = link.text.strip()
                        link_href = link.get_attribute('href')
                        
                        # Versuche, das gültig-ab Datum zu finden
                        valid_from = ''
                        try:
                            # Nimmt an, dass das Datum im nächsten Element nach dem Link steht
                            script = "return arguments[0].nextElementSibling.textContent;"
                            valid_from = self.browser.execute_script(script, link).strip()
                        except:
                            pass
                        
                        link_data.append({
                            'text': link_text,
                            'href': link_href,
                            'validFrom': valid_from
                        })
                    
                    details[label] = link_data
                else:
                    details[label] = value
            except:
                pass
        
        # Jetzt Module extrahieren
        modules = self._extract_modules()
        details['modules'] = modules
        
        program['details'] = details
    
    def _extract_modules(self):
        """Extrahiert die Moduldaten aus der Tabelle auf der Modulseite oder Studiengangsseite"""
        # Schaue nach "Alle anzeigen" Button für Module
        # Temporär auskommentiert für Testzwecke
        # try:
        #     show_all_elements = self.browser.find_elements(By.CSS_SELECTOR, 'a.tx-ezqueries-link.page-link.text-nowrap')
        #     for button in show_all_elements:
        #         if "Alle anzeigen" in button.text:
        #             print('Klicke "Alle anzeigen" für Module...')
        #             button.click()
        #             break
        # except:
        #     pass  # Falls kein Button vorhanden
        
        # Warte bis Modul-Tabelle vollständig geladen ist
        wait = WebDriverWait(self.browser, 30)
        try:
            wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 
                      'table.table.table-striped tbody tr.tx-ezqueries-list-row')) > 0)
        except TimeoutException:
            print('Keine Module gefunden oder Timeout')
            return []
        
        rows = self.browser.find_elements(By.CSS_SELECTOR, 'table.table.table-striped tbody tr.tx-ezqueries-list-row')
        print(f'Gefunden: {len(rows)} Module')
        
        modules = []
        for i, row in enumerate(rows):
            if i % 100 == 0:
                print(f'Verarbeite Modul {i+1}/{len(rows)}...')
            cells = row.find_elements(By.CSS_SELECTOR, 'th, td')
            
            # Helper function to get text content from a cell
            def get_cell_text(cell_index):
                if len(cells) > cell_index and cells[cell_index]:
                    return self.browser.execute_script("return arguments[0].textContent;", cells[cell_index]).strip()
                return ''

            # Korrigierte Indizes und Extraktionsmethode
            module = {
                'moduleNumber': get_cell_text(2),
                'moduleName': get_cell_text(3),
                'credits': get_cell_text(5),
                'lecturers': get_cell_text(6),
                'responsible': get_cell_text(7),
                'examinations': get_cell_text(8),
                'prerequisites': get_cell_text(9),
                'languages': get_cell_text(10),
                'startSemester': get_cell_text(11),
                'curriculum': get_cell_text(12),
                'moduluxLink': '',
                'sdgs': get_cell_text(14)
            }
            
            # Extrahiere Modulux-Link falls vorhanden (Index 13)
            try:
                link_cell = cells[13] if len(cells) > 13 else None
                if link_cell:
                    link_element = link_cell.find_element(By.TAG_NAME, 'a')
                    module['moduluxLink'] = link_element.get_attribute('href')
            except:
                pass
            
            modules.append(module)
        
        return modules


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Modulux Daten.')
    parser.add_argument('--mode', choices=['programs', 'modules', 'both'], default='both', help='Modus: programs für Studiengänge, modules für Module, both für beides')
    args = parser.parse_args()
    
    scraper = ModuluxScraper(headless=False)
    scraper.scrape_modulux(mode=args.mode)