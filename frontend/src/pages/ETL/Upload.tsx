import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import { etlService, UploadResult } from '../../api/etlService';

export default function ETLUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [entityType, setEntityType] = useState('MST_Lender');
  const [result, setResult] = useState<UploadResult | null>(null);
  const [progress, setProgress] = useState(0);
  const [uploading, setUploading] = useState(false);
  const navigate = useNavigate();

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setResult(null);
    setProgress(0);
    setFile(acceptedFiles[0] || null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxSize: 100 * 1024 * 1024,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'text/csv': ['.csv'],
    },
  });

  const upload = async () => {
    if (!file) return;
    setUploading(true);
    setProgress(10);
    const timer = window.setInterval(() => setProgress((p) => Math.min(90, p + 15)), 250);
    try {
      const response = await etlService.uploadFile(file, entityType);
      setResult(response);
      setProgress(100);
      if (response.status === 'mapping_required') {
        const flowId = response.file_name || file.name;
        navigate(`/etl/mapping/${encodeURIComponent(flowId)}`, {
          state: {
            proposal: response.proposal,
            fileName: response.file_name || file.name,
            entityType: response.entity_type || entityType,
          },
        });
      }
    } finally {
      window.clearInterval(timer);
      setUploading(false);
    }
  };

  return (
    <div className="space-y-4 max-w-4xl">
      <h2 className="text-2xl font-bold text-brand-ink">ETL Upload</h2>

      <div
        {...getRootProps()}
        className={`rounded-2xl border-2 border-dashed p-10 text-center cursor-pointer transition ${
          isDragActive ? 'border-brand-mint bg-green-50' : 'border-brand-deep/30 bg-white'
        }`}
      >
        <input {...getInputProps()} />
        <p className="text-brand-deep">
          {file ? `${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)` : 'Drag and drop Excel/CSV, or click to browse'}
        </p>
      </div>

      <select
        value={entityType}
        onChange={(e) => setEntityType(e.target.value)}
        className="rounded border border-brand-deep/20 bg-white px-3 py-2"
      >
        <option value="MST_Lender">MST_Lender</option>
        <option value="MST_Connector">MST_Connector</option>
        <option value="TRN_Case">TRN_Case</option>
      </select>

      <button
        onClick={upload}
        disabled={!file || uploading}
        className="rounded bg-brand-deep px-4 py-2 text-white disabled:opacity-50 hover:bg-brand-mint"
      >
        {uploading ? 'Uploading...' : 'Upload'}
      </button>

      {uploading && (
        <div className="w-full max-w-md h-2 bg-brand-deep/10 rounded">
          <div className="h-2 bg-brand-mint rounded" style={{ width: `${progress}%` }} />
        </div>
      )}

      {result && (
        <div className="rounded-xl border border-brand-deep/10 bg-white p-4">
          <p className="font-semibold">Status: {result.status}</p>
          {result.batch_guid && <p className="text-sm text-brand-deep/70">Batch: {result.batch_guid}</p>}
          {result.status === 'success' && <p className="text-sm text-green-700 mt-1">Template matched. Data processed automatically.</p>}
          {result.status === 'mapping_required' && <p className="text-sm text-amber-700 mt-1">No template matched. Continue in Mapping Approval.</p>}
        </div>
      )}
    </div>
  );
}
