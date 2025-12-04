"""
JSON Knowledge Base Loader
Loads and queries structured JSON knowledge base
"""
import json
import os
from pathlib import Path

class JSONKnowledgeBase:
    def __init__(self, kb_path="data/knowledge_base/analytics_kb.json"):
        self.kb_path = kb_path
        self.kb_data = None
        self.load()
    
    def load(self):
        """Load JSON knowledge base"""
        if not os.path.exists(self.kb_path):
            print(f"Knowledge base not found at {self.kb_path}")
            self.kb_data = {}
            return
        
        with open(self.kb_path, 'r', encoding='utf-8') as f:
            self.kb_data = json.load(f)
        
        print(f"Loaded JSON Knowledge Base: {self.kb_path}")
        print(f"   - Generated: {self.kb_data.get('metadata', {}).get('generated_at', 'Unknown')}")
        print(f"   - Total patients: {self.kb_data.get('summary', {}).get('total_patients', 0)}")
    
    def get_full_context(self):
        """Get full KB as formatted text for LLM context"""
        if not self.kb_data:
            return "Knowledge base is empty or not loaded."
        
        context = []
        
        # Add summary
        context.append("=== ANALYTICS SUMMARY ===")
        summary = self.kb_data.get('summary', {})
        for key, value in summary.items():
            if key == 'key_insights':
                context.append("\nKey Insights:")
                for insight in value:
                    context.append(f"  - {insight}")
            else:
                context.append(f"{key.replace('_', ' ').title()}: {value}")
        
        # Add disease trends
        context.append("\n=== DISEASE TRENDS ===")
        disease_trends = self.kb_data.get('analytics', {}).get('disease_trends', {})
        context.append(f"Interpretation: {disease_trends.get('interpretation', '')}")
        context.append("\nTop 10 Diseases:")
        for disease in disease_trends.get('top_10_diseases', []):
            context.append(f"  {disease['rank']}. {disease['disease_name']}: {disease['case_count']} cases ({disease['percentage']}%)")
        
        # Add doctor workload
        context.append("\n=== DOCTOR WORKLOAD ===")
        workload = self.kb_data.get('analytics', {}).get('doctor_workload', {})
        context.append(f"Interpretation: {workload.get('interpretation', '')}")
        context.append("\nTop 10 Busiest Doctors:")
        for doc in workload.get('top_10_busiest_doctors', []):
            context.append(f"  {doc['rank']}. Dr. {doc['doctor_name']} ({doc['specialty']}): {doc['patient_count']} patients")
        
        # Add geographic distribution
        context.append("\n=== GEOGRAPHIC DISTRIBUTION ===")
        geo = self.kb_data.get('analytics', {}).get('geographic_distribution', {})
        context.append(f"Interpretation: {geo.get('interpretation', '')}")
        context.append("\nTop 10 Areas:")
        for area in geo.get('top_10_areas', []):
            context.append(f"  {area['rank']}. {area['area_name']}: {area['patient_count']} patients ({area['percentage']}%)")
        
        return "\n".join(context)
    
    def query_disease_trends(self):
        """Get disease trends data"""
        return self.kb_data.get('analytics', {}).get('disease_trends', {})
    
    def query_doctor_workload(self):
        """Get doctor workload data"""
        return self.kb_data.get('analytics', {}).get('doctor_workload', {})
    
    def query_geographic_distribution(self):
        """Get geographic distribution data"""
        return self.kb_data.get('analytics', {}).get('geographic_distribution', {})
    
    def query_summary(self):
        """Get executive summary"""
        return self.kb_data.get('summary', {})
    
    def search(self, query_text):
        """Search KB for relevant information based on query keywords"""
        query_lower = query_text.lower()
        results = []
        
        # Check for disease-related queries
        if any(word in query_lower for word in ['disease', 'illness', 'condition', 'common', 'prevalent']):
            disease_data = self.query_disease_trends()
            results.append({
                "type": "disease_trends",
                "data": disease_data,
                "interpretation": disease_data.get('interpretation', '')
            })
        
        # Check for doctor-related queries
        if any(word in query_lower for word in ['doctor', 'physician', 'workload', 'busy', 'staff']):
            workload_data = self.query_doctor_workload()
            results.append({
                "type": "doctor_workload",
                "data": workload_data,
                "interpretation": workload_data.get('interpretation', '')
            })
        
        # Check for geographic queries
        if any(word in query_lower for word in ['area', 'location', 'geographic', 'where', 'branch', 'region']):
            geo_data = self.query_geographic_distribution()
            results.append({
                "type": "geographic_distribution",
                "data": geo_data,
                "interpretation": geo_data.get('interpretation', '')
            })
        
        # If no specific match, return summary
        if not results:
            summary_data = self.query_summary()
            results.append({
                "type": "summary",
                "data": summary_data,
                "interpretation": "General analytics summary"
            })
        
        return results

if __name__ == "__main__":
    kb = JSONKnowledgeBase()
    print("\n" + "="*70)
    print("FULL CONTEXT:")
    print("="*70)
    print(kb.get_full_context())
