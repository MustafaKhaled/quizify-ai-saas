"""
Static chapter knowledge base for the PMP agent.

Each chapter's `name` doubles as the quiz `topic` field so weak-topic
aggregation in QuizResult.user_answers maps 1:1 to chapters here.

Slug naming mirrors the seed exam bank (seed/exam_bank.json) so ingest can
resolve chapter_slug → chapter without a translation table.

NOTE: `content` for project_framework, ethics_professional_conduct, and the
PMBOK knowledge areas is a stable summary intended for grounding. Replace or
expand with richer PMBOK-aligned material when available.
"""

PMP_CHAPTERS = [
    {
        "slug": "project_framework",
        "name": "Project Framework",
        "summary": "Project vs. operations, lifecycle, process groups, organizational structures, and the triple constraint.",
        "content": (
            "Project Management fundamentals distinguish projects from operations. "
            "A project is temporary (has a defined start and end) and unique (creates a one-of-a-kind deliverable). "
            "Operations are ongoing and repetitive. "
            "PMBOK defines 5 process groups (Initiating, Planning, Executing, Monitoring & Controlling, Closing) "
            "and 10 knowledge areas (Integration, Scope, Schedule, Cost, Quality, Resource, Communications, Risk, Procurement, Stakeholder). "
            "Organizational structures influence PM authority: Functional (weak PM), Matrix (weak/balanced/strong — shared authority), "
            "and Projectized (strong PM). "
            "The project charter formally authorizes the project and grants the PM authority to apply resources. "
            "A project management plan integrates subsidiary plans across all knowledge areas. "
            "Progressive elaboration refines plans iteratively as information becomes available. "
            "The classic triple constraint is scope, time, and cost; the modern view adds quality, resources, and risk. "
            "Stakeholders are individuals or organizations actively involved in or affected by the project."
        ),
    },
    {
        "slug": "project_integration",
        "name": "Integration Management",
        "summary": "Coordinating all project elements: charter, plan, execution, change control, and closure.",
        "content": (
            "Project Integration Management coordinates the processes and activities across all knowledge areas. "
            "Key processes include: Develop Project Charter (formally authorize the project), "
            "Develop Project Management Plan (define how the project is executed and controlled), "
            "Direct and Manage Project Work (perform the work defined in the plan), "
            "Manage Project Knowledge (use existing and create new knowledge), "
            "Monitor and Control Project Work (track progress against the plan), "
            "Perform Integrated Change Control (review and approve change requests), "
            "and Close Project or Phase (finalize all activities). "
            "The project charter authorizes the project manager and provides high-level requirements. "
            "The charter is issued by a sponsor or manager external to the project at a level appropriate to its needs. "
            "Change requests must go through integrated change control before implementation. "
            "A Change Control System is the formal set of procedures (paperwork, tracking, approvals) that governs how changes are evaluated and authorized. "
            "Configuration Management focuses on the deliverables themselves — what they are and what version is current."
        ),
    },
    {
        "slug": "scope_management",
        "name": "Scope Management",
        "summary": "Defining and controlling what is and isn't included in the project.",
        "content": (
            "Project Scope Management ensures the project includes all the work required, and only the work required. "
            "Processes: Plan Scope Management, Collect Requirements, Define Scope, Create WBS (Work Breakdown Structure), "
            "Validate Scope (formal acceptance of deliverables by the customer), and Control Scope (managing changes to the scope baseline). "
            "The WBS decomposes deliverables into work packages — the lowest level. "
            "The scope baseline consists of the scope statement, WBS, and WBS dictionary. "
            "Scope creep is uncontrolled expansion; gold plating is adding extras the customer didn't ask for — both are bad. "
            "Validate Scope is formal customer acceptance of deliverables; Control Quality is verifying deliverables meet requirements before customer review."
        ),
    },
    {
        "slug": "schedule_management",
        "name": "Schedule Management",
        "summary": "Planning, sequencing, and controlling project timelines.",
        "content": (
            "Project Schedule Management includes the processes required to manage timely completion. "
            "Processes: Plan Schedule Management, Define Activities, Sequence Activities, "
            "Estimate Activity Durations, Develop Schedule, and Control Schedule. "
            "Activity Attributes — responsibility (who will perform the work), activity type (summary vs detailed), geographic area, and WBS classification — support further sorting and selection of planned activities. "
            "The Critical Path Method (CPM) finds the longest path through the network — it determines the shortest possible duration. "
            "Float (slack) is the amount of time an activity can be delayed without delaying the project. "
            "Critical path activities have zero float. "
            "Schedule compression techniques: crashing (adding resources, increases cost) and fast tracking (parallel activities, increases risk). "
            "PERT / three-point estimation: tE = (O + 4M + P) / 6; activity std dev = (P − O) / 6."
        ),
    },
    {
        "slug": "cost_management",
        "name": "Cost Management",
        "summary": "Estimating, budgeting, and controlling project costs.",
        "content": (
            "Project Cost Management includes processes for planning, estimating, budgeting, financing, and controlling costs. "
            "Processes: Plan Cost Management, Estimate Costs, Determine Budget, and Control Costs. "
            "Tools for Estimate Costs include Analogous Estimating (top-down, historical), Parametric Modeling (statistical relationship), Bottom-up Estimating, Three-point Estimating, and Computerized tools. "
            "Alternatives Identification belongs to scope / resource planning, not Estimate Costs. "
            "Earned Value Management (EVM) integrates scope, schedule, and cost. Key formulas: "
            "CV = EV - AC (Cost Variance), SV = EV - PV (Schedule Variance), "
            "CPI = EV / AC (Cost Performance Index), SPI = EV / PV (Schedule Performance Index). "
            "CPI/SPI < 1 means under-performing. "
            "EAC (Estimate at Completion) = BAC / CPI when variance is typical; "
            "ETC (Estimate to Complete) = EAC - AC; VAC (Variance at Completion) = BAC - EAC. "
            "Make-or-buy analyses compare total cost of in-house development (labor × time + overhead) vs. external purchase (price + integration)."
        ),
    },
    {
        "slug": "quality_management",
        "name": "Quality Management",
        "summary": "Ensuring deliverables meet requirements and stakeholder expectations.",
        "content": (
            "Project Quality Management includes processes to incorporate the organization's quality policy. "
            "Processes: Plan Quality Management, Manage Quality (audits and improvement), and Control Quality (measure and verify). "
            "Quality is conformance to requirements and fitness for use. "
            "Cost of Quality (COQ) splits into cost of conformance (prevention, appraisal) and cost of nonconformance (internal/external failures). "
            "Tools include cause-and-effect (Ishikawa/fishbone) diagrams, Pareto charts (80/20 rule), control charts, histograms, and Design of Experiments (DOE). "
            "In DOE, variables are properties being measured (e.g. weight); measures are the units used to express them (e.g. kilograms, pounds, dollars). "
            "Any decrease in quality level should be documented and discussed with the contractor — not silently accepted nor rejected without analysis. "
            "Prevention is preferred over inspection."
        ),
    },
    {
        "slug": "resource_management",
        "name": "Resource Management",
        "summary": "Identifying, acquiring, and managing the project team and physical resources.",
        "content": (
            "Project Resource Management identifies, acquires, and manages the resources needed for project completion. "
            "Processes: Plan Resource Management, Estimate Activity Resources, Acquire Resources, "
            "Develop Team, Manage Team, and Control Resources. "
            "Tools for Plan Human Resource Management include Organization Charts and Position Descriptions (matrix/hierarchical/text), Networking, and Organizational Theory. "
            "Recognition and Rewards is a tool of Develop Project Team (during execution), not Plan Human Resource Management. "
            "Tuckman's stages of team development: Forming, Storming, Norming, Performing, Adjourning. "
            "Conflict resolution techniques include collaborate/problem-solve (best), compromise, smooth/accommodate, force/direct, and withdraw/avoid (worst). "
            "Maslow's hierarchy and Herzberg's two-factor theory inform motivation. "
            "RACI charts (Responsible, Accountable, Consulted, Informed) clarify roles."
        ),
    },
    {
        "slug": "communications_management",
        "name": "Communications Management",
        "summary": "Planning, executing, and monitoring information exchange with stakeholders.",
        "content": (
            "Project Communications Management ensures timely and appropriate generation, collection, distribution, "
            "storage, retrieval, and ultimate disposition of project information. "
            "Processes: Plan Communications Management, Manage Communications, and Monitor Communications. "
            "Number of communication channels = n(n-1)/2 where n is the number of stakeholders. "
            "Communication methods: interactive (most effective, e.g. meetings), push (e.g. emails), pull (e.g. intranets). "
            "55% of communication is body language, 38% tone, 7% words. "
            "Project managers spend 90% of their time communicating."
        ),
    },
    {
        "slug": "risk_management",
        "name": "Risk Management",
        "summary": "Identifying, analyzing, and responding to project risks.",
        "content": (
            "Project Risk Management increases the likelihood and impact of positive events and decreases negative ones. "
            "Processes: Plan Risk Management, Identify Risks, Perform Qualitative Risk Analysis, "
            "Perform Quantitative Risk Analysis, Plan Risk Responses, Implement Risk Responses, and Monitor Risks. "
            "Threat response strategies: avoid, transfer, mitigate, accept, escalate. "
            "Opportunity response strategies: exploit, share, enhance, accept, escalate. "
            "EMV (Expected Monetary Value) = probability × impact. "
            "A Decision Tree diagram describes a decision and the implications of its alternatives, incorporating probabilities and costs/rewards — used to identify the decision that yields the greatest expected value. "
            "Reserves: contingency reserve (known unknowns, part of cost baseline) and management reserve (unknown unknowns, not in baseline)."
        ),
    },
    {
        "slug": "procurement_management",
        "name": "Procurement Management",
        "summary": "Acquiring goods and services from outside the project team.",
        "content": (
            "Project Procurement Management includes processes to purchase or acquire products, services, or results from outside the team. "
            "Processes: Plan Procurement Management, Conduct Procurements, and Control Procurements. "
            "Contract types: Fixed Price (FP, seller bears risk), Cost-Reimbursable (CR, buyer bears risk), and Time and Material (T&M, hybrid). "
            "FP variants: FFP (firm fixed price), FPIF (with incentive fee), FPEPA (economic price adjustment). "
            "CR variants: CPFF (fixed fee), CPIF (incentive fee), CPAF (award fee). "
            "Procurement documents include RFP (request for proposal), RFQ (quotation), and IFB/RFB (bid). "
            "Make-or-buy analysis decides between in-house vs. external based on total cost, capability, and strategic fit."
        ),
    },
    {
        "slug": "stakeholder_management",
        "name": "Stakeholder Management",
        "summary": "Identifying and engaging stakeholders to align expectations.",
        "content": (
            "Project Stakeholder Management identifies people, groups, or organizations impacted by the project. "
            "Processes: Identify Stakeholders, Plan Stakeholder Engagement, Manage Stakeholder Engagement, and Monitor Stakeholder Engagement. "
            "Stakeholder analysis tools: power/interest grid, power/influence grid, salience model. "
            "Engagement levels: unaware, resistant, neutral, supportive, leading. "
            "The stakeholder engagement plan documents strategies to interact effectively. "
            "Early identification and continuous engagement reduce surprises and improve project success."
        ),
    },
    {
        "slug": "ethics_professional_conduct",
        "name": "Ethics & Professional Conduct",
        "summary": "The PMI Code of Ethics: responsibility, respect, fairness, honesty.",
        "content": (
            "The PMI Code of Ethics and Professional Conduct establishes four core values: Responsibility, Respect, Fairness, and Honesty. "
            "Responsibility: ownership for decisions made or not made, actions taken or not taken, and their consequences. "
            "Includes reporting ethical violations, complying with laws, and fulfilling commitments. "
            "Respect: acknowledging the worth of others; behaving professionally, listening to others' views, approaching disagreements with courtesy, respecting property rights. "
            "Fairness: making decisions and acting impartially and objectively. Disclose conflicts of interest proactively. Do not discriminate. Apply rules fairly to all stakeholders. "
            "Honesty: truthfulness in all communications and conduct. Report accurately on project status. Do not deceive, mislead, or make false statements. "
            "Common exam scenarios: conflict of interest (disclose and recuse), kickbacks or bribery (never accept), cultural differences (respect local norms that do not violate ethics), "
            "estimate reporting (provide honest estimates even if unpopular), and confidentiality (protect information shared in trust)."
        ),
    },
]


def get_chapter_by_slug(slug: str):
    return next((c for c in PMP_CHAPTERS if c["slug"] == slug), None)


def get_chapter_by_name(name: str):
    return next((c for c in PMP_CHAPTERS if c["name"] == name), None)


def build_corpus_text(focus_chapter_slugs: list[str] | None = None) -> str:
    """Concatenate chapter contents, optionally filtered to a subset."""
    chapters = PMP_CHAPTERS
    if focus_chapter_slugs:
        focus_set = set(focus_chapter_slugs)
        filtered = [c for c in PMP_CHAPTERS if c["slug"] in focus_set]
        if filtered:
            chapters = filtered
    parts = []
    for ch in chapters:
        parts.append(f"--- Chapter: {ch['name']} ---\n{ch['content']}")
    return "\n\n".join(parts)
