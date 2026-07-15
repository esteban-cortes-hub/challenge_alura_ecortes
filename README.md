# Alura Agente — Asistente de documentación iTop

Proyecto final desarrollado para el challenge **Alura Agente**.

La empresa donde trabaja el autor implementó un sistema en ITOP y entregó a los especialista una variedad de documentación para poder administrarlo.

La aplicación implementa un asistente de inteligencia artificial capaz de responder preguntas en lenguaje natural utilizando documentación técnica de iTop almacenada en archivos DOCX, Markdown y PDF.

El proyecto utiliza una arquitectura RAG (*Retrieval-Augmented Generation*) para recuperar información relevante desde una base vectorial y generar respuestas fundamentadas en los documentos disponibles.

## Objetivo

Facilitar la consulta de documentación técnica de iTop sin necesidad de abrir y revisar manualmente múltiples archivos.

El usuario puede realizar preguntas como:

* ¿Cuál es el endpoint para enviar licencias?
* ¿Cómo se autentica la integración?
* ¿Qué campos requiere la API?
* ¿Cómo se crea un objeto en iTop?
* ¿Qué componentes forman parte de la arquitectura?

El asistente busca los fragmentos más relevantes dentro de la documentación y utiliza Gemini para redactar una respuesta clara, incluyendo el nombre de los documentos consultados.

## Funcionalidades

* Lectura de documentos DOCX.
* Lectura de archivos Markdown.
* Lectura de archivos PDF con texto seleccionable.
* División de documentos en fragmentos solapados.
* Generación de embeddings con Gemini.
* Almacenamiento vectorial local con ChromaDB.
* Búsqueda semántica mediante LangChain.
* Generación de respuestas con Gemini.
* Visualización de las fuentes consultadas.
* Interfaz de chat desarrollada con Streamlit.
* Historial de conversación durante la sesión.
* Botón para iniciar una nueva conversación.
* Manejo básico de errores de configuración.

## Arquitectura

El proyecto está dividido en dos procesos principales.

### 1. Indexación de documentos

Este proceso se ejecuta al agregar o modificar documentos.

```text
Documentos DOCX, MD y PDF
          │
          ▼
       ingest.py
          │
          ▼
      loaders.py
          │
          ▼
Conversión a documentos LangChain
          │
          ▼
RecursiveCharacterTextSplitter
          │
          ▼
Embeddings de Gemini
          │
          ▼
       ChromaDB
```

Durante esta etapa:

1. Se leen los documentos almacenados en `docs/`.
2. El contenido se convierte en objetos `Document` de LangChain.
3. Los textos se dividen en fragmentos con solapamiento.
4. Cada fragmento se transforma en un vector numérico.
5. Los vectores, textos y metadatos se guardan en ChromaDB.

### 2. Consulta del usuario

Este proceso ocurre cada vez que el usuario realiza una pregunta.

```text
Usuario
   │
   ▼
Streamlit — app.py
   │
   ▼
Cadena RAG — chat.py
   │
   ▼
Retriever de LangChain
   │
   ▼
ChromaDB
   │
   ▼
Fragmentos relevantes
   │
   ▼
Prompt + Gemini
   │
   ▼
Respuesta y fuentes
```

La aplicación no vuelve a leer todos los documentos en cada consulta. Utiliza la base vectorial creada previamente durante la indexación.

## Tecnologías utilizadas

* Python
* Streamlit
* LangChain
* LangChain Classic
* Gemini
* Google Generative AI Embeddings
* ChromaDB
* python-docx
* PyPDF
* python-dotenv

## Estructura del proyecto

```text
challenge_alura_ecortes/
│
├── app.py
├── ingest.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── docs/
│   └── README.md
│
├── src/
│   ├── loaders.py
│   ├── rag.py
│   ├── chat.py
│   └── utils.py
│
├── data/
└── screenshots/
```

La carpeta `data/` se genera durante la indexación y contiene la base vectorial de ChromaDB.

## Requisitos

* Python 3.11 o superior.
* Una API Key válida de Gemini.
* Conexión a Internet durante la generación de embeddings y las consultas.

## Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/esteban-cortes-hub/challenge_alura_ecortes.git
cd challenge_alura_ecortes
```

### 2. Crear un entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## Configuración de Gemini

Copia el archivo de ejemplo:

En Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

En Linux:

```bash
cp .env.example .env
```

Edita el archivo `.env` e ingresa una API Key válida:

```env
GOOGLE_API_KEY=tu_api_key_de_gemini
```

El archivo `.env` está excluido mediante `.gitignore` y no debe subirse al repositorio.

## Documentación

Agrega los documentos que utilizará el agente dentro de:

```text
docs/
```

Formatos soportados:

```text
.docx
.md
.pdf
```

Los PDF deben contener texto seleccionable. Los documentos escaneados como imágenes requieren OCR, funcionalidad que no está incluida en esta versión.

Por razones de confidencialidad, la documentación privada utilizada en el entorno empresarial no forma parte del repositorio público.

## Crear la base vectorial

Después de agregar o modificar documentos, ejecuta:

```bash
python ingest.py
```

La aplicación realizará lo siguiente:

1. Leerá los documentos.
2. Dividirá el contenido en fragmentos.
3. Generará los embeddings.
4. Creará la base vectorial en `data/chroma`.

Este proceso debe repetirse cuando se agreguen o modifiquen documentos.

## Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación quedará disponible localmente en:

```text
http://localhost:8501
```

## Ejemplos de uso

### Pregunta

```text
¿Cuál es el endpoint para enviar licencias?
```

### Respuesta esperada

```text
El endpoint utilizado para enviar licencias es
/api/estructura-licencia/bulk.
```

La interfaz también muestra el nombre de los documentos recuperados como fuentes.

### Pregunta sin información disponible

```text
¿Cuál es la contraseña del servidor productivo?
```

Cuando la documentación no contiene información suficiente, el asistente debe indicar que no encontró la respuesta en la base documental.

## Privacidad y seguridad

Este repositorio no incluye:

* Documentación privada de la empresa.
* API Keys.
* Credenciales.
* Tokens.
* Bases vectoriales generadas desde documentación interna.

Los documentos privados pueden utilizarse localmente siempre que permanezcan excluidos mediante `.gitignore`.

## Despliegue en OCI

La aplicación será desplegada en una instancia de OCI Compute.

El proceso de despliegue incluirá:

1. Creación de una instancia Linux.
2. Instalación de Python y Git.
3. Clonación del repositorio.
4. Creación del archivo `.env`.
5. Instalación de dependencias.
6. Generación de la base vectorial.
7. Ejecución de Streamlit.
8. Apertura del puerto de acceso a la aplicación.

La URL pública y la captura de la aplicación serán agregadas después de finalizar el despliegue.

## Capturas

Las capturas de la aplicación se almacenarán en:

```text
screenshots/
```

## Historial de desarrollo

El proyecto fue construido de forma incremental, manteniendo commits separados para:

* Estructura inicial.
* Configuración del entorno.
* Lectura de documentos.
* Base vectorial.
* Integración con Gemini.
* Cadena RAG.
* Interfaz Streamlit.
* Mejoras visuales y manejo de errores.
* Documentación.
* Despliegue en OCI.

## Autor

Esteban Cortes

Proyecto desarrollado como trabajo final del curso de inteligencia artificial de Alura.
