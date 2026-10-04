# COMICCRAFT — AI Comic Story Creator

ComicCraft is a complete, production-ready AI application that converts natural-language story prompts into illustrated, multi-panel comic books.

---

## 🌟 Key Features

- **Multi-Stage AI Pipeline**:
  1. **Story Analysis**: Extracts core narrative arc, genre, character specs, and themes.
  2. **Character Bible**: Maintains consistent character visual attributes (species, clothing, eyes, colors, personality) across panels.
  3. **Structured Comic Outline**: Plans sequential 4, 6, 8, or 10-panel comic layouts using Pydantic JSON validation.
  4. **Panel Scripting**: Generates concise narration captions, dialogue speech bubbles, speaker tags, and sound effects.
  5. **Visual Prompt Engineering & Continuity**: Combines character bible, scene environment, lighting, camera angles, and previous panel context for coherent visual artwork.
- **Speech Bubble Overlay System**: Dialogue and captions are dynamically rendered as vector overlays, preventing distorted AI text.
- **Interactive Comic Editor**:
  - Edit panel titles, narration text, and dialogue lines.
  - Change speech bubble types (`speech`, `thought`, `shout`, `whisper`).
  - Regenerate panel artwork without touching story context.
  - Regenerate dialogue without regenerating artwork.
  - Add, delete, and reorder comic panels.
- **Export Engine**:
  - Export professional **PDF Comic Books** with custom cover page and structured page layouts.
  - Export **Composite PNG Pages** ready for publishing.
- **Offline & Fallback Support**:
  - Abstracted `ImageProvider` with `GeminiImageProvider` (using official `google-genai` SDK) and built-in fallback canvas generator for zero-downtime development and offline testing.
- **Built-in Demo Project**: Seeded demo ("Free the Fox in Enchanted Forest") rendered using the real application canvas engine.

---

## 🏗️ Tech Stack

### Frontend
- **Framework**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS + Lucide Icons + Bangers Comic Typography
- **Routing**: React Router 6

### Backend
- **Framework**: Python FastAPI
- **Database**: SQLite with SQLAlchemy 2.0 ORM & Pydantic v2 validation
- **AI SDK**: Google official `google-genai` SDK
- **Exporting**: ReportLab (PDF) + PIL / Pillow (Composite PNG Rendering)

---

## 📁 Project Structure

```
comiccraft/
├── backend/
│   ├── app/
│   │   ├── ai/               # Gemini client, story analyzer, character bible, prompt builder, image generator
│   │   ├── exporters/        # PDF and PNG comic composition exporters
│   │   ├── generators/       # Page layout grid calculation
│   │   ├── models/           # SQLAlchemy database tables (project, character, panel, export)
│   │   ├── routes/           # REST API endpoints (health, projects, panels, export)
│   │   ├── schemas/          # Pydantic v2 data validation schemas
│   │   ├── services/         # Orchestrator pipeline, storage service, project service
│   │   ├── utils/            # Logger and filename sanitization
│   │   ├── config.py         # Environment & App configuration
│   │   ├── database.py       # DB engine and session
│   │   └── main.py           # FastAPI application entry point
│   ├── tests/                # Pytest unit & integration tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # Navbar, ComicCanvas, PanelCard, PanelEditor, SpeechBubbleOverlay, ExportModal
│   │   ├── pages/            # HomePage, CreateComicPage, PreviewComicPage, DashboardPage
│   │   ├── services/         # API client
│   │   └── types/            # TypeScript interfaces
│   ├── package.json
│   └── vite.config.ts
├── prompts/                  # AI prompt templates
├── storage/                  # Generated project assets, panel artwork & exports
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start & Installation

### 1. Environment Setup

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Configure your Gemini API key inside `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_TEXT_MODEL=gemini-2.5-flash
GEMINI_IMAGE_MODEL=imagen-3.0-generate-002
```

*(Note: If no API key is provided, ComicCraft automatically falls back to its built-in canvas generator, allowing full application functionality and testing.)*

### 2. Backend Setup & Startup

Install Python dependencies:

```bash
pip install -r backend/requirements.txt
```

Run backend server:

```bash
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Verify backend health at: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

### 3. Frontend Setup & Startup

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Open browser at: [http://localhost:5173](http://localhost:5173)

---

## 🧪 Running Automated Tests

Run backend unit & schema tests:

```bash
$env:PYTHONPATH="."
python -m pytest backend/tests
```

All 6 tests verify API health, database CRUD operations, schema validation, and demo project generation.

---

## 🎨 Interactive User Workflow

1. **Homepage**: Click **"Create Your Comic"** or **"View Built-in Demo"**.
2. **Create Page**: Enter story prompt, character name, setting, tone, art style, and panel count (4, 6, 8, 10, or AUTO).
3. **Generation Stage**: Watch multi-stage AI progress (Story Analysis -> Character Bible -> Outline -> Scripts -> Artwork).
4. **Comic Canvas Preview**: View full multi-panel comic with speech bubbles, narration boxes, and panel badges.
5. **Interactive Editor**: Click **Edit** on any panel to change dialogue lines, narration, or trigger single-panel image/story regeneration.
6. **Export**: Click **Export Comic** to download a high-resolution PDF comic book or composite PNG pages.
