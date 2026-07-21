# TEST-5.3 Document Management Test Pack

## Overview
This test pack validates the Document Management starter pack for Sprint 5.3. It covers API upload/download/delete functionality and UI-accessible document listing.

## 1. Test Data Setup
- Ensure a Case exists (e.g. `case_id=1`).
- Ensure the following file types are available for upload: `sample.pdf`, `sample.docx`, `sample.png`.

## 2. API Validation
1. `POST /api/masters/documents/upload`
   - Upload `sample.pdf` with `case_id=1`, `document_type=Application`, `uploaded_by=test.user`
   - Assert response status `201`.
   - Assert returned `document_id`, `filename`, `content_type`, `file_size`, `file_hash`.
2. `GET /api/masters/documents/{document_id}`
   - Assert response status `200`.
   - Assert returned metadata equals uploaded values.
3. `GET /masters/documents/download/{document_id}`
   - Assert response status `200`.
   - Assert downloaded file content matches original `sample.pdf`.
4. `DELETE /api/masters/documents/{document_id}`
   - Assert response status `204`.
   - Assert `GET /masters/documents/{document_id}` returns `404` or `is_active=false` where supported.

## 3. UI Validation
1. Open `http://localhost:8000/masters/documents`
   - Assert the page loads successfully.
   - Assert the document list shows uploaded documents.
2. Upload a document through the page.
   - Assert the page confirms upload success.
   - Assert the document appears in the list.
3. Click Download on a document.
   - Assert the browser receives the file.
4. Delete a document.
   - Assert the document disappears from the list.

## 4. Edge Cases
- Upload an unsupported file type: assert `400` or validation error.
- Upload a file larger than 10MB: assert `400` or size validation error.
- Upload with missing `document_type`: assert validation error.

## 5. Audit Verification
- Verify `AUD_Document` audit metadata is created.
- Verify `AUD_FileRepository` entry exists with `file_repository_id`, `filename`, `file_hash`.

## 6. Expected Results
- Document metadata stored correctly.
- File download returns the same data uploaded.
- Soft delete changes `is_active` status without physically deleting records.
