"""
Static chapter knowledge base for the German Grammar A2 (CEFR) agent.

Each chapter slug names ONE atomic Grammatik-Regel from the standard A2 syllabus
(Goethe-Zertifikat A2 / telc Deutsch A2 / ÖSD A2). Slugs are German-anchored.

Assumes A1 mastery — chapters here introduce A2 additions (Dativ,
Wechselpräpositionen, Präteritum, Konjunktiv II, Nebensätze, Reflexivverben,
Adjektivdeklination, Relativsätze, Passiv) without re-teaching A1 fundamentals.

Like A1, this subject ships without a seed exam bank — generation runs purely
off this corpus + instructions.md.
"""

DEUTSCH_A2_CHAPTERS = [
    {
        "slug": "dativ",
        "name": "Dativ",
        "summary": "The dative case — indirect object, dative verbs, and dative prepositions.",
        "content": (
            "The Dativ (dative case) marks the INDIRECT OBJECT — the recipient or beneficiary of an action. "
            "Ask 'Wem?' (to whom) after the verb. "
            "Definite articles in dative: masculine 'dem', feminine 'der', neuter 'dem', plural 'den' (+ '-n' on the noun). "
            "Indefinite articles: 'einem', 'einer', 'einem' (no plural form). "
            "Possessive/kein: 'meinem', 'meiner', 'meinem', 'meinen' (+ -n on plural nouns). "
            "Examples: Ich gebe dem Mann ein Buch. Ich helfe meiner Schwester. Wir geben den Kindern Geschenke (note the -n on Kindern). "
            "DATIVE VERBS — verbs that take dative even though there's no preposition: "
            "helfen (to help), danken (to thank), gefallen (to please), gehören (to belong to), schmecken (to taste good), "
            "antworten (to answer), glauben (to believe), gratulieren (to congratulate), folgen (to follow), passieren (to happen to). "
            "Examples: Ich helfe meinem Vater. Das Geschenk gefällt der Frau. Das Buch gehört dem Lehrer. "
            "DATIVE PREPOSITIONS — always trigger dative, no matter the verb: "
            "aus (from/out of), bei (at/by/near), mit (with), nach (to/after), seit (since/for), von (from/of), zu (to), "
            "gegenüber (across from). Mnemonic: 'aus, bei, mit, nach, seit, von, zu, gegenüber'. "
            "Examples: Ich komme aus der Türkei. Ich wohne bei meiner Mutter. Ich fahre mit dem Bus. Nach dem Essen gehen wir. "
            "Seit zwei Jahren lerne ich Deutsch. Das ist von meinem Freund. Wir gehen zum (zu + dem) Arzt. "
            "DATIVE PERSONAL PRONOUNS: mir (to me), dir (to you-sg), ihm (to him/it), ihr (to her), ihm (to it), uns (to us), euch (to you-pl), ihnen (to them), Ihnen (to you-formal). "
            "Common A2 mistake: forgetting the -n on plural dative nouns (mit den Kindern, NOT mit den Kinder); using accusative 'den' where dative 'dem' is needed."
        ),
    },
    {
        "slug": "wechselpraepositionen",
        "name": "Wechselpräpositionen",
        "summary": "The nine two-way prepositions — accusative for movement, dative for location.",
        "content": (
            "Nine prepositions can take EITHER accusative OR dative depending on meaning. They are called "
            "Wechselpräpositionen (two-way prepositions): "
            "in, an, auf, unter, über, vor, hinter, neben, zwischen. "
            "RULE: "
            "Akkusativ when the action involves MOVEMENT toward a destination (Wohin?). "
            "Dativ when describing LOCATION or stationary state (Wo?). "
            "Examples — Wo? (Dativ, location): "
            "Das Buch liegt auf dem Tisch. (location) "
            "Der Hund schläft unter dem Stuhl. (location) "
            "Wir wohnen in der Stadt. (location) "
            "Examples — Wohin? (Akkusativ, movement): "
            "Ich lege das Buch auf den Tisch. (movement onto) "
            "Der Hund läuft unter den Stuhl. (movement under) "
            "Wir gehen in die Stadt. (movement into) "
            "Note that location verbs (sein, liegen, stehen, sitzen, hängen, wohnen) take dative; "
            "movement verbs (gehen, fahren, fliegen, legen, stellen, setzen, hängen-trans) take accusative. "
            "CONTRACTIONS — common contractions of preposition + article: "
            "in dem → im (in the masc/neut dat). "
            "in das → ins (in the neut acc). "
            "an dem → am (at/on the masc/neut dat — used for days, dates, locations: am Montag, am Bahnhof). "
            "an das → ans (acc). "
            "auf das → aufs (informal). "
            "zu dem → zum (to the masc/neut dat). "
            "zu der → zur (to the fem dat). "
            "von dem → vom (from the masc/neut dat). "
            "Examples: Ich gehe ins Kino (Wohin? acc). Ich bin im Kino (Wo? dat). Ich gehe zum Arzt (zu+dem). "
            "Common A2 mistake: Wo/Wohin confusion — picking 'den Tisch' (acc) for a stationary location, or 'dem Tisch' (dat) for an action moving onto it."
        ),
    },
    {
        "slug": "praeteritum",
        "name": "Präteritum",
        "summary": "The simple past tense — used in writing and for sein, haben, modals in speech.",
        "content": (
            "The Präteritum (simple past) is the WRITTEN past tense in German (newspapers, novels, formal reports). "
            "In SPOKEN German, the Perfekt is preferred — except for these high-frequency verbs, which are spoken in Präteritum: "
            "sein, haben, the six modal verbs, and a few others (wissen, geben, sagen). "
            "sein (to be): ich war, du warst, er/sie/es war, wir waren, ihr wart, sie/Sie waren. "
            "haben (to have): ich hatte, du hattest, er hatte, wir hatten, ihr hattet, sie hatten. "
            "können: ich konnte, du konntest, er konnte, wir konnten, ihr konntet, sie konnten. "
            "müssen: ich musste, du musstest, er musste, wir mussten, ihr musstet, sie mussten. "
            "wollen: ich wollte, du wolltest, er wollte, wir wollten, ihr wolltet, sie wollten. "
            "dürfen: ich durfte, du durftest, er durfte... "
            "sollen: ich sollte, du solltest, er sollte... "
            "Note: modals lose the umlaut in Präteritum (können → konnte, müssen → musste, dürfen → durfte). "
            "REGULAR (weak) verbs: stem + -te + ending. lernen → ich lernte, du lerntest, er lernte, wir lernten, ihr lerntet, sie lernten. "
            "machen → ich machte. arbeiten → ich arbeitete (insert -e- before -te for stems ending in -t/-d). "
            "STRONG (irregular) verbs: stem vowel changes + bare endings on ich/er forms. "
            "kommen → ich kam, du kamst, er kam, wir kamen, ihr kamt, sie kamen. "
            "gehen → ich ging, du gingst, er ging, wir gingen. "
            "sehen → ich sah. essen → ich aß. trinken → ich trank. fahren → ich fuhr. nehmen → ich nahm. "
            "sprechen → ich sprach. schreiben → ich schrieb. lesen → ich las. "
            "Note that ich-form and er/sie/es-form are IDENTICAL in Präteritum (no ending added). "
            "Common A2 mistake: applying the -te pattern to strong verbs ('ich gehte' instead of 'ich ging')."
        ),
    },
    {
        "slug": "komparativ_superlativ",
        "name": "Komparativ & Superlativ",
        "summary": "Comparative (groß → größer) and superlative (am größten) forms of adjectives and adverbs.",
        "content": (
            "Komparativ (comparative) — add '-er' to the adjective. Used with 'als' (than). "
            "klein → kleiner. schnell → schneller. langsam → langsamer. "
            "Many one-syllable adjectives add an UMLAUT: "
            "alt → älter. jung → jünger. groß → größer. lang → länger. kurz → kürzer. warm → wärmer. kalt → kälter. stark → stärker. "
            "IRREGULAR comparatives — memorize: "
            "gut → besser. viel → mehr. hoch → höher. nah → näher. gern → lieber. teuer → teurer (drop the second 'e'). dunkel → dunkler. "
            "Examples: Ich bin größer als du. Berlin ist größer als München. Ich trinke lieber Tee als Kaffee. "
            "Important: in standard German, comparative + 'als' (NOT 'wie' — using 'wie' is dialectal/wrong in formal German). "
            "'so + adjective + wie' = as ... as: Ich bin so groß wie du. "
            "Superlativ (superlative) — two forms: "
            "PREDICATIVE (after sein/werden): am + adjective + -sten. "
            "Tom ist am schnellsten. Anna ist am schönsten. Berlin ist am größten. "
            "ATTRIBUTIVE (before a noun): der/die/das + adjective + -ste(n) — declined like a normal adjective. "
            "der schnellste Läufer. die schönste Stadt. das größte Haus. "
            "Adjectives ending in -d, -t, -s, -ß, -sch, -z usually insert an extra '-e-' before -sten: "
            "kalt → am kältesten. heiß → am heißesten. kurz → am kürzesten. "
            "IRREGULAR superlatives: gut → am besten. viel → am meisten. hoch → am höchsten. nah → am nächsten. gern → am liebsten. "
            "Common A2 mistake: 'mehr groß' (English-style 'more big' — wrong, must be 'größer'); using 'wie' instead of 'als' after a comparative."
        ),
    },
    {
        "slug": "konjunktiv_ii_hoeflichkeit",
        "name": "Konjunktiv II (Höflichkeit)",
        "summary": "Polite forms with würde, könnte, hätte, wäre, möchte — for requests, wishes, and politeness.",
        "content": (
            "Konjunktiv II (subjunctive II) is used at A2 level for POLITENESS and WISHES — not for the full subjunctive system. "
            "Three high-frequency irregular forms — memorize: "
            "sein → wäre: ich wäre, du wärest/wärst, er wäre, wir wären, ihr wärt, sie wären. "
            "haben → hätte: ich hätte, du hättest, er hätte, wir hätten, ihr hättet, sie hätten. "
            "können → könnte: ich könnte, du könntest, er könnte, wir könnten, ihr könntet, sie könnten. "
            "Other modal Konjunktiv II forms (rarer at A2): müsste, dürfte, sollte, wollte (= same as Präteritum), möchte (always polite — from mögen). "
            "For all other verbs, use würde + infinitive (the 'würde-construction'): "
            "würde: ich würde, du würdest, er würde, wir würden, ihr würdet, sie würden. "
            "Pattern: [Subject] [würde-V2] [...] [Infinitive-end]. Same word order as a modal verb. "
            "Examples — POLITE REQUESTS: "
            "Könnten Sie mir helfen? (more polite than 'Können Sie mir helfen?') "
            "Würden Sie das Fenster öffnen? "
            "Hätten Sie einen Moment Zeit? "
            "Examples — POLITE ORDERING/ASKING: "
            "Ich hätte gern einen Kaffee. (in a café — extremely common A2 phrase) "
            "Ich möchte bitte das Steak. "
            "Wir hätten gern die Rechnung. "
            "Examples — WISHES (often with 'gern'): "
            "Ich würde gerne nach Italien fahren. "
            "Ich wäre gern reicher. "
            "Common A2 mistake: using 'will' (rude in requests) where 'möchte' is needed; conjugating würden incorrectly ('ich würden' instead of 'ich würde'); forgetting the infinitive at the end ('Ich würde gehen ins Kino' instead of 'Ich würde ins Kino gehen')."
        ),
    },
    {
        "slug": "nebensatz_weil_dass",
        "name": "Nebensatz mit weil & dass",
        "summary": "Subordinate clauses with weil (because) and dass (that) — verb at the end.",
        "content": (
            "Subordinating conjunctions push the conjugated verb to the END of the subordinate clause. "
            "ALWAYS use a comma before the conjunction. "
            "weil = because (introduces a reason): "
            "Ich lerne Deutsch, weil ich in Berlin wohne. "
            "Tom ist müde, weil er den ganzen Tag gearbeitet hat. (Note: in Perfekt the auxiliary 'hat' goes to the very end, after the participle.) "
            "Sie kommt nicht, weil sie krank ist. "
            "dass = that (introduces a content/reported clause): "
            "Ich glaube, dass er müde ist. "
            "Ich weiß, dass du Deutsch lernst. "
            "Es ist schade, dass du nicht kommen kannst. (Modal verb at the very end after the infinitive.) "
            "DENN vs WEIL: 'denn' also means 'because' but is COORDINATING — it does NOT push the verb to the end. "
            "Use 'denn' if you want to keep main-clause word order in the second clause: "
            "Ich lerne Deutsch, weil ich in Berlin wohne. (verb 'wohne' at end) "
            "Ich lerne Deutsch, denn ich wohne in Berlin. (verb 'wohne' in V2 position) "
            "Both sentences mean the same; the structure differs. "
            "DASS vs DAS: 'dass' (with double-s) is the conjunction. 'das' (with single-s) is the neuter article or relative pronoun. They are NOT interchangeable. "
            "Wrong: Ich glaube, das er müde ist. Right: Ich glaube, dass er müde ist. "
            "Common A2 mistake: keeping the verb in V2 position in the subordinate clause ('weil ich bin müde' instead of 'weil ich müde bin'); confusing 'dass' and 'das'."
        ),
    },
    {
        "slug": "nebensatz_wenn_obwohl",
        "name": "Nebensatz mit wenn & obwohl",
        "summary": "Conditional and concessive clauses — wenn (when/if), ob (whether), obwohl (although), and the V2-flippers deshalb/trotzdem.",
        "content": (
            "wenn = when/if (conditional or repeated action). Subordinate-clause word order — verb at the end. "
            "Wenn ich Zeit habe, komme ich. (If I have time, I will come.) "
            "Wenn das Wetter schön ist, gehen wir spazieren. "
            "Note: when the subordinate clause comes FIRST, the main clause begins with the verb (V2 — the subordinate clause counts as position 1). "
            "Wenn vs Wann: 'wann' is for QUESTIONS about time ('Wann kommst du?'). 'wenn' is for conditions or repeated events. "
            "ob = whether (introduces an indirect yes/no question). Subordinate-clause word order. "
            "Ich weiß nicht, ob er kommt. "
            "Sie fragt mich, ob ich Zeit habe. "
            "obwohl = although (concessive). Subordinate-clause word order. "
            "Er kommt, obwohl er müde ist. "
            "Wir gehen spazieren, obwohl es regnet. "
            "V2-FLIPPERS — these adverbs occupy position 1 of the next clause, forcing the verb into position 2: "
            "deshalb / deswegen / darum (therefore): Ich bin müde, deshalb gehe ich nach Hause. (NOT 'deshalb ich gehe'.) "
            "trotzdem (nevertheless): Es regnet, trotzdem gehe ich spazieren. "
            "dann (then): Ich esse, dann gehe ich ins Bett. "
            "These behave like normal V2 adverbs — the verb comes immediately after them, with the subject in position 3. "
            "Common A2 mistake: using 'wann' where 'wenn' is needed ('Wann ich Zeit habe...' wrong); after 'deshalb', writing 'deshalb ich gehe' (V3 error)."
        ),
    },
    {
        "slug": "reflexivverben",
        "name": "Reflexivverben",
        "summary": "Reflexive verbs and the accusative vs dative reflexive pronouns.",
        "content": (
            "Reflexive verbs are conjugated with a REFLEXIVE PRONOUN (sich) referring back to the subject. "
            "ACCUSATIVE reflexive pronouns (most common): mich, dich, sich, uns, euch, sich. "
            "DATIVE reflexive pronouns (when there's also an accusative object, usually a body part): mir, dir, sich, uns, euch, sich. "
            "Note: the only difference between Akk and Dat is in the ich/du forms (mich/mir, dich/dir). The other forms (sich, uns, euch) are identical. "
            "ACCUSATIVE REFLEXIVE VERBS — most common A2 set: "
            "sich waschen (wash oneself), sich anziehen (get dressed), sich ausziehen (undress), sich freuen (be happy), "
            "sich erinnern an (remember), sich setzen (sit down), sich treffen (meet), sich bewerben (apply), "
            "sich verabreden (make a date), sich konzentrieren (concentrate), sich ärgern (be annoyed), sich entschuldigen (apologize), "
            "sich beeilen (hurry), sich entscheiden (decide), sich verlieben (fall in love). "
            "Examples: Ich wasche mich. Du freust dich. Er trifft sich mit Anna. Wir setzen uns. "
            "DATIVE REFLEXIVE — used when there's a DIRECT OBJECT (often a body part or possession): "
            "sich die Hände waschen. sich die Haare kämmen. sich die Zähne putzen. sich etwas wünschen (wish for something). sich etwas vorstellen (imagine something). "
            "Examples: Ich wasche mir die Hände. Du putzt dir die Zähne. Sie wünscht sich ein Auto. "
            "Compare: 'Ich wasche mich' (I wash myself — accusative; the whole self is the object) vs 'Ich wasche mir die Hände' (I wash my hands — accusative is 'die Hände', dative is 'mir' = 'for myself'). "
            "Position: the reflexive pronoun usually comes RIGHT AFTER the conjugated verb in main clauses. "
            "Common A2 mistake: using accusative reflexive where dative is needed ('Ich wasche mich die Hände' wrong, must be 'mir die Hände')."
        ),
    },
    {
        "slug": "adjektivdeklination",
        "name": "Adjektivdeklination",
        "summary": "Adjective endings before nouns — depend on gender, case, and article type.",
        "content": (
            "When an adjective stands BEFORE a noun, it takes an ending. The ending depends on three things: "
            "gender of the noun, case of the noun, and the type of article (definite, indefinite, none). "
            "When the adjective is PREDICATIVE (after sein/werden/bleiben), it has NO ending: 'Der Mann ist groß.' 'Das Auto ist neu.' "
            "AFTER A DEFINITE ARTICLE (der/die/das/die, dem/der/dem/den, etc.) — 'weak' endings: "
            "Nominative singular: -e on all genders. der große Mann. die schöne Frau. das kleine Kind. "
            "Accusative singular: -e for fem/neut, but -en for masculine. den großen Mann. die schöne Frau. das kleine Kind. "
            "Dative singular: -en across all genders. dem großen Mann. der schönen Frau. dem kleinen Kind. "
            "ALL plural forms (any case): -en. die großen Männer. den großen Männern. "
            "Rule of thumb: after the definite article, use -e in nominative singular and -en almost everywhere else. "
            "AFTER AN INDEFINITE ARTICLE (ein/eine/ein, einen/eine/ein, einem/einer/einem) — 'mixed' endings: "
            "The adjective adds the gender ending the article DOESN'T show. "
            "Nominative: ein großer Mann (-r — because 'ein' is the same for masc and neut, the adjective shows the masc -r). "
            "eine schöne Frau (-e). ein kleines Kind (-es — because 'ein' doesn't show neut -s). "
            "Accusative masc: einen großen Mann (-en). Accusative fem/neut: same as nominative. "
            "WITHOUT AN ARTICLE — 'strong' endings (the adjective takes the article-like ending itself): "
            "heißer Tee (-r masc nom). kalte Milch (-e fem nom). kaltes Wasser (-es neut nom). "
            "kalten Tee (-en masc acc). "
            "A2 focus: nominative + accusative, both definite and indefinite. Dative comes more in B1. "
            "Common A2 mistake: 'ein großes Mann' (wrong — masc nominative is 'großer Mann'); 'mit dem große Mann' (wrong — dative requires -en, so 'großen Mann')."
        ),
    },
    {
        "slug": "relativsaetze",
        "name": "Relativsätze",
        "summary": "Relative clauses with der/die/das — verb at the end.",
        "content": (
            "Relative clauses describe a noun in more detail. They are SUBORDINATE CLAUSES → conjugated verb goes to the END. "
            "The relative pronoun (der/die/das) replaces the noun and matches its GENDER and NUMBER, but its CASE depends on the role inside the relative clause. "
            "RELATIVE PRONOUNS — most are identical to the definite article: "
            "Nominative: der (m), die (f), das (n), die (pl). "
            "Accusative: den (m), die (f), das (n), die (pl). "
            "Dative: dem (m), der (f), dem (n), DENEN (pl — note the change!). "
            "Examples — nominative (subject of the relative clause): "
            "Der Mann, der dort steht, ist mein Vater. (der = subject of 'steht') "
            "Die Frau, die in Berlin wohnt, heißt Anna. "
            "Das Kind, das dort spielt, ist drei Jahre alt. "
            "Die Leute, die ich kenne, sind nett. "
            "Examples — accusative (direct object of the relative clause): "
            "Der Mann, den ich sehe, ist mein Lehrer. (den = direct object of 'sehe') "
            "Das Buch, das ich lese, ist interessant. "
            "Examples — dative (indirect object of the relative clause): "
            "Der Mann, dem ich helfe, ist mein Freund. (dem = dative because 'helfen' takes dative) "
            "Die Leute, denen ich danke, sind nett. (denen, NOT den, for plural dative) "
            "After a preposition: the preposition comes BEFORE the relative pronoun, and the case is determined by the preposition. "
            "Der Stuhl, auf dem ich sitze, ist alt. (auf + Wo? = dative → dem) "
            "Die Frau, mit der ich spreche, ist Lehrerin. (mit + dative → der) "
            "Common A2 mistake: wrong gender on the pronoun ('die Frau, der...' instead of 'die Frau, die...'); plural dative 'denen' confused with 'den'; verb in V2 instead of clause-end."
        ),
    },
    {
        "slug": "passiv_praesens",
        "name": "Passiv Präsens",
        "summary": "Present passive — werden + Partizip II — focuses on the action, not the doer.",
        "content": (
            "The Passiv (passive voice) shifts the focus from the doer to the action or the receiver of the action. "
            "Form: werden (conjugated) + Partizip II (at the end of the clause). "
            "werden in present: ich werde, du wirst, er/sie/es wird, wir werden, ihr werdet, sie/Sie werden. "
            "ACTIVE → PASSIVE transformation: "
            "The active subject becomes 'von' + DATIVE (or omitted). "
            "The active accusative object becomes the passive subject (nominative). "
            "Active: Der Lehrer fragt den Schüler. → Passive: Der Schüler wird vom Lehrer gefragt. "
            "Active: Die Mutter kocht das Essen. → Passive: Das Essen wird von der Mutter gekocht. "
            "Often AGENTLESS — when the doer is unimportant or unknown: "
            "Hier wird Deutsch gesprochen. (German is spoken here.) "
            "Das Auto wird repariert. (The car is being repaired.) "
            "Der Brief wird heute geschrieben. "
            "PASSIVE WITH MODAL VERB: modal in V2 + main verb infinitive Partizip II + werden at the end. "
            "Das Auto muss repariert werden. (The car must be repaired.) "
            "Der Brief kann heute geschrieben werden. "
            "Note the passive infinitive: 'Partizip II + werden'. "
            "VON vs DURCH: 'von' marks a personal agent (von dem Lehrer); 'durch' marks an impersonal cause or means (durch den Sturm = by the storm). "
            "Common A2 mistake: using 'sein' instead of 'werden' as the auxiliary ('Hier ist Deutsch gesprochen' wrong, must be 'wird'); wrong agent preposition ('bei' or 'mit' instead of 'von')."
        ),
    },
    {
        "slug": "verben_mit_praeposition",
        "name": "Verben mit festen Präpositionen",
        "summary": "Verbs that require a fixed preposition with a fixed case — memorize as a unit.",
        "content": (
            "Many verbs require a SPECIFIC preposition with a SPECIFIC case. The preposition is not predictable from English, "
            "and the case is fixed (it does NOT follow the Wechselpräposition Wo/Wohin rule). Memorize each verb + preposition + case as a unit. "
            "ACCUSATIVE-triggering verb-preposition combos: "
            "warten auf + Akk (wait for): Ich warte auf den Bus. "
            "sich freuen auf + Akk (look forward to): Ich freue mich auf das Wochenende. "
            "sich freuen über + Akk (be happy about — already received): Ich freue mich über das Geschenk. "
            "denken an + Akk (think of/about): Ich denke an dich. "
            "sich erinnern an + Akk (remember): Ich erinnere mich an meine Kindheit. "
            "sich interessieren für + Akk (be interested in): Sie interessiert sich für Musik. "
            "sich ärgern über + Akk (be annoyed about): Er ärgert sich über den Lärm. "
            "sich entscheiden für + Akk (decide for): Wir entscheiden uns für das blaue Auto. "
            "sich bewerben um + Akk (apply for a job): Ich bewerbe mich um die Stelle. "
            "DATIVE-triggering verb-preposition combos: "
            "träumen von + Dat (dream of/about): Ich träume von dir. "
            "sprechen mit + Dat (talk with): Ich spreche mit meiner Mutter. "
            "Angst haben vor + Dat (be afraid of): Ich habe Angst vor dem Hund. "
            "telefonieren mit + Dat (talk on the phone with): Ich telefoniere mit Anna. "
            "helfen bei + Dat (help with a task): Ich helfe dir bei der Arbeit. "
            "DOUBLE PREPOSITIONS — some verbs take TWO prepositions: "
            "sprechen mit + Dat über + Akk (talk with X about Y): Ich spreche mit Anna über den Film. "
            "sich unterhalten mit + Dat über + Akk: Wir unterhalten uns mit den Lehrern über die Prüfung. "
            "Common A2 mistake: using English-direct translations ('warten für' instead of 'warten auf'); right preposition with wrong case ('warten auf dem Bus' instead of 'auf den Bus' — 'auf' here is fixed-accusative, not Wechselpräposition)."
        ),
    },
    {
        "slug": "genitiv_basics",
        "name": "Genitiv (Grundlagen)",
        "summary": "The genitive case at A2 — names with -s, von + Dativ as a colloquial alternative, and a few prepositions.",
        "content": (
            "The Genitiv (genitive case) shows possession or 'of' relationships. At A2 level, only basic recognition is required — "
            "spoken German often replaces the genitive with 'von + Dativ'. "
            "GENITIVE ARTICLES: "
            "Definite: des (m), der (f), des (n), der (pl). "
            "Indefinite/possessive: eines (m), einer (f), eines (n), (no plural). "
            "Masculine and neuter nouns ALSO add -s or -es to the noun in genitive: "
            "des Mannes, des Lehrers, des Vaters; des Kindes, des Buches, des Autos. "
            "Feminine and plural nouns do NOT change. "
            "Examples: das Auto meines Vaters. der Hund meiner Schwester. die Farbe des Buches. die Bücher der Kinder. "
            "NAMES with -s — much more common in everyday speech: "
            "Annas Buch. Toms Auto. Marias Schwester. (No apostrophe in German — different from English 'Anna's'.) "
            "If the name ends in s/ss/ß/x/z, use an apostrophe instead: Hans' Auto. Max' Buch. "
            "VON + DATIV alternative — informal/spoken German: "
            "das Auto von meinem Vater = das Auto meines Vaters (more colloquial vs more formal). "
            "die Mutter von Anna = Annas Mutter. "
            "GENITIVE PREPOSITIONS — at A2, mostly recognition: "
            "wegen (because of), trotz (in spite of), während (during), statt/anstatt (instead of). "
            "wegen des Wetters (formal) / wegen dem Wetter (colloquial dative — also accepted in spoken German). "
            "Examples: Während des Essens spricht man nicht. Trotz des Regens gehen wir spazieren. "
            "Common A2 mistake: missing the -s on masculine/neuter nouns ('das Auto meines Vater' wrong, must be 'meines Vaters'); adding -s to feminine nouns (wrong)."
        ),
    },
    {
        "slug": "temporalpraepositionen",
        "name": "Temporalpräpositionen",
        "summary": "Time prepositions — am, um, im, seit, vor, nach, in, für, bis.",
        "content": (
            "German time prepositions follow specific patterns. Choose the right one for the type of time expression. "
            "AM (an + dem) — for days, dates, parts of the day: "
            "am Montag, am Dienstag, am Wochenende, am 5. Mai, am Morgen, am Abend, am Nachmittag. "
            "(Exception: in der Nacht — for 'at night'.) "
            "UM — for clock time (specific point): "
            "um 8 Uhr, um halb neun, um Viertel vor sieben, um Mitternacht. "
            "IM (in + dem) — for months, seasons, years (with 'Jahr'): "
            "im Januar, im Dezember, im Sommer, im Winter, im Jahr 2026. "
            "(NOT 'in 2026' alone in formal German — say 'im Jahr 2026' or just '2026'.) "
            "SEIT + Dat — duration starting in the past, continuing now ('since' / 'for'): "
            "Ich lerne seit zwei Jahren Deutsch. Sie wohnt seit Januar in Berlin. "
            "VOR + Dat — duration before now ('ago'): "
            "Ich war vor drei Tagen krank. Vor einer Stunde habe ich gegessen. "
            "NACH + Dat — after an event: "
            "Nach dem Essen gehen wir spazieren. Nach der Arbeit treffe ich meine Freunde. "
            "IN + Dat — duration in the future ('in/within'): "
            "In zwei Stunden kommt der Bus. Wir fahren in einer Woche nach Italien. "
            "FÜR + Akk — planned duration ('for'): "
            "Ich gehe für drei Tage nach Berlin. Wir bleiben für eine Woche. "
            "BIS — until (often with no article, or with zu + Dat for definite): "
            "Bis Montag. Bis morgen. Bis nächste Woche. Bis zum Ende des Monats. "
            "AB + Dat — starting from: "
            "Ab Montag arbeite ich wieder. Ab dem nächsten Jahr. "
            "Common A2 mistake: 'in zwei Jahren' (future) confused with 'vor zwei Jahren' (past); 'am' for clock time ('am 8 Uhr' wrong, must be 'um 8 Uhr')."
        ),
    },
    {
        "slug": "indirekte_fragen",
        "name": "Indirekte Fragen",
        "summary": "Indirect questions — verb at the end, ob for yes/no, W-word for content questions.",
        "content": (
            "Indirect questions are subordinate clauses that follow a 'reporting' or 'asking' main clause "
            "(Ich weiß nicht..., Ich frage..., Können Sie mir sagen..., Weißt du...). "
            "They follow SUBORDINATE-CLAUSE word order — conjugated verb at the END. "
            "OB = whether (used for indirect YES/NO questions): "
            "Direct: Kommt er? → Indirect: Ich weiß nicht, ob er kommt. "
            "Direct: Hast du Zeit? → Indirect: Sie fragt, ob du Zeit hast. "
            "Direct: Ist das richtig? → Indirect: Können Sie mir sagen, ob das richtig ist? "
            "W-WORD + clause (used for indirect WH-questions): "
            "Direct: Wann kommt der Bus? → Indirect: Ich weiß nicht, wann der Bus kommt. "
            "Direct: Wo wohnst du? → Indirect: Sie fragt, wo ich wohne. "
            "Direct: Warum lernst du Deutsch? → Indirect: Er möchte wissen, warum ich Deutsch lerne. "
            "Direct: Wie heißt du? → Indirect: Können Sie mir sagen, wie Sie heißen? "
            "POLITE QUESTIONS often use this structure with Konjunktiv II: "
            "Könnten Sie mir sagen, wo der Bahnhof ist? "
            "Wissen Sie, wann der nächste Zug kommt? "
            "Hätten Sie Zeit, mir zu erklären, wie das funktioniert? "
            "DASS vs OB: "
            "ob = whether (for yes/no — implies an open answer). "
            "dass = that (for known/asserted content). "
            "Wrong: Ich weiß nicht, dass er kommt oder nicht. "
            "Right: Ich weiß nicht, ob er kommt. "
            "Common A2 mistake: V2 word order leaked into the indirect clause ('Ich weiß nicht, wo wohnt er' instead of 'wo er wohnt'); using 'dass' for indirect yes/no questions instead of 'ob'."
        ),
    },
]


def get_chapter_by_slug(slug: str):
    return next((c for c in DEUTSCH_A2_CHAPTERS if c["slug"] == slug), None)


def get_chapter_by_name(name: str):
    return next((c for c in DEUTSCH_A2_CHAPTERS if c["name"] == name), None)


def build_corpus_text(focus_chapter_slugs: list[str] | None = None) -> str:
    """Concatenate chapter contents, optionally filtered to a subset."""
    chapters = DEUTSCH_A2_CHAPTERS
    if focus_chapter_slugs:
        focus_set = set(focus_chapter_slugs)
        filtered = [c for c in DEUTSCH_A2_CHAPTERS if c["slug"] in focus_set]
        if filtered:
            chapters = filtered
    parts = []
    for ch in chapters:
        parts.append(f"--- Chapter: {ch['name']} ---\n{ch['content']}")
    return "\n\n".join(parts)
