"""
Static chapter knowledge base for the German Grammar B1 (CEFR) agent.

Each chapter slug names ONE atomic Grammatik-Regel from the standard B1 syllabus
(Goethe-Zertifikat B1 / telc Deutsch B1 / ÖSD B1). Slugs are German-anchored.

Assumes A1 + A2 mastery — chapters here introduce B1 additions (full Konjunktiv II,
Plusquamperfekt, full Passiv, indirekte Rede, advanced Nebensätze, advanced
Relativsätze, full Adjektivdeklination, N-Deklination, da-/wo-compounds, full
Genitiv, Partizipien als Adjektive, subjektive Modalverben, Futur, and
Konjunktionaladverbien) without re-teaching A1/A2 fundamentals.

Like A1 and A2, this subject ships without a seed exam bank — generation runs
purely off this corpus + instructions.md.
"""

DEUTSCH_B1_CHAPTERS = [
    {
        "slug": "konjunktiv_ii_komplett",
        "name": "Konjunktiv II (komplett)",
        "summary": "Full Konjunktiv II — irreale Bedingungen, Wünsche, Höflichkeit, present and past forms.",
        "content": (
            "Konjunktiv II expresses HYPOTHETICAL, UNREAL, or POLITE meaning. At B1 the full system is required, "
            "not just the politeness forms learned in A2. "
            "PRESENT/FUTURE KONJUNKTIV II: "
            "For most verbs, use 'würde' + Infinitiv: Ich würde gehen. Du würdest kommen. Er würde arbeiten. "
            "For 'sein', 'haben', and modal verbs, use the dedicated K-II form (DO NOT use 'würde'): "
            "sein → wäre (ich wäre, du wärst, er wäre, wir wären, ihr wärt, sie wären) "
            "haben → hätte (ich hätte, du hättest, er hätte, wir hätten, ihr hättet, sie hätten) "
            "können → könnte; müssen → müsste; sollen → sollte; dürfen → dürfte; mögen → möchte; wollen → wollte. "
            "Some strong verbs have their own K-II forms still used in writing: ginge, käme, wüsste, gäbe, ließe, fände. "
            "PAST KONJUNKTIV II (Plusquamperfekt Konjunktiv) — for hypothetical situations in the PAST: "
            "Form: 'hätte' / 'wäre' + Partizip II. "
            "Examples: Ich hätte das gemacht. Wir wären gekommen. Du hättest mir helfen sollen. "
            "Modal verbs in past K-II take a double infinitive: Ich hätte das machen können (NOT 'gemocht'). "
            "IRREALE BEDINGUNGSSÄTZE (unreal conditionals): "
            "Present/future: Wenn ich Zeit hätte, würde ich kommen. Wenn er hier wäre, könnte er helfen. "
            "Past: Wenn ich Zeit gehabt hätte, wäre ich gekommen. Hätte ich das gewusst, wäre ich nicht gegangen. "
            "Note the optional inversion without 'wenn': Hätte ich Zeit, käme ich. Wäre er hier, könnte er helfen. "
            "WÜNSCHE (wishes): "
            "Present: Wenn ich nur mehr Zeit hätte! Ich wünschte, ich könnte das. "
            "Past: Wenn ich nur früher gekommen wäre! Hätte ich doch mehr gelernt! "
            "HÖFLICHKEIT (politeness — already familiar from A2): "
            "Könnten Sie mir helfen? Hätten Sie kurz Zeit? Ich würde gern bestellen. "
            "Common B1 mistake: using 'würde + Inf' with sein/haben/modal ('Ich würde Zeit haben' instead of 'Ich hätte Zeit'); "
            "mixing tenses across the two clauses ('Wenn ich Zeit hatte, würde ich kommen' — must be 'hätte'); "
            "wrong word order in past K-II ('Wenn ich gewusst hätte das' instead of 'Wenn ich das gewusst hätte')."
        ),
    },
    {
        "slug": "plusquamperfekt",
        "name": "Plusquamperfekt",
        "summary": "Past perfect tense — actions completed before another past action, especially with 'nachdem'.",
        "content": (
            "The Plusquamperfekt (past perfect) describes an action completed BEFORE another past action. "
            "FORMATION: 'hatte' or 'war' (Präteritum of haben/sein) + Partizip II. "
            "Auxiliary choice is the same as for Perfekt — most verbs use 'haben', motion / state-change verbs use 'sein'. "
            "Examples: "
            "Ich hatte schon gegessen, als er kam. (I had already eaten when he came.) "
            "Sie war nach Hause gegangen, bevor wir ankamen. (She had gone home before we arrived.) "
            "Nachdem wir die Hausaufgaben gemacht hatten, gingen wir spazieren. (After we had done the homework, we went for a walk.) "
            "Wir hatten den Film schon gesehen, deshalb sind wir nicht mitgegangen. "
            "USED MOST OFTEN with 'NACHDEM' — tense agreement is strict: "
            "Nachdem-clause in Plusquamperfekt → main clause in Präteritum or Perfekt. "
            "Nachdem ich gegessen hatte, bin ich/ging ich spazieren. "
            "Nachdem-clause in Perfekt → main clause in Präsens (less common, for habitual). "
            "Nachdem ich gegessen habe, gehe ich spazieren. (general routine) "
            "Plusquamperfekt is also natural with: bevor (rare — usually Präteritum is enough), als (one-time past event), "
            "and to express background completed action in narrative. "
            "WORD ORDER: "
            "Main clause: 'hatte/war' in V2, Partizip II at the end. (Ich hatte das schon gewusst.) "
            "Subordinate clause: 'hatte/war' at the very end, after Partizip II. (..., bevor ich gegessen hatte.) "
            "Common B1 mistake: using Perfekt after 'nachdem' instead of Plusquamperfekt; wrong auxiliary "
            "('Ich hatte gegangen' instead of 'Ich war gegangen'); placing the auxiliary in the wrong position in subordinate clauses."
        ),
    },
    {
        "slug": "passiv_komplett",
        "name": "Passiv (komplett)",
        "summary": "Full passive — Präsens, Präteritum, Perfekt, with Modalverben, and von/durch distinction.",
        "content": (
            "B1 extends Passiv beyond Präsens (learned in A2) to all tenses and to combinations with Modalverben. "
            "PASSIV PRÄSENS: 'werden' (conjugated) + Partizip II at end. "
            "Das Auto wird repariert. Die Briefe werden geschrieben. "
            "PASSIV PRÄTERITUM: 'wurde' + Partizip II. "
            "Das Auto wurde repariert. Die Häuser wurden gebaut. "
            "PASSIV PERFEKT: 'ist' + Partizip II + 'worden'. Note: 'worden', NOT 'geworden', in passive contexts. "
            "Das Auto ist repariert worden. Die Tür ist geöffnet worden. "
            "PASSIV PLUSQUAMPERFEKT: 'war' + Partizip II + 'worden'. "
            "Das Auto war repariert worden, bevor ich es kaufte. "
            "PASSIV MIT MODALVERB — the modal stays conjugated, infinitive form is 'Partizip II + werden' (= Passiv-Infinitiv): "
            "Das Problem muss gelöst werden. (must be solved) "
            "Die Tür kann nicht geöffnet werden. (cannot be opened) "
            "Word order: modal in V2, then everything else, then 'Partizip II + werden' at the end. "
            "PAST FORM with Modalverb: "
            "Das musste gemacht werden. (had to be done — Präteritum of modal) "
            "Das hätte gemacht werden müssen. (would have needed to be done — Konjunktiv II + double infinitive at end!) "
            "VON vs DURCH for the agent: "
            "VON (+ Dativ) — the personal AGENT, the doer. Das Buch wird von dem Lehrer gelesen. "
            "DURCH (+ Akkusativ) — the MEANS or CAUSE, often impersonal. Die Stadt wurde durch ein Erdbeben zerstört. "
            "Das Haus wurde durch Feuer beschädigt. (cause: fire) "
            "Generally use 'von' for people and direct agents, 'durch' for forces, instruments, or intermediaries. "
            "ZUSTANDSPASSIV vs VORGANGSPASSIV (state vs process passive): "
            "Vorgangspassiv ('werden' + P.II) = the PROCESS of doing something. Die Tür wird geschlossen. (someone is closing it) "
            "Zustandspassiv ('sein' + P.II) = the RESULTING STATE. Die Tür ist geschlossen. (it's closed; no implication of an actor) "
            "Common B1 mistake: writing 'geworden' instead of 'worden' in Perfekt passive; using 'sein' instead of 'werden' for Vorgangspassiv; "
            "using 'durch' for personal agents; wrong word order with Modalverb + Passiv (placing 'werden' before Partizip II)."
        ),
    },
    {
        "slug": "indirekte_rede",
        "name": "Indirekte Rede (Konjunktiv I)",
        "summary": "Reported speech — Konjunktiv I in formal writing, with Konjunktiv II as fallback.",
        "content": (
            "Indirekte Rede (reported / indirect speech) is used in news writing, formal reports, and academic German "
            "to relay what someone said without committing to its truth. Spoken German often uses indicative; "
            "WRITTEN B1-level German uses Konjunktiv I (or Konjunktiv II as fallback). "
            "KONJUNKTIV I FORMS (stem + K-I ending, the ending '-e' is the marker for 3rd singular): "
            "sein → ich sei, du sei(e)st, er sei, wir seien, ihr seiet, sie seien (irregular — most used!) "
            "haben → er habe (only 3rd singular is reliably distinct from indicative) "
            "machen → er mache; gehen → er gehe; kommen → er komme; wissen → er wisse. "
            "Modal verbs: er könne, er müsse, er solle, er dürfe, er wolle, er möge. "
            "For most verbs, only the 3rd-person singular K-I is clearly distinct from indicative. "
            "K-II FALLBACK: when K-I would be identical to the indicative (plural forms, mostly), switch to K-II. "
            "Indicative 'sie haben' / K-I 'sie haben' → identical → use K-II 'sie hätten'. "
            "Indicative 'sie gehen' / K-I 'sie gehen' → identical → use K-II 'sie gingen' (or 'sie würden gehen'). "
            "TENSE SHIFT in indirekte Rede: "
            "Direct present → K-I present: 'Ich bin müde' → Er sagte, er sei müde. "
            "Direct past (Präteritum/Perfekt/Plusquamperfekt) → K-I Perfekt: 'Ich war müde' → Er sagte, er sei müde gewesen. "
            "Direct future → K-I + werden: 'Ich werde kommen' → Er sagte, er werde kommen. "
            "WITH 'DASS': verb goes to the end of the dass-clause: Er sagte, dass er müde sei. "
            "WITHOUT 'DASS': verb stays in V2: Er sagte, er sei müde. (more common in journalism) "
            "REPORTING QUESTIONS: "
            "Yes/no: Er fragte, ob ich Zeit habe. (verb-end with 'ob') "
            "WH: Er fragte, wann ich komme. (verb-end with W-word) "
            "REPORTING IMPERATIVES: paraphrase with 'sollen' in K-I: 'Komm hierher!' → Er sagte, ich solle hierherkommen. "
            "Common B1 mistake: keeping indicative in formal indirect speech ('Er sagte, er ist krank' → 'sei krank'); "
            "not switching to K-II when K-I is identical to indicative; using 'das' instead of 'dass' for the subordinator."
        ),
    },
    {
        "slug": "temporale_nebensaetze",
        "name": "Temporale Nebensätze",
        "summary": "Temporal subordinate clauses — als, wenn, bevor, nachdem, während, sobald, seitdem, bis.",
        "content": (
            "Temporal Nebensätze express WHEN something happens. All take V-end word order (conjugated verb at the end of the clause). "
            "ALS — ONE-TIME event in the PAST. Als ich klein war, wohnten wir in Berlin. Als er kam, regnete es. "
            "WENN — REPEATED past event ('whenever'), OR present/future condition ('if/when'). "
            "Wenn ich Zeit habe, gehe ich spazieren. (whenever I have time) "
            "Immer wenn er kam, brachte er Blumen mit. (always whenever he came in the past) "
            "Wenn du morgen kommst, koche ich. (if/when tomorrow) "
            "Memory aid: ALS = one moment in the past; WENN = repeated or present/future. "
            "BEVOR — before. The bevor-clause is in Präsens or Präteritum (often same tense as main). "
            "Bevor ich gehe, schließe ich die Tür. Bevor er kam, putzte ich die Wohnung. "
            "NACHDEM — after. STRICT tense rule: nachdem-clause in Plusquamperfekt, main clause in Präteritum. "
            "Nachdem ich gegessen hatte, ging ich spazieren. "
            "WÄHREND — while / during. Während er kochte, deckte ich den Tisch. Während wir schliefen, regnete es. "
            "SOBALD — as soon as. Sobald er kommt, fangen wir an. Sobald ich Zeit habe, rufe ich dich an. "
            "SEITDEM (or SEIT) — since (a point in time). Seitdem ich hier wohne, geht es mir besser. Seit er kommt, ist die Arbeit einfacher. "
            "BIS — until. Ich warte, bis du kommst. Wir bleiben hier, bis das Wetter besser wird. "
            "WORD ORDER reminder: conjugated verb at the end of the Nebensatz; if the Nebensatz is FRONTED, the main clause "
            "starts with the verb in position 2 (after the comma): "
            "Wenn ich Zeit habe, gehe ich spazieren. (comma + V2: 'gehe') "
            "Common B1 mistake: confusing 'als' (one-time past) with 'wenn' (repeated/conditional); using 'wann' (only for questions) "
            "instead of 'wenn'; wrong tense after 'nachdem' (Perfekt instead of Plusquamperfekt); verb in V2 inside the Nebensatz."
        ),
    },
    {
        "slug": "finale_nebensaetze",
        "name": "Finale Nebensätze (damit / um ... zu)",
        "summary": "Purpose clauses — damit vs. um ... zu, governed by whether subjects are the same.",
        "content": (
            "Finale Nebensätze (final / purpose clauses) express the GOAL or REASON of an action — answering 'Wozu?' or 'Warum?'. "
            "There are two structures: 'damit' (full clause) and 'um ... zu' (infinitive construction). "
            "THE KEY RULE — subject identity decides which to use: "
            "If the subject of the main clause and the purpose clause are THE SAME → use 'um ... zu' (preferred, more elegant). "
            "If the subjects are DIFFERENT → must use 'damit'. "
            "UM ... ZU (same subject, infinitive construction): "
            "Ich gehe in die Stadt, um Brot zu kaufen. (I go ... to buy bread — I do both) "
            "Sie lernt Deutsch, um in Deutschland zu studieren. (she lernt and she studiert — same subject) "
            "Word order inside 'um ... zu': 'um' at start, all other elements next, 'zu + Infinitiv' at the end. "
            "Separable verbs: 'um anzurufen', 'um aufzustehen' — the 'zu' goes between the prefix and the stem. "
            "DAMIT (different subjects, full clause with V-end): "
            "Ich gebe dir Geld, damit du Brot kaufst. (I give YOU money so YOU buy bread — different subjects) "
            "Sie spricht laut, damit alle sie verstehen. (she speaks so they understand — different subjects) "
            "Damit-clause is a normal Nebensatz: conjugated verb at the END. "
            "ALTERNATIVE FOR SAME-SUBJECT (less common): you CAN use 'damit' even with same subjects, but 'um ... zu' is more natural. "
            "'um ... zu' is NOT allowed with different subjects. "
            "Wrong: Ich gebe dir Geld, um du Brot kaufst. (different subjects → must use 'damit') "
            "MODAL VERBS IN 'um ... zu' work normally — the 'zu' goes with the modal: "
            "Ich lerne, um den Test bestehen zu können. (in order to be able to pass) "
            "Common B1 mistake: using 'um ... zu' with different subjects; forgetting 'zu' ('um Brot kaufen'); "
            "placing 'zu' wrong with separable verbs ('um zu anrufen' instead of 'um anzurufen')."
        ),
    },
    {
        "slug": "konzessive_nebensaetze",
        "name": "Konzessive Nebensätze (obwohl / trotzdem)",
        "summary": "Concessive clauses — obwohl (subordinator, V-end) vs. trotzdem (adverb, V2 in main clause).",
        "content": (
            "Konzessive Nebensätze express CONCESSION — an unexpected contrast ('although', 'despite'). "
            "B1 requires careful distinction between the SUBORDINATING conjunction (V-end) and the ADVERB (V2). "
            "OBWOHL — subordinating conjunction, introduces a Nebensatz with V-END word order: "
            "Obwohl es regnet, gehe ich spazieren. (Although it's raining, ...) "
            "Ich gehe spazieren, obwohl es regnet. (..., although it's raining) "
            "Synonyms: 'obgleich', 'obschon' (more formal/literary). "
            "TROTZDEM — adverb (NOT a conjunction), goes in the MAIN clause and triggers V2 word order: "
            "Es regnet. Trotzdem gehe ich spazieren. (verb 'gehe' in position 2) "
            "Ich bin müde, trotzdem gehe ich aus. (after comma, V2) "
            "Common error: using 'trotzdem' like 'obwohl' with V-end ('trotzdem ich gehe aus' — wrong). "
            "TROTZ + GENITIV — preposition, takes a noun phrase, not a clause: "
            "Trotz des Regens gehe ich spazieren. (despite the rain) "
            "Trotz der Schwierigkeiten haben wir es geschafft. "
            "In spoken German you'll hear 'trotz dem Regen' (Dativ), but the standard B1 rule is Genitiv. "
            "OTHER CONCESSIVE LINKS: "
            "auch wenn — even if (concessive flavor, V-end like 'wenn'). Auch wenn es regnet, gehe ich raus. "
            "selbst wenn — even if (stronger concessive). Selbst wenn ich Zeit hätte, würde ich nicht kommen. "
            "zwar ... aber ... — admittedly ... but ... (both clauses are V2). Es ist zwar kalt, aber ich gehe trotzdem raus. "
            "Common B1 mistake: using 'trotzdem' as a subordinator with V-end; confusing 'trotz' (preposition + Genitiv) with 'trotzdem' (adverb); "
            "leaving V2 word order in 'obwohl'-clauses ('obwohl es regnet draußen' instead of 'obwohl es draußen regnet')."
        ),
    },
    {
        "slug": "konditional_irreal",
        "name": "Konditionalsätze (real / irreal)",
        "summary": "Conditional clauses — real (wenn/falls + Indikativ) vs. irreal (wenn + Konjunktiv II).",
        "content": (
            "Conditional clauses express IF-THEN logic. B1 distinguishes REAL (probable / open) from IRREAL (hypothetical / unreal). "
            "REALE BEDINGUNG — uses Präsens or Futur in BOTH clauses, with 'wenn' or 'falls': "
            "Wenn ich Zeit habe, komme ich. (probable — I might have time) "
            "Falls es regnet, bleiben wir zu Hause. (in case it rains) "
            "Wenn du müde bist, geh ins Bett. (imperative consequence) "
            "FALLS vs. WENN — both can introduce a real condition; nuance: "
            "'wenn' = neutral, often 'when' (more probable). "
            "'falls' = 'in case', emphasizes the conditional (less certain). "
            "Use 'falls' for written/formal style; use 'wenn' for everyday register. "
            "IRREALE BEDINGUNG — uses Konjunktiv II in BOTH clauses: "
            "Present/future irreal: Wenn ich Zeit hätte, würde ich kommen. (I don't have time, so I won't come) "
            "Past irreal: Wenn ich Zeit gehabt hätte, wäre ich gekommen. (I didn't have time, I didn't come) "
            "Inversion without 'wenn' (formal/literary): Hätte ich Zeit, käme ich. Wäre er hier, hätte er geholfen. "
            "MIXED CONDITIONALS — past condition with present result, or vice versa: "
            "Wenn ich besser gelernt hätte, wäre ich jetzt erfolgreich. (past condition, present result) "
            "Wenn du jetzt gehen würdest, könntest du den Bus noch erwischen. (present condition, future result) "
            "TENSE AGREEMENT in conditionals (CRITICAL): "
            "Real: Präsens + Präsens / Präsens + Futur. NEVER mix indicative with K-II. "
            "Irreal present: K-II + K-II (use 'würde + Inf' for most full verbs; 'hätte'/'wäre' for sein/haben/modal). "
            "Irreal past: Plusquamperfekt K-II + Plusquamperfekt K-II ('hätte/wäre' + Partizip II in both clauses). "
            "Common B1 mistake: mixing indicative and K-II ('Wenn ich Zeit hatte, würde ich kommen' — must be 'hätte'); "
            "using 'würde + Inf' in the 'wenn'-clause where 'hätte/wäre' is correct ('Wenn ich Zeit würde haben' — wrong); "
            "wrong word order in the inversion-form ('Hätte Zeit ich' instead of 'Hätte ich Zeit')."
        ),
    },
    {
        "slug": "relativsaetze_erweitert",
        "name": "Relativsätze (erweitert)",
        "summary": "Advanced relative clauses — with prepositions, was, wo, and indefinite antecedents.",
        "content": (
            "B1 extends Relativsätze beyond the basic forms (learned in A2). The new patterns are: relative pronouns "
            "AFTER prepositions, 'was' for indefinite antecedents, and 'wo' for places. "
            "RELATIVPRONOMEN — review: der/die/das + plural die, declined for case based on its role IN the relative clause: "
            "Nom: der/die/das/die  Akk: den/die/das/die  Dat: dem/der/dem/denen  Gen: dessen/deren/dessen/deren. "
            "PREPOSITION + RELATIVPRONOMEN — when the verb in the relative clause governs a preposition, the preposition "
            "comes FIRST, followed by the declined relative pronoun: "
            "Das Buch, von dem ich gesprochen habe, ist neu. (sprechen von + Dat) "
            "Die Frau, mit der ich arbeite, ist nett. (arbeiten mit + Dat) "
            "Das Thema, über das wir diskutieren, ist wichtig. (diskutieren über + Akk) "
            "Der Stift, mit dem ich schreibe, ist kaputt. (schreiben mit + Dat) "
            "WAS — relative pronoun for: "
            "(1) Indefinite antecedents: alles, etwas, nichts, vieles, das (the demonstrative). "
            "Alles, was ich gesagt habe, war wahr. Etwas, was mich freut. Nichts, was du tun kannst. "
            "(2) A whole preceding clause as antecedent: "
            "Er kam zu spät, was mich geärgert hat. (the whole event annoyed me) "
            "(3) Substantivierte Adjektive: das Beste, was ... ; das Schönste, was ... "
            "Das Beste, was uns passieren kann, ist Ruhe. "
            "WO — relative for PLACE antecedents (preferred over 'in dem' in everyday German): "
            "Die Stadt, wo ich aufgewachsen bin, ist klein. (= in der ich aufgewachsen bin) "
            "Das Hotel, wo wir gewohnt haben. (= in dem wir gewohnt haben) "
            "GENITIV-RELATIVPRONOMEN — dessen / deren — connects possession across clauses: "
            "Der Mann, dessen Auto rot ist, wohnt nebenan. (the man whose car is red) "
            "Die Frau, deren Sohn studiert, ist Lehrerin. (whose son studies) "
            "Note: dessen for masculine/neuter antecedents; deren for feminine and plural antecedents. "
            "DA-/WO-COMPOUNDS as ALTERNATIVE to preposition + pronoun (for things, not people): "
            "If the antecedent is a thing, you can sometimes use 'wo' + preposition: 'worüber', 'womit' — but these are less common "
            "in relative clauses than 'preposition + Relativpronomen'. They appear more in indirect questions. "
            "Common B1 mistake: wrong gender on the relative pronoun ('die Frau, der ich helfe' — should be 'der' is Dativ feminine ... "
            "wait: 'der' IS feminine Dativ here. The common mistake is 'die Frau, die ich helfe' — must be 'der' because 'helfen' takes Dativ); "
            "using 'was' after a concrete noun ('das Buch, was ich lese' — must be 'das'); using 'wo' for non-locations."
        ),
    },
    {
        "slug": "adjektivdeklination_komplett",
        "name": "Adjektivdeklination (komplett)",
        "summary": "Full adjective declension — strong / weak / mixed across all four cases and three article types.",
        "content": (
            "Adjektivdeklination depends on the article preceding the adjective. Three declension types: "
            "STRONG (no article), WEAK (after definite article der/die/das), MIXED (after indefinite article ein/eine, "
            "kein, mein/dein/sein/ihr/unser/euer/Ihr). "
            "WEAK (after der/die/das/die-plural): only TWO endings — '-e' or '-en'. "
            "  Nom Sg: der gute Mann / die gute Frau / das gute Kind  →  ending '-e' "
            "  Akk Sg: den guten Mann / die gute Frau / das gute Kind  →  masc '-en', fem/neut '-e' "
            "  Dat Sg: dem guten Mann / der guten Frau / dem guten Kind  →  all '-en' "
            "  Gen Sg: des guten Mannes / der guten Frau / des guten Kindes  →  all '-en' "
            "  Plural ALL cases: die guten Männer / den guten Männern / der guten Männer  →  all '-en' "
            "Mnemonic: 'der/die/das + -e in Nom Sg and Fem/Neut Akk Sg; otherwise -en'. "
            "MIXED (after ein/eine, kein, possessive): "
            "  Nom Sg: ein guter Mann / eine gute Frau / ein gutes Kind  →  masc '-er', fem '-e', neut '-es' "
            "  Akk Sg: einen guten Mann / eine gute Frau / ein gutes Kind  →  masc '-en', fem '-e', neut '-es' "
            "  Dat Sg: einem guten Mann / einer guten Frau / einem guten Kind  →  all '-en' "
            "  Gen Sg: eines guten Mannes / einer guten Frau / eines guten Kindes  →  all '-en' "
            "  Plural ALL cases (kein-/possessive only — ein has no plural): keine guten Männer  →  all '-en' "
            "Key insight: in mixed, when the article ITSELF lacks a clear case-marker (Nom Sg masc 'ein', Nom/Akk Sg neut 'ein'), "
            "the adjective takes the STRONG ending. Otherwise weak '-en'. "
            "STRONG (NO article): the adjective ITSELF carries the case-marker, copying the article ending: "
            "  Nom Sg: guter Wein / gute Milch / gutes Bier  →  masc '-er', fem '-e', neut '-es' "
            "  Akk Sg: guten Wein / gute Milch / gutes Bier  →  masc '-en', fem '-e', neut '-es' "
            "  Dat Sg: gutem Wein / guter Milch / gutem Bier  →  masc '-em', fem '-er', neut '-em' "
            "  Gen Sg: guten Weines / guter Milch / guten Bieres  →  masc/neut '-en' (because noun already has -es); fem '-er' "
            "  Plural ALL cases: gute Männer / guten Männern / guter Männer  →  strong endings (the only -en is dative plural) "
            "Common B1 mistake: strong endings after 'ein-'-words ('ein großes Mann' instead of 'ein großer Mann'); weak '-e' everywhere "
            "in non-Nom-Sg slots ('mit dem große Mann' instead of 'mit dem großen Mann'); forgetting that without an article the "
            "adjective takes strong endings ('gutes Essen' as accusative neuter — but it's 'gutes Essen' in Akk Sg neut too)."
        ),
    },
    {
        "slug": "n_deklination",
        "name": "N-Deklination",
        "summary": "Weak masculine nouns — take -(e)n in all cases except Nominativ Singular.",
        "content": (
            "A small group of masculine nouns — 'schwache Maskulina' — take the ending '-(e)n' in ALL CASES EXCEPT the "
            "Nominativ Singular. This is the N-Deklination. "
            "EXAMPLES of weak masculine nouns: "
            "der Student / den Studenten / dem Studenten / des Studenten — plural: die Studenten "
            "der Junge / den Jungen / dem Jungen / des Jungen — plural: die Jungen "
            "der Herr / den Herrn / dem Herrn / des Herrn — plural: die Herren (note: ALL forms get -n!) "
            "der Mensch / den Menschen / dem Menschen / des Menschen — plural: die Menschen "
            "der Name / den Namen / dem Namen / des Namens (irregular: gets -ns in Gen Sg!) "
            "der Held / den Helden / dem Helden / des Helden "
            "der Junge / der Kollege / der Kunde / der Nachbar / der Mensch / der Pilot / der Soldat — all N-deklination. "
            "WHICH NOUNS BELONG? Patterns: "
            "- Nouns ending in '-e' that refer to male persons or animals: der Junge, der Kollege, der Kunde, der Löwe. "
            "- Nationality/profession words from Greek/Latin: Student, Polizist, Pilot, Demokrat, Pädagoge, Praktikant. "
            "- A small group of irregular monosyllables: Mensch, Herr, Held, Bauer, Nachbar, Christ. "
            "- Some animals: der Bär, der Hase, der Affe, der Drache. "
            "SPECIAL CASES: "
            "- der Herr: takes '-n' in singular (den Herrn, dem Herrn, des Herrn), '-en' in plural (die Herren). "
            "- der Name / Glaube / Wille / Gedanke / Friede / Buchstabe — irregular: Gen Sg adds '-ns' (des Namens, des Willens). "
            "EXAMPLES IN SENTENCES: "
            "Ich kenne den Studenten. (NOT 'den Student') "
            "Ich helfe dem Jungen. (NOT 'dem Junge') "
            "Das Buch des Herrn liegt hier. (NOT 'des Herr') "
            "Wir laden den Kollegen ein. "
            "Common B1 mistake: forgetting the -en ending in Akk/Dat/Gen ('Ich sehe den Student'); applying N-Deklination to "
            "non-weak masculines ('Ich kenne den Mannen' — wrong, 'Mann' is not N-Dekl); misspelling 'Namen' in Genitiv "
            "(must be 'des Namens')."
        ),
    },
    {
        "slug": "verben_praep_da_wo_komposita",
        "name": "Verben + Präposition / da- / wo- Komposita",
        "summary": "Verbs with fixed prepositions and the da-/wo-compounds that replace 'preposition + es/das'.",
        "content": (
            "Many German verbs are LEXICALLY BOUND to a specific preposition. The preposition is part of the verb's meaning — "
            "you have to learn the pair. The preposition then governs the case of the following noun phrase. "
            "COMMON B1 VERB+PREPOSITION PAIRS (case in brackets): "
            "sich freuen auf [Akk] (look forward to) — Ich freue mich auf das Wochenende. "
            "sich freuen über [Akk] (be happy about) — Ich freue mich über das Geschenk. "
            "warten auf [Akk] — Ich warte auf den Bus. "
            "denken an [Akk] — Ich denke an meine Familie. "
            "sich erinnern an [Akk] — Ich erinnere mich an den Urlaub. "
            "sich kümmern um [Akk] — Sie kümmert sich um die Kinder. "
            "sich interessieren für [Akk] — Ich interessiere mich für Musik. "
            "sich bewerben um [Akk] — Er bewirbt sich um eine Stelle. "
            "achten auf [Akk] — Achten Sie auf die Schilder. "
            "verzichten auf [Akk] — Ich verzichte auf Zucker. "
            "bitten um [Akk] — Ich bitte um Hilfe. "
            "sich beschäftigen mit [Dat] — Sie beschäftigt sich mit Sprachen. "
            "sich befassen mit [Dat] — Wir befassen uns mit dem Problem. "
            "sprechen über [Akk] / von [Dat] — Wir sprechen über Politik / Wir sprechen von ihm. "
            "sich verlieben in [Akk] — Sie verliebt sich in ihn. "
            "abhängen von [Dat] — Das hängt von dir ab. "
            "leiden unter [Dat] — Er leidet unter Stress. "
            "profitieren von [Dat] — Wir profitieren von der Erfahrung. "
            "DA-KOMPOSITA — when the prepositional object is a THING (not a person), and you want to refer back to it pronoun-like, "
            "use 'da-' + preposition: "
            "daran, darauf, darüber, dafür, damit, davon, dazu, danach, dadurch, darum, darunter, dahinter, davor, daneben, dazwischen. "
            "Eine 'r' is inserted between 'da' and a vowel-initial preposition: dar-an, dar-auf, dar-über, dar-unter, dar-in. "
            "Example: 'Hast du an den Termin gedacht?' — 'Ja, ich habe DARAN gedacht.' (not 'an ihn') "
            "Example: 'Ich freue mich auf das Wochenende. Ich freue mich SEHR DARAUF.' "
            "WO-KOMPOSITA — for QUESTIONS about a thing's prepositional role: "
            "Worauf wartest du? (What are you waiting for?) — Auf den Bus. "
            "Worüber sprecht ihr? Wovon träumst du? Womit beschäftigst du dich? "
            "PEOPLE vs. THINGS — critical: da-/wo-compounds only work for THINGS. For people, use preposition + pronoun. "
            "'Mit wem arbeitest du?' (with whom) — NOT 'womit'. "
            "'Ich denke an ihn.' (at him) — NOT 'daran' if 'ihn' = a person. "
            "Common B1 mistake: using 'auf es' / 'an es' instead of 'darauf' / 'daran' for things; using 'womit' / 'worüber' for people "
            "instead of 'mit wem' / 'über wen'; choosing the wrong preposition for a verb (English interference: 'warten für' instead of 'warten auf')."
        ),
    },
    {
        "slug": "genitiv_komplett",
        "name": "Genitiv (komplett)",
        "summary": "Full Genitive — possession, genitive prepositions, attributive use, and idiomatic phrases.",
        "content": (
            "B1 extends Genitiv beyond the basics (learned in A2) to all major uses. "
            "ARTICLES IN GENITIV: "
            "  Masculine: des  Feminine: der  Neuter: des  Plural: der "
            "  Indefinite: eines / einer / eines (no plural for 'ein') "
            "  Possessive: meines / meiner / meines / meiner (plural) "
            "NOUN ENDINGS: masculine and neuter singular nouns add '-s' or '-es' in Genitiv: "
            "des Mannes, des Kindes, des Vaters, des Lehrers, des Autos. "
            "Feminine and plural nouns DO NOT take an ending in Genitiv: der Frau, der Frauen. "
            "ATTRIBUTIVE GENITIV (possession): "
            "das Auto meines Vaters / die Tasche meiner Mutter / das Spielzeug des Kindes / die Häuser der Nachbarn. "
            "Note: the genitive phrase typically FOLLOWS the noun it modifies (das Auto meines Vaters), unlike English "
            "(my father's car). "
            "GENITIV-PRÄPOSITIONEN (always Genitiv in standard / written German; spoken German often uses Dativ): "
            "wegen, trotz, während, statt/anstatt, innerhalb, außerhalb, oberhalb, unterhalb, aufgrund, mithilfe, anstelle. "
            "Examples: "
            "Wegen des schlechten Wetters bleiben wir zu Hause. "
            "Trotz der Schwierigkeiten haben wir es geschafft. "
            "Während des Urlaubs habe ich viel gelesen. "
            "Statt eines Kuchens habe ich Kekse gebacken. "
            "Innerhalb einer Woche müssen wir antworten. "
            "Aufgrund der hohen Preise verzichten viele Kunden. "
            "GENITIV WITH PROPER NAMES — names add '-s' (no apostrophe in German!): Annas Auto, Peters Buch, Goethes Werke. "
            "GENITIV WITH SUPERLATIVE — 'der größte / schönste / wichtigste ___ aller ___': "
            "Berlin ist eine der größten Städte Deutschlands. (one of the largest) "
            "Er ist der beste Schüler der Klasse. "
            "DATIV-ERSATZ (Dative replacement) — in spoken German, von + Dat replaces Genitiv: "
            "Das Auto von meinem Vater (spoken) = das Auto meines Vaters (written). "
            "B1 exam expects the GENITIV form in writing. "
            "Common B1 mistake: missing '-s' on masculine/neuter nouns ('das Auto meines Vater' instead of 'meines Vaters'); "
            "using Dativ after Genitiv-prepositions in formal contexts ('wegen dem Wetter' instead of 'wegen des Wetters'); "
            "adding '-s' to feminine nouns ('die Hand der Fraus' — wrong, feminine nouns take no ending)."
        ),
    },
    {
        "slug": "partizipien_als_adjektive",
        "name": "Partizipien als Adjektive",
        "summary": "Participle I (active/ongoing) and Participle II (passive/completed) used as adjectives.",
        "content": (
            "Both Partizip I and Partizip II can be used as ADJECTIVES in front of nouns. They differ in meaning and are "
            "declined like normal adjectives (strong / weak / mixed depending on the article). "
            "PARTIZIP I — active / ongoing meaning. Formed by adding '-end' to the verb stem (= English '-ing'): "
            "  laufen → laufend (running) "
            "  schlafen → schlafend (sleeping) "
            "  lesen → lesend (reading) "
            "  fließen → fließend (flowing) "
            "Examples: "
            "das schlafende Kind (the sleeping child — the child IS sleeping) "
            "die spielenden Hunde (the playing dogs) "
            "ein lachender Mann (a laughing man) "
            "fließendes Wasser (running/flowing water) "
            "PARTIZIP II — passive / completed meaning. Same form as the past participle used in Perfekt: "
            "  reparieren → repariert (repaired) "
            "  öffnen → geöffnet (opened) "
            "  schreiben → geschrieben (written) "
            "  beleidigen → beleidigt (insulted) "
            "Examples: "
            "das reparierte Auto (the repaired car — someone repaired it; it's done) "
            "die geöffnete Tür (the opened door) "
            "ein geschriebener Brief (a written letter) "
            "das gekochte Ei (the cooked egg) "
            "MEANING CONTRAST: "
            "der lesende Student = the student who is reading (active, ongoing). "
            "das gelesene Buch = the book that has been read (passive, completed). "
            "der singende Vogel = the singing bird (it's singing now). "
            "das gesungene Lied = the sung song (it has been sung). "
            "DECLENSION — just like regular adjectives, the participle takes endings agreeing with the noun's gender/case/article: "
            "Nom Sg masc, weak: der lesende Student / der reparierte Wagen "
            "Akk Sg masc, weak: den lesenden Studenten / den reparierten Wagen "
            "Dat Sg masc, weak: dem lesenden Studenten / dem reparierten Wagen "
            "Mixed (ein-words): ein lesender Student / ein reparierter Wagen "
            "Strong (no article): lesende Studenten / reparierte Wagen "
            "Common B1 mistake: forgetting the adjective ending on the participle ('das schlafend Kind' instead of 'das schlafende Kind'); "
            "confusing Partizip I (active/ongoing) with Partizip II (passive/completed) — using 'lesend' where 'gelesen' is meant or vice versa; "
            "trying to extend the participial phrase with adverbs to form a full B2-style extended attribute (not expected at B1)."
        ),
    },
    {
        "slug": "modalverben_subjektiv",
        "name": "Modalverben (subjektiv)",
        "summary": "Subjective use of modal verbs — epistemic meanings (inference, hearsay, possibility).",
        "content": (
            "Modal verbs at A1/A2 have OBJECTIVE meanings (ability, necessity, permission, desire). B1 introduces the "
            "SUBJECTIVE / EPISTEMIC use, where the speaker is making a JUDGEMENT about how certain or likely a statement is. "
            "MÜSSEN — high-certainty inference ('must be the case', 'I'm sure'): "
            "Er muss krank sein. (He must be sick — based on the evidence, I'm convinced.) "
            "Sie müssen sehr glücklich sein. (You must be very happy.) "
            "Past: Er muss krank gewesen sein. (He must have been sick.) [Modal + Perfekt-Inf at end] "
            "KÖNNEN — possibility ('it's possible', 'it could be'): "
            "Das kann sein. (That could be / that's possible.) "
            "Er kann auch krank sein. (He could be sick too.) "
            "Past: Er kann krank gewesen sein. (He could have been sick.) "
            "DÜRFEN (Konjunktiv II 'dürfte') — moderate inference ('I'd say', 'is probably'): "
            "Er dürfte schon zu Hause sein. (He's probably already home.) "
            "Das dürfte etwa 50 Euro kosten. (That would probably cost about 50 euros.) "
            "Note: this use almost ALWAYS appears in Konjunktiv II form 'dürfte', rarely in 'darf'. "
            "MÖGEN (Konjunktiv II 'möchte' for desire, but 'mag/mögen' for possibility): "
            "'mögen' for hesitant possibility, often with 'sein': "
            "Das mag sein. (That may be / perhaps.) "
            "Es mögen 50 Leute gewesen sein. (Maybe 50 people were there.) "
            "Note: this is a slightly more literary register. "
            "SOLLEN — HEARSAY ('it is said', 'apparently', reporting what others claim): "
            "Er soll sehr reich sein. (He's said to be very rich.) "
            "Das Hotel soll teuer sein. (The hotel is supposed to be expensive.) "
            "Past: Er soll krank gewesen sein. (He's supposed to have been sick.) "
            "WOLLEN — CLAIM ('claims to', the subject themselves asserts): "
            "Er will Arzt sein. (He claims to be a doctor — but maybe he isn't.) "
            "Sie will den Film gesehen haben. (She claims to have seen the film.) "
            "Past: Er will krank gewesen sein. (He claims to have been sick.) "
            "WORD ORDER for past subjective modals: 'Modal' + Infinitive + 'sein' or 'haben' as final infinitive — "
            "essentially 'Modal + Perfekt-Infinitiv': "
            "Er muss krank gewesen sein. (modal 'muss', then 'krank gewesen sein' = perfect infinitive of 'krank sein') "
            "Sie soll viel gearbeitet haben. (modal 'soll' + 'viel gearbeitet haben') "
            "Common B1 mistake: confusing 'müssen' (certainty / I infer) with 'sollen' (hearsay / others say); "
            "using objective past instead of modal + Perfekt-Inf ('Er musste krank sein' — past objective need; vs. "
            "'Er muss krank gewesen sein' — present subjective inference about a past state); using 'können' "
            "where 'dürfte' is more natural for moderate inference."
        ),
    },
    {
        "slug": "futur",
        "name": "Futur I & II",
        "summary": "Future tenses — Futur I for plans/predictions, Futur II for completed-in-future, both common for Vermutung.",
        "content": (
            "German uses Präsens + time adverb for most future references (Morgen komme ich). Futur I and II appear when "
            "the speaker wants to emphasize PREDICTION, PROMISE, or VERMUTUNG (assumption / probability). "
            "FUTUR I — 'werden' (conjugated) + Infinitiv at end: "
            "Ich werde morgen kommen. (I will come tomorrow.) "
            "Sie werden gewinnen. (They will win.) "
            "Wir werden uns sehen. (We will see each other.) "
            "USES of Futur I: "
            "(1) Prediction or strong intention: Ich werde Deutsch lernen. (I will learn German — firm plan.) "
            "(2) Promise: Ich werde dich anrufen. (I will call you.) "
            "(3) VERMUTUNG (assumption / probability — very common at B1!): "
            "Er wird wohl krank sein. (He's probably sick — supposition about NOW.) "
            "Sie wird gerade arbeiten. (She's probably working right now.) "
            "Das wird teuer sein. (That'll probably be expensive.) "
            "The word 'wohl' often accompanies Futur I as assumption — 'wohl' here means 'probably', not 'well'. "
            "FUTUR II — 'werden' + Partizip II + 'haben'/'sein' (Infinitiv) at end: "
            "Ich werde das gemacht haben. (I will have done that.) "
            "Wir werden angekommen sein. (We will have arrived.) "
            "USES of Futur II: "
            "(1) Action completed by a future point in time: "
            "Bis morgen werde ich den Brief geschrieben haben. (By tomorrow, I will have written the letter.) "
            "(2) VERMUTUNG about a PAST event (very common at B1): "
            "Er wird krank gewesen sein. (He probably was sick.) "
            "Sie wird das gewusst haben. (She probably knew that.) "
            "Das Paket wird angekommen sein. (The package has probably arrived.) "
            "WORD ORDER reminder: "
            "Main clause Futur I: 'werden' V2, Infinitiv at end. (Ich werde morgen kommen.) "
            "Main clause Futur II: 'werden' V2, then Partizip II + 'haben/sein' (Inf) at end. (Ich werde das gemacht haben.) "
            "Subordinate clause: 'werden' goes to the very end after the infinitive(s). "
            "(..., weil ich morgen kommen werde. / ..., weil ich das gemacht haben werde.) "
            "Common B1 mistake: using Futur I for ordinary near-future when Präsens + time adverb is more idiomatic "
            "('Ich werde morgen kommen' is fine but heavier than 'Ich komme morgen'); confusing Futur II formation "
            "(forgetting 'haben'/'sein' at the end); not recognizing 'wird wohl' as a Vermutung pattern."
        ),
    },
    {
        "slug": "konnektoren_adverbien",
        "name": "Konjunktionaladverbien (deshalb / trotzdem / sonst / dennoch)",
        "summary": "Adverbial connectors — trigger V2 word order in the main clause, distinct from subordinators.",
        "content": (
            "Konjunktionaladverbien (conjunctional adverbs / sentence connectors) are ADVERBS, NOT conjunctions. They link "
            "sentences logically but follow MAIN-CLAUSE V2 word order, with the verb in position 2. This is the key "
            "contrast with subordinators like 'weil' / 'obwohl' / 'damit', which require verb-end. "
            "MAIN CONNECTORS at B1: "
            "DESHALB / DAHER / DARUM / DESWEGEN — 'therefore' / 'that's why' (causal consequence): "
            "Es hat geregnet. Deshalb bin ich nass. "
            "Ich bin müde, deshalb gehe ich ins Bett. (verb 'gehe' in V2 after the connector) "
            "TROTZDEM / DENNOCH / ALLERDINGS — 'nevertheless' / 'however' (concessive): "
            "Es regnet. Trotzdem gehe ich spazieren. "
            "Er hat viel gelernt, dennoch hat er die Prüfung nicht bestanden. "
            "Note: 'allerdings' is slightly weaker, often = 'however' / 'though'. "
            "SONST — 'otherwise' / 'or else' (conditional consequence): "
            "Beeil dich, sonst kommst du zu spät. (Hurry up, or you'll be late.) "
            "Ich muss heute lernen, sonst werde ich morgen Probleme haben. "
            "AUßERDEM / ZUDEM / DARÜBER HINAUS — 'in addition' / 'moreover' (additive): "
            "Das Auto ist alt. Außerdem ist es teuer. "
            "Sie spricht Deutsch und Französisch. Zudem lernt sie Spanisch. "
            "STATTDESSEN — 'instead' (alternative): "
            "Ich gehe nicht ins Kino. Stattdessen bleibe ich zu Hause. "
            "ZUERST ... DANN ... SCHLIEßLICH — 'first ... then ... finally' (sequence): "
            "Zuerst kochen wir. Dann essen wir. Schließlich räumen wir auf. "
            "WORD ORDER (CRITICAL): "
            "Connector in position 1 → VERB in position 2 → SUBJECT in position 3. "
            "Wrong: 'Trotzdem ich gehe aus.' "
            "Right: 'Trotzdem gehe ich aus.' "
            "Connector AFTER a subject also works, but is less common: 'Ich gehe trotzdem aus.' "
            "CONTRAST WITH SUBORDINATORS — same meaning, different syntax: "
            "  'Es regnet. Trotzdem gehe ich aus.' (adverb, V2) "
            "  'Obwohl es regnet, gehe ich aus.' (subordinator, V-end in obwohl-clause) "
            "  'Es hat geregnet, deshalb bin ich nass.' (adverb, V2) "
            "  'Ich bin nass, weil es geregnet hat.' (subordinator, V-end in weil-clause) "
            "Common B1 mistake: using a Konjunktionaladverb with V-end word order ('Trotzdem ich gehe aus' — wrong); "
            "confusing the adverb with its subordinator equivalent (deshalb vs. weil; trotzdem vs. obwohl); failing to "
            "invert subject and verb after the connector ('Trotzdem ich gehe' instead of 'Trotzdem gehe ich')."
        ),
    },
]


def get_chapter_by_slug(slug: str):
    return next((c for c in DEUTSCH_B1_CHAPTERS if c["slug"] == slug), None)


def get_chapter_by_name(name: str):
    return next((c for c in DEUTSCH_B1_CHAPTERS if c["name"] == name), None)


def build_corpus_text(focus_chapter_slugs: list[str] | None = None) -> str:
    """Concatenate chapter contents, optionally filtered to a subset."""
    chapters = DEUTSCH_B1_CHAPTERS
    if focus_chapter_slugs:
        focus_set = set(focus_chapter_slugs)
        filtered = [c for c in DEUTSCH_B1_CHAPTERS if c["slug"] in focus_set]
        if filtered:
            chapters = filtered
    parts = []
    for ch in chapters:
        parts.append(f"--- Chapter: {ch['name']} ---\n{ch['content']}")
    return "\n\n".join(parts)
