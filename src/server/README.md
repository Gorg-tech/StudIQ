# StudIQ API

## Datenbank
- SQLite (automatisch als `db.sqlite3` erstellt)
- Nach Modelländerungen: `python manage.py makemigrations && python manage.py migrate`

## API-Endpoints

### User
- `/api/accounts/register/` (POST) - Registrierung
- `/api/accounts/login/` (POST) - Login (gibt Token zurück)

### Quiz
- `/api/quizzes/quizzes/` - Quiz-Verwaltung
- `/api/quizzes/questions/` - Fragen-Verwaltung
- `/api/quizzes/lernsets/` - Lernset-Verwaltung

## Authentifizierung
Nach Login/Register erhaltenen Token im Header verwenden. Der Token muss im Authorization-Header im Format `Token <dein-token>` mitgesendet werden.

**Beispiel:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Server starten
```
cd src/server
python manage.py runserver
```

## Administration
### Admin-Zugang
Für die Entwicklung ist ein gemeinsamer Admin-Account eingerichtet:
- Benutzername: `admin`
- Passwort: `admin`

Ein eigener Superuser kann optional erstellt werden:
```
python manage.py createsuperuser
```

### Admin-Panel
Das Admin-Panel ist nach Server-Start verfügbar unter:
```
http://127.0.0.1:8000/admin/
```
Hier lassen sich User, Quizze, Lernsets und weitere Daten verwalten.

## Version Control
**Kleiner Hinweis:** Während der Entwicklung checken wir die `db.sqlite3` Datei mit ins GitHub-Repo ein - macht den Einstieg einfacher für alle.

**Ist eigentlich nicht so der Bringer und auch nicht ganz ungefährlich!** In der Datenbank stecken sensible Infos wie Passwort-Hashes und persönliche Daten.

Für die richtige Produktion sollte die Datei definitiv in die `.gitignore` wandern!