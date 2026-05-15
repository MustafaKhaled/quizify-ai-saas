"""
Static chapter knowledge base for the German B1 Lesen (Reading) agent.

Mirrors the Hören chapters file. Each "chapter" maps to one of the five Teile
of the Goethe-Zertifikat B1 / telc B1 / ÖSD B1 reading section. The corpus
content for each Teil is the *format spec* — text type, length, item shape —
not example passages. Real B1 reading passages are copyright Goethe-Institut
and not redistributable; we generate fresh material that matches the format.

The five Teile differ by source-text type and answer shape:

  Teil 1: blog/forum post → 6 richtig/falsch items
  Teil 2: two press articles → 3 + 3 MCQ (a/b/c) items
  Teil 3: 10-ad pool + 7 situations → letter answer (a–j or "0")
  Teil 4: 7 reader comments → ja/nein per author
  Teil 5: institutional text (rules) → 4 MCQ items

The agent's instructions.md tells the model how to produce each shape.
"""

DEUTSCH_B1_LESEN_CHAPTERS = [
    {
        "slug": "teil_1_blogeintrag",
        "name": "Teil 1 — Blogeintrag",
        "summary": "One personal blog or forum post (~300–400 words). Six richtig/falsch comprehension items.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat B1 Lesen Teil 1.\n\n"
            "Source text: ONE personal blog post, forum post, or first-person email. "
            "Conversational tone, narrative structure, working-adult everyday topic.\n\n"
            "Length: 300–400 German words, one or two paragraphs.\n\n"
            "Voice/register: first person, informal but literate. Use natural connectors "
            "(zuerst, dann, danach, plötzlich, am Ende).\n\n"
            "Topic catalog — pick one situation:\n"
            "- Verlorene Geldbörse / verlorenes Handy und die Suche danach\n"
            "- Erster Marathon / erste Wanderung / sportliche Erfahrung\n"
            "- Umzug in eine neue Stadt / neue Wohnung\n"
            "- Reise mit einem Problem (verpasster Zug, falsches Hotel, defektes Gepäck)\n"
            "- Erster Tag im neuen Job / erstes Praktikum\n"
            "- Bewerbungsprozess (gutes oder schlechtes Vorstellungsgespräch)\n"
            "- Konflikt mit Nachbarn / Mitbewohnern\n"
            "- Ein neues Hobby ausprobiert (Kochkurs, Yoga, Tanzkurs)\n"
            "- Familienfeier / Hochzeit / Geburtstag mit unerwarteter Wendung\n"
            "- Auslandserfahrung (Sprachreise, Au-Pair, Studienaustausch)\n\n"
            "Comprehension items: 6 richtig/falsch statements (in addition to a worked example "
            "that we don't generate — only the 6 scored items). Each statement is a paraphrase "
            "of one specific claim made (or contradicted) in the post. Order follows the post: "
            "item 1 about an early section, item 6 about the closing section.\n\n"
            "Roughly half richtig, half falsch — never all one or all the other."
        ),
    },
    {
        "slug": "teil_2_zwei_zeitungsartikel",
        "name": "Teil 2 — Zwei Zeitungsartikel",
        "summary": "Two short press articles (~200 words each). Three MCQ comprehension items per article.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat B1 Lesen Teil 2.\n\n"
            "Source text: TWO short press articles on different topics. Factual, third-person, "
            "informative register. Each is independent — the test-taker reads the first article, "
            "answers 3 questions about it, then reads the second and answers 3 more.\n\n"
            "Length: 180–230 German words per article.\n\n"
            "Voice/register: news/feature article style. Use neutral connectors (jedoch, allerdings, "
            "deshalb, daher). Direct quotes are allowed and recommended for at least one question's evidence.\n\n"
            "Topic catalog — pick TWO different topics, one for each article:\n"
            "- Energiedorf / Solarenergie in einem Ort\n"
            "- Radtour / Wandertour mit besonderem Konzept\n"
            "- Neues Café / Restaurant mit ungewöhnlicher Idee\n"
            "- Stadtprojekt (Park-Sanierung, neue Brücke, Verkehrskonzept)\n"
            "- Erfolgreicher kleiner Betrieb (Bäckerei, Buchhandlung, Werkstatt)\n"
            "- Sport-Event (Marathon, Triathlon, Volkslauf in einer Stadt)\n"
            "- Festival / Markt (Mittelaltermarkt, Filmfestival, Streetfood-Festival)\n"
            "- Ehrenamtliches Projekt (Repair-Café, Lebensmittel-Retter-Verein, Lese-Mentoren)\n"
            "- Schulprojekt (Schulgarten, Schüler-Firma, Austauschprogramm)\n"
            "- Tier- oder Naturschutzprojekt (Bienen, Vögel, alte Obstsorten)\n"
            "- Neue Bibliothek / neues Museum / neues Kulturzentrum\n"
            "- Kursangebot für Senioren / für Jugendliche\n\n"
            "Comprehension items: 6 MCQs total (3 per article), each with 3 options (a/b/c). "
            "Items follow the order of the article they belong to. Exactly one option is correct. "
            "Distractors are facts that COULD be in the article but contradict its specifics."
        ),
    },
    {
        "slug": "teil_3_anzeigen_zuordnung",
        "name": "Teil 3 — Anzeigen-Zuordnung",
        "summary": "Pool of 10 ads (a–j) + 7 situations. The candidate matches each situation to one ad, or '0' for no match.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat B1 Lesen Teil 3.\n\n"
            "Source text: a pool of 10 German ads (Anzeigen) on a single THEME, lettered a–j. "
            "Each ad is 4–6 sentences (roughly 60–110 German words), realistic and detailed: course offers, "
            "venue listings, service ads, event announcements. The ad MUST include enough concrete details "
            "(price OR time OR location OR target audience OR prerequisites OR contact info — at least 3 of these) "
            "that the test-taker can match it against the constraints in a situation. Short two-line ads make "
            "Teil 3 too easy and don't match the real exam.\n\n"
            "Plus 7 situations. Each situation describes a specific person's need in 1–2 sentences "
            "('Sie suchen <X> für <Y>'). The candidate chooses which lettered ad matches that situation, "
            "or types '0' if no ad fits.\n\n"
            "ANSWER SHAPE: free-text input, exactly one character — a lowercase letter a–j or the digit '0'. "
            "This is a NEW question type the system needs to handle (`question_type: \"letter_matching\"`).\n\n"
            "Hard composition rules (the prompt enforces, the generator must check):\n"
            "  1. Pool has EXACTLY 10 ads (letters a, b, c, d, e, f, g, h, i, j).\n"
            "  2. EXACTLY 7 situations (orders 1–7).\n"
            "  3. EXACTLY ONE situation has correct_letter == \"0\" (the no-match case). The reason "
            "     for no-match must be derivable from the visible ad texts — never a hidden constraint.\n"
            "  4. Each non-\"0\" correct_letter MUST be unique. So 6 of the 10 ads are 'winners' \n"
            "     (matched once each) and 3 ads are 'distractor-only' (matched by no situation).\n"
            "  5. Distractor ads MUST be on-theme and look plausible at first glance — the test-taker "
            "     should have to read each ad fully to rule it out, not skim past obviously irrelevant ones.\n\n"
            "Theme catalog — pick ONE theme for the 10 ads:\n"
            "- Sprachkurse (language courses — Italienisch, Spanisch, Deutsch, ...)\n"
            "- Wohnungsangebote (apartment listings — different sizes, areas, prices, rules)\n"
            "- Ferienwohnungen / Hotels in einer Region\n"
            "- Veranstaltungen am Wochenende in einer Stadt\n"
            "- Fitness- und Sportangebote (Kurse, Vereine, Studios)\n"
            "- Gebrauchtes zu verkaufen / zu verschenken (Möbel, Haushalt, Elektrogeräte)\n"
            "- Mitfahrgelegenheiten und Reisepartner-Anzeigen\n"
            "- Babysitter / Nachhilfe / Haustierbetreuung — Privatangebote\n"
            "- Restaurants / Cafés mit Spezialitäten\n"
            "- Kurse an einer Volkshochschule (Kochen, Yoga, Fotografie, ...)\n"
            "- Freizeit-Aktivitäten für Kinder / für Familien\n"
            "- Kulturveranstaltungen (Konzerte, Theater, Lesungen, Ausstellungen)\n\n"
            "Each situation must specify enough constraints (price, time, audience, prerequisite, location) "
            "that the test-taker has to actively check at least 2–3 of those constraints against each candidate ad."
        ),
    },
    {
        "slug": "teil_4_leserkommentare",
        "name": "Teil 4 — Leserkommentare",
        "summary": "One prompt + 7 reader comments. The candidate decides ja/nein per author whether they support the prompt.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat B1 Lesen Teil 4.\n\n"
            "Source text: a short prompt question on a societal/lifestyle topic, followed by 7 reader "
            "comments responding to it. Each comment has a clear stance (for or against) the prompt's "
            "central question.\n\n"
            "Length: prompt 2–3 sentences. Each comment 60–110 German words.\n\n"
            "Voice/register: each comment has a distinct voice — different German first names, sometimes "
            "with city ('Hannah aus Köln'). Some comments are personal-experience-driven, others are "
            "argument-driven. Use natural opinion connectors (meiner Meinung nach, ich finde, allerdings, "
            "trotzdem, deshalb).\n\n"
            "Topic catalog — pick ONE prompt:\n"
            "- Sollte man Computerspiele für Kinder verbieten?\n"
            "- Sollte das Smartphone aus Schulen verbannt werden?\n"
            "- Sollte man im Homeoffice arbeiten dürfen, wenn die Arbeit es erlaubt?\n"
            "- Sollten Eltern den Schulweg ihrer Kinder begleiten?\n"
            "- Sollte man Plastiktüten in Supermärkten verbieten?\n"
            "- Sollte man Hunde in Restaurants erlauben?\n"
            "- Sollte man Hausaufgaben in der Grundschule abschaffen?\n"
            "- Sollte man Sportunterricht in der Schule mehr fördern?\n"
            "- Sollte man am Sonntag mehr Geschäfte öffnen dürfen?\n"
            "- Sollten Jugendliche schon mit 16 wählen dürfen?\n"
            "- Sollte man Werbung für ungesundes Essen einschränken?\n"
            "- Sollte man die Vier-Tage-Woche einführen?\n\n"
            "Hard composition rules:\n"
            "  1. EXACTLY 7 comments (comment_id t4_c1 through t4_c7).\n"
            "  2. EXACTLY 7 questions, one per comment, asking 'Findet <author>, dass <restated thesis>?'.\n"
            "  3. Each answer is 'ja' or 'nein' (lowercase). Roughly half/half — never all one.\n"
            "  4. Each comment must have a clear stance — no fence-sitters. If a comment hedges, "
            "     decide the stance based on the dominant signal and write the answer accordingly.\n"
            "  5. The 'stance' is whether the author supports the action proposed in the prompt — "
            "     not their general feelings on the topic. Be precise about what 'ja' / 'nein' answers."
        ),
    },
    {
        "slug": "teil_5_institutioneller_text",
        "name": "Teil 5 — Institutioneller Text",
        "summary": "One formal institutional document (~250–350 words). Four MCQ comprehension items.",
        "content": (
            "FORMAT SPEC — Goethe-Zertifikat B1 Lesen Teil 5.\n\n"
            "Source text: ONE formal institutional document — Hausordnung, Bibliotheksordnung, "
            "Mietvertrag-Auszug, Arbeitsvertrag-Auszug, Schwimmbad-Regeln, Museum-Regeln. Formal register, "
            "numbered or bulleted clauses where natural.\n\n"
            "Length: 250–350 German words.\n\n"
            "Voice/register: formal, impersonal Sie-form. Common phrases: 'Es ist nicht gestattet, ...', "
            "'Bitte beachten Sie, dass ...', 'Im Falle von ... wenden Sie sich bitte an ...'.\n\n"
            "Topic catalog — pick ONE document type:\n"
            "- Hausordnung einer Schule\n"
            "- Hausordnung eines Mehrfamilienhauses\n"
            "- Bibliotheks-Ordnung (Öffnungszeiten, Ausleihe, Verhalten)\n"
            "- Schwimmbad-Regeln\n"
            "- Fitnessstudio-Regeln\n"
            "- Museums-Hinweise für Besucher\n"
            "- Hostel- oder Jugendherbergs-Hausordnung\n"
            "- Mietvertrag-Auszug (Kündigung, Nebenkosten, Haustiere)\n"
            "- Arbeitsvertrag-Auszug (Pausen, Urlaub, Krankmeldung)\n"
            "- Vereinsstatuten (Beitragsregeln, Kündigung, Versammlungen)\n"
            "- Sprachschul-Hausordnung\n"
            "- Kindergarten-Regeln für Eltern\n\n"
            "Comprehension items: 4 MCQs with 3 options each (a/b/c). Items follow the order of the document. "
            "Each item targets a specific clause — what is allowed, what is forbidden, what to do in a "
            "specific situation, who to contact. Distractors are clauses that COULD plausibly be in such a "
            "document but that contradict the specifics in this one."
        ),
    },
]


