🌍 Climate Policy Intelligence

Climate Policy Intelligence is a multi-provider Retrieval-Augmented Generation (RAG) application for analyzing climate policy, ESG, sustainability, and corporate climate reports.

Instead of manually searching through long reports, users can upload PDF documents and generate a structured intelligence overview covering climate risks, mitigation, adaptation, emissions, net-zero commitments, sustainability targets, water risks, energy transition, and SDG alignment.

The application currently supports OpenAI and Google Gemini, allowing users to choose their preferred AI provider and use their own API key.

Project status: MVP / actively under development

⸻

🎯 Why This Project?

Climate and sustainability reports often contain hundreds of pages of targets, emissions data, risk assessments, transition strategies, and policy commitments.

Finding specific information across these documents can be slow and inconsistent.

Climate Policy Intelligence is designed to transform these reports into structured, searchable evidence.

Rather than acting as a generic PDF chatbot, the project focuses specifically on extracting decision-relevant climate and sustainability intelligence.

⸻

✨ Current Features

📄 Multi-PDF Analysis

Upload one or multiple climate-related PDF reports for analysis.

Typical documents include:

* Sustainability reports
* ESG reports
* Climate transition plans
* Corporate annual reports
* Climate policy documents
* Net-zero strategies
* Adaptation and resilience plans

🔎 Retrieval-Augmented Generation

Documents are indexed using the selected provider’s file-search infrastructure.

Relevant evidence is retrieved from the uploaded reports before an answer is generated, reducing reliance on unsupported model knowledge.

🤖 Multi-Provider Architecture

The application currently supports:

OpenAI

* OpenAI Responses API
* OpenAI File Search
* Vector Store-based document retrieval

Google Gemini

* Gemini API
* Gemini File Search
* Gemini Embeddings

Users provide their own API key directly in the application.

API keys are not stored by the project.

🧠 Structured Climate Intelligence

A single comprehensive analysis generates reusable results for:

* 📋 Executive Summary
* 🌡️ Climate Risks
* 🌱 Adaptation
* 🏭 Mitigation
* 🎯 Net-Zero Commitments
* ☁️ Scope 1, 2 & 3 Emissions
* 📊 Sustainability Targets
* 💧 Water & Drought
* ⚡ Energy Transition
* 🌍 SDG Alignment

The analysis is cached within the Streamlit session, allowing users to navigate between categories without generating a new model request for every section.

💬 Custom RAG Questions

Users can also ask their own questions about the indexed reports.

Examples:

What are the company’s most important climate-related financial risks?

What Scope 3 reduction targets are mentioned in the report?

Which adaptation measures address water scarcity?

What interim targets exist before the company’s net-zero target?

Answers are generated using evidence retrieved from the uploaded documents.

💡 Document-Specific Suggested Questions

After analyzing the reports, the model generates follow-up questions based specifically on the uploaded content.

This helps users identify potentially important areas for deeper investigation.

🗜️ PDF Optimization

Before uploading, PDFs can optionally be structurally optimized using PyMuPDF.

The optimization process attempts to reduce file size while preserving the document’s text layer and avoiding unnecessary rasterization.

⸻

🏗️ Architecture

                        User
                          │
                          ▼
                  Streamlit Interface
                          │
                 Upload PDF Report(s)
                          │
                          ▼
                   PDF Optimization
                      (PyMuPDF)
                          │
                          ▼
                  Choose AI Provider
                    /           \
                   /             \
              OpenAI             Gemini
                │                   │
                ▼                   ▼
          Vector Store        File Search Store
                │                   │
                └─────────┬─────────┘
                          │
                          ▼
                  Document Indexing
                          │
                          ▼
                 Retrieval-Augmented
                     Generation
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
     Master Climate Analysis      Custom Questions
             │                         │
             ▼                         ▼
    Structured Intelligence      Evidence-Grounded
         Dashboard                   Answers

⸻

⚙️ Technology Stack

Component	Technology
Application	Python
Interface	Streamlit
OpenAI Integration	OpenAI Python SDK
Google Integration	Google GenAI SDK
Retrieval	OpenAI File Search / Gemini File Search
PDF Processing	PyMuPDF
Structured Data	Pydantic
Configuration	python-dotenv

⸻

📁 Project Structure

climate-policy-rag/
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── rag/
    ├── __init__.py
    ├── openai_rag.py
    ├── gemini_rag.py
    └── pdf_optimizer.py

app.py

Main Streamlit application.

Handles:

* provider selection
* API key input
* PDF uploads
* document preparation
* analysis generation
* intelligence dashboard
* custom questions

rag/openai_rag.py

OpenAI RAG implementation.

Handles:

* OpenAI client creation
* vector-store creation
* document upload and indexing
* File Search
* structured climate analysis
* custom report questions

rag/gemini_rag.py

Google Gemini RAG implementation.

Handles:

* Gemini client creation
* File Search store creation
* PDF indexing
* Gemini retrieval
* structured climate analysis
* custom report questions

rag/pdf_optimizer.py

PDF preprocessing and optimization using PyMuPDF.

