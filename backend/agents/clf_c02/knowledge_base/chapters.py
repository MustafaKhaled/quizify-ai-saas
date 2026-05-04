"""
Static chapter knowledge base for the AWS Certified Cloud Practitioner (CLF-C02) agent.

Chapter slugs/names align loosely to the four official CLF-C02 domains:
  Domain 1: Cloud Concepts (24%)
  Domain 2: Security and Compliance (30%)
  Domain 3: Cloud Technology and Services (34%)
  Domain 4: Billing, Pricing, and Support (12%)

Each chapter's `name` doubles as the quiz `topic` field, and slugs match the
seed exam bank so ingest can resolve chapter_slug → chapter without translation.
"""

CLF_C02_CHAPTERS = [
    # ── Domain 1: Cloud Concepts ───────────────────────────────────────────
    {
        "slug": "cloud_concepts",
        "name": "Cloud Concepts",
        "summary": "Cloud computing fundamentals, deployment models, value proposition, and the AWS Cloud Adoption Framework.",
        "content": (
            "Cloud computing is the on-demand delivery of compute, storage, databases, and other IT resources "
            "over the internet with pay-as-you-go pricing. Three deployment models: cloud (fully in AWS), "
            "hybrid (mix of on-premises and cloud), and on-premises (private cloud). "
            "Six advantages of cloud: trade capital expense for variable expense, benefit from massive economies of scale, "
            "stop guessing about capacity, increase speed and agility, stop spending money on data centers, "
            "and go global in minutes. "
            "Three cloud service models: IaaS (Infrastructure as a Service — EC2), PaaS (Platform as a Service — Beanstalk), "
            "and SaaS (Software as a Service — third-party apps). "
            "AWS Global Infrastructure: Regions are isolated geographic areas; Availability Zones (AZs) are physically separate data centers within a Region "
            "(at least 3 per Region); Edge Locations cache content for CloudFront. "
            "AWS Cloud Adoption Framework (CAF) has six perspectives: Business, People, Governance, Platform, Security, Operations. "
            "Use CAF to align cloud transformation across stakeholders."
        ),
    },
    {
        "slug": "well_architected_framework",
        "name": "Well-Architected Framework",
        "summary": "The six pillars of the AWS Well-Architected Framework and their key design principles.",
        "content": (
            "The AWS Well-Architected Framework provides best-practice guidance through six pillars: "
            "1) Operational Excellence — run and monitor systems, perform operations as code, anticipate failure, learn from events. "
            "2) Security — implement strong identity foundation, enable traceability, apply defense in depth, automate security best practices, "
            "protect data in transit and at rest, prepare for security events. "
            "3) Reliability — automatically recover from failure, test recovery procedures, scale horizontally, stop guessing capacity, manage change in automation. "
            "4) Performance Efficiency — democratize advanced technologies, go global in minutes, use serverless architectures, experiment more often, "
            "consider mechanical sympathy (use the right tool for the job). "
            "5) Cost Optimization — adopt a consumption model, measure overall efficiency, stop spending on data center operations, analyze and attribute expenditure, use managed services. "
            "6) Sustainability — understand your impact, establish sustainability goals, maximize utilization, anticipate and adopt new more-efficient hardware, "
            "use managed services, reduce downstream impact of cloud workloads. "
            "Common exam question: identify which pillar a design principle belongs to."
        ),
    },

    # ── Domain 2: Security and Compliance ──────────────────────────────────
    {
        "slug": "iam_and_security",
        "name": "IAM & Security",
        "summary": "AWS Identity and Access Management, the Shared Responsibility Model, and core security services.",
        "content": (
            "AWS Identity and Access Management (IAM) controls who (authentication) can access what (authorization) in AWS. "
            "Components: Users (long-term identity), Groups (collection of users), Roles (temporary credentials assumed by services or users), "
            "Policies (JSON documents granting or denying permissions). "
            "Best practices: never use the root user for daily tasks (only initial setup, billing, account-wide changes); "
            "enable MFA on root and all users; grant least privilege; use roles for EC2 instances and cross-account access; rotate credentials. "
            "The Shared Responsibility Model splits security obligations: AWS is responsible for security OF the cloud (hardware, hypervisor, AZs, networking infrastructure); "
            "the customer is responsible for security IN the cloud (data, IAM, OS patching on EC2, application code, network/firewall config). "
            "Managed services like S3, DynamoDB, RDS shift more responsibility to AWS (AWS manages OS patching). "
            "Encryption: SSE-S3, SSE-KMS, SSE-C for S3 server-side encryption; KMS for managed keys; CloudHSM for dedicated hardware. "
            "AWS Shield (DDoS protection — Standard is free, Advanced is paid), WAF (web application firewall), GuardDuty (intelligent threat detection), "
            "Inspector (vulnerability scanning), Macie (sensitive data discovery in S3)."
        ),
    },
    {
        "slug": "compliance_and_governance",
        "name": "Compliance & Governance",
        "summary": "Compliance programs, audit tools, and governance services like CloudTrail, Config, Artifact, and Organizations.",
        "content": (
            "AWS Artifact is a self-service portal for on-demand access to AWS compliance reports (SOC 1/2/3, PCI DSS, ISO 27001, HIPAA, GDPR-related documents) "
            "and agreements (BAAs, NDAs). "
            "AWS CloudTrail records account-wide API calls — who did what, when, from where. Required for security forensics and audit trails. Logs to S3. "
            "AWS Config tracks resource configurations and changes over time, evaluates them against rules for compliance. "
            "AWS Organizations centrally manages multiple AWS accounts: consolidated billing, Service Control Policies (SCPs) to restrict permissions across accounts, "
            "Organizational Units (OUs) to group accounts, and Single Sign-On integration. "
            "AWS Control Tower automates account provisioning following best practices, with guardrails. "
            "AWS Trusted Advisor checks accounts against best practices in five categories: cost optimization, performance, security, fault tolerance, service limits. "
            "Compliance programs supported by AWS include HIPAA, FedRAMP, ISO 27001/27017/27018, PCI DSS Level 1, SOC 1/2/3, GDPR. "
            "Customer remains responsible for using AWS services in a compliant way."
        ),
    },

    # ── Domain 3: Cloud Technology and Services ────────────────────────────
    {
        "slug": "compute",
        "name": "Compute",
        "summary": "EC2, Lambda, container services, Auto Scaling, and load balancing.",
        "content": (
            "Amazon EC2 (Elastic Compute Cloud) provides resizable compute capacity (virtual machines). Key concepts: "
            "Instance types (general-purpose t/m, compute-optimized c, memory-optimized r/x, storage-optimized i/d, accelerated p/g), "
            "AMIs (Amazon Machine Images — OS templates), Security Groups (stateful firewalls at instance level), Key Pairs (SSH access). "
            "Pricing models: On-Demand (pay per hour/second, no commitment), Reserved Instances (1-3 year commitment, up to 72% off), "
            "Savings Plans (commitment to compute spend, more flexible than RIs), Spot Instances (up to 90% off, can be interrupted), Dedicated Hosts (compliance/licensing). "
            "AWS Lambda runs code without managing servers (Function as a Service). Pay only for execution time. Triggers from S3, API Gateway, EventBridge, etc. "
            "Max execution time 15 min. Supports many languages. "
            "Container services: ECS (Elastic Container Service — AWS-native orchestration), EKS (Elastic Kubernetes Service — managed Kubernetes), "
            "Fargate (serverless containers — no EC2 to manage), ECR (container registry). "
            "Auto Scaling automatically adjusts EC2 capacity based on demand or schedule. "
            "Elastic Load Balancing (ELB): Application Load Balancer (Layer 7, HTTP/HTTPS), Network Load Balancer (Layer 4, ultra-low latency), "
            "Gateway Load Balancer (third-party appliances), Classic Load Balancer (legacy). "
            "AWS Batch runs batch computing jobs at any scale. Lightsail provides simple VPS for small workloads."
        ),
    },
    {
        "slug": "storage",
        "name": "Storage",
        "summary": "S3, EBS, EFS, FSx, Storage Gateway, Snowball/Snowmobile, and storage classes.",
        "content": (
            "Amazon S3 (Simple Storage Service) is object storage with virtually unlimited scale. Concepts: Buckets (globally unique names), "
            "Objects (files up to 5TB), Keys (object names), 99.999999999% (11 nines) durability. "
            "S3 storage classes: Standard (frequent access), Intelligent-Tiering (automatic optimization), Standard-IA (infrequent access), "
            "One Zone-IA (single AZ, cheaper), Glacier Instant Retrieval (ms retrieval), Glacier Flexible Retrieval (minutes-hours), "
            "Glacier Deep Archive (12+ hours, cheapest). Lifecycle policies move objects between classes. "
            "S3 features: Versioning (keep multiple versions), Replication (cross-region or same-region), Encryption (SSE-S3/KMS/C), "
            "Access via bucket policies, IAM policies, ACLs, presigned URLs. "
            "Amazon EBS (Elastic Block Store) provides block storage for EC2 — like a virtual hard drive. Tied to a single AZ. "
            "Volume types: gp3/gp2 (general-purpose SSD), io2/io1 (provisioned IOPS SSD for databases), st1 (throughput-optimized HDD), sc1 (cold HDD). "
            "Snapshots are point-in-time backups stored in S3, can be copied across regions. "
            "Amazon EFS (Elastic File System) is managed NFS for Linux — shared file system mountable by multiple EC2 instances across AZs. "
            "Amazon FSx provides managed file systems: FSx for Windows File Server (SMB), FSx for Lustre (HPC), FSx for NetApp ONTAP, FSx for OpenZFS. "
            "AWS Storage Gateway hybridizes on-prem with AWS storage. "
            "Snow family for offline data transfer: Snowcone (small, ~14TB), Snowball Edge (~80TB), Snowmobile (truck, exabyte-scale)."
        ),
    },
    {
        "slug": "databases",
        "name": "Databases",
        "summary": "RDS, Aurora, DynamoDB, Redshift, ElastiCache, DocumentDB, and Neptune.",
        "content": (
            "Amazon RDS (Relational Database Service) provides managed relational databases: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, MS SQL. "
            "AWS handles patching, backups, replication. Multi-AZ for high availability (synchronous replication). Read Replicas for scaling reads (asynchronous). "
            "Amazon Aurora is AWS's MySQL/PostgreSQL-compatible engine — up to 5x faster than MySQL, up to 3x faster than PostgreSQL, "
            "auto-scaling storage up to 128TB, 6 copies across 3 AZs. Aurora Serverless auto-scales compute. "
            "Amazon DynamoDB is a managed NoSQL key-value/document database. Single-digit-millisecond latency at any scale. Serverless. "
            "Pricing: provisioned (predictable workloads) or on-demand (unpredictable). DAX adds in-memory caching. Global Tables for multi-region replication. "
            "Amazon Redshift is a managed data warehouse for analytics over petabytes. Columnar storage, massively parallel processing (MPP). "
            "Best for OLAP workloads, not OLTP. "
            "Amazon ElastiCache provides managed in-memory caches: Redis (rich data structures, replication, persistence) and Memcached (simple cache, multi-threaded). "
            "Amazon DocumentDB is MongoDB-compatible. Amazon Neptune is a graph database. Amazon Keyspaces is Cassandra-compatible. "
            "Amazon QLDB is an immutable ledger database. Amazon Timestream is for time-series data."
        ),
    },
    {
        "slug": "networking_and_content_delivery",
        "name": "Networking & Content Delivery",
        "summary": "VPC, subnets, gateways, Route 53, CloudFront, Direct Connect, and Global Accelerator.",
        "content": (
            "Amazon VPC (Virtual Private Cloud) is your isolated virtual network in AWS. Configure CIDR blocks, subnets (public/private), route tables, "
            "Internet Gateway (for public internet access), NAT Gateway/Instance (for private subnets to reach internet outbound), "
            "VPC Peering (connect two VPCs), Transit Gateway (hub for many VPCs and on-prem). "
            "Security at network level: Security Groups (stateful, instance-level, allow rules only) vs NACLs (stateless, subnet-level, allow + deny rules). "
            "Amazon Route 53 is a managed DNS service: domain registration, health checks, routing policies (Simple, Weighted, Latency, Failover, Geolocation, Geoproximity, Multi-value). "
            "Amazon CloudFront is a global CDN. Caches content at Edge Locations. Origins: S3, EC2, ALB, custom HTTP. Reduces latency for users. "
            "AWS Direct Connect provides dedicated private network from on-prem to AWS — bypasses internet, lower latency, more consistent throughput. "
            "AWS VPN: Site-to-Site VPN (encrypted tunnel over internet, slower than Direct Connect), Client VPN (remote workers). "
            "AWS Global Accelerator improves performance using AWS global network and 2 static anycast IPs. Routes traffic to optimal endpoint. "
            "AWS PrivateLink connects services across VPCs/accounts privately (no internet, no VPC peering)."
        ),
    },
    {
        "slug": "deployment_and_management",
        "name": "Deployment & Management",
        "summary": "CloudFormation, Elastic Beanstalk, OpsWorks, Systems Manager, CloudWatch, and CodePipeline.",
        "content": (
            "AWS CloudFormation is Infrastructure as Code (IaC). Define resources in YAML/JSON templates, deploy as 'stacks'. Repeatable, version-controlled infrastructure. "
            "AWS Elastic Beanstalk is PaaS for deploying web applications. Upload code, AWS handles capacity, load balancing, scaling, monitoring. "
            "Supports multiple platforms (Java, .NET, Node.js, Python, Ruby, Go, Docker). "
            "AWS OpsWorks uses Chef/Puppet for configuration management. "
            "AWS Systems Manager (SSM) provides operational visibility and control: Parameter Store (secrets/config), Session Manager (browser-based shell, no SSH), "
            "Patch Manager, Run Command, Inventory, Automation. "
            "Amazon CloudWatch monitors AWS resources and applications: Metrics (numerical data), Logs (application logs), Alarms (notifications), Events/EventBridge (event-driven actions), Dashboards. "
            "AWS X-Ray traces distributed applications to debug performance issues. "
            "Developer tools: CodeCommit (Git repos), CodeBuild (build/test), CodeDeploy (deploy to EC2/Lambda/ECS), CodePipeline (CI/CD orchestration), CodeStar, CodeArtifact. "
            "AWS CDK (Cloud Development Kit) lets you define infrastructure in TypeScript/Python/Java. "
            "AWS Service Catalog manages catalogs of approved IT services for organizations."
        ),
    },
    {
        "slug": "migration_and_innovation",
        "name": "Migration & Innovation",
        "summary": "Migration tools, the 7 Rs, AI/ML services, IoT, and innovation services.",
        "content": (
            "AWS migration strategies (the '7 Rs'): Rehost (lift-and-shift), Replatform (lift-tinker-and-shift), Repurchase (move to SaaS), "
            "Refactor (re-architect), Retain (keep on-prem), Retire (decommission), Relocate (move VMware infra to AWS without modification). "
            "Migration tools: AWS Application Migration Service (MGN — replication-based lift-and-shift), AWS Database Migration Service (DMS — minimal downtime DB migration with Schema Conversion Tool for heterogeneous), "
            "AWS Migration Hub (track migrations), AWS Application Discovery Service (assess on-prem environments). "
            "Snow family for offline data transfer (covered in Storage chapter). "
            "AI/ML services: Amazon Rekognition (image/video analysis), Amazon Polly (text-to-speech), Amazon Transcribe (speech-to-text), "
            "Amazon Translate (language translation), Amazon Comprehend (NLP, sentiment), Amazon Lex (chatbots), Amazon SageMaker (build/train/deploy ML models), "
            "Amazon Personalize (recommendations), Amazon Forecast (time-series), Amazon Bedrock (foundation models / generative AI). "
            "IoT services: AWS IoT Core (connect devices), Greengrass (edge compute), IoT Analytics. "
            "Other innovation services: Amazon Connect (cloud contact center), AWS Ground Station (satellite as a service), Amazon Sumerian (AR/VR — discontinued)."
        ),
    },

    # ── Domain 4: Billing, Pricing, and Support ────────────────────────────
    {
        "slug": "billing_and_pricing",
        "name": "Billing, Pricing & Support",
        "summary": "AWS pricing fundamentals, cost-management tools, support plans, and AWS Marketplace.",
        "content": (
            "AWS pricing fundamentals: pay-as-you-go (no upfront), pay less when you reserve (Reserved Instances, Savings Plans), "
            "pay less per unit using more (volume discounts on S3), pay even less as AWS grows (price reductions over time). "
            "Free tier: Always Free (Lambda, DynamoDB), 12-Months Free (EC2 t2.micro hours, S3 storage), Trials (specific services). "
            "AWS Pricing Calculator estimates monthly cost for proposed architectures (replaces TCO Calculator). "
            "AWS Cost Explorer visualizes spending and forecasts future costs. View by service, account, tag, etc. Up to 12 months historical, 12 months forecast. "
            "AWS Budgets sets custom budgets with alerts (cost, usage, RI utilization, Savings Plans coverage). Notifications via SNS or email. "
            "Cost and Usage Reports (CUR) give the most detailed billing data, delivered to S3. Use Athena/QuickSight/Redshift to analyze. "
            "AWS Organizations consolidated billing aggregates spending across linked accounts; volume discounts apply across the org; one bill for all. "
            "Tags enable cost allocation: tag resources, then group costs by tag in Cost Explorer/Reports. "
            "AWS Support plans: "
            "Basic (free — billing/account questions only, no tech support), "
            "Developer (~$29/mo or 3% of usage — business-hours email support, 1 contact, 24-hour response on general guidance), "
            "Business (~$100/mo or 10% — 24/7 email/chat/phone, all users, 1-hour response on production system down), "
            "Enterprise On-Ramp ($5,500/mo or 10% — 30-min response on critical, pool of TAM time), "
            "Enterprise ($15,000/mo or 10% — 15-min response on critical, dedicated Technical Account Manager (TAM), Concierge for billing). "
            "AWS Marketplace is a curated digital catalog where customers can find, buy, deploy, and manage third-party software (often billed through AWS). "
            "AWS Knowledge Center, re:Post, and Documentation are free self-service resources."
        ),
    },
]


def get_chapter_by_slug(slug: str):
    return next((c for c in CLF_C02_CHAPTERS if c["slug"] == slug), None)


def get_chapter_by_name(name: str):
    return next((c for c in CLF_C02_CHAPTERS if c["name"] == name), None)


def build_corpus_text(focus_chapter_slugs: list[str] | None = None) -> str:
    """Concatenate chapter contents, optionally filtered to a subset."""
    chapters = CLF_C02_CHAPTERS
    if focus_chapter_slugs:
        focus_set = set(focus_chapter_slugs)
        filtered = [c for c in CLF_C02_CHAPTERS if c["slug"] in focus_set]
        if filtered:
            chapters = filtered
    parts = []
    for ch in chapters:
        parts.append(f"--- Chapter: {ch['name']} ---\n{ch['content']}")
    return "\n\n".join(parts)
