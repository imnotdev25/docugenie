import React from 'react';

const ColorBall = ({ color }) => {
  return (
    <div 
      className={`w-5 h-5 rounded-full ${color}`}
    ></div>
  );
};

export default ColorBall;
