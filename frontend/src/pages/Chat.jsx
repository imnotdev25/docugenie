import React, { useState, useEffect, useRef } from 'react';
import { Button } from "@/components/ui/button.jsx";
import { Textarea } from "@/components/ui/textarea.jsx";
import { Send, HelpCircle, Upload, Loader } from "lucide-react";
import UploadOverlay from '@/components/UploadOverlay.jsx';
import HelpOverlay from '@/components/HelpOverlay.jsx';
import ChatMessage from '@/components/ChatMessage.jsx';
import Toast from '@/components/Toast.jsx';
import { useNavigate, useParams } from 'react-router-dom';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [showUpload, setShowUpload] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [warning, setWarning] = useState(false);
  const [toast, setToast] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const textareaRef = useRef(null);
  const navigate = useNavigate();
  const { uuid } = useParams();

  useEffect(() => {
    if (uuid) {
      fetchChatHistory(uuid);
    }
  }, [uuid]);

  const fetchChatHistory = async (uuid) => {
    try {
      const response = await fetch(`${process.env.API_URL}/api/query/history`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ uuid }),
      });
      if (response.ok) {
        const history = await response.json();
        setMessages(history);
      }
    } catch (error) {
      console.error('Error fetching chat history:', error);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (inputMessage.trim()) {
      setMessages([...messages, { type: 'user', content: inputMessage }]);
      setInputMessage('');
      setIsLoading(true);

      try {
        const response = await fetch(`${process.env.API_URL}/api/query/${uuid}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query: inputMessage }),
        });

        if (response.ok) {
          const botResponse = await response.json();
          setMessages(prev => [...prev, { type: 'bot', content: botResponse.response }]);
        } else {
          setToast({ message: 'Failed to get response from server', type: 'error' });
        }
      } catch (error) {
        console.error('Error sending message:', error);
        setToast({ message: 'Error sending message', type: 'error' });
      } finally {
        setIsLoading(false);
      }
    } else {
      setWarning(true);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  const handleTextareaChange = (e) => {
    setInputMessage(e.target.value);
  };

  const handleUploadSuccess = async (fileName) => {
    setToast({ message: `File '${fileName}' Uploaded`, type: 'success' });
    setIsLoading(true);
    try {
      const response = await fetch(`${process.env.API_URL}/api/upload`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fileName }),
      });
      if (response.ok) {
        const { uuid } = await response.json();
        navigate(`/chat/${uuid}`);
      } else {
        setToast({ message: 'Failed to process uploaded file', type: 'error' });
      }
    } catch (error) {
      console.error('Error processing upload:', error);
      setToast({ message: 'Error processing upload', type: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}
      </div>
      <form onSubmit={handleSendMessage} className="p-4 bg-white border-t">
        <div className="flex items-center space-x-2">
          <Button type="button" variant="outline" onClick={() => setShowUpload(true)} className="h-10 w-10 p-0 flex items-center justify-center">
            <Upload className="h-4 w-4" />
          </Button>
          <Button type="button" variant="outline" onClick={() => setShowHelp(true)} className="h-10 w-10 p-0 flex items-center justify-center">
            <HelpCircle className="h-4 w-4" />
          </Button>
          <div className="flex-1 relative">
            <Textarea
              ref={textareaRef}
              value={inputMessage}
              onChange={handleTextareaChange}
              onKeyDown={handleKeyDown}
              placeholder="Type a new message here"
              className={`w-full py-2 px-3 resize-none ${warning ? 'border-red-500' : ''}`}
              style={{
                height: '40px',
                minHeight: '40px',
                maxHeight: '40px',
                overflow: 'hidden',
                transition: 'border-color 0.3s ease',
              }}
            />
          </div>
          <Button type="submit" className="h-10 w-10 p-0 flex items-center justify-center">
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </form>
      {showUpload && <UploadOverlay onClose={() => setShowUpload(false)} onUploadSuccess={handleUploadSuccess} />}
      {showHelp && <HelpOverlay onClose={() => setShowHelp(false)} />}
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
      {isLoading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <Loader className="animate-spin text-white" size={48} />
        </div>
      )}
    </div>
  );
};

export default Chat;