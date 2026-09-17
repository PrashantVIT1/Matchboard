import React, { useState, useRef, useEffect } from 'react';
import { RefreshCw, Download, ChevronDown } from 'lucide-react';

export interface ExportFormat {
  type: 'csv' | 'excel' | 'pdf';
  label: string;
  onClick: () => void;
}

export interface Action {
  type: 'refresh' | 'export' | 'export-dropdown' | 'custom';
  icon?: React.ReactNode;
  label: string;
  onClick: () => void;
  loading?: boolean;
  disabled?: boolean;
  disabledTooltip?: string;
  exportFormats?: ExportFormat[];
}

interface HeaderActionsProps {
  actions: Action[];
  className?: string;
}

const HeaderActions: React.FC<HeaderActionsProps> = ({ actions, className = '' }) => {
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const dropdownRefs = useRef<Record<string, HTMLDivElement | null>>({});

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (openDropdown) {
        const dropdown = dropdownRefs.current[openDropdown];
        if (dropdown && !dropdown.contains(event.target as Node)) {
          setOpenDropdown(null);
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [openDropdown]);

  const handleActionClick = (action: Action, index: string) => {
    if (action.disabled) return;

    if (action.type === 'export-dropdown') {
      setOpenDropdown(openDropdown === index ? null : index);
    } else {
      action.onClick();
    }
  };

  const handleExportFormatClick = (format: ExportFormat) => {
    format.onClick();
    setOpenDropdown(null);
  };

  const getDefaultIcon = (type: Action['type'], loading?: boolean) => {
    if (type === 'refresh') {
      return <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />;
    }
    if (type === 'export' || type === 'export-dropdown') {
      return <Download className="w-4 h-4" />;
    }
    return null;
  };

  return (
    <div className={`flex flex-wrap gap-2 ${className}`}>
      {actions.map((action, index) => {
        const actionId = `action-${index}`;
        const icon = action.icon || getDefaultIcon(action.type, action.loading);

        return (
          <div key={index} className="relative" ref={(el) => (dropdownRefs.current[actionId] = el)}>
            <button
              onClick={() => handleActionClick(action, actionId)}
              disabled={action.disabled || action.loading}
              className={`
                flex items-center justify-center gap-2 px-4 py-2
                bg-white border border-gray-300 rounded-lg
                hover:bg-gray-50 transition-colors
                min-h-[44px] min-w-[100px]
                disabled:bg-gray-50 disabled:text-gray-400 disabled:cursor-not-allowed
                focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                text-sm font-medium text-gray-700
              `}
              title={action.disabled ? action.disabledTooltip : action.label}
              aria-label={action.label}
              aria-disabled={action.disabled}
            >
              {icon}
              <span>{action.label}</span>
              {action.type === 'export-dropdown' && !action.disabled && (
                <ChevronDown className="w-4 h-4" />
              )}
            </button>

            {action.type === 'export-dropdown' && 
             openDropdown === actionId && 
             !action.disabled && 
             action.exportFormats && (
              <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                {action.exportFormats.map((format, fmtIndex) => (
                  <button
                    key={fmtIndex}
                    onClick={() => handleExportFormatClick(format)}
                    className="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors text-sm text-gray-700 focus:outline-none focus:bg-gray-50"
                  >
                    {format.label}
                  </button>
                ))}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default HeaderActions;
