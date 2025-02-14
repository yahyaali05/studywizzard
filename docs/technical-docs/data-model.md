---
title: Data-Model
parent: Technical Docs
nav_order: 2
---

{: .label }
[StudyWizard Team]

{: .no_toc }
# Datenmodell

<details open markdown="block">
{: .text-delta }
<summary>Inhaltsverzeichnis</summary>
+ ToC
{: toc }
</details>

## Übersicht

Dieses Dokument beschreibt das Datenmodell von **StudyWizard**. Die Datenbank basiert auf **SQLite** und enthält mehrere Tabellen zur Verwaltung von Benutzern, Lernkarten, Lernfortschritten, Testergebnissen und Kategorien. Die Tabellen sind miteinander verknüpft, um den Lernprozess effizient nachzuverfolgen.

## Tabellen

### Benutzer (Users)
Diese Tabelle speichert die Anmeldeinformationen der Benutzer. Jeder Benutzer hat eine eindeutige ID, einen Benutzernamen (der einzigartig sein muss) und ein Passwort, das für die Authentifizierung gespeichert wird.

**Attribute:**
- `id`: Eindeutige Benutzer-ID.
- `username`: Benutzername (muss einzigartig sein).
- `password`: Gehashtes Passwort für die Authentifizierung.

---

### Lernkarten (Flashcards)
Diese Tabelle speichert die einzelnen Lernkarten mit den dazugehörigen Informationen. Jede Lernkarte gehört einem Benutzer und enthält ein englisches Wort sowie die deutsche Übersetzung. Zusätzlich gibt es optionale Attribute wie Thema, Kategorie und Schulstufe.

**Attribute:**
- `id`: Eindeutige ID der Lernkarte.
- `user_id`: Fremdschlüssel, der auf den Benutzer verweist.
- `subject`: Thema der Lernkarte.
- `question`: Das englische Wort.
- `answer`: Die deutsche Übersetzung.
- `category`: Die Kategorie (z. B. Haushalt, Arbeit, Natur).
- `grade_level`: Die Schulstufe (7–10).
- `is_learned`: Gibt an, ob die Karte gelernt wurde (0 = nein, 1 = ja).

---

### Lernfortschritt (Progress)
Diese Tabelle speichert den Fortschritt der Benutzer für jede Lernkarte. Sie verfolgt, wie oft eine Karte wiederholt wurde, wann sie zuletzt überprüft wurde und ob sie als "gelernt" markiert ist.

**Attribute:**
- `id`: Eindeutige ID für den Fortschrittseintrag.
- `user_id`: Fremdschlüssel zum Benutzer.
- `flashcard_id`: Fremdschlüssel zur Lernkarte.
- `review_count`: Anzahl der Wiederholungen der Karte.
- `last_reviewed`: Datum der letzten Wiederholung.
- `status`: Status der Lernkarte (z. B. "Aktiv" oder "Gelernt").

---

### Testergebnisse (Test Results)
Diese Tabelle speichert die Testergebnisse der Benutzer. Sie enthält Informationen zu richtigen und falschen Antworten sowie das Testdatum.

**Attribute:**
- `id`: Eindeutige ID des Testergebnisses.
- `user_id`: Fremdschlüssel zum Benutzer.
- `correct_answers`: Anzahl der richtigen Antworten.
- `incorrect_answers`: Anzahl der falschen Antworten.
- `total_questions`: Gesamtanzahl der Fragen im Test.
- `test_date`: Datum des Tests (automatisch auf das aktuelle Datum gesetzt).

---

### Kategorien (Categories)
Diese Tabelle speichert benutzerdefinierte Kategorien für Lernkarten. Jeder Benutzer kann eigene Kategorien erstellen, die für ihn eindeutig sind.

**Attribute:**
- `id`: Eindeutige ID der Kategorie.
- `name`: Name der Kategorie.
- `user_id`: Fremdschlüssel zum Benutzer, der die Kategorie erstellt hat.

---

## Beziehungen zwischen den Tabellen

- **Benutzer (Users) → Lernkarten (Flashcards)**  
  Ein Benutzer kann mehrere Lernkarten haben, aber eine Lernkarte gehört immer nur einem Benutzer.

- **Benutzer (Users) → Lernfortschritt (Progress)**  
  Jeder Benutzer hat seinen individuellen Fortschritt für jede Lernkarte. Die Beziehung wird über `user_id` und `flashcard_id` sichergestellt.

- **Benutzer (Users) → Testergebnisse (Test Results)**  
  Ein Benutzer kann mehrere Tests absolvieren, die mit seiner ID verknüpft sind.

- **Benutzer (Users) → Kategorien (Categories)**  
  Ein Benutzer kann eigene Kategorien für Lernkarten erstellen, die eindeutig für ihn sind.

Dieses Datenmodell ermöglicht eine effiziente Verwaltung der Lernkarten und eine präzise Nachverfolgung des Lernfortschritts für jeden Benutzer.
