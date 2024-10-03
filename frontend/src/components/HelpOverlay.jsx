import React from 'react';
import { Button } from "@/components/ui/button";
import { X } from "lucide-react";

const HelpOverlay = ({ onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Help</h2>
          <Button variant="ghost" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>
        <div className="mb-4">
          <h3 className="font-semibold mb-2">How to upload:</h3>
          <ol className="list-decimal list-inside">
            <li>Click the upload button next to the message input.</li>
            <li>Choose between file upload or web URLs.</li>
            <li>For file upload, select a file less than 5MB.</li>
            <li>For web URLs, enter the URLs separated by commas.</li>
            <li>Click the upload or done button to submit.</li>
          </ol>
        </div>
        <div>
          <h3 className="font-semibold mb-2">How to chat:</h3>
          <ol className="list-decimal list-inside">
            <li>Type your message in the input field.</li>
            <li>Press Enter or click the send button to send your message.</li>
            <li>Wait for the AI to respond to your query.</li>
          </ol>
        </div>
      </div>
    </div>
  );
};

export default HelpOverlay;