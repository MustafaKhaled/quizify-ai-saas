"""
Static chapter knowledge base for the German B1 Hören (listening) agent.

Each "chapter" maps to one of the four Teile of the Goethe-Zertifikat B1 /
telc B1 / ÖSD B1 listening section. The corpus content for each Teil is the
*format spec* (length, voices, topic, comprehension question type) — not
example transcripts. Real B1 exam transcripts are copyright Goethe-Institut
and not redistributable; we generate fresh scripts that match the format.

The agent's instructions.md tells the model how to produce a script + matching
comprehension item that fits the active Teil's format spec.
"""

DEUTSCH_B1_HOREN_CHAPTERS = [
    {
        "slug": "teil_1_kurze_texte",
        "name": "Teil 1 — Kurze Texte",
        "summary": "Five short single-speaker monologues (announcements, voicemails, info messages). One comprehension item per text.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat B1 Hören Teil 1.\n\n"
            "Audio: 5 short, independent monologues. Each is a single speaker. "
            "Played ONCE only on the real exam.\n\n"
            "Length per script: 25–40 seconds of speech, which is roughly 60–100 German words at normal speaking pace.\n\n"
            "Voice/register: a clear single speaker. Register depends on the context — formal for an announcement at a station "
            "or in a workplace, casual for a friend leaving a voicemail, neutral for a recorded info line.\n\n"
            "Topic catalog (rotate across these so a generated batch covers the breadth of the Teil):\n"
            "- Bahnhofsansagen (train station announcements — Verspätung, Gleiswechsel, Zugausfall)\n"
            "- Flughafenansagen (airport — Boarding, Gate change, weather delay)\n"
            "- Wetterbericht (weather report)\n"
            "- Verkehrsfunk (traffic report — Stau, Sperrung, Umleitung)\n"
            "- Mailbox-Nachrichten (voicemail from a friend, family member, colleague)\n"
            "- Geschäftsansagen (shop announcements — opening hours, special offers, closing soon)\n"
            "- Veranstaltungsansagen (event announcements — Beginn, Pause, Programmänderung)\n"
            "- Behördentexte (government info line — Öffnungszeiten, Termine)\n"
            "- Telefonansagen (phone menus — drücken Sie die 1 für …)\n\n"
            "Comprehension item per script: one MCQ with 3 options or richtig/falsch. "
            "The question targets a specific concrete fact in the script (a number, a place, a time, a reason). "
            "Distractors are values that COULD have been said but weren't — never random other German words.\n\n"
            "B1 vocabulary range: working-adult everyday language. Avoid academic, technical, or literary vocabulary. "
            "Allowed: everyday work, travel, shopping, health, free time, family, services, public transport. "
            "Numbers, dates, times, and place names appear frequently."
        ),
    },
    {
        "slug": "teil_2_vortrag",
        "name": "Teil 2 — Vortrag",
        "summary": "One longer single-speaker presentation (lecture, guided tour). Five MCQ comprehension items.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat B1 Hören Teil 2.\n\n"
            "Audio: ONE longer monologue — a presentation, lecture, guided tour, museum audio guide, "
            "company orientation, or workshop introduction.\n\n"
            "Length: 3–4 minutes of speech, roughly 400–600 German words. Played ONCE.\n\n"
            "Voice/register: single speaker, semi-formal. Speaker is in a presenter role — clear, structured, "
            "uses signposting (zuerst, dann, anschließend, zum Schluss).\n\n"
            "Topic catalog:\n"
            "- Stadtführung (guided city tour) — landmarks, history, practical info\n"
            "- Museumsführung (museum guided tour) — exhibits, opening hours, behavior rules\n"
            "- Betriebsführung (company tour) — departments, history, what employees do\n"
            "- Universitäts-/Schul-Orientierung (campus orientation) — facilities, schedule, contact persons\n"
            "- Workshop-Einführung (workshop intro) — agenda, materials, breaks\n"
            "- Reiseleitung im Bus (bus tour leader) — route, stops, timing\n"
            "- Vereinsversammlung (club meeting opening) — agenda, news, upcoming events\n\n"
            "Comprehension items: 5 MCQs with 3 options each. Items follow the order of the speech (item 1 about "
            "an early section, item 5 about the closing section). Distractors are facts that COULD be true based on "
            "the topic but contradict the script's specifics.\n\n"
            "Structural signposting in the script is required so test-takers can follow the order of information. "
            "Use connectors: zunächst, danach, weiterhin, schließlich, zum Abschluss."
        ),
    },
    {
        "slug": "teil_3_gespraech",
        "name": "Teil 3 — Gespräch",
        "summary": "Informal dialogue between two friends/colleagues. Seven richtig/falsch comprehension items.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat B1 Hören Teil 3.\n\n"
            "Audio: a natural conversation between TWO speakers — typically two friends, two colleagues, "
            "or a customer and a service worker. Played ONCE.\n\n"
            "Length: 3–4 minutes, roughly 500–700 German words spread across both speakers. "
            "Each speaker has multiple turns; turns are short (1–4 sentences typical).\n\n"
            "Voice/register: informal du-form between friends/colleagues, or polite Sie-form for service interactions. "
            "Use real conversational features: agreement (genau, klar), hesitation (also, na ja), "
            "feedback (mmh, achso, wirklich?), short overlaps in topic.\n\n"
            "Topic catalog:\n"
            "- Wochenendpläne (weekend plans — invitations, scheduling)\n"
            "- Urlaubsplanung (vacation planning — destinations, dates, who pays for what)\n"
            "- Wohnungssuche (apartment hunting — viewings, neighborhoods, rent)\n"
            "- Probleme im Alltag (everyday problems — broken appliance, missed appointment, finding a babysitter)\n"
            "- Arbeitswelt (work talk — neue Stelle, Kollegen, Chef, Bewerbung)\n"
            "- Gesundheit (health — Arzttermin, Sport, gesunde Ernährung)\n"
            "- Beziehungen (relationships — Streit mit Freund/Familie, ein Geburtstagsgeschenk)\n\n"
            "Comprehension items: 7 richtig/falsch statements, in the order they appear in the dialogue. "
            "Each statement is a paraphrase of one specific claim made (or contradicted) in the conversation. "
            "Avoid statements about the speakers' inner emotions unless they are stated explicitly. "
            "Roughly half the statements should be richtig, half falsch — never all one or all the other.\n\n"
            "Output the script with explicit speaker tags: [Speaker A] and [Speaker B]. "
            "Give each speaker a consistent name early in the script (Anna, Markus) so the TTS layer can assign voices."
        ),
    },
    {
        "slug": "teil_4_diskussion",
        "name": "Teil 4 — Diskussion",
        "summary": "Radio/TV-style discussion between three speakers. Eight 'who said what' MCQ items.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat B1 Hören Teil 4.\n\n"
            "Audio: a radio or TV panel discussion with THREE speakers. Played TWICE on the real exam. "
            "Typically a moderator + two guests with differing viewpoints, or three guests on a topical issue.\n\n"
            "Length: 4–5 minutes, roughly 700–900 German words across all speakers. "
            "Speakers take longer turns than in Teil 3 (3–6 sentences each), with the moderator interjecting briefly.\n\n"
            "Voice/register: semi-formal Sie-form. Each speaker has a clear, distinct viewpoint that surfaces in their turns. "
            "Speakers can express agreement and disagreement (Da haben Sie recht, aber …; Das sehe ich anders, weil …).\n\n"
            "Topic catalog:\n"
            "- Wohnungsmarkt (housing market — Mietpreise, Eigentum, Wohngemeinschaften)\n"
            "- Arbeitswelt im Wandel (changing world of work — Homeoffice, Vier-Tage-Woche, KI bei der Arbeit)\n"
            "- Klima und Umwelt (climate and environment — Verkehr, Energie, persönliche Verantwortung)\n"
            "- Bildung (education — Schule, Studium, lebenslanges Lernen)\n"
            "- Gesundheit und Lebensstil (health and lifestyle — Ernährung, Bewegung, mentale Gesundheit)\n"
            "- Digitalisierung (digitalization — soziale Medien, Datenschutz, Online-Shopping)\n"
            "- Familie und Gesellschaft (family and society — Kindererziehung, Generationen, Rollenverteilung)\n\n"
            "Comprehension items: 8 MCQs of the form 'Wer sagt das?' (who says X). Three options: Speaker A, Speaker B, Speaker C. "
            "Each item is a paraphrase of one specific claim a single speaker makes. Distractors are claims the OTHER two speakers "
            "could plausibly have made given their stated positions, but didn't actually say in this script.\n\n"
            "Output the script with explicit speaker tags. Use named speakers: [Moderator: Maria], [Gast 1: Stefan], [Gast 2: Lena]. "
            "Each speaker's stance must be internally consistent across all their turns — Stefan can't agree with X in turn 2 and disagree with X in turn 5."
        ),
    },
]


