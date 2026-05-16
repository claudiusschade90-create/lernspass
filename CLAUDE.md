# Lernspaß-App — Projekt-Briefing für Claude Code

## Was ist das?

Eine browser-basierte Lernapp für meine Tochter, 2. Klasse Grundschule, **Schwarzwaldtalschule in Berg (Bayern)**. Inhalte sind abgestimmt auf den bayerischen **LehrplanPLUS** für Jahrgangsstufe 2 in den Fächern **Mathe, Deutsch und HSU**.

Die App läuft als statische HTML-Seite auf **GitHub Pages**. Sie soll auch im Familien- und Freundeskreis nutzbar sein. Auf iPhone/iPad wird sie via "Zum Home-Bildschirm hinzufügen" wie eine native App genutzt.

## Zielgruppe & Tonalität

- **Primäre Nutzerin:** Mädchen, 7–8 Jahre, 2. Klasse
- **Sekundäre Nutzer:** ggf. andere Kinder im gleichen Alter, deren Eltern den Link bekommen
- **Sprache:** Deutsch, kindgerecht, ohne Anglizismen
- **Design-Prinzipien:** große Touch-Buttons, klare Farben (warmes Amber/Orange/Rose/Sky), positive Verstärkung, kein Punitives. Fehler werden mit Hinweis und richtiger Lösung erklärt, nicht "bestraft".
- **Sprache der App-Texte:** korrekte deutsche Rechtschreibung inkl. Umlaute (ä, ö, ü, ß) — niemals Ersatzschreibweisen wie "ae", "oe", "ue" im sichtbaren Text.

## Architektur

**Eine einzige Datei: `index.html`**

- Reines HTML mit React 18 via CDN (unpkg)
- Tailwind via CDN (`cdn.tailwindcss.com`)
- Babel Standalone für In-Browser-JSX-Transpilation (kein Build-Schritt!)
- Web Audio API für Sounds, keine Audio-Dateien
- Inline-SVG-Icons (kein lucide-react im HTML)
- `localStorage` für lokalen Fortschritt (Sterne, richtige Antworten, Fach-Statistik)

**Bewusste Entscheidung:** Kein Node/npm/Build-Pipeline. Die HTML-Datei lässt sich direkt auf GitHub Pages hochladen und im Browser öffnen.

## Inhaltliche Struktur

### Mathe (`genMatheAufgabe`)
Dynamisch generiert, fünf Aufgabentypen:
- Plus im Zahlenraum bis 100
- Minus im Zahlenraum bis 100
- Einmaleins: 1er-, 2er-, 3er-, 4er-, 5er-, 10er-Reihe (Standard für 2. Klasse Bayern)
- Zahlenvergleich mit `<`, `>`, `=`
- Stellenwert: Zehner/Einer

### Deutsch (`deutschAufgaben`)
Statische Liste mit 22 Aufgaben:
Großschreibung von Nomen, ie-Schreibung, ck/tz nach kurzem Vokal, Artikel (der/die/das), Silben zählen, Wortarten (Nomen/Verb/Adjektiv), Satzzeichen, Reime, Mehrzahlbildung.

### HSU (`hsuBienen` + `hsuRest`)
Zweigeteilt — Themenauswahl im UI:

**Bienen (`hsuBienen`, 25 Aufgaben):** aktuelles Schulthema. Gegliedert in: Körperbau, Bienenstaat (Königin/Arbeiterinnen/Drohnen), Bienenstock & Waben, Aufgaben & Nutzen (Nektar→Honig, Bestäubung, Imker, Schwänzeltanz), Stachel & Verhalten, Jahreszyklus/Winter.

**Alle anderen Themen (`hsuRest`):** Jahreszeiten, Tiere allgemein, Bayern/Heimat, Verkehrserziehung, menschlicher Körper, Zeit (Tag/Stunde/Woche/Jahr), Pflanzen.

## Belohnungssystem

