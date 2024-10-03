import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { X, Upload, Link, Check } from "lucide-react";

const UploadOverlay = ({ onClose, onUploadSuccess }) => {
  const [isFileUpload, setIsFileUpload] = useState(true);
  const [webUrls, setWebUrls] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isFileUpload && selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);

      try {
        const response = await fetch(`${process.env.API_URL}/api/upload`, {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const { uuid } = await response.json();
          onUploadSuccess(selectedFile.name);
          onClose();
        } else {
          console.error('Upload failed');
        }
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    } else if (!isFileUpload && webUrls) {
      // Handle web URL upload
      console.log('Web URLs:', webUrls);
      onUploadSuccess('Web URLs');
      onClose();
    }
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Upload</h2>
          <Button variant="ghost" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>
        <div className="flex mb-4">
          <Button
            variant={isFileUpload ? "default" : "outline"}
            onClick={() => setIsFileUpload(true)}
            className="flex-1 mr-2"
          >
            <Upload className="h-4 w-4 mr-2" /> File
          </Button>
          <Button
            variant={!isFileUpload ? "default" : "outline"}
            onClick={() => setIsFileUpload(false)}
            className="flex-1 ml-2"
          >
            <Link className="h-4 w-4 mr-2" /> Web URLs
          </Button>
        </div>
        <form onSubmit={handleSubmit}>
          {isFileUpload ? (
            <div className="border-2 border-dashed border-gray-300 p-4 text-center rounded-lg mb-4">
              <p>Upload File</p>
              <p className="text-sm text-gray-500">Documents less than 5MB</p>
              <Input type="file" className="hidden" id="fileUpload" onChange={handleFileChange} />
              <Button variant="outline" className="mt-2" onClick={() => document.getElementById('fileUpload').click()}>
                <Upload className="h-4 w-4 mr-2" /> Choose File
              </Button>
              {selectedFile && <p className="mt-2 text-sm">{selectedFile.name}</p>}
            </div>
          ) : (
            <Input
              value={webUrls}
              onChange={(e) => setWebUrls(e.target.value)}
              placeholder="Enter web URLs (url_1, url_2, ...)"
              className="mb-4"
            />
          )}
          <Button type="submit" className="w-full">
            {isFileUpload ? (
              <>
                <Upload className="h-4 w-4 mr-2" /> Upload
              </>
            ) : (
              <>
                <Check className="h-4 w-4 mr-2" /> Done
              </>
            )}
          </Button>
        </form>
      </div>
    </div>
  );
};

export default UploadOverlay;