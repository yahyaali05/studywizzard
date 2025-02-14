---
title: Architecture
parent: Technical Docs
nav_order: 1
---
{: .label }
[StudyWizard Team]

{: .no_toc }
# Architektur

{: .attention }
> Diese Seite beschreibt, wie die Anwendung aufgebaut ist und wie wichtige Teile der App funktionieren. Sie soll neuen Entwicklern ausreichend technisches Wissen vermitteln, um zum Code beizutragen.
> 
> Siehe [diesen Blogpost](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html) für eine Erklärung des Konzepts sowie diese Beispiele:
>
> + <https://github.com/rust-lang/rust-analyzer/blob/master/docs/dev/architecture.md>
> + <https://github.com/Uriopass/Egregoria/blob/master/ARCHITECTURE.md>
> + <https://github.com/davish/obsidian-full-calendar/blob/main/src/README.md>
> 
> Zur Veranschaulichung der Struktur und des Verhaltens können [Mermaid](../ui-components.md) oder Diagramme wie [C4](https://c4model.com/) oder [UML](https://www.omg.org/spec/UML) verwendet werden.
> 
> Dieser `attention`-Hinweis kann entfernt werden.

<details open markdown="block">
{: .text-delta }
<summary>Inhaltsverzeichnis</summary>
+ ToC
{: toc }
</details>

## Überblick

StudyWizard ist eine App zum Englischlernen für deutschsprachige Nutzer, die auf Karteikarten und interaktivem Lernen basiert. Die Anwendung stellt sicher, dass bekannte Wörter nicht wiederholt werden, während unbekannte Wörter häufiger erscheinen. Zudem können Nutzer Tests basierend auf den Karteikarten absolvieren, wobei die Ergebnisse direkt nach Abschluss angezeigt werden.

Das System umfasst mehrere Klassenstufen (7, 8, 9, 10) mit unterschiedlichen Schwierigkeitsgraden und Kategorien (z. B. Sport, Haushalt). Der Technologie-Stack umfasst Flask für das Backend, SQLite für die Datenverwaltung, Jinja für das Rendering von Formularen und Bootstrap für das UI-Design.

## Codeübersicht

### Frontend

#### HTML-Templates
- Definieren die Struktur und den Inhalt der Webseiten.
- Ermöglichen die dynamische Darstellung von Daten mit Jinja.

#### Bootstrap
- Wird für das responsive UI-Design verwendet.
- Sorgt für eine moderne und einheitliche Benutzeroberfläche.

#### Jinja-Templates
- Ermöglichen die dynamische Generierung von HTML.
- Erleichtern die nahtlose Interaktion zwischen Backend und Frontend.

### Backend

#### Flask
- Verwaltet das Routing und die Verarbeitung von HTTP-Anfragen.
- Handhabt Authentifizierung, Sitzungsverwaltung und Datenabruf.

#### Python
- Implementiert die Kernlogik der Anwendung.
- Regelt Geschäftslogik, Wiederholungsmechanismen für Karteikarten und Testauswertungen.

#### Flask WTForms
- Wird zur Formularerstellung und Validierung im Frontend und Backend genutzt.
- Stellt sicher, dass Benutzereingaben vor der Datenbankinteraktion überprüft werden.

#### SQLite
- Speichert den Fortschritt der Nutzer, Karteikarten, Testergebnisse und andere Anwendungsdaten.
- Bietet eine leichte, aber effiziente Datenbanklösung für StudyWizard.

## Querschnittsthemen

- **Authentifizierung & Benutzerverwaltung:** Flask-Login wird zur Verwaltung von Benutzersitzungen und Authentifizierung verwendet.
- **Datenpersistenz:** SQLite sorgt für eine strukturierte Speicherung und den Abruf von Daten.
- **Logging & Fehlerbehandlung:** Flask bietet integrierte Logging-Funktionen, wobei Fehler protokolliert werden, um die Stabilität zu gewährleisten.
- **Sicherheitsaspekte:** Benutzereingaben werden validiert, und Authentifizierungsmechanismen stellen die Sicherheit der Sitzungen sicher.

---