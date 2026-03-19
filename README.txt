Sudoku Solver - Architektonischer Plan

Ziel
- Das Projekt soll modular aufgebaut sein, damit klassische Solver und spaeter auch ein ML-Solver sauber nebeneinander existieren.
- Die Verantwortung jeder Schicht ist klar getrennt.
- Das Projekt bleibt ein Lernprojekt: kleine Schritte, wenig Magie, gut testbar.

Architektur (3 Schichten)

1) Domain-Schicht
- Datei: board.py
- Verantwortung:
	- 9x9 Grid verwalten
	- Werte setzen/lesen
	- row/col/block liefern
	- Basisvalidierung (Index 0-8, Werte 0-9)
- Keine Verantwortung:
	- Kein Backtracking
	- Keine API/HTTP Logik

2) Solver-Schicht
- Datei: solver.py
- Verantwortung:
	- Sudoku-Regeln anwenden
	- Loesungsalgorithmen kapseln
	- Solver austauschbar machen (Strategie-Pattern)
- Geplante Klassen:
	- Solver (Interface/abstrakte Basisklasse)
	- BacktrackingSolver
	- MLSolver (später)

3) Application/API-Schicht
- Dateien: service.py, api.py
- service.py Verantwortung:
	- Input validieren
	- Board aufbauen
	- Solver auswaehlen
	- Ergebnis normalisieren
- api.py Verantwortung:
	- Duenne Fassade fuer spaetere REST/CLI Integration
	- Request -> Service -> Response

Abhaengigkeiten (wichtig)
- api.py darf service.py nutzen.
- service.py darf board.py und solver.py nutzen.
- solver.py darf board.py nutzen.
- board.py kennt keine anderen Schichten.

Dateistruktur (Ziel)
- board.py
- solver.py
- service.py
- api.py
- tests/
	- test_board.py
	- test_solver_backtracking.py
	- test_service.py

Datenfluss
1. API bekommt ein Grid (9x9).
2. Service validiert Input und baut Board.
3. Service waehlt Solver (z. B. backtracking oder ml).
4. Solver loest das Board in-place oder auf Kopie (vorher festlegen).
5. Service gibt standardisiertes Ergebnis zurueck.
6. API liefert Response an Aufrufer.

Arbeitsplan (Lernorientiert)

Paket 1 - Board finalisieren
- Ziel: board.py als stabile Datenklasse.
- Aufgaben:
	- Methoden pruefen (add_value, get_row, get_col, get_block)
	- Fehlerfaelle sauber behandeln
	- Kleine manuelle Tests
- Done wenn:
	- Board verhaelt sich fuer gueltige und ungueltige Inputs erwartbar.

Paket 2 - Solver-Interface bauen
- Ziel: Austauschbare Solver vorbereiten.
- Aufgaben:
	- Solver-Vertrag definieren (solve(board) -> bool oder Ergebnisobjekt)
	- BacktrackingSolver als erste Implementierung
	- MLSolver als Stub (NotImplemented)
- Done wenn:
	- Solver kann ausgetauscht werden, ohne Board anzupassen.

Paket 3 - Service-Schicht bauen
- Ziel: Orchestrierung zentral.
- Aufgaben:
	- solve_grid(grid, solver_name)
	- Inputformat pruefen
	- Fehler in klare Fehlermeldungen umsetzen
- Done wenn:
	- Ein Funktionsaufruf loest ein Sudoku Ende-zu-Ende.

Paket 4 - API-Fassade bauen
- Ziel: Sauberer Einstiegspunkt fuer spaetere Integrationen.
- Aufgaben:
	- Request/Response Struktur definieren
	- Service aufrufen
	- Ergebnisse serialisierbar zurueckgeben
- Done wenn:
	- Gleicher Input ergibt reproduzierbare Outputstruktur.

Paket 5 - Tests als Sicherheitsnetz
- Ziel: Schnell refactoren koennen ohne Angst.
- Aufgaben:
	- Unit-Tests fuer Board
	- Unit-Tests fuer Backtracking-Solver
	- Integrationstest fuer Service
- Done wenn:
	- Kernfunktionen durch Tests abgedeckt sind.

Paket 6 - ML-Vorbereitung
- Ziel: ML spaeter einstecken, ohne Architekturbruch.
- Aufgaben:
	- Solver-Registry vorbereiten (backtracking, ml)
	- Gemeinsames Input/Output Format festlegen
	- Metriken definieren (Erfolgsrate, Laufzeit, Gueltigkeit)
- Done wenn:
	- ML-Solver spaeter nur neue Klasse + Registrierung braucht.

Architektur-Regeln
- Keep it thin: API ist duenn, Service orchestriert, Solver rechnet.
- Eine Schicht kennt nur die direkt darunterliegende Schicht.
- Keine Solver-Logik in board.py.
- Keine API-Logik in solver.py.
- Jede neue Funktion bekommt mindestens einen Testfall.

Naechster konkreter Schritt
- Starte mit Paket 1 und erstelle danach solver.py mit Solver-Interface und BacktrackingSolver.
