// app/layout.tsx
import React from 'react';
import './globals.css';

export const metadata = {
  title: 'Extractor de Texto de PDF',
  description: 'Extrae texto de tus archivos PDF',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
