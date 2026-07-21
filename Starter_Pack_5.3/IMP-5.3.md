# IMP-5.3 Document Management Starter Pack

## 1. Objective
Implement a new Document Management feature under Masters. The module should allow users to upload, view, download, and delete documents related to Cases, Customers, Lenders, or other master data.

## 2. Scope
- API: Document CRUD, upload, file storage metadata, download, delete, audit logging.
- UI: Document list, upload form, document details, download and delete actions.
- Support document metadata: document type, case id, customer id, lender id, uploaded by, upload date.
- Validate file uploads: allowed extensions, size limit.

## 3. Data Model
- `AUD_Document`
  - `document_id`
  - `case_id`
  - `customer_id`
  - `lender_id`
  - `document_type`
  - `file_repository_id`
  - `uploaded_by`
  - `uploaded_at`
  - `is_active`
- `AUD_FileRepository`
  - `file_repository_id`
  - `filename`
  - `file_hash`
  - `file_size`
  - `content_type`
  - `file_path`
  - `created_at`
  - `is_active`

## 4. Key Features
- Upload new documents, link to case/customer/lender.
- Display list of active documents with metadata.
- Download document file from repository.
- Soft-delete document and file repository entries (`is_active=false`).
- Upload validation:
  - max size 10 MB
  - allowed types: pdf, docx, png, jpg, jpeg

## 5. Implementation Notes
- Use `UploadFile` + `aiofiles` for file streaming. Install `aiofiles` if missing: `pip install aiofiles`.
- Save files to `uploads/documents/` or `uploads/files/`.
- Derive `file_hash` from file content for deduplication.
- Create UI template under `templates/masters/documents.html`.
- Add routes in `src/masters/ui/routes.py` for `GET /masters/documents`, `POST /masters/documents/upload`, `GET /masters/documents/download/{document_id}`.
- Add API routes under `/api/masters/documents` for programmatic upload and metadata retrieval.
- Use `case_id`, `customer_id`, and `lender_id` as optional lookup fields.

## 6. Test Pack Requirements
- Validate document upload via API and ensure metadata persists.
- Upload a PDF and verify `content_type`, `filename`, `file_size`, `file_hash`.
- Link uploaded document to an existing case and verify it appears in list view.
- Download document via UI route and verify file contents.
- Soft delete a document and verify `is_active` toggles.

## 7. Deployment
- Add new API routes to FastAPI application if needed.
- Run the app and open `http://localhost:8000/masters/documents`.

## 8. Notes
- If no case exists, use `case_id=1` or existing master id.
- This starter pack is intentionally minimal and should be adapted to your project's audit and repository schema.
