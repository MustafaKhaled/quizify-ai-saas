"""
Static chapter knowledge base for the German A2 Lesen (Reading) agent.

Mirrors the B1 Lesen chapters file. Maps to the four Teile of the
Goethe-Zertifikat A2 reading section (vs B1's five). Real A2 reading passages
are copyright Goethe-Institut and not redistributable; we generate fresh
material that matches the format spec.

A2 differs from B1 in the following ways the format spec encodes:

  1. Four Teile instead of five (no separate institutional-text Teil).
  2. Vocabulary range — everyday topics, simple sentence structure, mostly
     present + Perfekt tense. No Konjunktiv II beyond möchte/könnte/hätte.
  3. Teil 2 is unique: a building/store directory + 5 MCQ where the user
     picks which floor an item is on. No B1 equivalent.
  4. Teil 4 (matching) uses a smaller pool of 6 ads (a–f) with 5 situations,
     and the no-match marker is 'X' instead of B1's '0'.

The agent's instructions.md tells the model how to produce each shape.
"""

DEUTSCH_A2_LESEN_CHAPTERS = [
    {
        "slug": "teil_1_zeitungstext",
        "name": "Teil 1 — Zeitungstext",
        "summary": "One short newspaper article (~150–250 words). Five MCQ comprehension items.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat A2 Lesen Teil 1.\n\n"
            "Source text: ONE short newspaper-style article. Press-article register, "
            "third-person, factual. Topic should be person-focused (a profile of someone) "
            "or community-focused (a local project) so question stems can ask about "
            "who/what/when/where.\n\n"
            "Length: 150–250 German words.\n\n"
            "Voice/register: factual, neutral. Sentences stay short. Use simple "
            "connectors (jedoch, deshalb, danach, am Ende).\n\n"
            "Topic catalog — pick one:\n"
            "- Ein Koch / eine Köchin im Fernsehen\n"
            "- Ein Sportler / eine Sportlerin mit besonderer Geschichte\n"
            "- Ein Lehrer / eine Lehrerin mit einer ungewöhnlichen Methode\n"
            "- Eine Familie, die etwas Besonderes macht\n"
            "- Ein Schulprojekt mit Erfolg\n"
            "- Ein neues Café, eine neue Bäckerei mit besonderer Idee\n"
            "- Ein Verein, der etwas Gutes für die Stadt tut\n"
            "- Ein junger Mensch mit ungewöhnlichem Hobby\n"
            "- Eine Stadtbibliothek mit neuen Angeboten\n"
            "- Ein Kindergarten mit besonderem Programm\n\n"
            "Comprehension items: 5 MCQs with 3 options each (a/b/c). "
            "Items follow the order of the article. Distractors are facts that COULD be "
            "true based on the topic but contradict the article's specifics."
        ),
    },
    {
        "slug": "teil_2_wegweiser",
        "name": "Teil 2 — Wegweiser",
        "summary": "Building or department-store directory + 5 MCQ items asking which floor / area an item is on.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat A2 Lesen Teil 2.\n\n"
            "Source text: a building or department-store directory listing what's on each "
            "floor. Format the passage as floor-by-floor lines, e.g.:\n\n"
            "  Untergeschoss (UG): Lebensmittel, Drogerie, Getränke\n"
            "  Erdgeschoss (EG): Information, Schmuck, Parfümerie\n"
            "  1. Stock: Damenmode, Damenschuhe\n"
            "  2. Stock: Herrenmode, Herrenschuhe\n"
            "  3. Stock: Kindermode, Spielwaren\n"
            "  4. Stock: Restaurant, Café, Toiletten\n\n"
            "Length: 80–150 German words total. Cover at least 5 floors. Each line lists "
            "3–6 items, kept short and concrete.\n\n"
            "Building catalog — pick ONE:\n"
            "- Kaufhaus / Warenhaus\n"
            "- Bürgerzentrum mit Ämtern und Beratungsstellen\n"
            "- Sportkomplex mit verschiedenen Hallen und Räumen\n"
            "- Bibliothek über mehrere Stockwerke\n"
            "- Krankenhaus mit Stationen und Ambulanzen\n"
            "- Volkshochschule mit verschiedenen Räumen\n"
            "- Hotel mit Frühstücksraum, Wellness, Tagungsräumen\n"
            "- Universitätsgebäude mit Hörsälen, Mensa, Bibliothek\n\n"
            "Comprehension items: 5 MCQs with 3 options each. Each question asks 'Sie "
            "suchen <something> — wo finden Sie das?' and the options are 3 floors drawn "
            "from the directory plus optionally 'anderer Stock' as a no-match decoy.\n\n"
            "Hard composition rules:\n"
            "  - Each question's options are 3 floors (e.g. ['EG', '1. Stock', '2. Stock']) "
            "or 2 floors + 'anderer Stock'.\n"
            "  - At least one (NOT more than two) of the 5 questions has 'anderer Stock' "
            "as the correct answer — i.e. the searched item isn't actually in the directory.\n"
            "  - correct_index points to the option in THIS question's options array.\n"
            "  - Question stems MUST paraphrase the searched item — don't copy directory "
            "category names verbatim. Example: directory says 'Kindermode, Spielwaren' → "
            "question says 'Sie suchen ein Geschenk für ein Kind', not 'Sie suchen Spielwaren'."
        ),
    },
    {
        "slug": "teil_3_email",
        "name": "Teil 3 — E-Mail",
        "summary": "One personal email (~150–230 words). Five MCQ comprehension items.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat A2 Lesen Teil 3.\n\n"
            "Source text: ONE personal email between friends, family members, or a "
            "person and a service. Conversational tone, du-form between friends, polite "
            "Sie-form for service interactions.\n\n"
            "Length: 150–230 German words. Start with 'Hallo <Name>,' or 'Liebe/r "
            "<Name>,'. End with 'Viele Grüße, <sender>' or similar.\n\n"
            "Topic catalog — pick ONE:\n"
            "- Geburtstagseinladung mit Plänen für die Feier\n"
            "- Wochenendplanung mit Treffen, Kino, Ausflug\n"
            "- Bericht von einer Reise mit Erlebnissen\n"
            "- Bericht vom ersten Tag im neuen Job\n"
            "- Einladung zu einer Party mit Hinweisen zu Essen und Zeit\n"
            "- E-Mail an die Eltern aus dem Urlaub\n"
            "- E-Mail an eine Freundin mit Plänen für den Sommer\n"
            "- E-Mail an einen Kollegen mit Verschiebung eines Termins\n"
            "- E-Mail an die Sprachschule mit Frage zum Kurs\n"
            "- E-Mail an die Vermieterin mit Bitte um Reparatur\n\n"
            "Comprehension items: 5 MCQs with 3 options each. Items follow the order of "
            "the email. Distractors are plans/facts the writer could plausibly mention "
            "but didn't, or wrong specifics for things they did mention."
        ),
    },
    {
        "slug": "teil_4_anzeigen_zuordnung",
        "name": "Teil 4 — Anzeigen-Zuordnung",
        "summary": "Pool of 6 ads (a–f) + 5 situations. The candidate matches each situation to one ad, or 'X' for no match.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat A2 Lesen Teil 4.\n\n"
            "Source text: a pool of 6 short German ads (Anzeigen) on a single THEME, "
            "lettered a–f. Each ad is 3–5 sentences (50–90 German words), realistic and "
            "varied: cafés, restaurants, free-time offers, services, courses.\n\n"
            "Plus 5 situations. Each situation describes a specific person's need in 1–2 "
            "sentences. The candidate writes which ad letter matches, or 'X' if no ad fits.\n\n"
            "ANSWER SHAPE: free-text input, exactly one character — a lowercase letter a–f "
            "or the letter 'X' (no-match marker, A2-specific).\n\n"
            "Hard composition rules (the prompt enforces, the generator validates):\n"
            "  1. Pool has EXACTLY 6 ads (letters a, b, c, d, e, f).\n"
            "  2. EXACTLY 5 situations (orders 1–5).\n"
            "  3. EXACTLY ONE situation has correct_letter == 'X' (no-match case). The "
            "     reason for no-match must be derivable from the visible ad texts.\n"
            "  4. Each non-'X' correct_letter MUST be unique. So 4 of the 6 ads are "
            "     'winners' (matched once each) and 2 ads are 'distractor-only' ads.\n"
            "  5. Distractor ads MUST be on-theme and look plausible at first glance — "
            "     test-takers should have to read each ad fully to rule it out.\n\n"
            "Theme catalog — pick ONE theme for the 6 ads:\n"
            "- Cafés und Restaurants in einer Stadt\n"
            "- Freizeitangebote für das Wochenende\n"
            "- Sport- und Bewegungsangebote\n"
            "- Kurse an einer Volkshochschule\n"
            "- Gebrauchtes zu verkaufen oder zu verschenken\n"
            "- Babysitter / Nachhilfe / Hilfe im Haushalt\n"
            "- Kulturveranstaltungen — Konzerte, Kino, Theater\n"
            "- Tagesausflüge in der Region\n"
            "- Service-Angebote — Reparaturen, Reinigung\n"
            "- Veranstaltungen für Kinder und Familien\n\n"
            "Each situation specifies enough constraints (price, time, audience, location) "
            "that the test-taker has to actively check 2–3 of those constraints against "
            "each candidate ad."
        ),
    },
]


