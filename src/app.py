"""
Refactored FastAPI Application
- JSON knowledge base support
- No voice features
- Smart API fallback
- Analytics-driven chatbot
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import pandas as pd
import os

from src.json_kb import JSONKnowledgeBase
from src.llm import LLMGenerator

app = FastAPI(title="Saylani Medical Help Desk API - Refactored")

# Add CORS middleware for frontend connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize components
kb = JSONKnowledgeBase()
llm = LLMGenerator()

# Models
class QueryRequest(BaseModel):
    query: str

class AnalyticsRequest(BaseModel):
    metric: str  # 'disease_trends', 'doctor_workload', 'geographic_distribution'

# Endpoints

@app.get("/")
def root():
    return {
        "message": "Saylani Medical Help Desk API - Refactored",
        "version": "2.0",
        "features": [
            "JSON Knowledge Base",
            "Analytics-driven chatbot",
            "Smart API fallback",
            "No voice features"
        ]
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "kb_loaded": kb.kb_data is not None,
        "api_available": llm.api_available
    }

@app.get("/analytics/disease-trends")
def get_disease_trends():
    """Get disease trends from JSON KB"""
    try:
        if kb.kb_data is None:
            raise HTTPException(status_code=503, detail="Knowledge base not loaded")
        
        data = kb.query_disease_trends()
        
        if not data:
            raise HTTPException(status_code=404, detail="Disease trends data not found in knowledge base")
        
        return {"success": True, "data": data}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_disease_trends: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/analytics/doctor-workload")
def get_doctor_workload():
    """Get doctor workload from JSON KB"""
    try:
        if kb.kb_data is None:
            raise HTTPException(status_code=503, detail="Knowledge base not loaded")
        
        data = kb.query_doctor_workload()
        
        if not data:
            raise HTTPException(status_code=404, detail="Doctor workload data not found in knowledge base")
        
        return {"success": True, "data": data}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_doctor_workload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/analytics/geographic-distribution")
def get_geographic_distribution():
    """Get geographic distribution from JSON KB"""
    try:
        if kb.kb_data is None:
            raise HTTPException(status_code=503, detail="Knowledge base not loaded")
        
        data = kb.query_geographic_distribution()
        
        if not data:
            raise HTTPException(status_code=404, detail="Geographic distribution data not found in knowledge base")
        
        return {"success": True, "data": data}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_geographic_distribution: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/analytics/summary")
def get_summary():
    """Get executive summary from JSON KB"""
    try:
        if kb.kb_data is None:
            raise HTTPException(status_code=503, detail="Knowledge base not loaded")
        
        data = kb.query_summary()
        
        if not data:
            raise HTTPException(status_code=404, detail="Summary data not found in knowledge base")
        
        return {"success": True, "data": data}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/chat/query")
def chat_query(request: QueryRequest):
    """
    Analytics chatbot endpoint
    - Uses Gemini API if available
    - Falls back to JSON KB extraction if API fails/quota exceeded
    """
    try:
        # Detect query type
        query_lower = request.query.lower()
        
        # Keywords that indicate analytics queries
        analytics_keywords = [
            'trend', 'workload', 'busy', 'most common', 'prevalent', 
            'distribution', 'geographic', 'branch', 'area', 'location',
            'summary', 'analytics', 'dashboard', 'statistics', 'data',
            'how many', 'total', 'count', 'patients', 'visits', 'cases',
            'top', 'highest', 'lowest', 'average', 'comparison', 'compare'
        ]
        
        # Keywords that indicate medical questions
        medical_keywords = [
            'symptom', 'treatment', 'cure', 'medicine', 'diagnosis',
            'difference between', 'what is', 'how to treat', 'causes of',
            'prevent', 'contagious', 'infection', 'disease information',
            'sinus', 'cold', 'flu', 'fever', 'pain', 'ache'
        ]
        
        # Check if it's a medical question
        is_medical = any(keyword in query_lower for keyword in medical_keywords)
        is_analytics = any(keyword in query_lower for keyword in analytics_keywords)
        
        # If it's clearly a medical question and not analytics
        if is_medical and not is_analytics:
            return {
                "success": True,
                "query": request.query,
                "answer": """**Medical Information Notice**

I'm an **Analytics Assistant** for the Saylani Medical Help Desk, designed to provide insights about:
- Disease trends and statistics
- Doctor workload and availability
- Geographic distribution of patients
- Help desk performance metrics

**I cannot provide medical advice or information about diseases, symptoms, or treatments.**

For medical questions like yours, please:
1. **Consult a qualified healthcare professional**
2. **Visit a Saylani Medical Help Desk branch**
3. **Call our medical hotline for professional advice**

However, I can help you with questions like:
- "What are the most common diseases in our help desk?"
- "Which doctors are available in Gulshan area?"
- "What is the patient volume trend this month?"
- "Which branch has the highest workload?"

Would you like to ask an analytics-related question instead?""",
                "source": "System Response",
                "api_used": False,
                "query_type": "medical_question"
            }
        
        # Get full context from JSON KB for analytics queries
        context_text = kb.get_full_context()
        
        # Generate answer (with automatic fallback)
        answer = llm.generate_answer(request.query, context_text)
        
        # Determine actual source
        source_type = "Gemini API" if llm.api_available and "Extracted from Analytics Knowledge Base" not in answer else "JSON Knowledge Base (Fallback)"
        
        return {
            "success": True,
            "query": request.query,
            "answer": answer,
            "source": source_type,
            "api_used": llm.api_available,
            "query_type": "analytics"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analytics/search")
def search_analytics(request: QueryRequest):
    """
    Search JSON KB for specific analytics data
    Returns structured JSON data
    """
    try:
        results = kb.search(request.query)
        return {
            "success": True,
            "query": request.query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

