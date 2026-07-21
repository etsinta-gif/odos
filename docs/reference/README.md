# Reference Documents

This folder contains frozen architecture and reference documentation.

Place the following document types here:
- `DOC-010.md`, `DOC-011.md`, etc.
- `ADR-*.md`
- other formal architecture, enterprise, and standards documentation

These files are intended as stable references and should only be updated through formal revision.

## Folder structure
- `governance/` — DOCs covering repository, governance, and ADR registers
- `architecture/` — enterprise architecture and data model documentation
- `technical-standards/` — platform engineering, application development, AI, security, and operations standards
- `implementation-details/` — core module, business module, reporting, and template specifications
- `dsa-industry-customization/` — industry-specific configuration and mapping guides
- `misc/` — supporting notes and workflow documents

## When adding new IMPs
- Place new IMP documents under `docs/implementation/`
- Link them to the appropriate `docs/reference/` files so implementation is directly traceable to architecture and standards
- Keep the reference folder organized by category and update `docs/reference/index.md`
- Add a brief cross-reference note in the IMP to the relevant REF docs used for implementation decisions