def get_chapter_by_slug(slug: str):
    return next((c for c in DEUTSCH_B1_HOREN_CHAPTERS if c["slug"] == slug), None)


def get_chapter_by_name(name: str):
    return next((c for c in DEUTSCH_B1_HOREN_CHAPTERS if c["name"] == name), None)


# ── Topic catalogs per Teil ───────────────────────────────────────────────────
# A pool of concrete scenarios per Teil that the generator picks from at random
# (one per script). The catalogs are intentionally large and specific so that
# random selection produces real variety across exams. They override the
# topic-catalog hints embedded in each chapter's prose `content` blob — when
# `chosen_topic` is injected into the prompt, the model writes about exactly
# that scenario rather than picking a familiar default like "delayed train."

TOPICS_TEIL_1 = [
    # Train station / transport announcements
    "Bahnhofsansage über eine Verspätung wegen Personalmangels",
    "Bahnhofsansage über einen Gleiswechsel kurz vor Abfahrt",
    "Bahnhofsansage über einen Zugausfall wegen einer Stellwerksstörung",
    "S-Bahn-Ansage über eine Streckensperrung am Wochenende",
    "U-Bahn-Ansage über die letzte Bahn der Nacht",
    "Straßenbahn-Ansage über eine Umleitung wegen einer Demonstration",
    "Flughafen-Ansage über ein verändertes Boarding-Gate",
    "Flughafen-Ansage über eine wetterbedingte Verspätung",
    "Flughafen-Ansage über das Auffinden eines verlorenen Gegenstands",
    "Buslinien-Information am Haltestellen-Lautsprecher zur geänderten Route",
    "Fährenansage über das Beladen der Fahrzeuge",
    # Voicemails — friend / family / colleague / service
    "Mailbox-Nachricht von einer Freundin, die ein Treffen verschiebt",
    "Mailbox-Nachricht von einem Freund, der zu einem Geburtstag einlädt",
    "Mailbox-Nachricht von der Mutter über einen geplanten Familienbesuch",
    "Mailbox-Nachricht eines Kollegen über einen verschobenen Termin",
    "Mailbox-Nachricht des Vermieters über eine Wohnungsbesichtigung",
    "Mailbox-Nachricht der Werkstatt über das fertig reparierte Auto",
    "Mailbox-Nachricht der Arztpraxis über einen abgesagten Termin",
    "Mailbox-Nachricht des Friseurs zur Terminbestätigung",
    "Mailbox-Nachricht eines Nachbarn über ein angenommenes Paket",
    "Mailbox-Nachricht der Bibliothek über ein vorbestelltes Buch",
    "Mailbox-Nachricht eines Tierarztes mit Rückrufbitte",
    "Mailbox-Nachricht der Kita über einen krank werdenden Kollegen",
    # Weather / traffic
    "Wetterbericht für das kommende Wochenende mit Regenwarnung",
    "Wetterbericht mit einer Sturmwarnung für die Küstenregion",
    "Verkehrsfunk-Meldung über einen Stau auf der Autobahn A7",
    "Verkehrsfunk-Meldung über eine Vollsperrung wegen Bauarbeiten",
    "Verkehrsfunk-Meldung über Glatteis auf den Nebenstraßen",
    # Shop / venue announcements
    "Supermarkt-Ansage über die baldige Schließung am Abend",
    "Kaufhaus-Ansage über ein zeitlich begrenztes Sonderangebot",
    "Supermarkt-Ansage über ein vermisstes Kind an der Information",
    "Konzert-Ansage über den Beginn nach der Pause",
    "Kino-Ansage über eine technische Verzögerung beim Film",
    "Theater-Ansage zur Programmänderung wegen Krankheit",
    "Restaurant-Ansage über die bevorstehende Schließung der Küche",
    "Hotel-Frühstücks-Ansage über die Öffnungszeiten am Sonntag",
    "Schwimmbad-Ansage über bevorstehenden Beckenwechsel",
    "Museums-Ansage über die letzte Führung des Tages",
    "Bibliotheks-Ansage über die baldige Schließung",
    "Stadion-Ansage über die Sicherheitskontrollen am Eingang",
    # Phone IVR / office voicemails
    "Telefonansage einer Behörde mit Öffnungszeiten",
    "Telefonansage einer Bank mit einem Optionen-Menü",
    "Telefonansage einer Versicherung mit Notfallnummer",
    "Telefonansage einer Schule über Krankmeldungen",
    # Misc public-service info
    "Ansage über die Müllabfuhr im neuen Quartal",
    "Ansage über eine geplante Wasserabschaltung wegen Bauarbeiten",
    "Ansage einer Apotheke über lange Wartezeiten am Wochenende",
    "Ansage einer Tankstelle über eine Wagenwäsche-Aktion",
    "Ansage am Recyclinghof über neue Öffnungszeiten",
]

