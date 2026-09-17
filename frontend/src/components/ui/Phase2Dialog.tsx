import React from 'react';
import { Info, FileText, AlertCircle, Zap, Clock, TrendingUp } from 'lucide-react';
import Modal from './Modal';
import Button from './Button';

export interface Phase2FeatureConfig {
  title: string;
  description: string;
  plannedFeatures: string[];
  icon?: 'info' | 'report' | 'alert' | 'realtime' | 'activity' | 'growth';
  buttonText?: string;
}

interface Phase2DialogProps {
  isOpen: boolean;
  onClose: () => void;
  config: Phase2FeatureConfig;
}

const iconMap = {
  info: Info,
  report: FileText,
  alert: AlertCircle,
  realtime: Zap,
  activity: Clock,
  growth: TrendingUp,
};

const Phase2Dialog: React.FC<Phase2DialogProps> = ({ isOpen, onClose, config }) => {
  const IconComponent = config.icon ? iconMap[config.icon] : Info;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={config.title}
    >
      <div className="text-center mb-6">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
          <IconComponent className="w-8 h-8 text-blue-600" />
        </div>
      </div>
      <div className="text-gray-700 mb-6">
        <p className="mb-4">{config.description}</p>
        <p className="text-sm text-gray-600 mb-4">Planned functionality:</p>
        <ul className="text-sm text-gray-600 space-y-2 ml-4 list-disc">
          {config.plannedFeatures.map((feature, index) => (
            <li key={index}>{feature}</li>
          ))}
        </ul>
      </div>
      <div className="flex justify-center">
        <Button onClick={onClose}>
          {config.buttonText || 'Close'}
        </Button>
      </div>
    </Modal>
  );
};

export default Phase2Dialog;
