import React from 'react';
import { Inbox } from 'lucide-react';

interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
}

const EmptyState: React.FC<EmptyStateProps> = ({ icon, title, description, action }) => {
  const defaultIcon = icon || <Inbox className="w-16 h-16 text-[#999999]" />;

  return (
    <div className="flex flex-col items-center justify-center p-12 text-center">
      <div className="text-[#999999] mb-4">{defaultIcon}</div>
      <h3 className="text-lg font-semibold text-[#2d2d2d] mb-2">{title}</h3>
      {description && <p className="text-[#666666] mb-6 max-w-sm">{description}</p>}
      {action && <div>{action}</div>}
    </div>
  );
};

export default EmptyState;
