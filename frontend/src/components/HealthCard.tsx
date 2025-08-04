import React from 'react';
import { motion } from 'framer-motion';

interface HealthCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ReactNode;
  color: string;
  trend?: {
    direction: 'up' | 'down' | 'stable';
    value: string;
  };
  onClick?: () => void;
}

const HealthCard: React.FC<HealthCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  color,
  trend,
  onClick
}) => {
  const getTrendColor = (direction: string) => {
    switch (direction) {
      case 'up': return 'text-green-400';
      case 'down': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getTrendIcon = (direction: string) => {
    switch (direction) {
      case 'up': return '↗';
      case 'down': return '↘';
      default: return '→';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-slate-800 rounded-lg p-6 border border-slate-700 ${onClick ? 'cursor-pointer hover:bg-slate-750 transition-colors' : ''}`}
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <div className={`p-2 rounded-lg ${color}`}>
            {icon}
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-400">{title}</p>
            <p className="text-2xl font-semibold text-white">{value}</p>
            {subtitle && (
              <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
            )}
          </div>
        </div>
        {trend && (
          <div className={`text-right ${getTrendColor(trend.direction)}`}>
            <div className="text-sm font-medium">
              {getTrendIcon(trend.direction)} {trend.value}
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default HealthCard; 