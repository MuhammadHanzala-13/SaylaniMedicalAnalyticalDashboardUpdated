# 🚀 Railway Deployment Guide - Saylani Medical Help Desk Backend

This guide will help you deploy your FastAPI backend to Railway and connect it to your frontend.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Deployment Steps](#deployment-steps)
4. [Environment Variables](#environment-variables)
5. [Testing Your API](#testing-your-api)
6. [Connecting Frontend](#connecting-frontend)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

Before deploying, ensure you have:

- ✓ A [Railway account](https://railway.app/) (free tier available)
- ✓ Your project pushed to GitHub
- ✓ Gemini API key (from Google AI Studio)
- ✓ Basic understanding of REST APIs

---

## 📁 Project Structure

Your backend is now configured with these deployment files:

```
SaylaniHealthMangementHelpDesk V2.0/
├── src/
│   ├── app.py              # Main FastAPI application
│   ├── json_kb.py          # Knowledge base loader
│   ├── llm.py              # LLM generator with fallback
│   └── ...
├── data/
│   ├── knowledge_base/     # JSON knowledge base (auto-generated)
│   └── ...
├── requirements.txt        # Python dependencies (✓ Updated)
├── Procfile               # Railway start command (✓ Created)
├── railway.json           # Railway configuration (✓ Created)
├── runtime.txt            # Python version (✓ Created)
├── .railwayignore         # Files to exclude (✓ Created)
├── .env.example           # Environment template
└── README.md              # Project documentation
```

---

## 🚀 Deployment Steps

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Prepare backend for Railway deployment"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy to Railway

1. **Go to [Railway.app](https://railway.app/)** and sign in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `SaylaniHealthMangementHelpDesk V2.0`
5. Railway will automatically detect the configuration

### Step 3: Configure Environment Variables

In Railway dashboard:

1. Go to your project
2. Click on **"Variables"** tab
3. Add the following environment variables:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
PORT=8000
```

**Important:** Replace `your_actual_gemini_api_key_here` with your real Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Step 4: Deploy

Railway will automatically:
- ✓ Install dependencies from `requirements.txt`
- ✓ Start the FastAPI server using the `Procfile`
- ✓ Assign a public URL (e.g., `https://your-app.railway.app`)

---

## 🔐 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Your Google Gemini API key | `AIzaSy...` |
| `PORT` | Server port (auto-set by Railway) | `8000` |

### Optional Variables (for future expansion)

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Deployment environment | `production` |
| `LOG_LEVEL` | Logging verbosity | `info` |

---

## 🧪 Testing Your API

Once deployed, Railway will provide a URL like: `https://your-app.railway.app`

### Test Endpoints

#### 1. **Health Check**
```bash
curl https://your-app.railway.app/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "kb_loaded": true,
  "api_available": true
}
```

#### 2. **Root Endpoint**
```bash
curl https://your-app.railway.app/
```

**Expected Response:**
```json
{
  "message": "Saylani Medical Help Desk API - Refactored",
  "version": "2.0",
  "features": [
    "JSON Knowledge Base",
    "Analytics-driven chatbot",
    "Smart API fallback",
    "No voice features"
  ]
}
```

#### 3. **Chat Query**
```bash
curl -X POST https://your-app.railway.app/chat/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the most common diseases?"}'
```

#### 4. **Analytics Endpoints**

**Disease Trends:**
```bash
curl https://your-app.railway.app/analytics/disease-trends
```

**Doctor Workload:**
```bash
curl https://your-app.railway.app/analytics/doctor-workload
```

**Geographic Distribution:**
```bash
curl https://your-app.railway.app/analytics/geographic-distribution
```

**Summary:**
```bash
curl https://your-app.railway.app/analytics/summary
```

### Interactive API Documentation

Railway automatically serves FastAPI's interactive docs:

- **Swagger UI:** `https://your-app.railway.app/docs`
- **ReDoc:** `https://your-app.railway.app/redoc`

---

## 🔗 Connecting Frontend

### Option 1: JavaScript/React Frontend

```javascript
// config.js
const API_BASE_URL = 'https://your-app.railway.app';

// Example: Fetch disease trends
async function getDiseaseTrends() {
  const response = await fetch(`${API_BASE_URL}/analytics/disease-trends`);
  const data = await response.json();
  return data;
}

// Example: Ask chatbot
async function askChatbot(question) {
  const response = await fetch(`${API_BASE_URL}/chat/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query: question })
  });
  const data = await response.json();
  return data;
}
```

### Option 2: Python Frontend (Streamlit)

Update your Streamlit dashboard to use the Railway API:

```python
import requests

API_BASE_URL = "https://your-app.railway.app"

# Example: Get disease trends
def get_disease_trends():
    response = requests.get(f"{API_BASE_URL}/analytics/disease-trends")
    return response.json()

# Example: Ask chatbot
def ask_chatbot(query):
    response = requests.post(
        f"{API_BASE_URL}/chat/query",
        json={"query": query}
    )
    return response.json()
```

### CORS Configuration (if needed)

If your frontend is on a different domain, add CORS middleware to `src/app.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Troubleshooting

### Issue 1: Build Fails

**Problem:** Railway build fails with dependency errors

**Solution:**
```bash
# Test locally first
pip install -r requirements.txt

# If specific package fails, update requirements.txt
# Example: Change version constraints
pandas>=2.0.0  # Instead of pandas==2.1.0
```

### Issue 2: Knowledge Base Not Found

**Problem:** API returns "Knowledge base not found"

**Solution:**
The knowledge base is auto-generated. Ensure:
1. `data/cleaned/appointments.csv` exists
2. Run the data pipeline before deployment
3. Or deploy with pre-generated KB files

### Issue 3: Gemini API Errors

**Problem:** 429 errors or quota exceeded

**Solution:**
The app automatically falls back to JSON knowledge base extraction. No action needed - this is expected behavior with free tier.

### Issue 4: Port Binding Error

**Problem:** "Address already in use"

**Solution:**
Railway automatically sets the `PORT` environment variable. The app is configured to use it.

### Issue 5: Slow Cold Starts

**Problem:** First request takes long

**Solution:**
Railway's free tier has cold starts. Consider:
- Upgrading to Railway Pro
- Implementing a health check ping service
- Using Railway's "Keep Alive" feature

---

## 📊 Monitoring & Logs

### View Logs in Railway

1. Go to your Railway project
2. Click on **"Deployments"**
3. Select the latest deployment
4. View real-time logs

### Common Log Messages

```
✓ "Loaded JSON Knowledge Base" - KB loaded successfully
✓ "Gemini API initialized successfully" - LLM ready
⚠ "Gemini API not available - using fallback" - Using KB fallback
⚠ "API Failure: 429 Resource exhausted" - Rate limited (normal)
```

---

## 🎯 Next Steps

1. **Custom Domain:** Add your own domain in Railway settings
2. **Database:** Add PostgreSQL for persistent data storage
3. **Caching:** Implement Redis for faster responses
4. **Monitoring:** Add Sentry or LogRocket for error tracking
5. **CI/CD:** Set up automatic deployments on git push

---

## 📞 Support

- **Railway Docs:** https://docs.railway.app/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Project Issues:** https://github.com/YOUR_USERNAME/YOUR_REPO/issues

---

## 🎉 Success Checklist

- [ ] Backend deployed to Railway
- [ ] Environment variables configured
- [ ] Health check endpoint working
- [ ] API documentation accessible at `/docs`
- [ ] Chat endpoint responding
- [ ] Analytics endpoints working
- [ ] Frontend connected to Railway URL
- [ ] CORS configured (if needed)

---

**Congratulations! Your backend is now live on Railway! 🚀**

Your API URL: `https://your-app.railway.app`

Share this URL with your frontend team or use it in your applications.