def get_chapter_by_slug(slug: str):
    return next((c for c in DEUTSCH_B1_LESEN_CHAPTERS if c["slug"] == slug), None)


def get_chapter_by_name(name: str):
    return next((c for c in DEUTSCH_B1_LESEN_CHAPTERS if c["name"] == name), None)


# ── Topic catalogs per Teil ───────────────────────────────────────────────────
# Concrete scenarios per Teil. The generator picks one per script at random so
# successive exams don't keep returning the same default scenarios.

TOPICS_TEIL_1 = [
    "Verlorene Geldbörse im Bus und die Suche am nächsten Tag",
    "Verlorenes Handy auf einer Wanderung",
    "Erster Marathon nach monatelangem Training",
    "Erste lange Fahrradtour mit Pannen unterwegs",
    "Umzug in eine neue Stadt mit Schwierigkeiten am ersten Tag",
    "Eine neue Wohnung mit unerwarteten Mängeln",
    "Verpasster Zug am Hauptbahnhof und der Plan B",
    "Verpasstes Flugzeug wegen Stau zum Flughafen",
    "Falsches Hotel reserviert und die spontane Lösung",
    "Defektes Gepäck am Urlaubsort",
    "Erster Tag im neuen Job mit lustigen Missverständnissen",
    "Erstes Praktikum in einer großen Firma",
    "Vorstellungsgespräch, das ganz anders verlief als erwartet",
    "Konflikt mit lauten Nachbarn und das klärende Gespräch",
    "Streit mit Mitbewohnern über die Putzliste",
    "Ein neuer Kochkurs mit überraschenden Ergebnissen",
    "Yoga-Kurs für Anfänger mit körperlichen Erkenntnissen",
    "Tanzkurs zu zweit — peinliche Anfänge, gutes Ende",
    "Hochzeit mit einem unerwarteten Zwischenfall",
    "Geburtstagsfeier mit Überraschungsgästen",
    "Familienfeier mit einem Streit am Esstisch",
    "Sprachreise nach Spanien mit der ersten Woche zu Hause-Heimweh",
    "Au-Pair in Paris — die ersten Tage in der Gastfamilie",
    "Studienaustausch in Kanada mit der ersten Woche allein",
    "Erstes Wohnen ohne Eltern — erste Woche allein",
    "Eine schlecht gelaufene Bewerbung und das Lernen daraus",
    "Krankenhaus-Aufenthalt nach einem Sportunfall",
    "Verspäteter Flug und die Nacht am Flughafen",
    "Erste eigene Auto-Reparatur in der Werkstatt",
    "Erste Renovierung in der eigenen Wohnung",
]

