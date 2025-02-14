---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
[StudyWizard Team]

{: .no_toc }
# Referenz-Dokumentation

{: .attention }
> Diese Seite sammelt interne Funktionen, Routen mit ihren Funktionen und APIs (falls vorhanden).
>
> Siehe [Uber](https://developer.uber.com/docs/drivers/references/api) oder [PayPal](https://developer.paypal.com/api/rest/) für beispielhafte API-Referenzdokumentationen.
>
> Diese Box kann entfernt werden.

<details open markdown="block">
{: .text-delta }
<summary>Inhaltsverzeichnis</summary>
+ ToC
{: toc }
</details>

## Allgemeine Seiten

### `index()`

**Route:** `/`

**Methoden:** `GET`

**Zweck:** Lädt die Startseite der Anwendung.

**Beispielausgabe:**  
Rendert die `index.html` Seite.

---

### `about()`

**Route:** `/about`

**Methoden:** `GET`

**Zweck:** Zeigt die "Über uns"-Seite der Anwendung.

**Beispielausgabe:**  
Rendert die `about.html` Seite.

---

## Authentifizierung

### `login()`

**Route:** `/login`

**Methoden:** `GET`, `POST`

**Zweck:** Ermöglicht Benutzern die Anmeldung.

**Beispielausgabe:**  
- Erfolgreiche Anmeldung: Umleitung auf die Startseite mit Flash-Nachricht "Erfolgreich eingeloggt!"  
- Fehlgeschlagene Anmeldung: Zeigt eine Fehlermeldung "Ungültige Anmeldedaten."

---

### `register()`

**Route:** `/register`

**Methoden:** `GET`, `POST`

**Zweck:** Registriert einen neuen Benutzer.

**Beispielausgabe:**  
- Erfolgreiche Registrierung: Umleitung zur Login-Seite mit Flash-Nachricht "Registrierung erfolgreich!"  
- Fehlerhafte Registrierung: Zeigt eine Fehlermeldung.

---

## Lernkarten-Management

### `create_flashcard()`

**Route:** `/create_flashcard`

**Methoden:** `GET`, `POST`

**Zweck:** Erstellt eine neue Lernkarte für den eingeloggten Benutzer.

**Beispielausgabe:**  
- Erfolgreiche Erstellung: Umleitung zur Schulstufenauswahl mit Flash-Nachricht "Karteikarte erfolgreich erstellt!"  
- Fehlerhafte Eingabe: Zeigt eine Fehlermeldung.

---

### `view_flashcards()`

**Route:** `/view_flashcards`

**Methoden:** `GET`

**Zweck:** Zeigt die bekannten und unbekannten Lernkarten des Benutzers an.

**Beispielausgabe:**  
Rendert die `view_flashcards.html` Seite mit einer Liste von Lernkarten.

---

### `delete_flashcard(flashcard_id)`

**Route:** `/delete_flashcard/<int:flashcard_id>`

**Methoden:** `POST`

**Zweck:** Löscht eine Lernkarte des Benutzers.

**Beispielausgabe:**  
- Erfolgreiches Löschen: Flash-Nachricht "Karteikarte erfolgreich gelöscht!"  
- Fehlerhafte Anfrage: Umleitung zur Login-Seite, falls nicht eingeloggt.

---

### `mark_known(flashcard_id)`

**Route:** `/mark_known/<int:flashcard_id>`

**Methoden:** `POST`

**Zweck:** Markiert eine Lernkarte als gelernt.

**Beispielausgabe:**  
JSON `{ "success": true }`

---

### `mark_unknown(flashcard_id)`

**Route:** `/mark_unknown/<int:flashcard_id>`

**Methoden:** `POST`

**Zweck:** Markiert eine zuvor gelernte Lernkarte als unbekannt.

**Beispielausgabe:**  
JSON `{ "success": true }`

---

## Auswahlseiten

### `select_grade()`

**Route:** `/select_grade`

**Methoden:** `GET`, `POST`

**Zweck:** Ermöglicht dem Benutzer die Auswahl einer Schulstufe (7–10).

**Beispielausgabe:**  
Rendert die `select_grade.html` Seite mit einer Auswahl für Schulstufen.

---

### `select_category()`

**Route:** `/select_category`

**Methoden:** `GET`, `POST`

**Zweck:** Ermöglicht dem Benutzer die Auswahl einer Kategorie oder das Hinzufügen einer neuen Kategorie.

**Beispielausgabe:**  
- Erfolgreiche Kategoriewahl: Umleitung zur Lernkartenübersicht.  
- Erfolgreiches Hinzufügen: Flash-Nachricht "Neue Kategorie erfolgreich hinzugefügt!"  

---

### `select_flashcard_filters()`

**Route:** `/select_flashcard_filters`

**Methoden:** `GET`, `POST`

**Zweck:** Ermöglicht die Auswahl von Lernkarten basierend auf Schulstufe und Kategorie.

**Beispielausgabe:**  
Rendert die `select_flashcard_filters.html` Seite.

---

## Datenbank-Verwaltung

### `run_insert_sample()`

**Route:** `/insert/sample`

**Methoden:** `GET`

**Zweck:** Initialisiert die Datenbank und fügt Beispieldaten für den angemeldeten Benutzer hinzu.

**Beispielausgabe:**  
- Erfolgreiche Datenbankinitialisierung: Umleitung zur Schulstufenauswahl.  
- Fehlgeschlagene Aktion: Flash-Nachricht "Du musst eingeloggt sein, um diese Aktion auszuführen."

---

### `init_db_command()`

**Funktion:** Initialisiert die SQLite-Datenbank.

**Zweck:** Setzt die Datenbank zurück und erstellt alle Tabellen neu.

**Beispielausgabe:**  
Konsolenausgabe: `Datenbank erfolgreich initialisiert!`

---

Diese Dokumentation deckt alle derzeitigen internen Funktionen und API-Routen der **StudyWizard**-Anwendung ab.