"use client";

import React, { useState } from 'react';

const Home: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedType, setSelectedType] = useState<string>('test_1');
  const [extractedText, setExtractedText] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
      setExtractedText('');
    }
  };

  const handleTypeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedType(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!selectedFile) {
      alert('Por favor, selecciona un archivo PDF');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('type', selectedType);

    setIsLoading(true);

    try {
      const response = await fetch('/api/extract', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setExtractedText(data.text);
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.error}`);
      }
    } catch (error) {
      console.error('Error al enviar el archivo:', error);
      alert('Hubo un problema al conectarse con la API interna');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (selectedFile && extractedText) {
      const element = document.createElement('a');
      const fileBlob = new Blob([extractedText], { type: 'text/plain' });
      element.href = URL.createObjectURL(fileBlob);
      element.download = `${selectedFile.name.replace(/\.[^/.]+$/, '')}.txt`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    }
  };

  const handleClear = () => {
    setExtractedText('');
  };

  return (
    <div className="min-h-screen bg-gray-200 flex items-center justify-center p-8">
      <div className="bg-white rounded-lg shadow-lg p-10 max-w-xl w-full relative">
        <h1 className="text-3xl font-extrabold mb-8 text-center text-gray-900">Extractor de Texto de PDF</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="block w-full text-lg text-gray-700 border border-gray-400 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
          </div>

          <div className="flex flex-col space-y-2">
            <label htmlFor="type" className="text-lg font-semibold text-gray-800">
              Selecciona el tipo de documento:
            </label>
            <select
              id="type"
              value={selectedType}
              onChange={handleTypeChange}
              className="block w-full p-3 border text-gray-800 border-gray-400 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <option value="test_1">Test 1</option>
              <option value="test_2">Test 2</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-3 px-5 rounded-md text-white font-bold transition-colors ${
              isLoading
                ? 'bg-teal-400 cursor-not-allowed'
                : 'bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-4 focus:ring-teal-300'
            }`}
          >
            {isLoading ? 'Procesando...' : 'Subir y Extraer Texto'}
          </button>
        </form>

        {isLoading && (
          <p className="mt-6 text-center text-lg font-medium text-teal-700">Procesando el archivo, por favor espera...</p>
        )}

        {extractedText && (
          <>
          <div className=''>
            <button
              onClick={handleClear}
              className={`mt-1 w-full py-3 px-5 rounded-md font-bold transition-colors text-white bg-red-500 hover:bg-red-700 focus:outline-none`}
            >
              Limpiar
            </button>
            <button
              onClick={handleDownload}
              className="mt-1 w-full py-3 px-5 rounded-md bg-blue-600 text-white font-bold hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-teal-300"
            >
              Descargar
            </button>
          </div>
          <div className="mt-10 bg-teal-50 p-6 rounded-md">
            <h2 className="text-2xl font-bold mb-4 text-teal-900">Texto Extraído:</h2>
            <p className="text-lg text-gray-800 whitespace-pre-wrap">{extractedText}</p>
            <button
              onClick={handleDownload}
              className="mt-4 w-full py-3 px-5 rounded-md bg-teal-600 text-white font-bold hover:bg-teal-700 focus:outline-none focus:ring-4 focus:ring-teal-300"
            >
              Descargar
            </button>
          </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Home;
