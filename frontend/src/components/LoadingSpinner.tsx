import React from 'react';

interface LoadingSpinnerProps {
  size?: number;
  text?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ size = 32, text }) => (
  <div className="flex flex-col items-center justify-center" role="status" aria-live="polite" tabIndex={0}>
    <svg
      className="animate-spin text-blue-500"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
      />
    </svg>
    {text && <span className="mt-2 text-sm text-gray-500" aria-label={text}>{text}</span>}
  </div>
);

export default LoadingSpinner; 