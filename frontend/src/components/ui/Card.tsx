import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  subtitle?: string;
  actions?: React.ReactNode;
}

const Card: React.FC<CardProps> = ({ children, className = '', title, subtitle, actions }) => {
  return (
    <div className={`bg-white rounded-lg shadow-sm border border-[#e0e0e0] ${className}`}>
      {(title || subtitle || actions) && (
        <div className="px-6 py-4 border-b border-[#e0e0e0] flex justify-between items-center">
          <div>
            {title && <h3 className="text-lg font-semibold text-[#2d2d2d]">{title}</h3>}
            {subtitle && <p className="text-sm text-[#666666] mt-1">{subtitle}</p>}
          </div>
          {actions && <div className="flex items-center space-x-2">{actions}</div>}
        </div>
      )}
      <div className="p-6">{children}</div>
    </div>
  );
};

export default Card;
