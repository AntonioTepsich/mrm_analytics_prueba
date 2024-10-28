// app/api/extract/route.ts
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    // Obtener el FormData desde la solicitud
    const formData = await request.formData();
    const file = formData.get('file');
    const type = formData.get('type');


    // Verificar si se ha proporcionado un archivo válido
    if (!file || !(file instanceof Blob)) {
      return NextResponse.json({ error: 'No se proporcionó un archivo válido' }, { status: 400 });
    }

    if (!type) {
      return NextResponse.json({ error: 'No se proporcionó un tipo válido de extractor' }, { status: 400 });
    }

    // Crear un nuevo FormData para reenviar al backend
    const backendFormData = new FormData();
    backendFormData.append('file', file, 'uploaded.pdf'); // Añadir un nombre de archivo adecuado
    backendFormData.append('type', type.toString()); // Añadir el tipo de extractor

    // Hacer la solicitud al backend de FastAPI
    const backendResponse = await fetch('http://127.0.0.1:8000/api/v1/extract-pdf', {
      method: 'POST',
      body: backendFormData,
    });

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      console.error('Error del backend:', errorText);
      return NextResponse.json({ error: 'Error al comunicarse con el backend' }, { status: backendResponse.status });
    }

    const data = await backendResponse.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('Error en el API interno:', error);
    return NextResponse.json({ error: 'Error al procesar el archivo' }, { status: 500 });
  }
}

