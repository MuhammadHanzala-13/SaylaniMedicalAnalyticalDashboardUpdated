# 🏥 Saylani Medical Help Desk - Real-World Data Analytics

## 📊 Overview

This system has been **fully adapted** to work with your real-world data file: `augmented_patient_appointments.csv`

**Your Data:**
- ✅ **2,000 patient appointments**
- ✅ **5 branches** (Hyderabad Medical, Gulshan Branch, North Nazimabad Medical, Punjab Chowrangi Medical, Time Press Medical)
- ✅ **20 doctors** across 4 specialties
- ✅ **23 different diseases** tracked
- ✅ **Date range:** January 2024 - December 2025

---

## 🚀 Quick Start

### 1. Your Data is Already Loaded!
Your CSV file `augmented_patient_appointments.csv` is already in the `data/raw/` folder.

### 2. Run the Pipeline
Simply execute:
```bash
.\run_pipeline.bat
```

This will:
1. ✅ Clean and process your 2,000 appointments
2. ✅ Generate analytics knowledge base
3. ✅ Create visualizations
4. ✅ Start API server (port 8000)
5. ✅ Launch dashboard (port 8501)

### 3. Access Your System
- **Dashboard:** http://localhost:8501
- **API Documentation:** http://localhost:8000/docs

---

## 📁 Your Data Structure

### Input File: `augmented_patient_appointments.csv`

**Columns:**
- `visit_id` - Unique visit identifier (V0001, V0002, etc.)
- `branch_name` - Branch where visit occurred
- `patient_id` - Unique patient identifier (MR-2024-XXXXXX)
- `patient_name` - Patient name
- `gender` - Male/Female
- `age` - Patient age
- `doctor_name` - Attending doctor
- `specialty` - Doctor's specialty (Dentist, Cardiology, Oncology, General Physician)
- `visit_timestamp` - Date and time of visit
- `disease_name` - Diagnosed condition

### Generated Files (Cleaned Data)

After running the pipeline, you'll find in `data/cleaned/`:

1. **appointments.csv** - All 2,000 appointments (cleaned)
2. **doctors.csv** - 20 unique doctors extracted
3. **branches.csv** - 5 branches extracted
4. **diseases.csv** - 23 diseases categorized
5. **cleaning_report.json** - Data quality report

---

## 📈 Analytics Generated

The system automatically generates comprehensive analytics:

### 1. Disease Trends
- Most common diseases
- Disease distribution by percentage
- Top 10 diseases
- Category-wise breakdown

### 2. Doctor Workload
- Busiest doctors
- Average patients per doctor
- Workload distribution
- Specialty-wise analysis

### 3. Geographic Distribution
- Patient distribution by area
- Branch-wise patient count
- Top service areas
- Coverage analysis

### 4. Temporal Patterns
- Daily visit patterns
- Peak traffic days
- Visit trends over time
- Seasonal patterns

---

## 🤖 AI-Powered Chatbot

Ask questions about your data:

**Example Queries:**
```
✅ "What are the top 10 diseases?"
✅ "Who is the busiest doctor?"
✅ "Which branch has the most patients?"
✅ "Show me disease trends"
✅ "What's the average doctor workload?"
✅ "Which area has the highest patient volume?"
```

The chatbot uses:
1. **Gemini API** (if available) for natural language responses
2. **JSON Knowledge Base** fallback for guaranteed answers

---

## 📊 Your Real-World Statistics

Based on your actual data:

### Patients & Visits
- **Total Appointments:** 2,000
- **Unique Patients:** 2,000
- **Date Range:** Jan 1, 2024 - Dec 31, 2025

### Medical Staff
- **Total Doctors:** 20
- **Specialties:** 4 (Dentist, Cardiology, Oncology, General Physician)

### Facilities
- **Total Branches:** 5
- **Areas Served:** Multiple areas across Karachi

### Health Conditions
- **Diseases Tracked:** 23 different conditions
- **Categories:** Dental, Cardiac, Oncology, General

---

## 🔄 Updating Your Data

### Option 1: Replace the CSV File
1. Replace `data/raw/augmented_patient_appointments.csv` with your new file
2. Run `.\run_pipeline.bat`
3. System will automatically process the new data

### Option 2: Add More Data
1. Append new rows to the existing CSV
2. Ensure same column structure
3. Run the pipeline again

