# Implementation Packs

This folder contains sprint implementation pack documentation.

Each `IMP-*.md` document should include:
- sprint-specific goals and scope
- implementation assumptions
- acceptance criteria
- linked reference documents from `docs/reference/`

## Cross-reference guidance
- Link each IMP to the reference documents that support its design decisions.
- Use the stable docs in `docs/reference/` to explain why the implementation choices were made.
- Update `docs/reference/index.md` whenever you add or rename reference documents.
- Keep references read-only unless there is a formal ADR or document revision process.

## Usage
- Add new sprint documents here as `IMP-1.6.md`, `IMP-1.7.md`, etc.
- Maintain traceability by citing the relevant reference doc(s) at the top of each IMP.
- Example link format:
  - `See docs/reference/architecture/enterprise-application-model.md`
  - `See docs/reference/technical-standards/security-architecture.md`

## Current files
- `IMP-1.1.md`
- `IMP-1.2.md`
- `IMP-1.3.md`
- `IMP-1.4.md`
- `IMP-1.5.md`
- `IMP-5.7.md`
- `IMP-5.8.md`
