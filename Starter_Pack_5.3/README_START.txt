=============================================
SPRINT 5.3 STARTER PACK
=============================================

This is the starter pack for Sprint 5.3 – Document Management (UI & API).

PREREQUISITES:
- Sprint 5.2 completed (Case Management UI)
- AUD_Document and AUD_FileRepository tables exist
- At least one case exists for testing document uploads

WHAT YOU WILL BUILD:
- UI screens to upload, view, download, and delete documents
- Documents can be linked to Cases, Customers, Lenders, etc.
- File upload with validation (size, type)

STEPS:
1. Copy ALL files and folders from this pack into your odos project root
2. Follow IMP-5.3.md step by step
3. Start the server and test at http://localhost:8000/masters/documents

FILES INCLUDED:
- src/masters/api/document.py       (Document CRUD + file upload/download; requires `aiofiles`)
- src/masters/ui/routes.py          (UI routes – you will ADD new routes)
- src/templates/masters/*.html      (Document list, upload, detail)
- scripts/seed_test_documents.py    (Optional test data)

ESTIMATED DURATION: 2 days
CONTACT: CTO or Technical Programme Manager
