import React from 'react';

const JobDescriptionInput = ({ value, onChange, error, compact = false }) => {
  if (compact) {
    return (
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste the job description here..."
        rows={6}
        className={`w-full max-w-full min-w-0 box-border px-3 py-2 bg-[#FFF8D9] border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#FF9B4A] focus:border-transparent resize-none text-[#2d2d2d] leading-relaxed text-sm ${
          error ? 'border-[#FF9B4A]' : 'border-[#e0e0e0]'
        } transition-all`}
      />
    );
  }

  return (
    <div>
      <label htmlFor="jobDescription" className="block text-sm font-medium text-[#4A4A4A] mb-3">
        Job description
      </label>
      <textarea
        id="jobDescription"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste the role description here..."
        rows={12}
        className={`w-full px-5 py-4 bg-white border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#E07A5F] focus:border-transparent resize-none text-[#1A1A1A] leading-relaxed text-base ${
          error ? 'border-[#FECACA]' : 'border-[#D4D4D4]'
        } transition-all`}
      />
      <div className="flex justify-between items-center mt-2">
        {error && <p className="text-sm text-[#991B1B]">{error}</p>}
        <p className="text-xs text-[#8B8B8B] ml-auto">{value.length} characters</p>
      </div>
    </div>
  );
};

export default JobDescriptionInput;
