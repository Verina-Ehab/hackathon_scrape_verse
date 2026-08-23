# ⚡ JOGO City-Pulse: Self-Healing Cultural Quest & Merchant Ingestion Engine

> **Autonomous, Self-Healing Real-World Game Quest & Merchant Pipeline Powered by Bright Data Scraper Studio & Gemini AI**

[![Bright Data](https://img.shields.io/badge/Powered%20By-Bright%20Data%20Scraper%20Studio-blue?style=for-the-badge&logo=databricks)](https://brightdata.com/)
[![Gemini AI](https://img.shields.io/badge/Enriched%20With-Google%20Gemini%203.5%20Flash-orange?style=for-the-badge&logo=google)](https://aistudio.google.com/)
[![Built for](https://img.shields.io/badge/Platform-JOGO%20Mobile%20App-emerald?style=for-the-badge)](https://github.com/)

---

## 📌 1. Project Overview

**JOGO City-Pulse** is an automated, self-healing data ingestion and game design pipeline built for **JOGO**—an AI-powered gamified social wellness platform that bridges the gap between digital screen addiction and real-world urban exploration.

Instead of manually designing hundreds of location quests and cold-calling cafes, **JOGO City-Pulse** utilizes **Bright Data Scraper Studio** to autonomously crawl live venue listings (amenities, customer review highlights, opening schedules, and pricing), repairs itself when site layouts change via **Self-Healing**, and transforms raw scraped data into **culturally authentic, localized game quests** (Riddles, AI Vision Lens Targets, and Time-Gated Mega Quests) ready for direct ingestion into a **PostgreSQL / Supabase** backend.

---

## 🏗️ 2. System Architecture

┌──────────────────────────────────────────────────────────────────────────────────┐
│ JOGO CITY-PULSE PIPELINE │
├──────────────────────────────────────────────────────────────────────────────────┤
│ │
│ [ Public Venue Directories ] (TripAdvisor / F&B Catalogs) │
│ │ │
│ ▼ │
│ ┌──────────────────────────────────────────────────────────────────────────┐ │
│ │ 1. BRIGHT DATA SCRAPER STUDIO (Multi-Level Crawler) │ │
│ │ • Extracts: Venue Name, Category, Address, Phone, Sub-Ratings, │ │
│ │ Features, Operating Hours, Price Level, Review Highlights │ │
│ │ • Resilient: Automatic Self-Healing on DOM layout/selector changes │ │
│ └──────────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ (raw_venues.json) │
│ ┌──────────────────────────────────────────────────────────────────────────┐ │
│ │ 2. CULTURAL AI ENRICHMENT ENGINE (Python + Gemini 3.5 Flash) │ │
│ │ • Bilingual Cultural Localization (Alexandrian Egyptian Slang & EN) │ │
│ │ • Synthesizes: Rhyming Riddles, AI Camera Targets, Off-Peak Deals │ │
│ │ • Supabase DDL Compliance & Geocoding Mapping │ │
│ └──────────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ (jogo_quests.json) │
│ ┌────────────────────────────────────┬─────────────────────────────────────┐ │
│ │ A. Interactive Map Visualizer │ B. JOGO Production Backend │ │
│ │ (Leaflet.js / Dark-Neon Theme) │ (Supabase PostgreSQL Table) │ │
│ └────────────────────────────────────┴─────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────┘

---

## 🌟 3. Key Features

### 1. Multi-Level Deep Web Extraction

- Traverses public category listings to scrape complete, rich venue profiles without authentication barriers.
- Extracts structured metadata: exact street addresses, contact phone numbers, operating schedules, multi-dimensional rating breakdowns (Atmosphere, Food, Service, Value), and customer quote highlights.

### 2. Built-in Self-Healing Scraper Architecture

- Web directories frequently alter CSS classes and DOM hierarchies. With **Bright Data Scraper Studio**, the scraper detects structural failures, recalculates element selectors automatically, and resumes data collection with zero code rewrites or downtime.

### 3. Cultural AI Quest Generation (Bilingual)

- Converts raw venue data into interactive gameplay assets tailored to city culture:
  - **Witty Alexandrian/Egyptian Riddles (`riddle_ar`):** Culturally authentic rhyming riddles based on signature items.
  - **Global English Riddles (`riddle_en`):** Accessible for international travelers and expats.
  - **Lens Hunter Targets (`target_object_prompt`):** Computer vision physical targets derived from interior decor and customer reviews for on-device AI camera verification.
  - **Mega Quest Time-Gated Deals (`mega_quest_deal`):** Dynamic off-peak discount windows (e.g., 1:00 PM - 4:00 PM) calculated from operating hours to drive foot traffic during dead hours.

### 4. 100% Supabase PostgreSQL DDL Compliant

- Generated output maps directly to JOGO's production `public.treasures` database schema with full UUID compliance, coordinate mappings, and check-constraint alignments.

---

## 🛠️ 4. How Bright Data Scraper Studio is Used

1. **Scraper Definition:** Created a custom multi-level scraper using Scraper Studio natural language prompts to target venue directories.
2. **Schema Configuration:** Configured structured field extractors for parent cards and nested sub-pages (address, phone, hours, review snippets, sub-ratings).
3. **Execution:** Triggered via Bright Data's cloud runtime using proxy management and automated browser unblocking to extract structured venue datasets.
4. **Self-Healing in Action:** When tested against DOM structure changes (e.g., modified rating and review class containers), Scraper Studio's AI analyzed the new layout and regenerated working selectors seamlessly.

---

## 📁 5. Repository Structure

hackathon_scrape_verse/
├── enricher.py # Cultural AI data enrichment pipeline (Gemini API)
├── raw_venues.json # Raw structured output from Bright Data Scraper Studio
├── jogo_quests.json # Enriched bilingual quests matching JOGO Supabase schema
├── index.html # Interactive Dark-Neon Leaflet.js Quest Visualizer
├── .gitignore # Environment & credential protection
└── README.md # Project documentation

---

## 🚀 6. Getting Started / How to Run

### Prerequisites

- Python 3.9+
- A Google Gemini API Key ([Get it for free at Google AI Studio](https://aistudio.google.com/))

### Installation & Execution

````bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/jogo-city-pulse.git
cd jogo-city-pulse

# 2. Set your Gemini API Key
export GEMINI_API_KEY="your-gemini-api-key-here"

# 3. Run the Cultural AI Enrichment Pipeline
python3 enricher.py

### Launch Interactive Map Demo

Open `index.html` in any modern web browser or serve it locally:

```bash
# Python simple HTTP server
python3 -m http.server 8000
# Open http://localhost:8000 in your browser

---

## 📊 7. Example Output Preview (`jogo_quests.json`)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "PuffyPops",
  "title_en": "PuffyPops",
  "title_ar": "بافي بوبس",
  "location": "35 Abd El-Moneim Riad, Abu An Nawatir, Alexandria 00203 Egypt",
  "city": "Alexandria",
  "lat": 31.2335,
  "lng": 29.9542,
  "reward_coins": 300,
  "rating": 5.0,
  "category": "food",
  "clue_ar": "مدورة ومنفوخة خفيفة، بتروق المود وتطيرك لسابع سما في إسكندرية.. مغرقانا بنوتيلا أو كيندر وبيسمونا أحلى تحلية. تفتكر إيه هي؟",
  "clue_en": "Fluffy, light, and golden bites drizzled with warm Nutella and melted Kinder chocolate in the heart of Alexandria.. What am I?",
  "riddle_answer": "Puffy Pops",
  "riddle_answer_ar": "بافي بوبس",
  "riddle_accepted_answers": [
    "PuffyPops",
    "Puffy Pops",
    "بافي بوبس",
    "باف بوبس"
  ],
  "target_object_prompt": "A freshly served plate of Kinder or Nutella Puffy Pops drizzled with melted chocolate sauce",
  "target_object_prompt_ar": "طبق بافي بوبس مغطى بصلصة النوتيلا أو الكيندر",
  "is_lens_hunter": true,
  "is_pulse_radar": true,
  "is_mega": false,
  "geofence_radius_meters": 70,
  "radar_found_radius_meters": 15
}

---

## 👥 8. Built By

- **Verina Ehab** — Founder, CEO & Lead Systems Architect at **JOGO**
- _Built for the "Into the Scrape-Verse" Hackathon organized by WeMakeDevs & Bright Data._


````
