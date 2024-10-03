import React from 'react';
import { Button } from "@/components/ui/button.jsx";
import { useNavigate } from 'react-router-dom';
import ColorBall from '@/components/ColorBall.jsx';
import Fastapi from '@/assets/fastapi.svg';
import ReactIcon from '@/assets/react.svg';
import Langchain from '@/assets/langchain.svg';
import OpenAI from '@/assets/openai.svg';
import ChromaDB from '@/assets/chroma.svg';
import VectorSearch from '@/assets/elasticsearch.svg';

const Index = () => {
  const navigate = useNavigate();

  const techStack = [
    { name: 'FastAPI', image: Fastapi, color: 'bg-teal-500' },
    { name: 'ReactJS', image: ReactIcon, color: 'bg-blue-500' },
    { name: 'Open AI', image: OpenAI, color: 'bg-black' },
    { name: 'Lang Chain', image: Langchain, color: 'bg-green-500' },
    { name: 'Chroma DB', image: ChromaDB, color: 'bg-yellow-500' },
    { name: 'Vector Search', image: VectorSearch, color: 'bg-pink-700' },
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4 relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 -left-10 w-48 md:w-72 h-48 md:h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute top-1/3 -right-10 w-48 md:w-72 h-48 md:h-72 bg-red-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
        <div className="absolute -bottom-8 left-1/4 w-48 md:w-72 h-48 md:h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-6000"></div>
        <div className="absolute -top-10 right-1/4 w-48 md:w-72 h-48 md:h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute bottom-1/3 left-1/3 w-48 md:w-72 h-48 md:h-72 bg-green-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-8000"></div>
      </div>
      <div className="relative z-10 text-center mb-12">
        <h1 className="text-4xl md:text-6xl font-bold mb-6 text-gray-800 mt-20">DocuGenie</h1>
        <p className="text-lg md:text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Are You Facing Difficulties With Your Website? Do You Have A Website But Lack Traffic? No Need To Worry.
        </p>
        <Button onClick={() => navigate('/chat')} className="bg-black text-white hover:bg-gray-800 text-base md:text-lg px-6 md:px-8 py-2 md:py-3">
          Get Started
        </Button>
      </div>
      <div className="w-full max-w-4xl relative z-10">
        <h2 className="text-2xl md:text-3xl font-semibold mb-8 text-center text-gray-800">Tech Stack</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 md:gap-8">
          {techStack.map((tech, index) => (
            <div key={index} className="bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg rounded-xl shadow-lg relative aspect-square overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-transparent via-white to-transparent opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
              <div className="absolute inset-0 flex flex-col items-center justify-between p-4">
                <div className="flex-1 flex items-center justify-center mt-4 md:mt-8">
                  <img src={`${tech.image}`} alt={tech.name} className="w-12 h-12 md:w-16 md:h-16 transition-transform duration-300 group-hover:scale-110" />
                </div>
                <div className="mb-4 md:mb-8">
                  <span className="text-sm md:text-lg font-medium text-center text-gray-800">{tech.name}</span>
                </div>
              </div>
              <div className="absolute top-3 right-3">
                <ColorBall color={tech.color} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Index;
