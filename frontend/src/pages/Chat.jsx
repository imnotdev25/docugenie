import React, { useState, useEffect, useRef } from 'react';
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Send, HelpCircle, Upload, Loader2 } from "lucide-react";
import UploadOverlay from '@/components/UploadOverlay';
import HelpOverlay from '@/components/HelpOverlay';
import ChatMessage from '@/components/ChatMessage';
import { useNavigate, useParams } from 'react-router-dom';
import { useToast } from "@/components/ui/use-toast";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [showUpload, setShowUpload] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();
  const { uuid } = useParams();
  const { toast } = useToast();

  // Fetch chat history when component mounts or uuid changes
  useEffect(() => {
    if (uuid) {
      fetchChatHistory();
    }
  }, [uuid]);

  // Auto scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchChatHistory = async () => {
    try {
      const resp = await fetch(
          `${import.meta.env.VITE_API_URL}/documents/${uuid}/chat-history`
      );

      if (!resp.ok) {
        throw new Error('Failed to fetch chat history');
      }

      const history = await resp.json();
      setMessages(history.flatMap(msg => [
        { type: 'user', content: msg.user_input },
        { type: 'assistant', content: msg.assistant_response },
      ]));
    } catch (error) {
      console.error('Error fetching chat history:', error);
      toast({
        title: "Error",
        description: "Failed to load chat history",
        variant: "destructive",
      });
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);

    // Add user message immediately
    setMessages(prev => [...prev, { type: 'user', content: userMessage }]);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: userMessage,
          doc_uuid: uuid,
          limit: 5
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      // Add assistant's response
      setMessages(prev => [...prev, {
        type: 'assistant',
        content: data.gpt_response
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
      toast({
        title: "Error",
        description: "Failed to get response from assistant",
        variant: "destructive",
      });
      // Remove the user's message if there was an error
      // setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  useEffect(() => {
    if (!uuid) {
      toast({
        title: "No Document Selected",
        description: "Please upload a document to continue",
        variant: "destructive",
      });
    }
  }, [uuid]);


  return (
      <div className="flex flex-col h-screen bg-gray-50">
        <div className="flex-1 overflow-y-auto p-4">
          {messages.map((message, index) => (
              <ChatMessage key={index} message={message} />
          ))}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSendMessage} className="p-4 bg-white border-t">
          <div className="flex items-center space-x-2">
            <Button
                type="button"
                variant="outline"
                onClick={() => setShowUpload(true)}
                className="h-10 w-10 p-0"
            >
              <Upload className="h-4 w-4" />
            </Button>
            <Button
                type="button"
                variant="outline"
                onClick={() => setShowHelp(true)}
                className="h-10 w-10 p-0"
            >
              <HelpCircle className="h-4 w-4" />
            </Button>

            <div className="flex-1">
              <Textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Type your message..."
                  className="min-h-[40px] max-h-[200px]"
                  disabled={isLoading}
              />
            </div>

            <Button
                type="submit"
                disabled={isLoading || !inputMessage.trim()}
                className="h-10 w-10 p-0"
            >
              {isLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                  <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
        </form>

        {showUpload && (
            <UploadOverlay onClose={() => setShowUpload(false)} />
        )}
        {showHelp && (
            <HelpOverlay onClose={() => setShowHelp(false)} />
        )}
      </div>
  );
};

export default Chat;
