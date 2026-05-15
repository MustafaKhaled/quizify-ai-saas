"""
Static chapter knowledge base for the German A2 Hören (listening) agent.

Mirrors the B1 Hören chapters file. Each "chapter" maps to one of the four
Teile of the Goethe-Zertifikat A2 / telc A2 / ÖSD A2 listening section. The
corpus content for each Teil is the *format spec* (length, voices, topic,
comprehension question type) — not example transcripts. Real A2 exam
transcripts are copyright Goethe-Institut and not redistributable; we generate
fresh scripts that match the format.

A2 differs from B1 in three ways the format spec encodes:

  1. **Vocabulary & sentence structure.** Everyday topics, simple main clauses
     joined by und/aber/oder/denn. Subjunctive limited to möchte / könnte /
     hätte. Perfekt preferred over Präteritum.
  2. **Length.** Each script is ~50–60% the word count of the equivalent B1
     Teil so test-takers can keep up at A2 listening speed.
  3. **Item counts in Teil 3 and Teil 4.** A2 caps both at 5 items per Teil,
     vs B1's 7 (Teil 3) and 8 (Teil 4).

The agent's instructions.md tells the model how to produce a script + matching
comprehension item that fits the active Teil's format spec.
"""

DEUTSCH_A2_HOREN_CHAPTERS = [
    {
        "slug": "teil_1_kurze_mitteilungen",
        "name": "Teil 1 — Kurze Mitteilungen",
        "summary": "Five short single-speaker monologues (announcements, voicemails, info messages). One comprehension item per text.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat A2 Hören Teil 1.\n\n"
            "Audio: 5 short, independent monologues. Each is a single speaker. "
            "Played TWICE on the real A2 exam (the test-taker hears each text twice).\n\n"
            "Length per script: 15–25 seconds of speech, roughly 40–70 German words at normal speaking pace. "
            "Significantly shorter than B1 — A2 listeners need bounded chunks of input.\n\n"
            "Voice/register: a clear single speaker. Register depends on the context — formal for an announcement at a station "
            "or in a workplace, casual for a friend leaving a voicemail, neutral for a recorded info line.\n\n"
            "Topic catalog (rotate across these so a generated batch covers the breadth of the Teil):\n"
            "- Bahnhofsansagen (train station — Verspätung, Gleiswechsel)\n"
            "- Flughafenansagen (airport — Boarding, Gate change)\n"
            "- Wetterbericht (simple weather report)\n"
            "- Verkehrsmeldungen (simple traffic reports)\n"
            "- Mailbox-Nachrichten von Freunden / Familie / Kollegen\n"
            "- Geschäftsansagen (shop announcements — opening hours, special offers)\n"
            "- Veranstaltungsansagen (event announcements — Beginn, Pause)\n"
            "- Schul- und Kindergartensansagen (school / Kita announcements)\n"
            "- Telefonansagen (Praxis, Apotheke, Behörde — Öffnungszeiten)\n\n"
            "Comprehension item per script: one MCQ with 3 options. "
            "The question targets a specific concrete fact in the script (a number, a place, a time, a reason). "
            "Distractors are values that COULD have been said but weren't — never random other German words.\n\n"
            "A2 vocabulary range: everyday A2 — family, daily routines, weather, shopping, hobbies, school, simple work, "
            "transport, food, basic health. Avoid academic, technical, professional, abstract or political vocabulary. "
            "Numbers, dates, times, and place names appear frequently and clearly."
        ),
    },
    {
        "slug": "teil_2_kurze_praesentation",
        "name": "Teil 2 — Kurze Präsentation",
        "summary": "One short single-speaker presentation (intro, school tour, club info). Five MCQ comprehension items.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat A2 Hören Teil 2.\n\n"
            "Audio: ONE short monologue — an intro talk, simple school or club tour, museum welcome, "
            "course orientation, or workshop intro. Speaker is in a presenter role.\n\n"
            "Length: 1.5–2.5 minutes of speech, roughly 200–350 German words. Played ONCE.\n\n"
            "Voice/register: single speaker, semi-formal. Speaker uses simple signposting "
            "(zuerst, dann, danach, am Ende). Sentences stay short.\n\n"
            "Topic catalog:\n"
            "- Schulführung (school tour for new students or parents) — Klassenzimmer, Mensa, Sporthalle\n"
            "- Stadtführung für Schüler oder Anfänger (simple city tour)\n"
            "- Vereins-Einführung (sports club, music club intro for new members)\n"
            "- Volkshochschulkurs-Begrüßung (course welcome — Italienisch, Yoga, Kochen)\n"
            "- Kindergarten- oder Hort-Vorstellung für Eltern\n"
            "- Hotel- oder Pension-Begrüßung für Gäste\n"
            "- Museumsbegrüßung mit einfacher Übersicht der Räume\n"
            "- Sportzentrums-Orientierung am ersten Tag\n"
            "- Bibliotheks-Einführung für neue Mitglieder\n"
            "- Restaurant-Vorstellung am Buffet\n\n"
            "Comprehension items: 5 MCQs with 3 options each. Items follow the order of the speech (item 1 about "
            "an early section, item 5 about the closing section). Distractors are facts that COULD be true based on "
            "the topic but contradict the script's specifics.\n\n"
            "Structural signposting in the script is required so test-takers can follow the order of information. "
            "Use simple connectors: zuerst, dann, danach, am Ende, zum Schluss."
        ),
    },
    {
        "slug": "teil_3_gespraech",
        "name": "Teil 3 — Gespräch",
        "summary": "Informal dialogue between two friends, family members, or colleagues. Five richtig/falsch comprehension items.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat A2 Hören Teil 3.\n\n"
            "Audio: a natural conversation between TWO speakers — typically two friends, two colleagues, "
            "two family members, or a customer and a service worker. Played TWICE on the real exam.\n\n"
            "Length: 2–2.5 minutes, roughly 300–500 German words spread across both speakers. "
            "Each speaker has multiple turns; turns are SHORT (1–3 sentences typical).\n\n"
            "Voice/register: informal du-form between friends/family, or polite Sie-form for service interactions. "
            "Use real conversational features at A2 level: agreement (genau, klar, ja), short questions (echt?, wirklich?), "
            "simple feedback (ach so, na ja, gut). Avoid complex hesitations or argumentative back-and-forth.\n\n"
            "Topic catalog:\n"
            "- Wochenendpläne (weekend plans — Treffen, Kino, Besuch)\n"
            "- Einkaufen (shopping plans — Geschenke, Geburtstag, Lebensmittel)\n"
            "- Hobbys (hobbies — Sport, Musik, Lesen)\n"
            "- Familie (family — Geschwister, Eltern, Besuch bei Verwandten)\n"
            "- Schule und Lernen (school and learning — Hausaufgaben, Prüfungen, Sprachen lernen)\n"
            "- Wohnen (simple flat talk — neue Wohnung, Möbel, Nachbarn)\n"
            "- Essen und Trinken (food talk — Lieblingsessen, Restaurant, Kochen zu Hause)\n"
            "- Reisen (simple travel plans — Urlaub, Ausflug, Verkehrsmittel)\n"
            "- Gesundheit (basic health — Arzttermin, krank sein, Sport)\n"
            "- Wetter und Jahreszeiten (weather and seasons — Plan abhängig vom Wetter)\n\n"
            "Comprehension items: 5 richtig/falsch statements (NOT 7 like B1), in the order they appear in the dialogue. "
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
        "summary": "Simple radio-style discussion between three speakers about everyday preferences. Five 'who said what' MCQ items.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat A2 Hören Teil 4 (simplified, A2 level).\n\n"
            "Audio: a short radio panel with THREE speakers — typically a moderator + two guests sharing simple "
            "preferences or everyday opinions. NOT a heated debate — a friendly exchange of personal preferences. "
            "Played TWICE on the real exam.\n\n"
            "Length: 2.5–3.5 minutes, roughly 400–600 German words across all speakers. "
            "Speakers take SHORT turns (2–4 sentences each), with the moderator interjecting briefly.\n\n"
            "Voice/register: semi-formal Sie-form. Each speaker has a clear, distinct preference that surfaces in their turns. "
            "Speakers can softly disagree (Ich finde das anders. / Bei mir ist das so:) but no aggressive argument or "
            "complex political stance.\n\n"
            "Topic catalog (deliberately concrete and personal, NOT abstract debate topics):\n"
            "- Sport im Alltag (which sport people like, when they exercise)\n"
            "- Lieblingsessen (favorite foods, vegetarian / meat preferences at A2 level)\n"
            "- Urlaub am Meer oder in den Bergen (vacation preferences)\n"
            "- Musik im Alltag (favorite music, where/when they listen)\n"
            "- Lesen oder Filme schauen (reading vs movies)\n"
            "- Stadt- oder Landleben (city vs countryside life)\n"
            "- Auto, Fahrrad oder öffentliche Verkehrsmittel (transport preferences)\n"
            "- Frühaufsteher oder Nachtmensch (morning vs evening person)\n"
            "- Lieblingsjahreszeit (favorite season and why)\n"
            "- Hobbys nach der Arbeit (after-work hobbies)\n"
            "- Kochen oder Essen gehen (cooking at home vs eating out)\n\n"
            "Comprehension items: 5 MCQs (NOT 8 like B1) of the form 'Wer sagt das?' (who says X). "
            "Three options: Speaker A, Speaker B, Speaker C. "
            "Each item is a paraphrase of one specific claim a single speaker makes. Distractors are claims the OTHER two "
            "speakers could plausibly have made given their stated preferences, but didn't actually say in this script. "
            "Each guest should be the correct answer at least once across the 5 items.\n\n"
            "Output the script with explicit speaker tags. Use named speakers: [Moderator: Maria], [Gast 1: Stefan], [Gast 2: Lena]. "
            "Each speaker's preference must be internally consistent across all their turns — Stefan can't prefer X in turn 2 and prefer Y in turn 4."
        ),
    },
]


