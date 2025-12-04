"""
JSON-based Knowledge Base Generator
Converts analytics data into structured JSON knowledge base
"""
import json
import pandas as pd
import os
from datetime import datetime

class JSONKnowledgeBaseGenerator:
    def __init__(self):
        self.kb_dir = "data/knowledge_base"
        os.makedirs(self.kb_dir, exist_ok=True)
        
    def generate_from_data(self, doctors_df, branches_df, diseases_df, patients_df):
        """Generate comprehensive JSON knowledge base from analytics data"""
        
        kb = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "2.0",
                "format": "json",
                "description": "Saylani Medical Help Desk Analytics Knowledge Base"
            },
            "analytics": {
                "disease_trends": self._analyze_disease_trends(patients_df, diseases_df),
                "doctor_workload": self._analyze_doctor_workload(patients_df, doctors_df),
                "geographic_distribution": self._analyze_geographic_distribution(patients_df, branches_df),
                "temporal_patterns": self._analyze_temporal_patterns(patients_df)
            },
            "entities": {
                "doctors": self._format_doctors(doctors_df),
                "branches": self._format_branches(branches_df),
                "diseases": self._format_diseases(diseases_df)
            },
            "summary": self._generate_summary(patients_df, doctors_df, branches_df, diseases_df)
        }
        
        # Save to JSON file
        kb_path = os.path.join(self.kb_dir, "analytics_kb.json")
        with open(kb_path, 'w', encoding='utf-8') as f:
            json.dump(kb, f, indent=2, ensure_ascii=False)
        
        print(f"JSON Knowledge Base generated: {kb_path}")
        return kb
    
    def _analyze_disease_trends(self, patients_df, diseases_df):
        """Analyze disease trends and return structured data"""
        disease_counts = patients_df['disease_name'].value_counts()
        
        return {
            "overview": {
                "total_unique_diseases": len(disease_counts),
                "total_cases": len(patients_df),
                "most_common_disease": {
                    "name": disease_counts.index[0],
                    "count": int(disease_counts.iloc[0]),
                    "percentage": round((disease_counts.iloc[0] / len(patients_df)) * 100, 2)
                }
            },
            "top_10_diseases": [
                {
                    "rank": i + 1,
                    "disease_name": disease,
                    "case_count": int(count),
                    "percentage": round((count / len(patients_df)) * 100, 2)
                }
                for i, (disease, count) in enumerate(disease_counts.head(10).items())
            ],
            "interpretation": f"The most prevalent disease is {disease_counts.index[0]} with {disease_counts.iloc[0]} cases, "
                            f"representing {round((disease_counts.iloc[0] / len(patients_df)) * 100, 2)}% of all patient visits. "
                            f"This indicates a significant health concern that requires focused medical resources and preventive measures."
        }
    
    def _analyze_doctor_workload(self, patients_df, doctors_df):
        """Analyze doctor workload distribution"""
        workload = patients_df['doctor_name'].value_counts()
        avg_load = workload.mean()
        
        # Get doctor details
        doctor_workload = []
        for i, (doc_name, count) in enumerate(workload.head(10).items()):
            # Get specialty from doctors_df or patients_df
            doc_info = doctors_df[doctors_df['doctor_name'] == doc_name]
            if not doc_info.empty:
                specialty = doc_info['specialty'].iloc[0]
            else:
                # Fallback to patients_df
                specialty_info = patients_df[patients_df['doctor_name'] == doc_name]['specialty'].iloc[0] if len(patients_df[patients_df['doctor_name'] == doc_name]) > 0 else "Unknown"
                specialty = specialty_info
            
            doctor_workload.append({
                "rank": i + 1,
                "doctor_name": doc_name,
                "specialty": specialty,
                "patient_count": int(count),
                "load_vs_average": round((count / avg_load) * 100, 2)
            })
        
        return {
            "overview": {
                "total_doctors": len(doctors_df),
                "average_patients_per_doctor": round(avg_load, 2),
                "busiest_doctor": {
                    "doctor_name": workload.index[0],
                    "patient_count": int(workload.iloc[0])
                }
            },
            "top_10_busiest_doctors": doctor_workload,
            "interpretation": f"The average workload is {round(avg_load, 2)} patients per doctor. "
                            f"The busiest doctor ({workload.index[0]}) has {workload.iloc[0]} patients, "
                            f"which is {round((workload.iloc[0] / avg_load) * 100, 2)}% of the average load. "
                            f"This suggests potential workload imbalance that may require staff redistribution."
        }
    
    def _analyze_geographic_distribution(self, patients_df, branches_df):
        """Analyze patient geographic distribution"""
        area_counts = patients_df['area'].value_counts()
        branch_counts = patients_df['branch_name'].value_counts()
        
        return {
            "overview": {
                "total_areas_served": len(area_counts),
                "total_branches": len(branches_df),
                "most_served_area": {
                    "area_name": area_counts.index[0],
                    "patient_count": int(area_counts.iloc[0]),
                    "percentage": round((area_counts.iloc[0] / len(patients_df)) * 100, 2)
                }
            },
            "top_10_areas": [
                {
                    "rank": i + 1,
                    "area_name": area,
                    "patient_count": int(count),
                    "percentage": round((count / len(patients_df)) * 100, 2)
                }
                for i, (area, count) in enumerate(area_counts.head(10).items())
            ],
            "branch_distribution": [
                {
                    "branch_name": branch_name,
                    "patient_count": int(count),
                    "percentage": round((count / len(patients_df)) * 100, 2)
                }
                for branch_name, count in branch_counts.items()
            ],
            "interpretation": f"The area with the highest patient volume is {area_counts.index[0]} with {area_counts.iloc[0]} patients. "
                            f"This represents {round((area_counts.iloc[0] / len(patients_df)) * 100, 2)}% of total patient traffic, "
                            f"indicating this is a primary catchment area requiring adequate medical infrastructure."
        }
    
    def _analyze_temporal_patterns(self, patients_df):
        """Analyze temporal visit patterns if timestamp data exists"""
        if 'visit_timestamp' not in patients_df.columns:
            return {
                "overview": "Temporal data not available",
                "interpretation": "Visit timestamp information is not present in the current dataset."
            }
        
        patients_df_copy = patients_df.copy()
        patients_df_copy['visit_date'] = pd.to_datetime(patients_df_copy['visit_timestamp'], errors='coerce')
        daily_counts = patients_df_copy.groupby(patients_df_copy['visit_date'].dt.date).size()
        
        return {
            "overview": {
                "total_days_recorded": len(daily_counts),
                "average_daily_visits": round(daily_counts.mean(), 2),
                "peak_day": {
                    "date": str(daily_counts.idxmax()),
                    "visit_count": int(daily_counts.max())
                }
            },
            "interpretation": f"Peak traffic occurred on {daily_counts.idxmax()} with {daily_counts.max()} visits. "
                            f"The average daily visit count is {round(daily_counts.mean(), 2)}. "
                            f"Understanding these patterns helps optimize staff scheduling and resource allocation."
        }
    
    def _format_doctors(self, doctors_df):
        """Format doctor information"""
        return [
            {
                "doctor_id": row['doctor_id'],
                "name": row['doctor_name'],
                "specialty": row['specialty']
            }
            for _, row in doctors_df.iterrows()
        ]
    
    def _format_branches(self, branches_df):
        """Format branch information"""
        return [
            {
                "branch_id": row['branch_id'],
                "branch_name": row['branch_name'],
                "area": row['area']
            }
            for _, row in branches_df.iterrows()
        ]
    
    def _format_diseases(self, diseases_df):
        """Format disease information"""
        return [
            {
                "disease_name": row['canonical_name'],
                "category": row['category']
            }
            for _, row in diseases_df.iterrows()
        ]
    
    def _generate_summary(self, patients_df, doctors_df, branches_df, diseases_df):
        """Generate executive summary"""
        disease_counts = patients_df['disease_name'].value_counts()
        workload = patients_df['doctor_name'].value_counts()
        area_counts = patients_df['area'].value_counts()
        
        return {
            "total_patients": len(patients_df),
            "total_doctors": len(doctors_df),
            "total_branches": len(branches_df),
            "total_diseases_recorded": len(disease_counts),
            "key_insights": [
                f"Most common disease: {disease_counts.index[0]} ({disease_counts.iloc[0]} cases)",
                f"Busiest doctor: {workload.index[0]} ({workload.iloc[0]} patients)",
                f"Top service area: {area_counts.index[0]} ({area_counts.iloc[0]} patients)",
                f"Average patients per doctor: {round(workload.mean(), 2)}"
            ]
        }

if __name__ == "__main__":
    # Test the generator
    generator = JSONKnowledgeBaseGenerator()
    
    # Load data
    doctors = pd.read_csv("data/cleaned/doctors.csv")
    branches = pd.read_csv("data/cleaned/branches.csv")
    diseases = pd.read_csv("data/cleaned/diseases.csv")
    appointments = pd.read_csv("data/cleaned/appointments.csv")
    
    # Generate KB
    kb = generator.generate_from_data(doctors, branches, diseases, appointments)
    print("Knowledge Base generated successfully!")
