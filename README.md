<p align="center">
  <img src="https://i.postimg.cc/mrzQQ23m/notes-Gravity.png" alt="NotesGravity Logo" width="200"/>
</p>

<h1 align="center">NotesGravity AI</h1>

<p align="center">
  <strong>An AI Note-Taking Transformer that destroys grammar to maximize meaning.</strong>
  <br>
  <br>
  <img src="https://img.shields.io/badge/Model-BART_Base-blue" alt="Model">
  <img src="https://img.shields.io/badge/Frontend-Streamlit-FF4B4B" alt="Frontend">
  <img src="https://img.shields.io/badge/Backend-Gradio_%7C_HuggingFace-F9AB00" alt="Backend">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

<hr>

## 🧠 What is NotesGravity?

Standard LLMs produce fluent, grammatically correct summaries. **NotesGravity does not.** NotesGravity is a fine-tuned `facebook/bart-base` Transformer designed with a singular philosophy: *Grammar is a bug, not a feature.* It reads complex textbook paragraphs, articles, or transcripts and compresses them into terse, symbolic, bullet-ready notes optimized for extreme memory recall.

### Core Capabilities
* **Extreme Compression:** Translates verbose text into dense logic using native Unicode symbols (`→`, `↑`, `↓`, `∝`, `+`).
* **Infinite Context Window:** Uses intelligent NLTK sentence-chunking to process entire pages of text without hitting context limits or OOM errors.
* **Serverless Architecture:** The heavy lifting is handled by a merged model hosted on the Hugging Face Serverless Inference API, accessed via an ultra-lightweight Streamlit frontend.

---

## ⚡ Examples

**Input Text:**
> *Photosynthesis converts sunlight into chemical energy through chlorophyll in plant cells, producing glucose and oxygen.*

**Generated Note:**
> • Photosynthesis: sunlight → chlorophyll → energy → glucose + O₂ → cell energy

**Input Text:**
> *The central limit theorem states that the distribution of sample means approaches normality as sample size increases.*

**Generated Note:**
> • Central limit theorem: sample mean distribution approaches normality as sample size ↑

---

## 🏗️ System Architecture

NotesGravity operates on a decoupled frontend/backend architecture for maximum efficiency and VRAM safety.

1. **The Model:** `facebook/bart-base` aggressively fine-tuned using LoRA (targeting `q_proj`, `v_proj`). The adapters were permanently merged back into the base model to allow for instant, serverless API deployment.
2. **The Backend (Gradio API):** Hosted on Hugging Face Spaces. It intercepts the incoming text, utilizes `nltk.tokenize` to break large paragraphs into safe single-sentence chunks, processes them through the model, and stitches the bullet points back together.
3. **The Frontend (Streamlit):** A lightweight dashboard using `gradio_client` to communicate with the cloud API. It requires no local ML libraries, making it lightning-fast to run.

---

## 🚀 Quick Start (Local Frontend)

Since the model is hosted in the cloud, running the NotesGravity UI locally takes seconds.

### 1. Clone the repository
```bash
git clone [https://github.com/Priyanshu-i/NotesGravity.git](https://github.com/Priyanshu-i/NotesGravity.git)
cd NotesGravity