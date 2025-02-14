---
title: Design decisions
nav_order: 3
---

{: .label }
StudyWizard

{: .no_toc }
# Designentscheidungen

<details open markdown="block">
{: .text-delta }
<summary>Inhaltsverzeichnis</summary>
+ ToC
{: toc }
</details>

## 01: Wahl des Frontend-Designs

### Meta

Status  
: **Entschieden**  

Aktualisiert  
: 08-Feb-2025  

### Problemstellung

Für die Benutzeroberfläche von StudyWizard benötigen wir ein Framework, das eine schnelle Entwicklung ermöglicht und gleichzeitig ein modernes, responsives Design unterstützt. Eine vollständig maßgeschneiderte CSS- und JavaScript-Implementierung wäre zu zeitaufwendig, daher brauchen wir eine effiziente Lösung, die mit Flask gut kompatibel ist.

### Entscheidung

Wir haben uns für **Bootstrap** als CSS-Framework entschieden.

- **Gründe:**  
  - Bootstrap bietet ein **responsives Grid-System**, das die Anpassung an verschiedene Bildschirmgrößen erleichtert.  
  - Die vordefinierten Komponenten ermöglichen eine **schnelle Entwicklung** mit einem professionellen Design.  
  - Es ist **leicht zu erlernen** und lässt sich gut mit Flask und Jinja-Templates kombinieren.  

*Entscheidung getroffen von:* github.com/deingithub  

### In Betracht gezogene Optionen

| Option | Vorteile | Nachteile |
| --- | --- | --- |
| **Eigenes CSS + JavaScript** | ✔️ Volle Kontrolle über das Design <br> ✔️ Individuelle Gestaltung möglich | ❌ Zeitaufwendig <br> ❌ Weniger strukturierte Entwicklung |
| **Bootstrap** | ✔️ Schnelle Entwicklung <br> ✔️ Responsives Design ohne großen Aufwand <br> ✔️ Große Community-Unterstützung | ❌ Weniger Designflexibilität <br> ❌ Größere Stylesheets können die Ladezeit beeinflussen |

---

## 02: Datenbankwahl

### Meta

Status  
: **Entschieden**  

Aktualisiert  
: 08-Feb-2025  

### Problemstellung

Für die Speicherung der Benutzerdaten und Flashcards benötigen wir eine einfache und zuverlässige Datenbank. Die Datenbank sollte sich leicht in Flask integrieren lassen und keine komplexe Einrichtung erfordern.

### Entscheidung

Wir haben uns für **SQLite** als Datenbank entschieden.

- **Gründe:**  
  - SQLite ist eine **leichtgewichtige Datenbank**, die keine separate Serverinstallation benötigt.  
  - Sie lässt sich problemlos mit **Flask-SQLAlchemy** verwenden.  
  - Ideal für kleinere bis mittelgroße Anwendungen wie StudyWizard.  

*Entscheidung getroffen von:* github.com/deingithub  

### In Betracht gezogene Optionen

| Option | Vorteile | Nachteile |
| --- | --- | --- |
| **SQLite** | ✔️ Einfach zu integrieren <br> ✔️ Keine Serverkonfiguration nötig <br> ✔️ Perfekt für kleinere Apps | ❌ Skalierbarkeit begrenzt <br> ❌ Keine parallelen Schreibzugriffe möglich |
| **PostgreSQL** | ✔️ Skalierbar <br> ✔️ Unterstützt parallele Anfragen | ❌ Aufwendigere Einrichtung <br> ❌ Nicht notwendig für eine kleinere Anwendung |

---

## 03: Formularverwaltung

### Meta

Status  
: **Entschieden**  

Aktualisiert  
: 08-Feb-2025  

### Problemstellung

Die Anwendung benötigt eine effiziente Möglichkeit zur Verwaltung von Formularen für Benutzereingaben, z. B. zur Registrierung, zum Teststart oder zur Bewertung von Flashcards.

### Entscheidung

Wir haben uns für **Jinja-Forms** entschieden.

- **Gründe:**  
  - Jinja-Forms lassen sich **direkt in Flask-Vorlagen** einbetten.  
  - Sie ermöglichen eine **dynamische Formularerstellung** mit variablen Werten.  
  - Die Verwendung in Kombination mit Bootstrap sorgt für eine **schöne und funktionale UI**.  

*Entscheidung getroffen von:* github.com/deingithub  

### In Betracht gezogene Optionen

| Option | Vorteile | Nachteile |
| --- | --- | --- |
| **Jinja-Forms** | ✔️ Direkt in Flask integriert <br> ✔️ Leicht zu verwalten <br> ✔️ Gut kombinierbar mit Bootstrap | ❌ Eingeschränkte Interaktivität <br> ❌ Kein JavaScript-Handling |
| **WTForms** | ✔️ Erweiterte Validierung <br> ✔️ Besser für komplexe Formulare | ❌ Zusätzliche Bibliothek erforderlich <br> ❌ Komplexer als nötig für unser Projekt |

---

Diese Designentscheidungen stellen sicher, dass **StudyWizard** eine effiziente, wartbare und nutzerfreundliche Anwendung bleibt.
