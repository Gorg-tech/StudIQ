# StudIQ API

## Datenbank & Administration
- SQLite (automatisch als `db.sqlite3` erstellt)
- Nach Modelländerungen:  
  ```bash
  python manage.py makemigrations && python manage.py migrate
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

## Authentifizierung
Die Authentifizierung erfolgt über Cookie-basierte Sessions. Bei erfolgreichem Login/Register wird ein Session-Cookie gesetzt, das bei nachfolgenden Anfragen automatisch mitgesendet wird.

Vorteile dieser Methode:
- Sicherere Lösung als Token im Local Storage
- CSRF-Schutz durch Django's CSRF-Mechanismus
- Automatische Session-Verwaltung

> **Hinweis:**  
> **Alle API-Endpunkte (außer Registrierung und Login) erfordern eine Authentifizierung!**  
> Nicht authentifizierte Anfragen werden mit HTTP 403 oder 401 abgelehnt.

## Server starten
```bash
cd src/server
python manage.py runserver
```

## Version Control
**Kleiner Hinweis:** Während der Entwicklung checken wir die `db.sqlite3` Datei mit ins GitHub-Repo ein – macht den Einstieg einfacher für alle.

**Ist eigentlich nicht so der Bringer und auch nicht ganz ungefährlich!** In der Datenbank stecken sensible Infos wie Passwort-Hashes und persönliche Daten.

Für die richtige Produktion sollte die Datei definitiv in die `.gitignore` wandern!

## API-Endpoints

### Authentifizierung
- `POST /api/auth/register/` – Neuen Benutzer registrieren
- `POST /api/auth/login/` – Benutzer anmelden
- `POST /api/auth/logout/` – Benutzer abmelden

### User
- `GET /api/users/me/` – Eigene Benutzerdaten abrufen
- `PUT /api/users/me/` – Eigene Benutzerdaten aktualisieren

### Studiengänge
- `GET /api/studiengaenge/` – Alle Studiengänge abrufen
- `GET /api/studiengaenge/{id}/` – Einzelnen Studiengang abrufen
- `POST /api/studiengaenge/` – Neuen Studiengang anlegen (nur Moderator/Lecturer)
- `PUT /api/studiengaenge/{id}/` – Studiengang aktualisieren (nur Moderator/Lecturer)
- `DELETE /api/studiengaenge/{id}/` – Studiengang löschen (nur Moderator/Lecturer)

### Module
- `GET /api/modules/` – Alle Module abrufen
- `GET /api/modules/{id}/` – Einzelnes Modul abrufen
- `POST /api/modules/` – Neues Modul anlegen (nur Moderator/Lecturer)
- `PUT /api/modules/{id}/` – Modul aktualisieren (nur Moderator/Lecturer)
- `DELETE /api/modules/{id}/` – Modul löschen (nur Moderator/Lecturer)
- `GET /api/modules/{moduleId}/lernsets/` – Alle Lernsets eines Moduls abrufen

### Lernsets
- `GET /api/lernsets/` – Alle Lernsets abrufen
- `GET /api/lernsets/{id}/` – Einzelnes Lernset abrufen
- `POST /api/lernsets/` – Neues Lernset anlegen
- `PUT /api/lernsets/{id}/` – Lernset aktualisieren (nur Ersteller oder Moderator)
- `DELETE /api/lernsets/{id}/` – Lernset löschen (nur Ersteller oder Moderator)

### Quizze
- `GET /api/quizzes/` – Alle Quizze abrufen
- `GET /api/quizzes/{id}/` – Einzelnes Quiz abrufen
- `POST /api/quizzes/` – Neues Quiz anlegen
- `PUT /api/quizzes/{id}/` – Quiz aktualisieren (nur Ersteller oder Moderator)
- `DELETE /api/quizzes/{id}/` – Quiz löschen (nur Ersteller oder Moderator)
- `GET /api/quizzes/{quizId}/questions/` – Alle Fragen eines Quiz abrufen

### Fragen
- `GET /api/questions/` – Alle Fragen abrufen
- `GET /api/questions/{id}/` – Einzelne Frage abrufen
- `POST /api/questions/` – Neue Frage anlegen
- `PUT /api/questions/{id}/` – Frage aktualisieren (nur Ersteller oder Moderator)
- `DELETE /api/questions/{id}/` – Frage löschen (nur Ersteller oder Moderator)
- `GET /api/questions/{questionId}/answers/` – Antwortoptionen zu einer Frage abrufen
- `POST /api/questions/{questionId}/answers/` – Neue Antwortoption anlegen
- `PUT /api/questions/{questionId}/answers/{answerId}/` – Antwortoption aktualisieren
- `DELETE /api/questions/{questionId}/answers/{answerId}/` – Antwortoption löschen

### Quiz-Fortschritt
- `GET /api/progress/` – Eigenen Quiz-Fortschritt für alle Quizze abrufen
- `GET /api/progress/{id}/` – Fortschritt für einen bestimmten Eintrag abrufen
- `POST /api/progress/` – Neuen Fortschritt speichern
- `PUT /api/progress/{id}/` – Fortschritt aktualisieren

### Quiz-Sitzungen
- `GET /api/sessions/` – Eigene Quiz-Sitzungen abrufen
- `POST /api/sessions/` – Neue Quiz-Sitzung starten
- `POST /api/sessions/{id}/complete/` – Quiz-Sitzung beenden und Antworten einreichen

### Feedback
- `GET /api/feedback/` – Eigenes Feedback abrufen
- `POST /api/feedback/` – Neues Feedback abgeben
- `PUT /api/feedback/{id}/` – Feedback aktualisieren
- `DELETE /api/feedback/{id}/` – Feedback löschen

### Errungenschaften
- `GET /api/achievements/` – Alle Errungenschaften abrufen
- `GET /api/achievements/user/` – Eigene freigeschaltete Errungenschaften abrufen