TOPICS_TEIL_2 = [
    "Stadtführung durch Berlin mit Hinweisen zum Brandenburger Tor und Reichstag",
    "Stadtführung durch München mit Fokus auf Marienplatz und Englischer Garten",
    "Stadtführung durch Hamburg mit Schwerpunkt Speicherstadt und Hafen",
    "Museumsführung im Pergamonmuseum mit Fokus auf antike Architektur",
    "Museumsführung im Deutschen Museum München zur Geschichte der Technik",
    "Museumsführung in einem Kunstmuseum zur Moderne",
    "Betriebsführung in einer mittelständischen Druckerei",
    "Betriebsführung auf einem Bio-Bauernhof",
    "Betriebsführung in einer Autofabrik",
    "Betriebsführung in einer Bäckerei mit traditionellem Backofen",
    "Universitätsorientierung für Erstsemester in München",
    "Volkshochschulkurs-Einführung zu einem Sprachkurs Italienisch",
    "Workshop-Einführung für ein Fotografie-Wochenende",
    "Workshop-Einführung für einen Töpferkurs",
    "Bus-Reiseleitung auf einer Tagesfahrt durch das Rheintal",
    "Vereinsversammlung eines Sportvereins zum Saisonbeginn",
    "Hotelorientierung für neue Gäste eines Wellnesshotels",
    "Sicherheitseinweisung für neue Mitarbeiter in einem Lager",
    "Erste-Hilfe-Kurs Eröffnung im Vereinsheim",
    "Kochkurs-Einführung für italienische Küche",
    "Kochkurs-Einführung für vegane Küche",
    "Sportverein-Aufnahme für neue Mitglieder",
    "Fitnessstudio-Orientierung am ersten Tag",
    "Tagungseröffnung einer Branchenkonferenz im Bereich Bildung",
    "Mitarbeiter-Versammlung zur Vorstellung einer neuen Unternehmensstrategie",
    "Theaterbesuch-Einführung vor einer Aufführung von Schiller",
    "Konzerteinführung mit Hintergrundinformationen zum Komponisten",
    "Filmvorführungs-Einleitung im Programmkino",
    "Ausstellungseröffnung in einer Galerie für zeitgenössische Kunst",
    "Buchpräsentation in einer Buchhandlung",
    "Naturparkführung mit Informationen zur Tierwelt",
    "Botanischer Garten Führung zu seltenen Pflanzen",
    "Zoo-Führung mit Schwerpunkt auf Erhaltungszucht",
    "Stadtarchiv-Vorstellung für Familienforscher",
    "Recyclinghof-Führung für eine Schulklasse",
    "Kraftwerks-Führung mit Erklärung der Energiewende",
    "Bibliotheksführung für neue Mitglieder",
    "Schulführung für Eltern beim Tag der offenen Tür",
    "Bauernhof-Führung mit Schwerpunkt auf Tierhaltung",
    "Brauerei-Führung mit Verkostung",
    "Kaffeerösterei-Führung mit Erläuterung des Röstprozesses",
    "Schokoladenfabrik-Führung",
    "Käserei-Führung mit Demonstration der Herstellung",
]

