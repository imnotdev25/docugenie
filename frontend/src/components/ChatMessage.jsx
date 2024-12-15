import React from 'react';

const ChatMessage = ({ message }) => {
  const isUser = message.type === 'user';

  return (
      <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
          {!isUser && (
              <div className="w-8 h-8 rounded-full flex items-center justify-center mr-3 bg-gray-400 overflow-hidden">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" viewBox="0 0 20 20"
                       fill="currentColor">
                      <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"/>
                      <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"/>
                  </svg>
              </div>
          )}
          <div className={`max-w-[70%] p-3 rounded-lg ${isUser ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
              <p>{message.content}</p>
          </div>
          {isUser && (
              <div className="w-8 h-8 rounded-full flex items-center justify-center ml-3 bg-blue-600 overflow-hidden">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" viewBox="0 0 20 20"
                       fill="currentColor">
                      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                            clipRule="evenodd"/>
                  </svg>
              </div>

          )}

      </div>
  );
};

export default ChatMessage;