def get_chapter_by_slug(slug: str):
    return next((c for c in DEUTSCH_A2_LESEN_CHAPTERS if c["slug"] == slug), None)


def get_chapter_by_name(name: str):
    return next((c for c in DEUTSCH_A2_LESEN_CHAPTERS if c["name"] == name), None)


# ── Topic catalogs per Teil ───────────────────────────────────────────────────
# A2-adapted scenarios. The generator picks one per script at random so
# successive exams don't keep returning the same default scenarios.

TOPICS_TEIL_1 = [
    "Eine bekannte Köchin im Fernsehen mit einem neuen Programm",
    "Ein junger Sportler mit besonderer Geschichte",
    "Eine Lehrerin, die mit Musik unterrichtet",
    "Ein Vater, der mit seinem Kind eine Reise macht",
    "Ein Schüler, der einen Preis gewonnen hat",
    "Eine Schulklasse, die ein Theaterstück aufführt",
    "Ein neues Café in einem alten Bahnhof",
    "Eine Bäckerei, die nur Bio-Brot verkauft",
    "Ein Verein, der einen Park sauber hält",
    "Ein junger Mensch mit einem ungewöhnlichen Hobby",
    "Eine Bibliothek, die Bücher kostenlos verschickt",
    "Ein Kindergarten mit einem eigenen Garten",
    "Ein Großvater, der jeden Tag tanzt",
    "Eine Großmutter, die mit 70 noch Sport macht",
    "Ein Mädchen, das mit 15 schon ein Buch geschrieben hat",
    "Ein Junge, der jeden Tag Klavier spielt",
    "Eine Familie, die in einem alten Bus wohnt",
    "Ein Mann, der jeden Tag mit dem Fahrrad zur Arbeit fährt",
    "Ein Stadtfest mit vielen Konzerten",
    "Ein Marathon, bei dem Geld für ein Krankenhaus gesammelt wird",
    "Eine Tiergeschichte aus dem Zoo",
    "Ein Hund, der seinen Besitzer gerettet hat",
    "Ein Café, in dem Senioren und junge Leute zusammenkommen",
    "Ein Sportplatz, der jetzt jeden Abend offen ist",
    "Ein Theaterprojekt für Kinder aus verschiedenen Ländern",
    "Eine Schulleiterin, die seit 30 Jahren in derselben Schule arbeitet",
    "Ein Briefträger, der seit 40 Jahren im Dorf bekannt ist",
]

