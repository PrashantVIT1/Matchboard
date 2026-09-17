import React, { useState } from 'react';

const ResumeUploader = ({ files, onFilesChange, error, compact = false }) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const validFiles = selectedFiles.filter(
      (file) => file.type === 'application/pdf' || file.name.endsWith('.docx')
    );
    
    if (validFiles.length !== selectedFiles.length) {
      alert('Some files were not added. Only PDF and DOCX files are supported.');
    }
    
    onFilesChange([...files, ...validFiles]);
  };

  const removeFile = (index) => {
    onFilesChange(files.filter((_, i) => i !== index));
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFiles = Array.from(e.dataTransfer.files);
    const validFiles = droppedFiles.filter(
      (file) => file.type === 'application/pdf' || file.name.endsWith('.docx')
    );
    
    if (validFiles.length !== droppedFiles.length) {
      alert('Some files were not added. Only PDF and DOCX files are supported.');
    }
    
    onFilesChange([...files, ...validFiles]);
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  if (compact) {
    return (
      <>
        {/* Upload Area */}
        <div
          className={`border-2 border-dashed rounded-lg p-4 text-center transition-all ${
            isDragging
              ? 'border-[#20C4CF] bg-[#FFF8D9]'
              : 'border-[#e0e0e0] hover:border-[#20C4CF]'
          }`}
          onDragOver={input => handleDragOver(input)}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <p className="text-sm text-[#2d2d2d] mb-1">
            Drop PDF or DOCX files here
          </p>
          <p className="text-xs text-[#666666] mb-3">
            or browse from your computer
          </p>
          <input
            type="file"
            multiple
            accept=".pdf,.docx"
            onChange={handleFileChange}
            className="hidden"
            id="resume-upload"
          />
          <label
            htmlFor="resume-upload"
            className="inline-block px-3 py-1.5 bg-[#20C4CF] text-white text-xs font-medium rounded-lg hover:bg-[#1ab0ba] cursor-pointer transition-all"
          >
            Browse files
          </label>
        </div>

        {/* Selected Files */}
        {files.length > 0 && (
          <div className="mt-3">
            <div className="space-y-2">
              {files.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between px-3 py-2 bg-[#FFF8D9] rounded-lg"
                >
                  <div className="flex items-center flex-1 min-w-0">
                    <div className="flex-shrink-0 mr-2">
                      <span className="inline-flex items-center justify-center w-5 h-5 rounded bg-white text-[#666666] text-[10px] font-medium">
                        {file.type === 'application/pdf' ? 'PDF' : 'DOCX'}
                      </span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-medium text-[#2d2d2d] truncate">
                        {file.name}
                      </p>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => removeFile(index)}
                    className="ml-2 text-[#999999] hover:text-[#FF9B4A] transition-colors p-1"
                    title="Remove file"
                  >
                    <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </>
    );
  }

  return (
    <div>
      <label className="block text-sm font-medium text-[#4A4A4A] mb-3">
        Resumes
      </label>
      
      {/* Upload Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-all ${
          isDragging 
            ? 'border-[#E07A5F] bg-[#FEF3F2]' 
            : 'border-[#D4D4D4] hover:border-[#1A1A1A]'
        }`}
        onDragOver={input => handleDragOver(input)}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="mb-4">
          <svg className="mx-auto h-8 w-8 text-[#8B8B8B]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>
        <p className="text-[#1A1A1A] mb-1">
          Drop resumes here
        </p>
        <p className="text-sm text-[#6B6B6B] mb-4">
          or browse from your computer
        </p>
        <p className="text-xs text-[#8B8B8B]">
          PDF • DOCX
        </p>
        <input
          type="file"
          multiple
          accept=".pdf,.docx"
          onChange={handleFileChange}
          className="hidden"
          id="resume-upload"
        />
        <label
          htmlFor="resume-upload"
          className="inline-block mt-4 px-4 py-2 bg-white border border-[#D4D4D4] text-[#1A1A1A] text-sm font-medium rounded hover:border-[#1A1A1A] cursor-pointer transition-all"
        >
          Browse files
        </label>
      </div>

      {error && <p className="mt-3 text-sm text-[#991B1B]">{error}</p>}
      
      {/* Selected Files */}
      {files.length > 0 && (
        <div className="mt-4">
          <p className="text-sm font-medium text-[#4A4A4A] mb-3">
            {files.length} file{files.length !== 1 ? 's' : ''} selected
          </p>
          <div className="space-y-2">
            {files.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between px-4 py-3 bg-white border border-[#D4D4D4] rounded hover:border-[#1A1A1A] transition-colors"
              >
                <div className="flex items-center flex-1 min-w-0">
                  <div className="flex-shrink-0 mr-3">
                    <span className="inline-flex items-center justify-center w-8 h-8 rounded bg-[#F5F5F0] text-[#6B6B6B] text-xs font-medium">
                      {file.type === 'application/pdf' ? 'PDF' : 'DOCX'}
                    </span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-[#1A1A1A] truncate">
                      {file.name}
                    </p>
                    <p className="text-xs text-[#8B8B8B]">
                      {formatFileSize(file.size)}
                    </p>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => removeFile(index)}
                  className="ml-3 text-[#8B8B8B] hover:text-[#991B1B] transition-colors p-1"
                  title="Remove file"
                >
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResumeUploader;