⸻

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/onursenturky/climate-policy-rag.git
cd climate-policy-rag

⸻

2. Create a Virtual Environment

macOS / Linux

python -m venv .venv
source .venv/bin/activate

Windows

python -m venv .venv
.venv\Scripts\activate

⸻

3. Install Dependencies

pip install -r requirements.txt

⸻

4. Start the Application

streamlit run app.py

Streamlit will provide a local address, typically:

http://localhost:8501

Open it in your browser.

⸻

🔑 API Keys

Climate Policy Intelligence follows a Bring Your Own Key (BYOK) approach.

Users select an AI provider and enter their own API key.

OpenAI

Create an API key through the OpenAI developer platform.

OpenAI API usage is billed separately from ChatGPT subscriptions.

Google Gemini

Create a Gemini API key through Google AI Studio.

Gemini may provide free-tier API usage depending on Google’s current limits and policies.

Never commit API keys to GitHub.

The application accepts API keys at runtime and does not require API credentials to be stored in the repository.

⸻

🧪 Typical Workflow

1. Select OpenAI or Gemini
        ↓
2. Enter API key
        ↓
3. Upload report(s)
        ↓
4. Optimize PDFs
        ↓
5. Prepare Reports
        ↓
6. Documents are indexed
        ↓
7. Generate Report Intelligence
        ↓
8. Explore climate categories
        ↓
9. Ask custom RAG questions

⸻

💰 API Efficiency

The MVP is designed to reduce unnecessary model requests.

Instead of generating a new request whenever a user opens a dashboard category, the application performs one comprehensive analysis and stores the structured result in the current Streamlit session.

Report indexing
      │
      ▼
Master analysis ──────► Structured result
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
             Risks       Net Zero      Adaptation
                 │            │            │
                 └──── No additional ─────┘
                        model request

Custom questions intentionally generate additional API requests because they require new retrieval and generation.

⸻

🔐 Privacy & Security

API keys should never be committed to the repository.

The .gitignore configuration excludes common sensitive and local files such as:

.env
.venv/
__pycache__/
*.pyc
.DS_Store
.streamlit/secrets.toml

Users should also consider the data-handling policies of their selected AI provider before uploading confidential, proprietary, or sensitive corporate documents.

⸻

🗺️ Roadmap

The current version establishes the core RAG pipeline.

Planned improvements include:

Evidence & Citations

Display the supporting document and page/source for individual findings.

Net-zero target: 2050
Source:
Sustainability Report 2025 — p. 42

Multi-Report Comparison

Compare organizations, reports, or reporting periods across common climate dimensions.

                         Company A     Company B
Net Zero                   2050          2040
Scope 3 Target              ✓             ✓
Water Target                ✓             —
Transition Plan             ✓             ✓

Structured Evidence Extraction

Extract climate indicators into reusable structured datasets, including:

* emissions
* target years
* baseline years
* renewable-energy targets
* water targets
* climate risks
* adaptation measures
* transition investments

Report Metadata

Track:

* organization
* report title
* publication year
* reporting period
* document type
* source

Export

Export analysis results to formats such as:

* CSV
* JSON
* PDF
* structured research tables

Improved Session & Storage Management

Future versions will improve:

* document hashing
* persistent analysis caching
* vector-store lifecycle management
* duplicate detection
* provider switching

Climate Intelligence Layer

Longer-term development will move beyond document Q&A toward comparative climate intelligence across organizations, sectors, policies, and reporting periods.

⸻

🔬 Research Direction

The project is particularly relevant to workflows involving:

* climate-policy analysis
* sustainability research
* ESG intelligence
* corporate climate disclosures
* systematic evidence synthesis
* climate-risk assessment
* transition-plan analysis
* net-zero commitment tracking

A longer-term objective is to combine RAG with structured extraction and comparative analysis so that large collections of climate documents can be transformed into queryable evidence rather than isolated PDF conversations.

⸻

⚠️ Current Limitations

This project is currently an MVP.

Important limitations include:

* Generated results should be verified against original documents.
* Citation extraction is not yet fully implemented.
* Analysis quality depends on document quality and retrieval performance.
* Scanned PDFs may require additional OCR processing.
* API availability, pricing, rate limits, and model capabilities depend on the selected provider.
* Streamlit session data is not currently designed as permanent storage.
* Repeated document preparation may create additional provider-side file/vector resources.

The application should therefore be treated as a research and analysis assistant rather than an authoritative source.

⸻

🤝 Contributing

The project is currently under active development.

Issues, ideas, and contributions related to climate NLP, RAG, document intelligence, sustainability reporting, information retrieval, and structured climate-data extraction are welcome.

⸻

👨‍💻 Author

Onur Şentürk

Geomatics Engineering
Istanbul Technical University (ITU)

Interests:

GIS · Climate Technology · Sustainability · Artificial Intelligence · Spatial Data · Climate Policy

⸻

📄 License

A license has not yet been selected for this project.

If you intend to reuse or distribute the code, please check the repository for updated licensing information.

⸻

Climate Policy Intelligence

Turning climate reports into structured, searchable intelligence.