TOPICS_TEIL_3 = [
    "Zwei Freundinnen planen ein gemeinsames Wochenende am See",
    "Zwei Kollegen besprechen das geplante Sommerfest der Firma",
    "Ein Paar plant einen Urlaub auf Mallorca",
    "Ein Paar diskutiert über ein Reiseziel für die Herbstferien",
    "Zwei Freunde diskutieren über eine geplante Wohnungsbesichtigung",
    "Eine Freundin erzählt ihrer Mitbewohnerin von einem Streit mit dem Vermieter",
    "Zwei Kollegen besprechen die Vorbereitung auf ein Bewerbungsgespräch",
    "Zwei Freunde diskutieren, welches Geburtstagsgeschenk für eine gemeinsame Freundin passt",
    "Ein Paar entscheidet, in welches Restaurant sie am Samstag gehen",
    "Zwei Freundinnen empfehlen sich gegenseitig Filme und Serien",
    "Zwei Studenten besprechen, welche Bücher sie für ein Seminar lesen sollten",
    "Zwei Freunde planen einen gemeinsamen Konzertbesuch",
    "Ein Paar plant einen gemeinsamen Einkauf für eine Geburtstagsfeier",
    "Zwei Kollegen sprechen über einen neuen Sport, den sie ausprobieren wollen",
    "Zwei Freundinnen tauschen sich über ihre Hobbys aus",
    "Zwei Sprachschüler besprechen, wie sie ihre Sprachkenntnisse verbessern können",
    "Zwei Freunde planen einen Kochabend mit neuen Rezepten",
    "Ein Paar bespricht den Kauf eines Gebrauchtwagens",
    "Zwei Freunde diskutieren über die Reparatur eines defekten Fahrrads",
    "Ein Paar plant einen Umzug in eine neue Stadt",
    "Zwei Kollegen sprechen über die Renovierung ihrer Wohnung",
    "Zwei Freundinnen besprechen die Pflege eines neuen Haustiers",
    "Ein Paar plant den Besuch bei den Eltern am Wochenende",
    "Zwei Freundinnen besprechen die Hochzeitsplanung der einen",
    "Eine Mutter erzählt einer Freundin von Schulproblemen ihrer Tochter",
    "Zwei Studenten besprechen die Wahl eines Praktikumsplatzes",
    "Zwei Kollegen tauschen sich nach einem Bewerbungsgespräch aus",
    "Zwei Mitarbeiter sprechen über Probleme mit einem Kollegen",
    "Eine Freundin berichtet einer anderen von einem Mietproblem",
    "Zwei Freunde tauschen sich über eine Auslandsreise aus",
    "Zwei Nachbarn diskutieren über laute Musik im Hausflur",
    "Zwei Kollegen besprechen einen geplanten Teamausflug",
    "Eine Studentin und ihre Mutter sprechen über die Wahl eines Studiengangs",
    "Zwei Freundinnen planen einen Fitness-Trainingsplan zusammen",
    "Zwei Freunde organisieren eine Überraschungsparty",
    "Ein Paar bespricht, ob sie ein Haustier anschaffen sollen",
    "Eine Kundin und ein Kellner besprechen Allergien beim Bestellen",
    "Eine Bürgerin und eine Beraterin in der Touristen-Information besprechen Ausflüge",
]

