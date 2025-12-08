# StudIQ API
---
# todo (fehlt noch)
```
POST /api/quizzes/{id}/start/     – Quiz starten
POST /api/quizzes/{id}/complete/  – Quiz beenden
GET /api/quizzes/{id}/session/    – Aktuelle Session abrufen (falls vorhanden)
GET /api/studiengaenge/{id}/modules/           – Module eines Studiengangs
GET /api/lernsets/{lernsetId}/quizzes/         – Quizze eines Lernsets  
```
---

## Datenbank & Administration
- SQLite (automatisch als `db.sqlite3` erstellt)
 - Alternatively you can configure a remote MySQL/MariaDB server and connect using environment variables (see `README_MYSQL.md`).
- Nach Modelländerungen:  
  ```bash
  python manage.py makemigrations && python manage.py migrate
  ```
- **Datenbank initialisieren (nach Klonen des Projekts):**
  ```bash
  python manage.py migrate
  python scraper/populate_db.py
  ```
- **Admin-Zugang für Entwicklung:**  
  - Benutzername: `admin`  
  - Passwort: `admin`
- Eigenen Superuser anlegen (optional):  
  ```bash
  python manage.py createsuperuser
  ```
- Admin-Panel nach Server-Start erreichbar unter:  
  [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
  Hier lassen sich User, Quizze, Lernsets und weitere Daten verwalten.

## Verwendung eines entfernten MySQL/MariaDB-Servers

Um eine Verbindung zur entfernten MySQL-Datenbank herzustellen:

1. Kopiere die Beispiel-Umgebungsdatei:
   ```bash
   cp .env.sample .env
   ```

2. Bearbeite `.env` und setze das korrekte `DB_PASSWORD`.

## Authentifizierung
Die Authentifizierung erfolgt über Cookie-basierte Sessions. Bei erfolgreichem Login/Register wird ein Session-Cookie gesetzt, das bei nachfolgenden Anfragen automatisch mitgesendet wird.

Vorteile dieser Methode:
- Sicherere Lösung als Token im Local Storage
- CSRF-Schutz durch Django's CSRF-Mechanismus
- Automatische Session-Verwaltung

## Server starten
```bash
cd src/server
python manage.py runserver
```
## API-Endpoints

### Authentifizierung
- `POST /api/auth/register/` – Neuen Benutzer registrieren
- `POST /api/auth/login/` – Benutzer anmelden
- `POST /api/auth/logout/` – Benutzer abmelden

### User
- `GET /api/users/me/` – Eigene Benutzerdaten abrufen
- `PUT /api/users/me/` – Eigene Benutzerdaten aktualisieren
- `GET /api/users/me/stats` – Der Rank und die Statistiken des self-users
- `GET /api/users/me/streaks` – Die Streak- und Streaktage
- **Freunde**
  - `GET /api/users/me/friends` - Freundesliste abrufen
  - `GET /api/users/me/friend-requests` - Alle Freundesanfragen an einen selbst abrufen
  - `POST /api/users/me/friend-requests` - Freundesanfage an jemanden senden oder akzeptieren
  - `DELETE /api/users/me/friend-requests` - Freundesanfang von jemandem ablehnen

### Suche
 - `GET /api/search/?q={query}&filter={type}` – Suche über alle Inhalte
   - **Parameter:**
     -   `q` (optional): Suchbegriff
     -   `filter` (optional): lernsets, quizzes, modules, studiengaenge
     -   Ohne Parameter werden die ersten Einträge zurückgegeben
     -   Mit Filter werden nur Ergebnisse des angegebenen Typs zurückgegeben

### Studiengänge
- `GET /api/studiengaenge/` – Alle Studiengänge abrufen
- `GET /api/studiengaenge/{id}/` – Einzelnen Studiengang abrufen
- `POST /api/studiengaenge/` – Neuen Studiengang anlegen (nur Moderator/Lecturer)
- `PUT /api/studiengaenge/{id}/` – Studiengang aktualisieren (nur Moderator/Lecturer)
- `DELETE /api/studiengaenge/{id}/` – Studiengang löschen (nur Moderator/Lecturer)

### Module
- `GET /api/modules/{id}/` – Einzelnes Modul abrufen
- `POST /api/modules/` – Neues Modul anlegen (nur Moderator/Lecturer)
- `PUT /api/modules/{id}/` – Modul aktualisieren (nur Moderator/Lecturer)
- `DELETE /api/modules/{id}/` – Modul löschen (nur Moderator/Lecturer)
- `GET /api/modules/{moduleId}/lernsets/` – Alle Lernsets eines Moduls abrufen

### Lernsets
- `GET /api/lernsets/{id}/` – Einzelnes Lernset abrufen
- `POST /api/lernsets/` – Neues Lernset anlegen
- `PUT /api/lernsets/{id}/` – Lernset aktualisieren (nur Ersteller oder Moderator)
- `DELETE /api/lernsets/{id}/` – Lernset löschen (nur Ersteller oder Moderator)

### Quizze
- `GET /api/quizzes/{id}/` – Einzelnes Quiz abrufen
- `POST /api/quizzes/` – Neues Quiz anlegen
- `PUT /api/quizzes/{id}/` – Quiz aktualisieren (nur Ersteller oder Moderator)
- `DELETE /api/quizzes/{id}/` – Quiz löschen (nur Ersteller oder Moderator)
- `GET /api/quizzes/{quizId}/questions/` – Alle Fragen eines Quiz abrufen

### Fragen
  Fragen und Antworten werden beim Abrufen eines Quiz über den Endpunkt  
  `GET /api/quizzes/{id}/` direkt mitgeliefert.  
  Es ist kein separater API-Call für die Fragen eines Quiz notwendig.
  (noch nicht implementiert)

### Antworten
- `GET /api/answer-options/{id}/` Einzelne Antwortoption abrufen
- `POST /api/answer-options/` Neue Antwortoption erstellen (question im Body)
- `PUT /api/answer-options/{id}` Antwortoption aktualisieren
- `DELETE /api/answer-options/{id}` Antwortoption löschen

### Quiz-Fortschritt
- `GET /api/progress/` – Eigenen Quiz-Fortschritt für alle Quizze abrufen
- `GET /api/progress/{id}/` – Fortschritt für einen bestimmten Eintrag abrufen
- `POST /api/progress/` – Neuen Fortschritt speichern
- `PUT /api/progress/{id}/` – Fortschritt aktualisieren

### Quiz-Sitzungen
- `GET /api/sessions/` – Eigene Quiz-Sitzungen abrufen
- `POST /api/sessions/` – Neue Quiz-Sitzung starten
- `POST /api/sessions/{id}/complete/` – Quiz-Sitzung beenden und Antworten einreichen

### Leaderboard
- `GET /api/leaderboard?limit=N&around=M&category=O` – Die ersten N User des Leaderboards und M Users um den self-user herum (nach Streak); O kann 'all', 'friends', 'studiengang' sein 