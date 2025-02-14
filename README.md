# studywizzard
# Diese Anleitung bietet schrittweise Anweisungen, um die Flask-Anwendung, die im bereitgestellten Python-Skript beschrieben ist, einzurichten und auszuführen. Befolge diese Schritte, um die Anwendung auf deinem lokalen Computer zum Laufen zu bringen.

# Schritt 1: Erstelle und aktiviere eine virtuelle Umgebung für Python, um die Abhängigkeiten zu verwalten:

python3 -m venv venv
source venv/bin/activate  # Auf Unix/macOS


# Schritt 2: Installiere die notwendigen Python-Pakete. Stelle sicher, dass du eine requirements.txt-Datei hast oder installiere die Pakete manuell, die im bereitgestellten Skript aufgelistet sind:

(venv) $ pip install Flask Flask-Session WTForms Flask-Migrate

# Schritt 3: Starte die Flask-Anwendung. Stelle sicher, dass die Umgebungsvariable FLASK_APP auf deine Hauptdatei (z. B. app.py) gesetzt ist:

(venv) $ export FLASK_APP=app.py  
(venv) $ flask run --reload

Dieser Befehl startet einen lokalen Entwicklungsserver und überwacht Änderungen im Quellcode, um den Server automatisch neu zu laden.

# Schritt 4: Greife auf die Anwendung im Webbrowser zu. Sobald der Server läuft, kannst du die Anwendung über http://127.0.0.1:5000/ aufrufen, um die Startseite der Anwendung anzuzeigen.

# Schritt 5: Erkunde die Funktionen der Anwendung. Nutze die verschiedenen Routen und Funktionalitäten, die innerhalb deiner Flask-Anwendung definiert sind, um ihre Fähigkeiten zu testen.
