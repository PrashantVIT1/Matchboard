import React from 'react';
import Button from './ui/Button';

const JDComposer = ({ value, onChange, files, onFilesChange, topN, onTopNChange, maxTopN, loading, onSubmit, error }) => {
  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    onFilesChange([...files, ...selectedFiles]);
  };

  const removeFile = (index) => {
    const newFiles = files.filter((_, i) => i !== index);
    onFilesChange(newFiles);
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Top-N Card */}
      <div className="mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-[#e0e0e0] p-6">
          <h3 className="text-base font-medium text-[#2d2d2d] mb-4">How many top candidates?</h3>
          <div className="flex items-center justify-center gap-4">
            <button
              type="button"
              onClick={() => onTopNChange(Math.max(1, topN - 1))}
              disabled={topN <= 1}
              className="w-10 h-10 flex items-center justify-center rounded-lg border border-[#e0e0e0] text-[#666666] hover:border-[#FF9B4A] hover:text-[#FF9B4A] disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              −
            </button>
            <span className="text-3xl font-medium text-[#2d2d2d] w-12 text-center">
              {topN}
            </span>
            <button
              type="button"
              onClick={() => onTopNChange(Math.min(maxTopN, topN + 1))}
              disabled={topN >= maxTopN}
              className="w-10 h-10 flex items-center justify-center rounded-lg border border-[#e0e0e0] text-[#666666] hover:border-[#FF9B4A] hover:text-[#FF9B4A] disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              +
            </button>
          </div>
          <p className="text-xs text-[#999999] text-center mt-2">
            of {maxTopN} candidates
          </p>
        </div>
      </div>

      {/* Resume Upload Area */}
      <div className="mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-[#e0e0e0] p-6">
          <h3 className="text-base font-medium text-[#2d2d2d] mb-4">Upload Resumes</h3>
          
          {/* Upload Area */}
          <div className="border-2 border-dashed rounded-lg p-6 text-center transition-all border-[#e0e0e0] hover:border-[#20C4CF]">
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
              className="inline-flex items-center gap-2 px-4 py-2 bg-[#20C4CF] text-white text-sm font-medium rounded-lg hover:bg-[#1ab0ba] cursor-pointer transition-all"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Add PDF or DOCX files
            </label>
          </div>

          {/* Selected Files */}
          {files.length > 0 && (
            <div className="mt-4 space-y-2">
              {files.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between px-4 py-3 bg-[#FFF8D9] rounded-lg"
                >
                  <div className="flex items-center flex-1 min-w-0">
                    <span className="inline-flex items-center justify-center w-6 h-6 rounded bg-white text-[#666666] text-[10px] font-medium mr-3">
                      {file.type === 'application/pdf' ? 'PDF' : 'DOCX'}
                    </span>
                    <p className="text-sm font-medium text-[#2d2d2d] truncate">
                      {file.name}
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => removeFile(index)}
                    className="ml-3 text-[#999999] hover:text-[#FF9B4A] transition-colors p-1"
                  >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* JD Composer */}
      <div className="bg-white rounded-lg shadow-sm border border-[#e0e0e0] p-6">
        <div className="flex items-start gap-4">
          {/* Plus Button for Resume Upload */}
          <div className="flex-shrink-0">
            <label
              htmlFor="resume-upload-composer"
              className="w-10 h-10 flex items-center justify-center rounded-lg border border-[#e0e0e0] text-[#666666] hover:border-[#FF9B4A] hover:text-[#FF9B4A] cursor-pointer transition-all"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
            </label>
            <input
              type="file"
              multiple
              accept=".pdf,.docx"
              onChange={handleFileChange}
              className="hidden"
              id="resume-upload-composer"
            />
          </div>

          {/* Textarea */}
          <div className="flex-1 min-w-0">
            <textarea
              value={value}
              onChange={(e) => onChange(e.target.value)}
              placeholder="Paste your job description..."
              rows={4}
              className="w-full max-w-full min-w-0 box-border px-4 py-3 bg-[#FFF8D9] border border-[#e0e0e0] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#FF9B4A] focus:border-transparent resize-none text-[#2d2d2d] leading-relaxed text-sm transition-all"
            />
          </div>

          {/* Analyze Button */}
          <div className="flex-shrink-0">
            <Button
              type="button"
              onClick={onSubmit}
              disabled={loading || !value.trim() || files.length === 0}
              loading={loading}
              size="md"
              className="rounded-full"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
            </Button>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mt-4 bg-[#FFF8D9] border border-[#FF9B4A] rounded-lg p-3">
            <p className="text-sm text-[#FF9B4A]">{error}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default JDComposer;