TOPICS_TEIL_2 = [
    "Ein Energiedorf in Bayern, das vollständig auf erneuerbare Energien setzt",
    "Eine Solar-Genossenschaft, die alle Häuser im Ort mit Strom versorgt",
    "Ein neues Radwege-Netz in einer mittelgroßen Stadt",
    "Eine grenzüberschreitende Radtour zwischen Deutschland und der Schweiz",
    "Ein Café, das nur regionale Produkte anbietet",
    "Ein Restaurant ohne festes Menü — der Koch entscheidet täglich",
    "Ein Stadtteil-Park, der nach langer Sanierung wiedereröffnet wurde",
    "Ein neues Verkehrskonzept mit autofreier Innenstadt",
    "Eine kleine Bäckerei, die mit alten Getreidesorten Erfolg hat",
    "Eine Buchhandlung, die wöchentliche Lesungen organisiert",
    "Eine Stadt-Werkstatt, die Reparaturen für alle Bürger anbietet",
    "Ein Stadt-Marathon mit Rekord-Teilnehmerzahl im letzten Jahr",
    "Ein Volkslauf, der das Geld für ein soziales Projekt spendet",
    "Ein Mittelaltermarkt, der seit zwanzig Jahren stattfindet",
    "Ein Filmfestival in einer kleinen Stadt mit überraschend großem Publikum",
    "Ein Streetfood-Festival mit mehr als fünfzig Ständen",
    "Ein Repair-Café, das jede Woche ehrenamtlich Geräte repariert",
    "Ein Verein, der gerettete Lebensmittel an Bedürftige verteilt",
    "Ein Mentoren-Programm, das Schülern beim Lesen hilft",
    "Ein Schulgarten, der von den Schülern selbst geplant wurde",
    "Eine Schüler-Firma, die Bio-Müsli verkauft",
    "Ein Austausch-Programm zwischen einer deutschen und einer französischen Schule",
    "Ein Bienenprojekt auf dem Dach eines Stadtgebäudes",
    "Ein Vogelschutz-Projekt in der Stadt",
    "Ein Verein, der alte Apfelsorten erhält",
    "Eine neue Bibliothek mit langem offenen Lesebereich",
    "Ein neues Museum für Industriegeschichte in einer ehemaligen Fabrik",
    "Ein Kulturzentrum, das alte und junge Generationen zusammenbringt",
    "Ein Computerkurs für Senioren in der Volkshochschule",
    "Ein Theaterprojekt für Jugendliche aus verschiedenen Stadtteilen",
    "Ein Programm, das Pensionäre als Lesepaten in Schulen einsetzt",
    "Eine Tagespflege, die einen eigenen Garten betreibt",
]