def get_chapter_by_slug(slug: str):
    return next((c for c in DEUTSCH_A2_HOREN_CHAPTERS if c["slug"] == slug), None)


def get_chapter_by_name(name: str):
    return next((c for c in DEUTSCH_A2_HOREN_CHAPTERS if c["name"] == name), None)


# ── Topic catalogs per Teil ───────────────────────────────────────────────────
# A2-adapted pool of concrete scenarios per Teil. Topics are deliberately simpler
# and more concrete than the B1 catalog — everyday life, family, simple work
# situations, basic services. The generator picks one at random per script so
# successive exams don't keep producing the same default scenarios.

TOPICS_TEIL_1 = [
    # Train / transport announcements
    "Bahnhofsansage über eine Verspätung von zehn Minuten",
    "Bahnhofsansage über einen Gleiswechsel",
    "S-Bahn-Ansage über eine kurze Pause am nächsten Bahnhof",
    "U-Bahn-Ansage über die letzte Bahn am Abend",
    "Straßenbahn-Ansage über eine geänderte Endhaltestelle",
    "Bus-Ansage über eine kurze Umleitung",
    "Flughafen-Ansage über ein neues Boarding-Gate",
    "Flughafen-Ansage über eine Verspätung wegen Wetter",
    # Voicemails — friend / family / colleague / service
    "Mailbox von einer Freundin, die das Treffen verschiebt",
    "Mailbox von einem Freund mit Einladung zum Geburtstag",
    "Mailbox von der Mutter mit Einladung zum Mittagessen",
    "Mailbox vom Vater mit einer Frage zum Wochenende",
    "Mailbox von einer Kollegin über einen späteren Termin",
    "Mailbox vom Vermieter über eine kurze Wohnungsbesichtigung",
    "Mailbox aus der Werkstatt — das Auto ist fertig",
    "Mailbox aus der Arztpraxis über einen verschobenen Termin",
    "Mailbox vom Friseur zur Bestätigung eines Termins",
    "Mailbox aus der Kita über einen krank gewordenen Erzieher",
    "Mailbox aus der Bibliothek — ein Buch ist abholbereit",
    # Weather / traffic — simple
    "Wetterbericht für das Wochenende mit einem Regentag",
    "Wetterbericht für die nächste Woche mit Sonne und Wärme",
    "Wetterbericht über einen kalten Tag mit Schnee",
    "Verkehrsmeldung über einen kurzen Stau auf der Autobahn",
    "Verkehrsmeldung über Bauarbeiten in der Innenstadt",
    # Shop / venue announcements
    "Supermarkt-Ansage über die Schließung in zehn Minuten",
    "Supermarkt-Ansage über ein Angebot bei Obst und Gemüse",
    "Kaufhaus-Ansage über ein Sonderangebot bei Kleidung",
    "Bäckerei-Ansage über frisches Brot am Nachmittag",
    "Café-Ansage über die Pause zwischen Frühstück und Mittag",
    "Restaurant-Ansage über die Schließung der Küche um 22 Uhr",
    "Schwimmbad-Ansage über die Schließung am Abend",
    "Museums-Ansage über die letzte Führung des Tages",
    "Bibliotheks-Ansage über die baldige Schließung",
    "Kino-Ansage über den Beginn des Films in fünf Minuten",
    "Konzert-Ansage über eine kurze Pause",
    "Theater-Ansage über den Beginn nach der Pause",
    # Phone / public-service info
    "Telefonansage einer Praxis über die Öffnungszeiten",
    "Telefonansage einer Apotheke über den Notdienst am Wochenende",
    "Telefonansage einer Behörde über Öffnungszeiten",
    "Telefonansage einer Schule für Krankmeldungen",
    "Telefonansage einer Bank mit einem einfachen Menü",
    # School / Kita / family-life
    "Schulansage über einen verschobenen Schulausflug",
    "Schulansage über das Schulfest am Samstag",
    "Kita-Ansage über einen freien Tag wegen Renovierung",
    "Sportverein-Ansage über das Training am Mittwoch",
    "Musikschule-Ansage über einen Raumwechsel",
]

