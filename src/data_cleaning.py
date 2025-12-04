"""
Data Cleaning Pipeline for Single CSV File
Processes augmented_patient_appointments.csv
"""
import pandas as pd
import os
import json
from datetime import datetime

# Paths
RAW_FILE = "data/raw/augmented_patient_appointments.csv"
CLEANED_DIR = "data/cleaned"
REPORT_PATH = "data/cleaned/cleaning_report.json"

def load_data():
    """Load the augmented patient appointments CSV"""
    print("Loading data from:", RAW_FILE)
    df = pd.read_csv(RAW_FILE)
    print(f"Loaded {len(df)} records")
    return df

def clean_timestamps(df):
    """Convert timestamps to proper datetime format"""
    print("\nCleaning timestamps...")
    
    # Try multiple date formats
    df['visit_timestamp'] = pd.to_datetime(
        df['visit_timestamp'], 
        format='%d/%m/%Y %H:%M',
        errors='coerce'
    )
    
    # Check for any failed conversions
    null_count = df['visit_timestamp'].isnull().sum()
    if null_count > 0:
        print(f"Warning: {null_count} timestamps could not be parsed")
    else:
        print(f"All timestamps converted successfully")
    
    return df

def clean_text_fields(df):
    """Clean and standardize text fields"""
    print("\nCleaning text fields...")
    
    # Strip whitespace from all string columns
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        if col != 'visit_timestamp':  # Skip timestamp
            df[col] = df[col].str.strip()
    
    # Standardize gender
    df['gender'] = df['gender'].str.title()
    
    # Standardize branch names
    df['branch_name'] = df['branch_name'].str.strip()
    
    # Standardize disease names
    df['disease_name'] = df['disease_name'].str.strip()
    
    # Standardize specialty
    df['specialty'] = df['specialty'].str.strip()
    
    print("Text fields cleaned")
    return df

def extract_area_from_branch(df):
    """Extract area information from branch name"""
    print("\nExtracting area information...")
    
    # Create area column based on branch name
    # Remove 'Medical' or 'Branch' suffix to get area name
    df['area'] = df['branch_name'].str.replace(' Medical', '').str.replace(' Branch', '').str.strip()
    
    print("Area information extracted")
    return df

def validate_data(df):
    """Validate data quality"""
    print("\nValidating data...")
    
    issues = []
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.any():
        print("\nMissing values found:")
        for col, count in missing[missing > 0].items():
            print(f"   {col}: {count} missing values")
            issues.append(f"{col}: {count} missing values")
    
    # Check age range
    if df['age'].min() < 0 or df['age'].max() > 150:
        print(f"Unusual age values: min={df['age'].min()}, max={df['age'].max()}")
        issues.append(f"Age range: {df['age'].min()} to {df['age'].max()}")
    
    # Check for duplicates
    duplicates = df.duplicated(subset=['visit_id']).sum()
    if duplicates > 0:
        print(f"Found {duplicates} duplicate visit IDs")
        issues.append(f"Duplicate visit IDs: {duplicates}")
    
    if not issues:
        print("Data validation passed")
    
    return df, issues

def generate_derived_tables(df):
    """Generate separate tables for doctors, branches, and diseases"""
    print("\nGenerating derived tables...")
    
    # Doctors table
    doctors = df[['doctor_name', 'specialty']].drop_duplicates().reset_index(drop=True)
    doctors['doctor_id'] = range(1, len(doctors) + 1)
    doctors = doctors[['doctor_id', 'doctor_name', 'specialty']]
    
    # Branches table
    branches = df[['branch_name', 'area']].drop_duplicates().reset_index(drop=True)
    branches['branch_id'] = range(1, len(branches) + 1)
    branches = branches[['branch_id', 'branch_name', 'area']]
    
    # Diseases table
    diseases = df[['disease_name', 'specialty']].drop_duplicates().reset_index(drop=True)
    diseases['disease_id'] = range(1, len(diseases) + 1)
    diseases.rename(columns={'disease_name': 'canonical_name', 'specialty': 'category'}, inplace=True)
    diseases = diseases[['disease_id', 'canonical_name', 'category']]
    
    print(f"Generated {len(doctors)} doctors, {len(branches)} branches, {len(diseases)} diseases")
    
    return doctors, branches, diseases

def main():
    """Main data cleaning pipeline"""
    print("=" * 60)
    print("Saylani Medical Help Desk - Data Cleaning Pipeline")
    print("=" * 60)
    
    os.makedirs(CLEANED_DIR, exist_ok=True)
    
    # Load data
    df = load_data()
    initial_rows = len(df)
    
    # Clean data
    df = clean_timestamps(df)
    df = clean_text_fields(df)
    df = extract_area_from_branch(df)
    df, issues = validate_data(df)
    
    # Generate derived tables
    doctors, branches, diseases = generate_derived_tables(df)
    
    # Save cleaned data
    print("\nSaving cleaned data...")
    
    # Main appointments file
    appointments_path = os.path.join(CLEANED_DIR, "appointments.csv")
    df.to_csv(appointments_path, index=False)
    print(f"Saved: {appointments_path}")
    
    # Derived tables
    doctors.to_csv(os.path.join(CLEANED_DIR, "doctors.csv"), index=False)
    print(f"Saved: doctors.csv")
    
    branches.to_csv(os.path.join(CLEANED_DIR, "branches.csv"), index=False)
    print(f"Saved: branches.csv")
    
    diseases.to_csv(os.path.join(CLEANED_DIR, "diseases.csv"), index=False)
    print(f"Saved: diseases.csv")
    
    # Generate report
    report = {
        "timestamp": datetime.now().isoformat(),
        "status": "Success",
        "input_file": RAW_FILE,
        "rows_processed": {
            "initial": initial_rows,
            "final": len(df),
            "doctors": len(doctors),
            "branches": len(branches),
            "diseases": len(diseases)
        },
        "data_quality": {
            "issues": issues if issues else ["No issues found"]
        },
        "summary": {
            "total_appointments": len(df),
            "unique_patients": df['patient_id'].nunique(),
            "unique_doctors": len(doctors),
            "unique_branches": len(branches),
            "unique_diseases": len(diseases),
            "date_range": {
                "start": df['visit_timestamp'].min().isoformat() if pd.notna(df['visit_timestamp'].min()) else None,
                "end": df['visit_timestamp'].max().isoformat() if pd.notna(df['visit_timestamp'].max()) else None
            }
        }
    }
    
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=4)
    
    print(f"Saved: {REPORT_PATH}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("Cleaning Summary")
    print("=" * 60)
    print(f"Total Appointments: {len(df)}")
    print(f"Unique Patients: {df['patient_id'].nunique()}")
    print(f"Unique Doctors: {len(doctors)}")
    print(f"Unique Branches: {len(branches)}")
    print(f"Unique Diseases: {len(diseases)}")
    print(f"Date Range: {df['visit_timestamp'].min()} to {df['visit_timestamp'].max()}")
    print("=" * 60)
    print("Data cleaning complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