TOPICS_TEIL_3 = [
    "Sprachkurse — verschiedene Sprachen, Niveaus, Termine, Preise",
    "Wohnungsangebote in einer Stadt mit verschiedenen Größen, Lagen und Bedingungen",
    "Ferienwohnungen an einem Reiseziel mit verschiedenen Eigenschaften",
    "Veranstaltungen am Wochenende in einer Stadt — Konzerte, Lesungen, Ausstellungen, Führungen",
    "Fitness- und Sportangebote — Kurse, Vereine, Studios, verschiedene Sportarten",
    "Gebrauchte Möbel und Haushaltsgeräte zu verkaufen oder zu verschenken",
    "Mitfahrgelegenheiten und Reisepartner-Anzeigen für verschiedene Strecken",
    "Babysitter, Nachhilfe und Haustierbetreuung — Privatangebote",
    "Restaurants und Cafés mit Spezialitäten in einer Stadt",
    "VHS-Kurse — Kochen, Yoga, Fotografie, Computer, Sprachen",
    "Freizeit-Aktivitäten für Kinder und Familien am Wochenende",
    "Kulturveranstaltungen — Konzerte, Theater, Lesungen, Ausstellungen",
    "Tagesausflüge in der Region mit verschiedenen Schwerpunkten",
    "Sportkurse für Anfänger in einer Stadt",
    "Tanzkurse — verschiedene Stile, Niveaus, Tageszeiten",
    "Sommerlager und Ferienprogramme für Kinder",
    "Tauschangebote — Bücher, Werkzeuge, Kleidung",
    "Reparaturservices in der Stadt für verschiedene Geräte",
    "Reinigungsservices und Hilfe im Haushalt",
    "Garten- und Pflanzenpflege-Angebote",
    "Kostenlose Veranstaltungen in der Stadt am Wochenende",
    "Vortrags- und Diskussionsabende in der Region",
    "Sport- und Bewegungskurse für Senioren",
    "Musikunterricht für verschiedene Instrumente und Niveaus",
    "Mal- und Zeichenkurse für verschiedene Altersgruppen",
    "Yoga- und Meditationskurse mit verschiedenen Schwerpunkten",
]