TOPICS_TEIL_2 = [
    "Schulführung für neue Schüler mit Klassenzimmern und Mensa",
    "Schulführung für Eltern beim Tag der offenen Tür",
    "Stadtführung für Schüler in Berlin",
    "Stadtführung für Anfänger in München",
    "Stadtführung für eine Klassenfahrt in Hamburg",
    "Sportverein-Begrüßung für neue Mitglieder",
    "Tennisclub-Vorstellung mit Trainingszeiten",
    "Volkshochschulkurs-Begrüßung für einen Italienisch-Anfängerkurs",
    "Volkshochschulkurs-Begrüßung für einen Kochkurs",
    "Volkshochschulkurs-Begrüßung für einen Yogakurs",
    "Hotel-Begrüßung für Gäste mit Frühstück und Schwimmbad",
    "Pension-Begrüßung mit Hinweisen zu Frühstück und Zimmern",
    "Jugendherberge-Vorstellung für eine Schulklasse",
    "Kindergarten-Vorstellung für Eltern mit Räumen und Tagesablauf",
    "Hort-Einführung für Eltern mit Hausaufgabenbetreuung",
    "Museumsbegrüßung mit einfacher Übersicht der Ausstellungen",
    "Kindermuseum-Begrüßung mit Hinweisen zu Spielbereichen",
    "Sportzentrums-Orientierung am ersten Tag",
    "Fitnessstudio-Begrüßung am Probetag",
    "Schwimmbad-Einführung mit Bahnen und Öffnungszeiten",
    "Bibliotheks-Einführung für neue Mitglieder",
    "Restaurant-Vorstellung am Buffet bei einem Brunch",
    "Bus-Reiseleitung auf einer Tagesfahrt zum See",
    "Zoo-Führung für Kinder mit Tierhäusern",
    "Bauernhof-Besuch für Schulkinder",
    "Bäckerei-Besichtigung für eine Kindergruppe",
    "Tagesheim für Senioren — Vorstellung der Aktivitäten",
    "Kursvorstellung für einen Schwimmkurs für Anfänger",
    "Tanzkurs-Begrüßung für ein Anfängerkurs",
    "Konzert-Einführung im Stadtpark mit dem Programm",
    "Kinder-Theater-Einführung vor der Vorstellung",
    "Stadtteilfest-Einführung mit den Programmpunkten",
]

