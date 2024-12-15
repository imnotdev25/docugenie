import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { X, Upload, Link } from "lucide-react";
import { useNavigate } from 'react-router-dom';
import { useToast } from "@/components/ui/use-toast";

const UploadOverlay = ({ onClose }) => {
  const [isFileUpload, setIsFileUpload] = useState(true);
  const [url, setUrl] = useState(''); // Changed from webUrls to url
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      let response;

      if (isFileUpload && selectedFile) {
        // File upload
        const formData = new FormData();
        formData.append('file', selectedFile);

        response = await fetch(`${import.meta.env.VITE_API_URL}/upload/file`, {
          method: 'POST',
          body: formData,
        });
      } else if (!isFileUpload && url.trim()) {
        // URL upload
        response = await fetch(`${import.meta.env.VITE_API_URL}/upload/url`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: url.trim() }), // Changed payload structure
        });
      } else {
        throw new Error('Please provide a file or URL');
      }

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Upload failed');
      }

      const data = await response.json();

      toast({
        title: "Success",
        description: isFileUpload
            ? "Document uploaded successfully!"
            : "URL processed successfully!",
      });

      navigate(`/chat/${data.doc_uuid}`);
    } catch (error) {
      console.error('Upload error:', error);
      toast({
        title: "Error",
        description: error.message || "Failed to process document",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
      onClose();
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.size > 5 * 1024 * 1024) { // 5MB limit
      toast({
        title: "Error",
        description: "File size should be less than 5MB",
        variant: "destructive",
      });
      return;
    }
    setSelectedFile(file);
  };

  return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-background p-6 rounded-lg w-full max-w-md">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">Upload Document</h2>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>

          <div className="flex mb-4 gap-2">
            <Button
                variant={isFileUpload ? "default" : "outline"}
                onClick={() => setIsFileUpload(true)}
                className="flex-1"
            >
              <Upload className="h-4 w-4 mr-2" /> File
            </Button>
            <Button
                variant={!isFileUpload ? "default" : "outline"}
                onClick={() => setIsFileUpload(false)}
                className="flex-1"
            >
              <Link className="h-4 w-4 mr-2" /> URL
            </Button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {isFileUpload ? (
                <div className="border-2 border-dashed border-muted rounded-lg p-4 text-center">
                  <Input
                      type="file"
                      id="file"
                      className="hidden"
                      onChange={handleFileChange}
                      accept=".pdf,.doc,.docx,.txt"
                  />
                  <Button
                      type="button"
                      variant="outline"
                      onClick={() => document.getElementById('file').click()}
                  >
                    <Upload className="h-4 w-4 mr-2" />
                    Choose File
                  </Button>
                  {selectedFile && (
                      <p className="mt-2 text-sm text-muted-foreground">
                        {selectedFile.name}
                      </p>
                  )}
                </div>
            ) : (
                <Input
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Enter URL"
                    type="url"
                    className="w-full"
                />
            )}

            <Button
                type="submit"
                className="w-full"
                disabled={isLoading || (!selectedFile && !url)}
            >
              {isLoading ? (
                  <>Loading...</>
              ) : (
                  <>
                    <Upload className="h-4 w-4 mr-2" />
                    Upload
                  </>
              )}
            </Button>
          </form>
        </div>
      </div>
  );
};

export default UploadOverlay;
