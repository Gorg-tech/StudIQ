## Seqzuenzdiagram Seite Laden (Daten abfragen)
:::Mermaid  
sequenceDiagram
    participant U as User
    participant FE as Browser (Vue SPA)
    participant API as ApiClient
    participant QS as Quiz API (/api/...)

    %% Studiengang-Landingpage
    U->>FE: Seite "Studiengänge" öffnen
    FE->>API: GET /api/studiengaenge/
    API->>QS: StudiengangViewSet.list()
    QS-->>API: 200 OK + [Studiengang...]
    API-->>FE: Studiengänge
    FE-->>U: Liste der Studiengänge anzeigen

    %% Modul-Landingpage
    U->>FE: Studiengang auswählen
    FE->>FE: Route /studiengang/:id
    FE->>API: GET /api/modules/?studiengang=<id> (oder eigene Filter-Logik)
    note over FE,API: Alternative: Module schon über<br/>StudiengangSerializer.module geladen
    API->>QS: ModulViewSet.list()/Filter
    QS-->>API: 200 OK + [Modul...]
    API-->>FE: Module für Studiengang
    FE-->>U: Modulliste anzeigen

    %% Modul-Detail mit Lernsets
    U->>FE: Modul klicken
    FE->>FE: Route /modul/:modulId
    FE->>API: GET /api/modules/:modulId/
    API->>QS: ModulViewSet.retrieve() → ModulDetailSerializer
    QS-->>API: 200 OK + Modul + lernsets[]
    API-->>FE: Modul + Lernsets
    FE-->>U: Modul-Detailseite mit Lernset-Karten

    %% Lernset-Detail mit Quizzes
    U->>FE: Lernset auswählen
    FE->>FE: Route /lernsets/:id
    FE->>API: GET /api/lernsets/:id/ (optional, wenn du Details brauchst)
    FE->>API: GET /api/lernsets/:id/quizzes/
    API->>QS: QuizzesByLernsetView.get_queryset()
    QS-->>API: [Quiz...]
    API-->>FE: Quizzes
    FE-->>U: Lernset-Detailseite mit Quiz-Liste (QuizOverviewView)

:::

## Sequendiagramm Login
:::Mermaid
sequenceDiagram
    participant U as User
    participant FE as Browser (Vue SPA)
    participant API as ApiClient (Axios/Fetch)
    participant AUTH as Auth API (accounts.urls)
    
    %% Initialer App-Start: Prüfen, ob eingeloggt
    U->>FE: App öffnen
    FE->>API: GET /api/auth/me/
    API->>AUTH: GET /api/auth/me/ (Session-Cookie)
    AUTH-->>API: 200 OK + User JSON / 401 Unauthorized
    API-->>FE: User-Daten oder Fehler
    alt User ist eingeloggt
        FE->>FE: userStore.setUser(user)
        FE-->>U: Dashboard / Startseite mit User-Info
    else Nicht eingeloggt
        FE-->>U: Login-Form anzeigen
    end

    %% Login
    U->>FE: Login-Formular ausfüllen + "Login"
    FE->>API: POST /api/auth/login/ (username, password)
    API->>AUTH: LoginView.validate + authenticate + login()
    AUTH-->>API: 200 OK + User JSON (Session-Cookie gesetzt)
    API-->>FE: User JSON
    FE->>FE: userStore.setUser(user)
    FE-->>U: Weiterleitung auf Startseite / vorherige Route
:::

## Sequenzdiagram Quizz durchfuehren
:::Mermaid
sequenceDiagram
    participant U as User
    participant FE as Browser (QuizView/ResultView)
    participant API as ApiClient
    participant QS as Quiz API (/api/quizzes/...)
    participant ACC as Accounts API (/api/users/...)

    %% QuizView laden
    U->>FE: Quiz starten (z.B. aus QuizOverviewView)
    FE->>FE: Route /quiz/:quizId
    FE->>API: GET /api/quizzes/:quizId/
    API->>QS: QuizViewSet.retrieve()
    QS-->>API: Quiz + Questions + AnswerOptions
    API-->>FE: Quiz-JSON
    FE-->>U: Fragen anzeigen

    %% User beantwortet Fragen rein im FE
    loop Jede Frage
        U->>FE: Antwort auswählen / weiter
        FE->>FE: Lokalen State aktualisieren (correctCount, totalCount, timer...)
    end

    %% Quiz-Abschluss
    U->>FE: "Quiz abschließen" klicken
    FE->>FE: correct = Anzahl richtiger Antworten
    FE->>API: POST /api/quizzes/:quizId/complete/ ({ correct })
    API->>QS: QuizCompletionView.post()

    note over QS: Holt Quiz + QuizProgress.get_or_create(user, quiz)

    QS->>QS: total = quiz.questions.count()<br/>accuracy = correct/total<br/>Punkte + Boni berechnen
    QS->>ACC: User laden und updaten (iq_level, solved_quizzes, correct_answers, wrong_answers)
    ACC-->>QS: User gespeichert
    QS->>QS: QuizProgress updaten (attempts, correct_answers, wrong_answers, last_reviewed)
    QS->>ACC: register_study_activity(user)<br/>→ StudyDay + streak
    ACC-->>QS: streak aktualisiert
    QS-->>API: 200 OK + { attempts, streak, base_points, ... , prev_iq, new_iq }
    API-->>FE: Completion-Result

    %% Ergebnis-Seite + Stats
    FE->>FE: quizResultStore.setCompletionData(...)
    FE->>FE: Route /quiz/:quizId/result
    FE->>API: GET /api/users/me/stats/
    API->>ACC: UserStatsView.get()
    ACC-->>API: User JSON + rank
    API-->>FE: Stats
    FE-->>U: Ergebnisseite: Punkte, neue IQ-Stufe, Streak, Rank etc.
:::

## Sequenzdiagramm Suche 
:::Mermaid
sequenceDiagram
    participant U as User
    participant FE as Browser (SearchView)
    participant API as ApiClient
    participant QS as Search API (/api/search/)

    U->>FE: Suchbegriff eingeben
    FE->>FE: debounce(q)
    FE->>API: GET /api/search/?q=q&filter=optional&limit=15
    API->>QS: HTTP Request an SearchView
    QS-->>API: 200 OK mit Ergebnissen (JSON)
    API-->>FE: Suchergebnisse
    FE-->>U: Treffer nach Typ gruppiert anzeigen

:::