TOPICS_TEIL_2 = [
    "Kaufhaus mit fünf Stockwerken — Mode, Schmuck, Restaurant",
    "Großes Warenhaus mit Lebensmitteln, Mode und Spielzeug",
    "Modernes Bürgerzentrum mit Ämtern und Beratungsstellen",
    "Stadtteilzentrum mit Kursräumen und Café",
    "Sportkomplex mit Schwimmbad, Sauna und Fitnessräumen",
    "Sportzentrum mit Hallen für verschiedene Sportarten",
    "Stadtbibliothek über drei Stockwerke",
    "Universitätsbibliothek mit Lesebereichen",
    "Krankenhaus mit Stationen, Notaufnahme und Ambulanz",
    "Volkshochschule mit verschiedenen Kursräumen",
    "Hotel mit Frühstücksraum, Wellness und Tagungsräumen",
    "Universitätsgebäude mit Hörsälen, Mensa, Bibliothek",
    "Stadtmuseum mit verschiedenen Ausstellungen",
    "Großes Sportgeschäft mit Abteilungen für jede Sportart",
    "Möbelhaus mit Wohn-, Schlaf- und Küchenmöbeln",
    "Buchhandlung mit verschiedenen Bereichen über zwei Stockwerke",
    "Tierhandlung mit Bereichen für Hunde, Katzen, Vögel und Fische",
    "Gartencenter mit Pflanzen, Werkzeug und einem Café",
]

