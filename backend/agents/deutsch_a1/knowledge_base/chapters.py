"""
Static chapter knowledge base for the German Grammar A1 (CEFR) agent.

Each chapter slug names ONE atomic Grammatik-Regel (grammar rule) drawn from the
standard A1 syllabus (Goethe-Zertifikat A1 / telc Deutsch A1 / Schritte plus
Neu A1). Slugs are German-anchored so they read as the rule itself.

Each chapter's `name` doubles as the quiz `topic` field. There is intentionally
no seed exam bank for this subject — questions are generated on-demand from
this corpus + the agent's instructions.md style guide.
"""

DEUTSCH_A1_CHAPTERS = [
    {
        "slug": "personalpronomen",
        "name": "Personalpronomen",
        "summary": "Personal pronouns and their use as sentence subjects.",
        "content": (
            "German has nine personal pronouns in the nominative case: "
            "ich (I), du (you, informal singular), er (he/it-masc), sie (she/it-fem), es (it-neut), "
            "wir (we), ihr (you, informal plural), sie (they), Sie (you, formal — always capitalized). "
            "'du' is used with family, friends, children, and peers; 'Sie' is used with strangers, "
            "in business, with older people, and in formal writing. 'ihr' addresses two or more people "
            "you'd individually call 'du'. "
            "'er', 'sie', 'es' replace nouns according to their grammatical gender, NOT their natural sex: "
            "der Tisch → er, die Lampe → sie, das Mädchen → es (because Mädchen is grammatically neuter, "
            "even though the person is female). "
            "Common A1 mistakes: using 'es' for a female person ('Wo ist Anna? Es ist hier' is wrong — should be 'Sie ist hier'), "
            "confusing 'sie' (she) with 'sie' (they) and 'Sie' (you formal) — context and verb form disambiguate. "
            "Examples: Ich heiße Tom. Du kommst aus Spanien. Er wohnt in Berlin. Sie ist Lehrerin. "
            "Es ist kalt. Wir lernen Deutsch. Ihr seid Studenten. Sie sprechen Englisch. Sie heißen Müller, oder?"
        ),
    },
    {
        "slug": "verbkonjugation_praesens",
        "name": "Verbkonjugation Präsens",
        "summary": "Present-tense conjugation of regular verbs.",
        "content": (
            "Regular German verbs in the present tense (Präsens) take a stem plus a personal ending. "
            "Find the stem by removing the infinitive ending '-en' (lernen → lern-, kommen → komm-, machen → mach-). "
            "Then add: ich -e, du -st, er/sie/es -t, wir -en, ihr -t, sie/Sie -en. "
            "Example with 'lernen': ich lerne, du lernst, er lernt, wir lernen, ihr lernt, sie lernen. "
            "Example with 'kommen': ich komme, du kommst, er kommt, wir kommen, ihr kommt, sie kommen. "
            "Spelling adjustments: stems ending in -t, -d, -n (after consonant), or -m (after consonant) insert an 'e' "
            "before -st and -t for pronunciation: arbeiten → du arbeitest, er arbeitet, ihr arbeitet (NOT 'arbeitst'). "
            "Stems ending in -s, -ss, -ß, -z, -tz drop the 's' from the du-ending: heißen → du heißt (not 'heißst'); "
            "tanzen → du tanzt. "
            "Some verbs have a vowel change in du and er/sie/es forms (Vokalwechsel) — "
            "a → ä: fahren → du fährst, er fährt; schlafen → du schläfst, er schläft. "
            "e → i: sprechen → du sprichst, er spricht; essen → du isst, er isst; geben → du gibst, er gibt. "
            "e → ie: lesen → du liest, er liest; sehen → du siehst, er sieht. "
            "These vowel changes apply ONLY in 2nd and 3rd person singular — wir, ihr, sie/Sie keep the original vowel."
        ),
    },
    {
        "slug": "sein_haben",
        "name": "sein & haben",
        "summary": "Conjugation and use of the irregular auxiliaries sein and haben.",
        "content": (
            "'sein' (to be) and 'haben' (to have) are the two most important verbs in German. They are highly "
            "irregular — memorize them. "
            "sein: ich bin, du bist, er/sie/es ist, wir sind, ihr seid, sie/Sie sind. "
            "haben: ich habe, du hast, er/sie/es hat, wir haben, ihr habt, sie/Sie haben. "
            "Use 'sein' for: identity (Ich bin Lehrer), origin (Sie ist aus Italien), location (Wir sind in Berlin), "
            "states (Es ist kalt; Du bist müde), age (Er ist 25 Jahre alt). "
            "Use 'haben' for: possession (Ich habe ein Auto), age in the alternative pattern (NOT used in German — German uses 'sein' for age, unlike French/Spanish), "
            "stating what someone has/owns (Wir haben einen Hund), expressing hunger/thirst (Ich habe Hunger; Sie hat Durst — note: NO article). "
            "Both are also Hilfsverben (auxiliary verbs) used to form the Perfekt past tense — see the Perfekt chapter. "
            "Common A1 mistakes: 'Ich bin 25 Jahre alt' (correct) vs 'Ich habe 25 Jahre' (wrong, English/Spanish interference); "
            "'Ich habe Hunger' (correct) vs 'Ich bin hungrig' (also possible but less common at A1)."
        ),
    },
    {
        "slug": "artikel",
        "name": "Artikel (bestimmt & unbestimmt)",
        "summary": "Definite (der/die/das) and indefinite (ein/eine) articles in the nominative case.",
        "content": (
            "Every German noun has a grammatical gender: masculine (m), feminine (f), or neuter (n). "
            "The article reveals the gender. Always learn nouns WITH their article. "
            "Bestimmter Artikel (definite article — 'the'): masculine der, feminine die, neuter das, plural die. "
            "Examples: der Mann, der Tisch, der Hund; die Frau, die Lampe, die Katze; das Kind, das Buch, das Auto; "
            "die Männer, die Frauen, die Kinder. "
            "Unbestimmter Artikel (indefinite article — 'a/an'): masculine ein, feminine eine, neuter ein. "
            "There is NO plural indefinite article — just use the bare plural noun: ein Mann → Männer; eine Frau → Frauen. "
            "Examples: ein Mann, eine Frau, ein Kind, ein Auto. "
            "When to use which: definite article for something specific or already mentioned ('Der Hund ist groß' — a particular dog); "
            "indefinite article for something new or unspecific ('Ich habe einen Hund' — some dog, first mention); "
            "no article for professions and nationalities after sein/werden ('Ich bin Lehrer' NOT 'Ich bin ein Lehrer'). "
            "Common A1 mistakes: using 'das' for everything (English speakers default to 'the'); guessing gender from natural sex "
            "(das Mädchen is neuter despite meaning 'girl'; die Person is feminine for any gender of person)."
        ),
    },
    {
        "slug": "nomen_genus_plural",
        "name": "Nomen — Genus & Plural",
        "summary": "Noun gender hints and the five common plural patterns.",
        "content": (
            "Every German noun is capitalized — always. There is no shortcut to noun gender, but rough patterns help: "
            "MASCULINE (der): days, months, seasons (der Montag, der Januar, der Sommer); weather (der Regen, der Schnee, der Wind); "
            "alcoholic drinks except beer (der Wein); car brands (der BMW); -er agent nouns (der Lehrer, der Arbeiter). "
            "FEMININE (die): most nouns ending in -e (die Lampe, die Tasche), -ung (die Wohnung, die Zeitung), "
            "-heit (die Freiheit), -keit (die Möglichkeit), -ion (die Information), -schaft (die Freundschaft). "
            "Most names of trees and flowers (die Eiche, die Rose). "
            "NEUTER (das): diminutives -chen and -lein (das Mädchen, das Brötchen, das Häuschen); most countries (das Deutschland, das Italien); "
            "metals (das Gold, das Silber); infinitives used as nouns (das Lernen, das Essen). "
            "PLURAL formation has five common patterns. The plural article is always 'die'. "
            "1) -e: der Tag → die Tage; der Tisch → die Tische. Often with umlaut for masculine: der Stuhl → die Stühle. "
            "2) -er: das Kind → die Kinder; das Buch → die Bücher (with umlaut). "
            "3) -(e)n: die Frau → die Frauen; die Lampe → die Lampen; die Zeitung → die Zeitungen — most feminine nouns. "
            "4) -s: foreign borrowings — das Auto → die Autos; das Hotel → die Hotels; das Baby → die Babys. "
            "5) ∅ (no ending, sometimes umlaut): der Lehrer → die Lehrer; der Vater → die Väter. "
            "Always learn the plural with the noun: der Tisch, -e; das Kind, -er; die Frau, -en."
        ),
    },
    {
        "slug": "nominativ",
        "name": "Nominativ",
        "summary": "The nominative case — used for the sentence subject and after sein/werden/heißen.",
        "content": (
            "The Nominativ (nominative case) is the dictionary form of articles and nouns. It marks: "
            "1) The SUBJECT of a sentence — the person or thing performing the verb. Ask 'Wer?' (who) or 'Was?' (what) before the verb. "
            "Example: 'Der Mann liest ein Buch.' Wer liest? → Der Mann (subject, nominative). "
            "2) The PREDICATE NOUN after the linking verbs sein, werden, heißen, bleiben. "
            "Example: 'Das ist ein Lehrer.' Both 'Das' (subject) and 'ein Lehrer' (predicate) are nominative. "
            "Example: 'Er wird Arzt.' Both 'Er' and 'Arzt' are nominative. "
            "Article forms in the nominative: "
            "Definite — masculine der, feminine die, neuter das, plural die. "
            "Indefinite — masculine ein, feminine eine, neuter ein, plural (none — bare noun). "
            "Negative (kein) — masculine kein, feminine keine, neuter kein, plural keine. "
            "Possessive (mein, dein, sein, ihr, unser, euer, ihr/Ihr) — same endings as ein/eine/ein. "
            "The nominative is the form learners see first; the trick is recognizing when a noun is the subject "
            "(versus a direct object, which takes accusative). Word order does NOT determine the subject in German — "
            "the case marking does. 'Den Mann sieht der Hund' = 'The dog sees the man' (Der Hund is subject because nominative)."
        ),
    },
    {
        "slug": "akkusativ",
        "name": "Akkusativ",
        "summary": "The accusative case — direct object of most transitive verbs.",
        "content": (
            "The Akkusativ (accusative case) marks the DIRECT OBJECT — the person or thing the action affects. "
            "Ask 'Wen?' (whom) or 'Was?' (what) after the verb. "
            "Example: 'Ich sehe den Hund.' Wen sehe ich? → den Hund (direct object, accusative). "
            "ONLY masculine articles change in the accusative; feminine, neuter, and plural articles look identical to nominative. "
            "Definite: der → den, die → die, das → das, die → die. "
            "Indefinite: ein → einen, eine → eine, ein → ein, (no plural) → (no plural). "
            "Negative: kein → keinen, keine → keine, kein → kein, keine → keine. "
            "Possessive: mein → meinen (for masculine objects), meine, mein, meine — endings mirror ein. "
            "Examples: Ich kaufe einen Apfel (m). Ich kaufe eine Banane (f). Ich kaufe ein Brot (n). Ich kaufe Äpfel (pl). "
            "Ich sehe den Lehrer. Ich sehe die Lehrerin. Ich sehe das Kind. Ich sehe die Kinder. "
            "Verbs that always take accusative (the most common at A1): haben, sehen, kaufen, essen, trinken, lesen, schreiben, "
            "machen, brauchen, suchen, finden, mögen, lieben, hören, fragen, kennen, besuchen, treffen. "
            "Some prepositions ALWAYS trigger accusative: durch, für, gegen, ohne, um (mnemonic 'DOGFU' or 'FUDGO'). "
            "Example: 'Das Geschenk ist für den Vater.' "
            "Common A1 mistake: forgetting that only masculine changes — learners often write 'die → den' or 'das → den' incorrectly."
        ),
    },
    {
        "slug": "negation_nicht_kein",
        "name": "Negation: nicht & kein",
        "summary": "When to negate with 'nicht' versus 'kein'.",
        "content": (
            "German has two negation words: 'nicht' (not) and 'kein' (no/not a/not any). Choosing between them is rule-based. "
            "Use 'kein' to negate a noun that has an indefinite article OR no article. "
            "ein Auto → kein Auto. eine Frau → keine Frau. Brot (no article) → kein Brot. Äpfel (plural, no article) → keine Äpfel. "
            "Examples: Ich habe ein Auto. → Ich habe kein Auto. Sie trinkt Kaffee. → Sie trinkt keinen Kaffee. "
            "Wir haben Zeit. → Wir haben keine Zeit. "
            "'kein' takes the same endings as 'ein' and follows the case of the noun it negates. "
            "Nominativ: kein (m), keine (f), kein (n), keine (pl). "
            "Akkusativ: keinen (m), keine (f), kein (n), keine (pl). "
            "Use 'nicht' for everything else: "
            "1) To negate a verb: Ich komme nicht. Sie arbeitet nicht. "
            "2) To negate a noun with a DEFINITE article: Das ist nicht der Lehrer. Ich kaufe das Buch nicht. "
            "3) To negate a noun with a possessive: Das ist nicht mein Auto. "
            "4) To negate adjectives, adverbs, names, places: Er ist nicht groß. Sie kommt nicht heute. Ich heiße nicht Anna. Wir wohnen nicht in Berlin. "
            "Position of 'nicht': usually at the END when negating the whole sentence (Ich verstehe das nicht); "
            "directly BEFORE the element being negated for partial negation (Ich komme nicht heute, sondern morgen). "
            "Common A1 mistake: 'Ich habe nicht ein Auto' (wrong) — must be 'Ich habe kein Auto'. "
            "Another: 'Das ist kein der Lehrer' (wrong) — definite article requires 'nicht': 'Das ist nicht der Lehrer'."
        ),
    },
    {
        "slug": "possessivartikel",
        "name": "Possessivartikel",
        "summary": "Possessive articles (mein, dein, sein, ihr, unser, euer, ihr/Ihr) and their endings.",
        "content": (
            "Possessivartikel show ownership. Each personal pronoun has a corresponding possessive: "
            "ich → mein (my), du → dein (your, informal sg.), er → sein (his), sie → ihr (her), es → sein (its), "
            "wir → unser (our), ihr → euer (your, informal pl.), sie → ihr (their), Sie → Ihr (your, formal — capitalized). "
            "Possessivartikel take the SAME endings as 'ein/kein' depending on the gender, number, and case of the noun they precede. "
            "Stem only (nominative masculine and neuter): mein Bruder (m), mein Auto (n). "
            "Stem + -e (nominative feminine and all plurals): meine Schwester (f), meine Eltern (pl). "
            "Stem + -en (accusative masculine only): Ich sehe meinen Bruder. "
            "Same -e in accusative for feminine, neuter, plural: meine Schwester, mein Auto, meine Eltern (no change from nominative). "
            "Full nominative paradigm (using 'mein' as example): "
            "m: mein Vater. f: meine Mutter. n: mein Kind. pl: meine Eltern. "
            "Full accusative paradigm: "
            "m: meinen Vater. f: meine Mutter. n: mein Kind. pl: meine Eltern. "
            "'euer' drops the second 'e' when an ending is added: euer Auto (n) but eure Schwester (f), euren Bruder (acc m). "
            "Pay attention to er/sie distinction: 'sein Buch' = his book; 'ihr Buch' = her book or their book (context decides). "
            "Common A1 mistake: confusing 'ihr' (her/their/your-pl) with 'Ihr' (your-formal) — capitalization matters in writing."
        ),
    },
    {
        "slug": "modalverben",
        "name": "Modalverben",
        "summary": "The six modal verbs and the verb-second / infinitive-final word order they trigger.",
        "content": (
            "German has six Modalverben: können (can/be able to), müssen (must/have to), dürfen (be allowed to), "
            "sollen (should/be supposed to), wollen (want to), möchten (would like to — polite form, technically Konjunktiv of mögen). "
            "All six are irregular in the singular — they share a vowel change pattern. "
            "können: ich kann, du kannst, er kann, wir können, ihr könnt, sie können. "
            "müssen: ich muss, du musst, er muss, wir müssen, ihr müsst, sie müssen. "
            "dürfen: ich darf, du darfst, er darf, wir dürfen, ihr dürft, sie dürfen. "
            "sollen: ich soll, du sollst, er soll, wir sollen, ihr sollt, sie sollen. "
            "wollen: ich will, du willst, er will, wir wollen, ihr wollt, sie wollen. "
            "möchten: ich möchte, du möchtest, er möchte, wir möchten, ihr möchtet, sie möchten. "
            "Note: ich-form and er/sie/es-form are IDENTICAL (no -t added) — this is the modal signature. "
            "Word order: the modal verb takes position 2 (the normal verb slot); the main verb goes to the END as an infinitive. "
            "Pattern: [Subject] [Modal-V2] [...] [Infinitive-end]. "
            "Examples: Ich kann Deutsch sprechen. Du musst jetzt schlafen. Wir wollen morgen kommen. "
            "Sie möchte einen Kaffee trinken. Er darf hier nicht rauchen. "
            "Meaning notes: 'müssen' = must/have to (necessity); 'sollen' = should (someone else says so); "
            "'dürfen' = may/be allowed (permission); negated 'dürfen' = must not (prohibition); "
            "negated 'müssen' = don't have to (no necessity, NOT prohibition). "
            "'möchten' is the polite go-to in restaurants and shops: 'Ich möchte einen Kaffee, bitte.'"
        ),
    },
    {
        "slug": "trennbare_verben",
        "name": "Trennbare Verben",
        "summary": "Separable-prefix verbs and how the prefix moves to the end of the clause.",
        "content": (
            "Trennbare Verben (separable verbs) consist of a separable prefix + a base verb. In the infinitive form they are "
            "written as one word, with stress on the prefix: AUFstehen (to get up), EINkaufen (to shop), MITkommen (to come along), "
            "ANrufen (to call/phone), ABfahren (to depart), ZUmachen (to close), AUFmachen (to open), AUSgehen (to go out), "
            "FERNsehen (to watch TV), VORstellen (to introduce). "
            "Common separable prefixes: ab-, an-, auf-, aus-, ein-, mit-, nach-, vor-, weg-, zu-, zurück-, zusammen-, fern-, fest-, los-, weiter-. "
            "RULE: in the present tense (and imperative), the prefix DETACHES and moves to the END of the main clause. "
            "The base verb conjugates normally in position 2. "
            "Examples: aufstehen → Ich stehe um 7 Uhr auf. (NOT 'Ich aufstehe...') "
            "einkaufen → Wir kaufen heute ein. "
            "mitkommen → Kommst du mit? "
            "anrufen → Sie ruft ihre Mutter an. "
            "fernsehen → Er sieht jeden Abend fern. "
            "With a modal verb, the separable verb stays TOGETHER as an infinitive at the end (the prefix does not detach): "
            "'Ich möchte um 7 Uhr aufstehen.' 'Du musst die Tür zumachen.' "
            "Inseparable prefixes (be-, ge-, er-, ver-, zer-, ent-, emp-, miss-) never detach: bekommen, verstehen, gefallen → "
            "'Ich verstehe das' (NOT 'Ich stehe das ver'). The unstressed prefix is the giveaway. "
            "Common A1 mistake: failing to detach (Ich aufstehe um 7) or moving the wrong piece (Ich auf um 7 Uhr stehe)."
        ),
    },
    {
        "slug": "imperativ",
        "name": "Imperativ",
        "summary": "Command forms for du, ihr, and Sie.",
        "content": (
            "The Imperativ gives commands, instructions, and polite requests. German has three forms — one for each "
            "informal/formal address: du, ihr, Sie. "
            "Du-Form: take the du-conjugation, drop the '-st' ending. NO subject pronoun. "
            "kommen → du kommst → Komm! "
            "lernen → du lernst → Lern! (Lerne! is also acceptable, especially with stem ending in -t/-d) "
            "arbeiten → du arbeitest → Arbeite! "
            "Verbs with vowel change e→i/ie KEEP the change in the imperative: sprechen → Sprich! lesen → Lies! geben → Gib! "
            "Verbs with a→ä DROP the umlaut in the imperative: fahren → Fahr! schlafen → Schlaf! "
            "sein is irregular: Sei! (e.g., Sei ruhig! — Be quiet!) "
            "Ihr-Form: identical to the present-tense ihr-form, no subject pronoun. "
            "kommen → Kommt! lernen → Lernt! sprechen → Sprecht! sein → Seid! "
            "Sie-Form: invert the Sie-form of the present tense — verb FIRST, then 'Sie'. "
            "kommen → Kommen Sie! lernen → Lernen Sie! sprechen → Sprechen Sie! sein → Seien Sie! "
            "Trennbare Verben split in the imperative just like in the present: aufstehen → Steh auf! mitkommen → Komm mit! "
            "Add 'bitte' for politeness (anywhere — beginning, middle, or end): Komm bitte! / Bitte komm! / Komm, bitte! "
            "Use cases: instructions (Öffnen Sie das Buch!), requests (Bitte sprich langsamer!), warnings (Pass auf!), "
            "encouragement (Komm mit!). "
            "Common A1 mistake: keeping the -st ending in du-form (Kommst! — wrong) or including the pronoun (Du komm! — wrong, except in Sie-form which requires 'Sie')."
        ),
    },
    {
        "slug": "w_fragen",
        "name": "W-Fragen",
        "summary": "Question words (wer, was, wo, wann, wie, warum…) and their word order.",
        "content": (
            "W-Fragen (W-questions / open questions) start with a question word that begins with 'W'. "
            "The question word is in position 1; the conjugated verb is in position 2; the subject follows the verb. "
            "Common W-words and their use: "
            "wer = who (asks about a person, nominative): Wer ist das? — Das ist Anna. "
            "wen = whom (person, accusative): Wen siehst du? — Ich sehe den Lehrer. "
            "was = what (thing): Was machst du? — Ich lerne Deutsch. "
            "wo = where (location, no movement): Wo wohnst du? — Ich wohne in Berlin. "
            "woher = where from (origin): Woher kommst du? — Ich komme aus Spanien. "
            "wohin = where to (movement/destination): Wohin gehst du? — Ich gehe nach Hause. "
            "wann = when: Wann kommst du? — Ich komme um 8 Uhr. "
            "wie = how: Wie heißt du? Wie geht es dir? "
            "wie viel / wie viele = how much / how many: Wie viele Kinder hast du? "
            "warum / wieso / weshalb = why: Warum lernst du Deutsch? "
            "welcher / welche / welches = which (declines like der/die/das): Welches Buch liest du? "
            "was für (ein) = what kind of: Was für ein Auto hast du? "
            "Word order: [W-Wort] [V-konjugiert] [Subjekt] [Rest]. "
            "Compare with English: 'Where do you live?' uses an auxiliary 'do' — German uses NO auxiliary, the main verb moves: 'Wo wohnst du?' "
            "Common A1 mistake: keeping English-style auxiliary ('Wo do du wohnen?' — wrong) or wrong case after 'wer' vs 'wen'."
        ),
    },
    {
        "slug": "wortstellung_hauptsatz",
        "name": "Wortstellung im Hauptsatz",
        "summary": "Verb-second (V2) word order in German main clauses.",
        "content": (
            "In a German main clause (Hauptsatz), the conjugated verb is ALWAYS in position 2. This is the V2 rule and it is "
            "the single most important syntax rule in A1. Position 1 can be filled by the subject, an adverb, a time expression, "
            "an object, or a prepositional phrase — but the verb stays in position 2. "
            "Standard order — subject in position 1: "
            "'Ich gehe heute ins Kino.' (Position 1 = Ich, Position 2 = gehe, then everything else.) "
            "Inverted order — adverb or object in position 1, subject moves AFTER the verb: "
            "'Heute gehe ich ins Kino.' (Position 1 = Heute, Position 2 = gehe, then ich.) "
            "'Ins Kino gehe ich heute.' (Position 1 = Ins Kino.) "
            "What you CANNOT do: 'Heute ich gehe ins Kino' (wrong — verb must be in position 2). "
            "Yes/no questions invert: verb first, then subject. 'Gehst du ins Kino?' "
            "W-questions: W-word in position 1, verb in position 2. 'Wann gehst du ins Kino?' "
            "Within position 1, you can put one whole element (a noun phrase, a prepositional phrase, a time expression) — "
            "but only ONE element occupies position 1. 'Heute Abend gehe ich ins Kino' — 'Heute Abend' counts as one time expression. "
            "Sentence-end position is reserved for: separable prefixes (Ich rufe dich später AN), past participles in Perfekt "
            "(Ich habe Deutsch GELERNT), and infinitives after modal verbs (Ich kann Deutsch SPRECHEN). This creates the "
            "Satzklammer (sentence bracket) — the conjugated verb in position 2 and another verbal element at the end. "
            "Common A1 mistake: V3 errors after a fronted adverb ('Heute ich komme') and SVO order in questions ('Du kommst?' is technically OK in spoken language but the textbook form is 'Kommst du?')."
        ),
    },
    {
        "slug": "perfekt",
        "name": "Perfekt",
        "summary": "Past tense formed with haben/sein + past participle (Partizip II).",
        "content": (
            "Perfekt is the standard SPOKEN past tense in German (the written/literary past, Präteritum, is used mainly for "
            "sein, haben, modals, and in formal writing). Perfekt is formed with TWO parts: "
            "1) An auxiliary verb (Hilfsverb) — either 'haben' or 'sein' — conjugated in the present tense in position 2. "
            "2) The Partizip II (past participle) of the main verb at the END of the clause. This forms the Satzklammer. "
            "Pattern: [Subject] [haben/sein-V2] [...] [Partizip II-end]. "
            "Example: 'Ich habe gestern Deutsch gelernt.' 'Wir sind nach Berlin gefahren.' "
            "Choosing haben vs sein: "
            "Use 'sein' with verbs of MOTION/CHANGE OF LOCATION (gehen, kommen, fahren, fliegen, laufen, reisen, steigen) "
            "and verbs of CHANGE OF STATE (werden, sterben, einschlafen, aufwachen, wachsen) and the verbs sein and bleiben. "
            "Use 'haben' for everything else — including most transitive verbs (verbs that take a direct object). "
            "Examples with sein: Ich bin gegangen. Du bist gekommen. Er ist gefahren. Wir sind geflogen. Sie ist geblieben. "
            "Examples with haben: Ich habe gegessen. Du hast getrunken. Er hat gelesen. Wir haben gearbeitet. Sie hat gekauft. "
            "Forming the Partizip II: "
            "Regular (weak) verbs: ge- + stem + -t. lernen → gelernt; machen → gemacht; kaufen → gekauft; arbeiten → gearbeitet. "
            "Irregular (strong) verbs: ge- + altered stem + -en. Memorize these. kommen → gekommen; gehen → gegangen; "
            "lesen → gelesen; sehen → gesehen; essen → gegessen; trinken → getrunken; sprechen → gesprochen; schreiben → geschrieben; "
            "fahren → gefahren; nehmen → genommen. "
            "Trennbare Verben insert -ge- between prefix and stem: aufstehen → aufgestanden; einkaufen → eingekauft; mitkommen → mitgekommen. "
            "Verbs ending in -ieren and verbs with inseparable prefixes (be-, ge-, er-, ver-, zer-, ent-, emp-) take NO ge-: "
            "studieren → studiert; telefonieren → telefoniert; bekommen → bekommen; verstehen → verstanden; erzählen → erzählt. "
            "Common A1 mistake: wrong auxiliary ('Ich habe nach Berlin gefahren' — wrong, motion verb takes sein → 'Ich bin nach Berlin gefahren'); "
            "missing ge- ('Ich habe lernt' — wrong → 'Ich habe gelernt'); putting the participle in position 2 ('Ich gelernt habe Deutsch' — wrong)."
        ),
    },
]


def get_chapter_by_slug(slug: str):
    return next((c for c in DEUTSCH_A1_CHAPTERS if c["slug"] == slug), None)


def get_chapter_by_name(name: str):
    return next((c for c in DEUTSCH_A1_CHAPTERS if c["name"] == name), None)


def build_corpus_text(focus_chapter_slugs: list[str] | None = None) -> str:
    """Concatenate chapter contents, optionally filtered to a subset."""
    chapters = DEUTSCH_A1_CHAPTERS
    if focus_chapter_slugs:
        focus_set = set(focus_chapter_slugs)
        filtered = [c for c in DEUTSCH_A1_CHAPTERS if c["slug"] in focus_set]
        if filtered:
            chapters = filtered
    parts = []
    for ch in chapters:
        parts.append(f"--- Chapter: {ch['name']} ---\n{ch['content']}")
    return "\n\n".join(parts)
