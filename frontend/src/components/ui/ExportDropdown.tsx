import React, { useState, useRef, useEffect } from 'react';
import { Download, ChevronDown } from 'lucide-react';

interface ExportDropdownProps {
  onExportCSV: () => void;
  onExportExcel: () => void;
  disabled?: boolean;
  disabledTooltip?: string;
}

const ExportDropdown: React.FC<ExportDropdownProps> = ({
  onExportCSV,
  onExportExcel,
  disabled = false,
  disabledTooltip = 'No data available to export.'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleExportCSV = () => {
    onExportCSV();
    setIsOpen(false);
  };

  const handleExportExcel = () => {
    onExportExcel();
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => !disabled && setIsOpen(!isOpen)}
        disabled={disabled}
        className={`flex items-center space-x-2 px-4 py-2 border rounded-lg transition-colors ${
          disabled
            ? 'border-gray-200 bg-gray-50 text-gray-400 cursor-not-allowed'
            : 'border-gray-300 bg-white hover:bg-gray-50'
        }`}
        title={disabled ? disabledTooltip : ''}
      >
        <Download className="w-4 h-4" />
        <span>Export</span>
        {!disabled && <ChevronDown className="w-4 h-4" />}
      </button>

      {isOpen && !disabled && (
        <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
          <button
            onClick={handleExportCSV}
            className="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors text-sm"
          >
            Export as CSV
          </button>
          <button
            onClick={handleExportExcel}
            className="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors text-sm"
          >
            Export as Excel
          </button>
        </div>
      )}
    </div>
  );
};

export default ExportDropdown;
