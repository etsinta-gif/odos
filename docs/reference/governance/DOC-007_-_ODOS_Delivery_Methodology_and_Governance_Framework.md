# DOC-007 – ODOS Delivery Methodology & Governance Framework

__DOC\-007 – ODOS Delivery Methodology & Governance Framework__

__Document ID:__ DOC\-007  
__Version:__ 1\.0  
__Status:__ Approved / Frozen  
__Owner:__ CTO \(ChatGPT\)  
__Technical Programme Manager:__ DeepSeek  
__Development Lead:__ Aniket  
__Classification:__ Programme Governance

__1\. Purpose__

This document defines the official Software Delivery Lifecycle \(SDLC\), governance model, approval workflow, quality standards, and execution methodology for the ODOS Enterprise Platform\.

No work shall be performed outside this methodology\.

This document is the constitutional document governing the delivery of ODOS\.

__2\. Objectives__

The methodology ensures that:

- Architecture drives implementation\.
- Business requirements drive engineering\.
- Every implementation is reviewed\.
- Every deliverable is traceable\.
- Technical debt is minimised\.
- Quality is built into every sprint\.
- AI assistants work consistently\.
- Engineering remains architecture compliant\.

__3\. Programme Hierarchy__

ODOS is delivered as an Enterprise Programme\.

Programme

↓

Capability

↓

Sprint

↓

User Story

↓

Task

↓

Implementation Pack

↓

Engineering

↓

Review

↓

Acceptance

↓

Release

Every engineering activity belongs to this hierarchy\.

__4\. Delivery Lifecycle__

Every capability follows the same lifecycle\.

Business Requirement

↓

Business Proposal

↓

CTO Architecture Review

↓

Architecture Approval

↓

Technical Planning

↓

Implementation Pack

↓

Development

↓

Technical Review

↓

Architecture Review

↓

Business Acceptance

↓

Release

↓

Support

No stage may be skipped\.

__5\. Roles & Responsibilities__

__Business Owner__

Responsible for:

- Business requirements
- Prioritisation
- Acceptance
- Business validation

__CTO \(ChatGPT\)__

Responsible for:

- Enterprise architecture
- Technical governance
- ADR approval
- Architecture compliance
- Final implementation approval

The CTO does __not__ write production code\.

__Technical Programme Manager \(DeepSeek\)__

Responsible for:

- Sprint planning
- Technical design
- Task decomposition
- Implementation Packs
- Engineering review
- Progress monitoring
- Risk identification

The TPM does __not__ make architectural decisions\.

__Engineering \(Aniket\)__

Responsible for:

- Development
- Unit testing
- Bug fixing
- Documentation
- Code quality
- Technical delivery

Engineering follows approved implementation packs only\.

__6\. Governance Principles__

Every implementation shall satisfy the following principles\.

- Business before Technology
- Architecture before Development
- Metadata before Code
- Review before Merge
- Test before Release
- Traceability always
- Documentation always
- Reuse before Build
- Security by Design
- AI Assisted Engineering

__7\. Capability\-Based Delivery__

Development is organised around __Capabilities__, not features\.

Example:

Capability

Metadata Engine

↓

Sprint 1\.3

↓

Stories

↓

Tasks

↓

Implementation Pack

Capabilities remain stable while implementation evolves\.

__8\. Capability Gates__

Progress is measured using Capability Gates\.

Examples include:

__Gate 1__

Foundation Ready

Checklist:

- Repository
- Logging
- Configuration
- Database
- CI/CD
- Migrations

__Gate 2__

Enterprise Security Ready

Checklist:

- Authentication
- RBAC
- Audit
- User Management
- Feature Toggles

__Gate 3__

Metadata Engine Ready

Checklist:

- Metadata Tables
- Configuration Engine
- Validation Engine
- Dynamic APIs

__Gate 4__

Canonical Database Ready

Checklist:

- Master Tables
- Reference Data
- Multi\-tenancy
- Seed Data

Each capability must pass its gate before dependent work begins\.

__9\. Official Delivery Workflow__

