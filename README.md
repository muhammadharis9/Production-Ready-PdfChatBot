# 💎 FileSense: Enterprise Document Intelligence

**FileSense** is a production-ready **Retrieval-Augmented Generation (RAG)** application designed to transform how you interact with your data. Built with a modern **FastAPI** backend and a sleek, corporate-themed **Streamlit** frontend, FileSense allows you to upload PDFs and get precise, context-aware answers through a suite of specialized AI agents.



---

## 📖 Table of Contents
* [What is RAG?](#-what-is-rag)
* [Tech Stack](#-tech-stack)
* [Key Features](#-key-features)
* [Project Structure](#-project-structure)
* [Getting Started (Local)](#-getting-started-local)
* [Dockerization (The Easy Way)](#-dockerization-the-easy-way)
* [How to Use](#-how-to-use)

---

## 🤖 What is RAG?

If you are new to AI, **RAG (Retrieval-Augmented Generation)** is a technique that gives a Large Language Model (like Gemini) access to specific data it wasn't originally trained on—like your private company PDFs.

**How it works in FileSense:**
1. **Ingestion:** You upload a PDF.
2. **Chunking & Embedding:** The system breaks the PDF into small pieces and converts them into mathematical vectors.
3. **Storage:** These vectors are stored in **ChromaDB**.
4. **Retrieval:** When you ask a question, FileSense finds the most relevant pieces of your PDF.
5. **Augmentation:** It combines those pieces with your question and sends them to the AI to generate a grounded, factual answer.



---

## 🛠 Tech Stack

* **Frontend:** Streamlit (Custom "FileSense Blue" Theme)
* **Backend:** FastAPI (High-performance Asynchronous Python)
* **LLM:** Google Gemini 1.5 Flash
* **Vector Database:** ChromaDB
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
* **Package Manager:** `uv` (Fastest Python package management)

---

## ✨ Key Features

* **Specialized AI Agents:** Toggle between "Legal", "Finance", "HR", and more to refine the focus of your queries.
* **Corporate UI:** A modern, high-contrast professional interface designed for enterprise usability.
* **Real-time Connectivity:** Live health checks in the sidebar to monitor backend and database status.
* **Full Containerization:** Deploy anywhere instantly with Docker and Docker Compose.
* **Lightning Fast:** Optimized dependency resolution and build times using `uv`.

---

## 📁 Project Structure

```text
FileSense/
├── app/                  # FastAPI Backend logic
│   ├── api/              # API Endpoints (Chat, Upload)
│   ├── core/             # Database & Security Configuration
│   ├── services/         # RAG Engine & AI Logic
│   └── main.py           # Backend Entrypoint
├── chroma_db_data/       # Persistent Vector Storage
├── logo.png              # FileSense Branding
├── ui.py                 # Streamlit Frontend Interface
├── pyproject.toml        # Environment & Dependencies
├── Dockerfile            # Container definition
└── docker-compose.yml    # Multi-service orchestration