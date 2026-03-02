import React from 'react';

interface LogoProps {
  className?: string;
  lightMode?: boolean;
}

const Logo: React.FC<LogoProps> = ({ className = "h-16 w-auto", lightMode = false }) => {
  const primaryFill = lightMode ? "#ffffff" : "#1a1a1a";
  const moneyFill = lightMode ? "#1a1a1a" : "#ffffff";
  
  return (
    <svg 
      className={className} 
      viewBox="0 0 250 60" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
    >
      <text x="5" y="38" fontFamily="Arial, sans-serif" fontWeight="bold" fontSize="28" fill={primaryFill}>
        Dolar<tspan fill="#C8A045">Express</tspan>
      </text>
      <circle cx="220" cy="30" r="18" fill="#C8A045"/>
      <text x="213" y="38" fontFamily="Arial, sans-serif" fontWeight="bold" fontSize="24" fill={moneyFill}>$</text>
    </svg>
  );
};

export default Logo;