TOPICS_TEIL_3 = [
    "Zwei Freundinnen planen einen Kinobesuch am Samstag",
    "Zwei Freunde besprechen den Einkauf für eine Geburtstagsfeier",
    "Ein Paar plant einen Familienbesuch bei den Eltern",
    "Eine Mutter und ein Sohn besprechen die Schultasche für morgen",
    "Zwei Schüler besprechen die Hausaufgaben für Mathe",
    "Zwei Studenten planen, gemeinsam für eine Prüfung zu lernen",
    "Zwei Kollegen sprechen über das Mittagessen in der Kantine",
    "Zwei Freundinnen tauschen sich über ihre Hobbys aus",
    "Eine Freundin erzählt einer anderen von ihrem Wochenende",
    "Zwei Freunde planen einen Ausflug an den See",
    "Ein Paar bespricht eine kurze Reise nach Hamburg",
    "Zwei Nachbarinnen sprechen über das Wetter und den Garten",
    "Eine Tochter und ihre Mutter sprechen über Kleidung für die Schule",
    "Zwei Brüder besprechen ein Geschenk für die Schwester",
    "Zwei Freundinnen planen einen Café-Besuch nach der Arbeit",
    "Ein Vater und sein Kind besprechen den Sportverein",
    "Zwei Studenten besprechen, welche Sprache sie als nächstes lernen",
    "Eine Patientin und der Arzt sprechen über Medikamente",
    "Eine Kundin und der Verkäufer im Schuhgeschäft sprechen über die Größe",
    "Eine Kundin und die Bäckerin sprechen über Brot und Brötchen",
    "Zwei Freunde besprechen ein neues Restaurant in der Stadt",
    "Zwei Freundinnen sprechen über ein Buch, das sie beide gelesen haben",
    "Eine Mutter und ihre Tochter sprechen über eine Geburtstagsparty",
    "Zwei Schüler besprechen einen Schulausflug ins Museum",
    "Zwei Kollegen sprechen über eine geplante Fortbildung",
    "Ein Paar entscheidet, was sie am Wochenende kochen",
    "Zwei Freundinnen planen ein Picknick im Park",
    "Zwei Freunde besprechen, wann sie zusammen Sport machen",
    "Eine Patientin und die Sprechstundenhilfe sprechen über einen Termin",
    "Ein Mieter und der Hausmeister sprechen über die Heizung",
    "Eine Mutter und ihre Tochter besprechen ein neues Hobby",
    "Zwei Freundinnen sprechen über ein Konzert am Wochenende",
    "Zwei Freunde besprechen, welches Geschenk gut für die Lehrerin ist",
    "Zwei Mitschüler sprechen über die nächste Klassenarbeit",
    "Ein Paar plant den Wocheneinkauf im Supermarkt",
]