TOPICS_TEIL_3 = [
    "Geburtstagseinladung mit Plänen für die Feier",
    "Einladung zu einer Hochzeitsfeier",
    "Wochenendplanung mit Vorschlag für ein Treffen",
    "Bericht von einer Reise nach Italien",
    "Bericht vom ersten Tag im neuen Job",
    "Einladung zu einer Grillparty im Garten",
    "E-Mail an die Eltern aus dem Urlaub am Meer",
    "E-Mail an eine Freundin mit Plänen für den Sommer",
    "E-Mail an einen Kollegen mit Verschiebung eines Termins",
    "E-Mail an die Sprachschule mit Frage zum Kurs",
    "E-Mail an die Vermieterin mit Bitte um Reparatur",
    "E-Mail an einen Freund mit Bitte um Hilfe beim Umzug",
    "E-Mail an die Lehrerin mit Krankmeldung des Kindes",
    "E-Mail an die Schule mit Frage zum Schulausflug",
    "E-Mail an einen Bekannten mit Tipps für eine Stadt",
    "E-Mail an eine Freundin mit Bericht von einem Konzert",
    "E-Mail an die Mutter mit Plänen zu Weihnachten",
    "E-Mail an einen Freund mit Frage zu einem neuen Hobby",
    "E-Mail an einen Mitbewohner mit Plan für die Wohnung",
    "E-Mail an die Reisegruppe mit Treffpunkt und Zeit",
    "E-Mail an einen Verein mit Anmeldung",
    "E-Mail an einen Freund nach einem Streit",
    "E-Mail an die Großeltern mit Bericht aus der Schule",
    "E-Mail an die Tante mit Geburtstagsglückwünschen",
    "E-Mail an einen Freund mit Empfehlung für einen Film",
]

TOPICS_TEIL_4 = [
    "Cafés und Restaurants in einer Stadt",
    "Freizeitangebote für das Wochenende",
    "Sport- und Bewegungsangebote in einer Stadt",
    "Kurse an einer Volkshochschule",
    "Gebrauchtes zu verkaufen oder zu verschenken",
    "Babysitter und Hilfe im Haushalt",
    "Nachhilfe für Schüler",
    "Kulturveranstaltungen — Konzerte, Kino, Theater",
    "Tagesausflüge in der Region",
    "Service-Angebote — Reparaturen, Reinigung",
    "Veranstaltungen für Kinder und Familien",
    "Mitfahrgelegenheiten für verschiedene Strecken",
    "Sprachkurse — verschiedene Sprachen und Niveaus",
    "Tanzkurse — verschiedene Stile und Tageszeiten",
    "Musikunterricht für verschiedene Instrumente",
    "Mal- und Zeichenkurse für verschiedene Altersgruppen",
    "Sportkurse für Anfänger",
    "Yogakurse mit verschiedenen Schwerpunkten",
    "Kochkurse für verschiedene Küchen",
    "Wochenmarkt-Angebote in der Stadt",
    "Ferienwohnungen am Meer",
    "Ferienwohnungen in den Bergen",
    "Hotels in der Region",
    "Kostenlose Veranstaltungen am Wochenende",
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
    chapters = DEUTSCH_A2_LESEN_CHAPTERS
    if focus_chapter_slugs:
        focus_set = set(focus_chapter_slugs)
        filtered = [c for c in DEUTSCH_A2_LESEN_CHAPTERS if c["slug"] in focus_set]
        if filtered:
            chapters = filtered
    parts = []
    for ch in chapters:
        parts.append(f"--- Chapter: {ch['name']} ---\n{ch['content']}")
    return "\n\n".join(parts)