Every implementation follows this workflow\.

Business Requirement Proposal

↓

CTO Review

↓

Approved

↓

DeepSeek Technical Planning

↓

Implementation Pack

↓

Engineering

↓

Technical Review

↓

CTO Architecture Review

↓

Business Acceptance

↓

Complete

This workflow is mandatory\.

__10\. Sprint Workflow__

Each sprint consists of:

1. Sprint Planning
2. Capability Review
3. Story Definition
4. Task Breakdown
5. Implementation Pack
6. Development
7. Testing
8. Technical Review
9. Architecture Review
10. Acceptance
11. Sprint Closure

__11\. Implementation Pack Contents__

Every Implementation Pack shall include:

- Sprint Information
- Capability
- Objectives
- Stories
- Tasks
- Dependencies
- Architecture References
- ADR References
- Acceptance Criteria
- Definition of Done
- Testing Requirements
- Risks
- Deliverables

No implementation begins without an approved Implementation Pack\.

__12\. Definition of Ready__

A task is Ready when:

- Business requirement approved\.
- Capability identified\.
- Dependencies resolved\.
- Architecture reviewed\.
- ADRs identified\.
- Acceptance criteria defined\.
- Implementation Pack approved\.

__13\. Definition of Done__

Work is Done only when:

- Code completed\.
- Tests passed\.
- Architecture compliant\.
- Documentation updated\.
- ADR references included\.
- Code reviewed\.
- Business accepted\.
- Repository updated\.

__14\. Quality Gates__

Every implementation must pass:

- Build Validation
- Unit Testing
- Integration Testing
- Architecture Compliance
- Security Review
- Documentation Review
- Business Acceptance

__15\. Architecture Compliance__

Before approval, every implementation shall be checked against:

- Architecture Principles
- ADRs
- Canonical Data Model
- Security Standards
- Metadata Standards
- Naming Standards
- Coding Standards

Non\-compliant implementations are rejected\.

__16\. AI Operating Model__

__ChatGPT \(CTO\)__

Responsible for:

- Strategy
- Architecture
- Governance
- Final approval

__DeepSeek \(Technical Programme Manager\)__

Responsible for:

- Planning
- Technical design
- Implementation Packs
- Engineering reviews
- Progress monitoring

__Engineering AI \(Cursor / Claude Code / GitHub Copilot\)__

Responsible for:

- Code generation
- Refactoring
- Testing assistance

They shall never override architecture\.

__17\. Change Management__

Architecture changes require:

- New ADR
- Impact assessment
- CTO approval
- Repository update

Implementation changes require:

- Updated Implementation Pack
- TPM approval
- Engineering review

__18\. Risk Management__

Risks are categorised as:

- Architecture
- Technical
- Business
- Security
- Performance
- Delivery
- Operational

High\-impact risks are escalated to the CTO\.

__19\. Repository Integration__

This methodology references:

- Vision & Strategy
- Enterprise Architecture
- ADR Register
- Capability Register
- Sprint Roadmap
- Master Backlog
- Repository Standards

Every implementation pack shall identify the documents it depends upon\.

__20\. Success Measures__

The delivery methodology is successful when:

- No architecture violations occur\.
- Every implementation is traceable\.
- Technical debt remains controlled\.
- Sprint predictability improves\.
- AI assistants produce consistent outputs\.
- Engineering focuses on implementation rather than redesign\.
- Business receives predictable, high\-quality releases\.

__21\. Governance Statement__

__Business defines WHAT\.__

__Architecture defines HOW\.__

__DeepSeek defines the IMPLEMENTATION PLAN\.__

__Engineering builds the APPROVED PLAN\.__

__ChatGPT approves ARCHITECTURAL COMPLIANCE\.__

This governance model shall be followed for every capability, sprint, and release throughout the lifecycle of the ODOS Enterprise Platform\.

__End of Document__

__Document ID:__ DOC\-007  
__Document Name:__ *ODOS Delivery Methodology & Governance Framework*  
__Version:__ 1\.0  
__Status:__ Approved / Frozen