### Data Format Requirements
- **Date Format:** DD/MM/YYYY HH:MM
- **Visit IDs:** Unique identifiers (V0001, V0002, etc.)
- **Patient IDs:** Format MR-YYYY-XXXXXX
- **No empty rows**
- **UTF-8 encoding**

---

## 🎯 Key Features

### 1. Fully Automated
- No manual data entry required
- Automatic data cleaning
- Smart error handling
- Validation and quality checks

### 2. Real-Time Analytics
- Live dashboard updates
- Interactive visualizations
- Drill-down capabilities
- Export functionality

### 3. AI-Powered Insights
- Natural language queries
- Contextual answers
- Data-driven recommendations
- Trend analysis

### 4. Production-Ready
- Error handling
- Data validation
- Performance optimization
- Scalable architecture

---

## 📝 Data Quality Report

After each pipeline run, check:
```
data/cleaned/cleaning_report.json
```

This contains:
- ✅ Rows processed
- ✅ Data quality issues
- ✅ Missing values
- ✅ Validation results
- ✅ Summary statistics

---

## 🛠️ Technical Details

### Data Processing Pipeline

```
augmented_patient_appointments.csv
           ↓
    [Data Cleaning]
           ↓
    ├── appointments.csv (2000 rows)
    ├── doctors.csv (20 doctors)
    ├── branches.csv (5 branches)
    └── diseases.csv (23 diseases)
           ↓
    [JSON KB Generation]
           ↓
    analytics_kb.json
           ↓
    [Dashboard & API]
```

### Technologies Used
- **Python 3.x** - Core processing
- **Pandas** - Data manipulation
- **FastAPI** - REST API
- **Streamlit** - Interactive dashboard
- **Plotly** - Visualizations
- **Google Gemini** - AI responses (optional)

---

## 🐛 Troubleshooting

### Issue: "File not found"
**Solution:** Ensure `augmented_patient_appointments.csv` is in `data/raw/`

### Issue: "Date parsing errors"
**Solution:** Check date format is DD/MM/YYYY HH:MM

### Issue: "Missing values"
**Solution:** Check the cleaning report for details. System handles missing values automatically.

### Issue: "API not responding"
**Solution:** 
1. Check if `.env` file exists with `GEMINI_API_KEY`
2. System will use JSON fallback automatically

### Issue: "Dashboard shows no data"
**Solution:**
1. Run the pipeline first: `.\run_pipeline.bat`
2. Check if `analytics_kb.json` was generated
3. Restart the dashboard

---

## 📞 Support

### Quick Commands

**Run full pipeline:**
```bash
.\run_pipeline.bat
```

**Clean data only:**
```bash
python src/data_cleaning.py
```

**Generate KB only:**
```bash
python src/json_kb_generator.py
```

**Start API only:**
```bash
python -m uvicorn src.app:app --reload
```

**Start dashboard only:**
```bash
streamlit run src/dashboard.py
```

---

## ✅ Success Checklist

After running the pipeline, verify:

- [ ] `data/cleaned/appointments.csv` exists (2000 rows)
- [ ] `data/cleaned/doctors.csv` exists (20 doctors)
- [ ] `data/cleaned/branches.csv` exists (5 branches)
- [ ] `data/cleaned/diseases.csv` exists (23 diseases)
- [ ] `data/knowledge_base/analytics_kb.json` exists
- [ ] Dashboard accessible at http://localhost:8501
- [ ] API accessible at http://localhost:8000/docs
- [ ] Chatbot responds to queries
- [ ] Visualizations display correctly

---

## 🎉 What's Next?

1. **Explore the Dashboard** - Interactive analytics and visualizations
2. **Try the Chatbot** - Ask questions about your data
3. **Check the API** - Integrate with other systems
4. **Review Analytics** - Gain insights from your data
5. **Update Data** - Add new appointments and rerun pipeline

---

**Version:** 3.0 (Real-World Data Edition)  
**Last Updated:** 2025-12-03  
**Status:** ✅ Production Ready with Real Data

---

## 🌟 Your Data at a Glance

```
📊 2,000 Appointments
👨‍⚕️ 20 Doctors
🏥 5 Branches
🦠 23 Diseases
📅 2 Years of Data
🌍 Multiple Areas Covered
```

**Your medical analytics system is ready to use!** 🚀