`tiere`-Array mit elf freischaltbaren Tieren, Schwellen von 0 (Marienkäfer) bis 220 Sterne (Bär). Aktuell:

| Stern-Schwelle | Tier |
|---|---|
| 0 | Marienkäfer 🐞 |
| 3 | Biene 🐝 |
| 8 | Schmetterling 🦋 |
| 15 | Frosch 🐸 |
| 30 | Eichhörnchen 🐿️ |
| 50 | Igel 🦔 |
| 75 | Reh 🦌 |
| 100 | Fuchs 🦊 |
| 130 | Eule 🦉 |
| 170 | Pferd 🐴 |
| 220 | Bär 🐻 |

Pro richtige Antwort: ein Stern. Streak-Anzeige ab zwei richtigen in Folge. Konfetti-Animation bei richtigen Antworten.

## Deployment

- GitHub Pages auf `main`-Branch, Root-Ordner
- URL-Schema: `https://USER.github.io/lernspass/`
- Bei jedem Push auf `main` aktualisiert sich die Live-Version nach 1–2 Minuten automatisch

## Workflow-Konventionen

- **Branches:** Direkt auf `main` arbeiten ist okay, solange das Repo klein bleibt. Bei größeren Umbauten Feature-Branch und Merge.
- **Commits:** Aussagekräftige deutsche Commit-Messages, Präsens, kurz (z. B. "Bienen-Kapitel erweitert um Honigernte").
- **Tests:** Da es ein In-Browser-Babel-Setup ist, gibt es keine klassische Test-Suite. Vor jedem Push prüft Claude Code per Babel-Parser, dass das JSX im `<script type="text/babel">`-Block sauber parsed.
- **Keine externen Dependencies hinzufügen**, ohne das mit mir abzustimmen. Wir wollen die Single-File-Architektur erhalten.

## Was geht NICHT verändert werden ohne Rückfrage

- Single-File-Architektur (kein Node-Build, kein npm)
- Kindgerechter, freundlicher Ton ohne Bestrafungs-Elemente
- `localStorage`-basierter Fortschritt (Sync-Konzept wird separat diskutiert)
- Schul- und Ortsangabe im Header (Schwarzwaldtalschule Berg)

## Roadmap-Ideen (Backlog, in keiner festen Reihenfolge)

**Inhalt:**
- Eigene Lernwörter aus dem aktuellen Schulheft pflegen (separates Deutsch-Kapitel)
- Schwierigkeitsstufen, automatisch an Trefferquote angepasst
- Weitere HSU-Themen-Schwerpunkte parallel zum Lehrplan (z. B. "Apfel", "Igel", "Hecke" — typische 2.-Klasse-Themen)
- Mathe: Sachaufgaben mit Bildern, Uhrzeit lesen lernen, Geld rechnen
- Deutsch: Drag-Drop-Spiele (Silben sortieren, Wortarten zuordnen)

**Funktion:**
- Fortschrittsdiagramm pro Themengebiet ("2er-Reihe: 12 richtig, 3 falsch")
- Mehrere Profile auf einem Gerät (Geschwister)
- Geräte-übergreifende Synchronisation via Firebase (separates Mini-Projekt)
- Lern-Erinnerungen (PWA-Notifications)

**Technisch:**
- PWA-Manifest und Service Worker für echte Offline-Nutzung
- Eigene Bilder-Sets für HSU-Aufgaben (Bienen-Körperteile beschriften etc.)
- Tastatur-Eingabe für offene Antworten (statt nur Multiple Choice)

## Kontext zu mir

Ich bin Claudius, Inhaber von BACneXt GmbH (Ingenieurbüro für Gebäudeautomation, Neumarkt in der Oberpfalz). Technisch versiert, aber dieses Projekt ist privat, nicht beruflich. Antworte mir auf Deutsch.

Bei technischen Themen darfst du Fachsprache verwenden. Beim Code-Inhalt für die App selbst (Aufgaben, UI-Texte) bitte immer kindgerecht.
