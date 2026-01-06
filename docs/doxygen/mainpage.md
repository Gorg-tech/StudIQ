# StudiQ – Quiz-Plattform für Studierende

## Einleitung

StudiQ ist eine Webanwendung, mit der Studierende ihren Lernfortschritt
in verschiedenen Modulen und Studiengängen über Quizzes tracken können.

Die Anwendung besteht aus:

- einem **Django-Backend** mit REST-API (User, Studiengänge, Module, Lernsets, Quizzes, Fortschritt),
- einem **Vue-Frontend** als Single-Page-Application (Navigation, Quiz-UI, Auswertung),
- einem **Scraper**, der Modul- und Studiengangsdaten aus Modulux importiert.

Diese Dokumentation beschreibt den technischen Aufbau von Backend und Frontend
und soll Entwickler:innen beim Verständnis und bei der Weiterentwicklung
von StudiQ unterstützen.

---

## Gesamtarchitektur

StudiQ folgt einer klassischen Client–Server-Architektur:

1. Der Browser lädt die Vue-Single-Page-App.
2. Die Vue-Router-Views holen Daten über API-Services vom Backend.
3. Das Django-Backend verarbeitet die Anfragen, greift auf die Datenbank zu
   und liefert JSON zurück.
4. Das Frontend rendert Quizzes, Lernsets, Statistiken und Fortschritt.

---

## Projektstruktur

### Backend – `src/server`

- `accounts`  
  Benutzer, Rollen, StudyDays, Statistiken (IQ-Level, Streak, etc.).

- `quizzes`  
  Studiengänge, Module, Lernsets, Quizzes, Fragen, QuizAttempts, Sessions, Leaderboard, Suche.

- `scraper`  
  Modulux-Scraper zum Import von Studiengängen und Modulen.

- `config`  
  Django-Einstellungen und URL-Routing.

### Frontend – `src/client`

- `src/views` – Seiten wie Studiengänge, Module, Lernsets, Quiz, Ergebnis, Suche, Einstellungen.
- `src/router` – Routen für die SPA-Navigation.
- `src/stores` – State-Management (User, App-Settings, ggf. Quiz-Editor).
- `src/services` – API-Clients für Backend-Endpunkte (auth, user, quizzes, lernsets, modules, studiengaenge, …).

---

## Nutzung dieser Dokumentation

- **Namespaces / Modules**  
  Gruppiert Python- und JS/TS-Module, z. B. `quizzes.models`, `accounts.views`,
  `router/index`, `services/quizzes`.

- **Classes**  
  Listet Django-Models, Serializers, ViewSets und relevante Klassen/Funktionen im Frontend.

- **Files**  
  Zeigt die einzelnen Quelltext-Dateien mit optionaler Quellansicht.

Empfohlene Einstiege:

- Datenmodell: `quizzes.models`
- REST-API: `quizzes.views`, `accounts.views`
- Frontend-Navigation & API-Aufrufe: `src/client/src/router`, `src/client/src/services`

---

## Doxygen selbst ausführen

Im Projekt:

```bash
cd docs/doxygen
doxygen Doxyfile
