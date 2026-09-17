import React from 'react';
import { Filter as FilterIcon, X } from 'lucide-react';

interface FilterOption {
  label: string;
  value: string;
}

interface FilterProps {
  label: string;
  options: FilterOption[];
  value: string;
  onChange: (value: string) => void;
  onClear?: () => void;
}

const Filter: React.FC<FilterProps> = ({ label, options, value, onChange, onClear }) => {
  return (
    <div className="flex flex-col space-y-2">
      <label className="text-sm font-medium text-gray-700 flex items-center">
        <FilterIcon className="w-4 h-4 mr-2" />
        {label}
      </label>
      <div className="relative">
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none bg-white"
        >
          <option value="">All</option>
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        {value && onClear && (
          <button
            onClick={() => onClear()}
            className="absolute right-8 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
          >
            <X className="w-4 h-4" />
          </button>
        )}
        <div className="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
          <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
    </div>
  );
};

export default Filter;