TOPICS_TEIL_4 = [
    "Diskussion über Lieblingssport im Alltag",
    "Diskussion über Lieblingsessen und Kochen zu Hause",
    "Diskussion über Urlaub am Meer oder in den Bergen",
    "Diskussion über Musik im Alltag und Lieblingsstil",
    "Diskussion über Lesen oder Filme schauen am Abend",
    "Diskussion über Stadtleben oder Landleben",
    "Diskussion über Auto, Fahrrad oder Bus im Alltag",
    "Diskussion über Frühaufsteher oder Nachtmensch sein",
    "Diskussion über die Lieblingsjahreszeit",
    "Diskussion über Hobbys nach der Arbeit oder Schule",
    "Diskussion über Kochen zu Hause oder Essen gehen",
    "Diskussion über Sport im Verein oder allein",
    "Diskussion über Bücher oder Hörbücher",
    "Diskussion über Frühstück zu Hause oder im Café",
    "Diskussion über Familienurlaub oder Urlaub mit Freunden",
    "Diskussion über Garten oder Balkon — wer hat was",
    "Diskussion über Tierhaltung — Hund, Katze oder kein Tier",
    "Diskussion über Musik machen oder Musik hören",
    "Diskussion über Sprachen lernen — wann macht es Spaß",
    "Diskussion über Sport im Sommer oder im Winter",
    "Diskussion über Geschenke selbst machen oder kaufen",
    "Diskussion über Lieblingsfest im Jahr",
    "Diskussion über Wochenende zu Hause oder unterwegs",
    "Diskussion über Lieblingsplätze in der Stadt",
    "Diskussion über Lernen am Morgen oder am Abend",
    "Diskussion über Sport allein oder mit Freunden",
    "Diskussion über Telefon oder Schreiben mit Freunden",
    "Diskussion über Lesen am Strand oder Wandern in den Bergen",
    "Diskussion über Brot kaufen oder selber backen",
    "Diskussion über alte oder neue Möbel in der Wohnung",
    "Diskussion über Geschenke zu Weihnachten — selbst gemacht oder gekauft",
    "Diskussion über Picknick im Park oder Restaurant",
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
    chapters = DEUTSCH_A2_HOREN_CHAPTERS
    if focus_chapter_slugs:
        focus_set = set(focus_chapter_slugs)
        filtered = [c for c in DEUTSCH_A2_HOREN_CHAPTERS if c["slug"] in focus_set]
        if filtered:
            chapters = filtered
    parts = []
    for ch in chapters:
        parts.append(f"--- Chapter: {ch['name']} ---\n{ch['content']}")
    return "\n\n".join(parts)