TOPICS_TEIL_4 = [
    "Diskussion über steigende Mietpreise in deutschen Großstädten",
    "Diskussion über die Vier-Tage-Woche in deutschen Unternehmen",
    "Diskussion über Homeoffice und seine Auswirkungen auf die Arbeitskultur",
    "Diskussion über Klimaschutz im Alltag",
    "Diskussion über ein generelles Tempolimit auf deutschen Autobahnen",
    "Diskussion über Schulreformen und Digitalisierung im Klassenzimmer",
    "Diskussion über lebenslanges Lernen und Weiterbildung",
    "Diskussion über vegetarische und vegane Ernährung",
    "Diskussion über die Zukunft des Einzelhandels",
    "Diskussion über Online-Shopping und Datenschutz",
    "Diskussion über soziale Medien und psychische Gesundheit",
    "Diskussion über Kinderbetreuung und Vereinbarkeit von Beruf und Familie",
    "Diskussion über die Rolle von Vätern in der Erziehung",
    "Diskussion über Pflege im Alter",
    "Diskussion über das deutsche Rentensystem",
    "Diskussion über die Energiewende und Atomkraft",
    "Diskussion über öffentlichen Nahverkehr versus Auto",
    "Diskussion über Tourismus in beliebten Reisezielen",
    "Diskussion über Wohnformen der Zukunft (Tiny House, WG)",
    "Diskussion über Mehrsprachigkeit in der Schule",
    "Diskussion über Künstliche Intelligenz im Berufsleben",
    "Diskussion über Gleichberechtigung am Arbeitsplatz",
    "Diskussion über Sport und Bewegung im Alltag",
    "Diskussion über gesunde Ernährung in Schulen",
    "Diskussion über Plastikvermeidung im Haushalt",
    "Diskussion über regionale versus globale Lebensmittel",
    "Diskussion über E-Bikes und Verkehrssicherheit",
    "Diskussion über Smart Home und Lebensqualität",
    "Diskussion über Online-Lernen versus Präsenzunterricht",
    "Diskussion über Lehrermangel an deutschen Schulen",
    "Diskussion über das Gesundheitssystem in Deutschland",
    "Diskussion über das ehrenamtliche Engagement in der Gesellschaft",
    "Diskussion über die Wohnsituation von Studierenden",
    "Diskussion über die Zukunft des Buchhandels",
    "Diskussion über Mode und Nachhaltigkeit",
    "Diskussion über das Tierwohl in der Landwirtschaft",
]


TOPICS_BY_TEIL: dict[int, list[str]] = {
    1: TOPICS_TEIL_1,
    2: TOPICS_TEIL_2,
    3: TOPICS_TEIL_3,
    4: TOPICS_TEIL_4,
}


def topics_for_teil(teil: int) -> list[str]:
    """Return the full topic catalog for a given Teil."""
    return TOPICS_BY_TEIL.get(teil, [])


def build_corpus_text(focus_chapter_slugs: list[str] | None = None) -> str:
    """Concatenate chapter format specs, optionally filtered to a subset."""
    chapters = DEUTSCH_B1_HOREN_CHAPTERS
    if focus_chapter_slugs:
        focus_set = set(focus_chapter_slugs)
        filtered = [c for c in DEUTSCH_B1_HOREN_CHAPTERS if c["slug"] in focus_set]
        if filtered:
            chapters = filtered
    parts = []
    for ch in chapters:
        parts.append(f"--- Chapter: {ch['name']} ---\n{ch['content']}")
    return "\n\n".join(parts)
