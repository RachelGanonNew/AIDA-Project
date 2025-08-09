import React from 'react';
import { Card, CardContent, Box, Typography } from '@mui/material';

interface HealthCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ReactNode;
  color: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info';
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

  const getTrendIcon = (direction: string) => {
    switch (direction) {
      case 'up': return '↗';
      case 'down': return '↘';
      default: return '→';
    }
  };

  return (
    <Card
      variant="outlined"
  className={`healthcard-root${onClick ? ' healthcard-clickable' : ''}`}
      onClick={onClick}
    >
  <CardContent className="healthcard-content">
        <Box className="healthcard-main">
          <Box className={`healthcard-icon healthcard-icon-${color}`}>{icon}</Box>
          <Box>
            <Typography variant="body2" color="text.secondary">{title}</Typography>
            <Typography variant="h6" fontWeight={700}>{value}</Typography>
            {subtitle && (
              <Typography variant="caption" color="text.secondary">{subtitle}</Typography>
            )}
          </Box>
        </Box>
        {trend && (
          <Box className={`healthcard-trend healthcard-trend-${trend.direction}`}> 
            <Typography variant="body2" fontWeight={600}>
              {getTrendIcon(trend.direction)} {trend.value}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default HealthCard;