TOPICS_TEIL_4 = [
    "Sollte man Computerspiele für Kinder verbieten?",
    "Sollte das Smartphone aus Schulen verbannt werden?",
    "Sollte man im Homeoffice arbeiten dürfen, wenn die Arbeit es erlaubt?",
    "Sollten Eltern den Schulweg ihrer Kinder begleiten?",
    "Sollte man Plastiktüten in Supermärkten verbieten?",
    "Sollte man Hunde in Restaurants erlauben?",
    "Sollte man Hausaufgaben in der Grundschule abschaffen?",
    "Sollte man Sportunterricht in der Schule mehr fördern?",
    "Sollte man am Sonntag mehr Geschäfte öffnen dürfen?",
    "Sollten Jugendliche schon mit 16 wählen dürfen?",
    "Sollte man Werbung für ungesundes Essen einschränken?",
    "Sollte man die Vier-Tage-Woche einführen?",
    "Sollte man E-Scooter in Innenstädten verbieten?",
    "Sollte man im Park grillen dürfen?",
    "Sollte man Schul-Uniformen in Deutschland einführen?",
    "Sollte man im Sommer kürzer arbeiten?",
    "Sollte man weniger Fleisch essen, um das Klima zu schützen?",
    "Sollte man Tickets für öffentliche Verkehrsmittel kostenlos machen?",
    "Sollte man Werbung in der U-Bahn verbieten?",
    "Sollte man Schulkonzerte für alle Eltern verpflichtend machen?",
    "Sollte man kleine Kinder schon eine Sprache in der Kita lernen lassen?",
    "Sollte man in jeder Wohnung einen Erste-Hilfe-Kasten haben?",
    "Sollte man Lebensmittel kurz vor dem Mindesthaltbarkeitsdatum verschenken müssen?",
    "Sollte man auf Autobahnen ein Tempolimit einführen?",
]

