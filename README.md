# Saylani Medical Help Desk Dashboard

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Streamlit](https://img.shields.io/badge/streamlit-1.38.0-red)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.115.0-orange)](https://fastapi.tiangolo.com/)
[![Railway](https://img.shields.io/badge/deploy-railway-blueviolet)](https://railway.app/)

## Overview
The **Saylani Medical Help Desk** is an end‑to‑end analytics platform for a medical help‑desk system. It ingests raw appointment data, cleans and enriches it, generates analytical insights, and exposes them through:
- An interactive **Streamlit** dashboard for visual exploration.
- A **FastAPI** backend providing REST endpoints for programmatic access.
- An **LLM‑powered chatbot** that answers queries based on the generated knowledge base.

All emojis have been removed from the codebase to ensure a clean, production‑ready repository.

## Features
- **Data cleaning pipeline** – robust handling of timestamps, missing values, and categorical standardisation.
- **Automated EDA** – generates visualisations (trend lines, heatmaps, geographic distribution, etc.) and a summary report.
- **Knowledge‑base generation** – creates a JSON KB used by the LLM for context‑aware answers.
- **Streamlit dashboard** – real‑time visual analytics with metric cards, interactive charts and filters.
- **FastAPI service** – endpoints for analytics data and chatbot queries.
- **Rate‑limited LLM integration** – graceful fallback to the knowledge base when the Gemini API is unavailable or throttled.
- **Railway deployment ready** – configured for one-click cloud deployment.

## Architecture
```
┌─────────────────────┐   ┌─────────────────────┐
│   Raw CSV data      │   │   .env (secrets)    │
└─────────┬───────────┘   └─────────┬───────────┘
          │                         │
          ▼                         ▼
   ┌───────────────┐   ┌─────────────────────┐
   │ data_cleaning │   │   LLM (Gemini)      │
   └───────┬───────┘   └───────┬─────────────┘
           │               │
           ▼               ▼
   ┌─────────────────────┐   ┌─────────────────────┐
   │   JSON KB (analytics)│   │   FastAPI (REST)   │
   └───────┬─────────────┘   └───────┬─────────────┘
           │                         │
           ▼                         ▼
   ┌─────────────────────┐   ┌─────────────────────┐
   │   Streamlit UI      │   │   Chatbot endpoint │
   └─────────────────────┘   └─────────────────────┘
```
*The diagram is a textual representation; you can replace it with an image if desired.*

## Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/MuhammadHanzala-13/SaylaniMedicalAnalyticalDashboardUpdated.git
   cd SaylaniMedicalAnalyticalDashboardUpdated
   ```
2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # on Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in the required API keys (Gemini, etc.).
   - The `.gitignore` already excludes `.env` from being committed.

## Running the Pipeline
The pipeline processes the raw CSV, creates cleaned files, generates the knowledge base and the EDA report.
```bash
./run_pipeline.bat
```
All generated artefacts are placed under the `data/` folder.

## Launching the Dashboard
```bash
streamlit run src/dashboard.py
```
Open the displayed URL (usually `http://localhost:8501`) in a browser.

## Starting the API server
```bash
uvicorn src.app:app --reload
```
The API documentation is available at `http://localhost:8000/docs`.

## 🚀 Railway Deployment

### Quick Deploy
This project is configured for one-click deployment to Railway:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Railway"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to [Railway.app](https://railway.app/)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select this repository
   - Add environment variable: `GEMINI_API_KEY=your_key`
   - Railway will auto-deploy!

3. **Get Your API URL**
   - Railway assigns a URL like: `https://your-app.railway.app`
   - API docs at: `https://your-app.railway.app/docs`

### Frontend Integration
```javascript
// Use your Railway URL in frontend
const API_URL = 'https://your-app.railway.app';

// Example: Get disease trends
fetch(`${API_URL}/analytics/disease-trends`)
  .then(res => res.json())
  .then(data => console.log(data));
```

**📖 Detailed Guide:** See [`RAILWAY_DEPLOYMENT_GUIDE.md`](RAILWAY_DEPLOYMENT_GUIDE.md)  
**✅ Quick Checklist:** See [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md)  
**📊 Full Analysis:** See [`PROJECT_ANALYSIS.md`](PROJECT_ANALYSIS.md)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/analytics/disease-trends` | Disease statistics |
| GET | `/analytics/doctor-workload` | Doctor performance |
| GET | `/analytics/geographic-distribution` | Patient locations |
| GET | `/analytics/summary` | Executive summary |
| POST | `/chat/query` | AI chatbot query |
| POST | `/analytics/search` | Search knowledge base |

## Usage Example (Chatbot)
Send a POST request to `/chat/query` with JSON payload:
```json
{ "query": "What are the most common diseases?" }
```
The endpoint will return an answer generated by the LLM or fallback to the knowledge base.

## Testing
If you add tests, run them with:
```bash
pytest
```
(Tests are not included in the current version but can be added later.)

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes with clear messages.
4. Open a Pull Request targeting the `main` branch.

Make sure to run the linting and formatting tools before submitting.

## License
This project is licensed under the **MIT License** – see the `LICENSE` file for details.

## Acknowledgements
- **Streamlit** – for rapid UI development.
- **FastAPI** – for high‑performance API creation.
- **Google Gemini** – for LLM capabilities.
- **Railway** – for seamless cloud deployment.
- **Saylani Welfare Trust** – inspiration for the medical help‑desk use case.

---
*Last updated: 2025‑12‑11*