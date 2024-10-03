import React, { useEffect, useState } from 'react';
import { X } from 'lucide-react';

const Toast = ({ message, onClose }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      onClose();
    }, 3000);

    return () => clearTimeout(timer);
  }, [onClose]);

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded-md shadow-lg flex items-center">
      <span>{message}</span>
      <button onClick={() => setIsVisible(false)} className="ml-2">
        <X size={16} />
      </button>
    </div>
  );
};

export default Toast;