TOPICS_TEIL_5 = [
    "Hausordnung einer Grundschule mit Regeln zu Pausen, Garderobe, Pünktlichkeit",
    "Hausordnung einer weiterführenden Schule mit Handynutzung und Aufenthalt",
    "Hausordnung eines Mehrfamilienhauses mit Ruhezeiten und Müll",
    "Hausordnung eines Studentenwohnheims mit Gemeinschaftsräumen",
    "Bibliotheks-Ordnung mit Öffnungszeiten, Ausleihe und Verhalten",
    "Schwimmbad-Regeln mit Sicherheits- und Hygiene-Hinweisen",
    "Fitnessstudio-Regeln mit Vertragsbedingungen und Verhaltenscodex",
    "Hinweise für Museumsbesucher mit Foto- und Verhaltenshinweisen",
    "Jugendherbergs-Hausordnung mit Ankunfts- und Abreisezeiten",
    "Mietvertrag-Auszug zu Kündigung und Nebenkosten",
    "Mietvertrag-Auszug zu Haustieren und Untervermietung",
    "Arbeitsvertrag-Auszug zu Pausen, Urlaub und Krankmeldung",
    "Arbeitsvertrag-Auszug zu Probezeit und Überstunden",
    "Vereinsstatuten zu Beitragsregeln und Kündigung",
    "Vereinsstatuten zu Mitgliederversammlungen und Wahlen",
    "Sprachschul-Hausordnung mit Kursteilnahme und Pausen",
    "Kindergarten-Regeln für Eltern zu Bringzeiten und Krankmeldung",
    "Hortordnung mit Hausaufgabenbetreuung und Abholung",
    "Sport-Vereins-Ordnung mit Trainingszeiten und Wettkampf-Regeln",
    "Volkshochschul-Hausordnung mit Anmeldung und Rücktritt",
    "Theater-Hausordnung mit Einlass, Garderobe und Pause",
    "Kinosaal-Regeln mit Verhalten und Mitnahme von Speisen",
]


TOPICS_BY_TEIL: dict[int, list[str]] = {
    1: TOPICS_TEIL_1,
    2: TOPICS_TEIL_2,
    3: TOPICS_TEIL_3,
    4: TOPICS_TEIL_4,
    5: TOPICS_TEIL_5,
}


def topics_for_teil(teil: int) -> list[str]:
    """Return the full topic catalog for a given Teil."""
    return TOPICS_BY_TEIL.get(teil, [])


def build_corpus_text(focus_chapter_slugs: list[str] | None = None) -> str:
    """Concatenate chapter format specs, optionally filtered to a subset."""
    chapters = DEUTSCH_B1_LESEN_CHAPTERS
    if focus_chapter_slugs:
        focus_set = set(focus_chapter_slugs)
        filtered = [c for c in DEUTSCH_B1_LESEN_CHAPTERS if c["slug"] in focus_set]
        if filtered:
            chapters = filtered
    parts = []
    for ch in chapters:
        parts.append(f"--- Chapter: {ch['name']} ---\n{ch['content']}")
    return "\n\n".join(parts)
