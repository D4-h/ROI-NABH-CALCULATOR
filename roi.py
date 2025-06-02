import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Hospital Accreditation ROI Calculator",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for healthcare theme
st.markdown("""
<style>
    .main {
        background-color: #FFFFFF;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #007DC5 0%, #005a8b 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Section styling */
    .section-header {
        background-color: #E6F4FA;
        color: #007DC5;
        padding: 1rem;
        border-radius: 8px;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #007DC5;
    }
    
    .section-header h3 {
        margin: 0;
        color: #007DC5;
        font-weight: 600;
    }
    
    /* ROI Results styling */
    .roi-result {
        background: linear-gradient(135deg, #007DC5 0%, #005a8b 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
        text-align: center;
    }
    
    .roi-number {
        font-size: 3rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .alert-error {
        background-color: #ffe6e6;
        color: #E31B23;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #E31B23;
        margin: 1rem 0;
    }
    
    .metric-card {
        background-color: #E6F4FA;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #D3D3D3;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #007DC5;
        margin: 0;
    }
    
    .metric-label {
        color: #333333;
        font-size: 0.9rem;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Load data from CSV files
@st.cache_data
def load_procedures_data():
    try:
        # Try to load from CSV file first
        return pd.read_csv("procedure.csv")
    except FileNotFoundError:
        st.error("procedures.csv file not found. Using sample data.")
        # Fallback to sample data
        procedures_data = [
            {"Specialty": "Burns Management", "Specialty Code": "BM", "Package Name": "Thermal burns", 
             "Procedure Code": "BM001A", "Procedure Name": "Criteria 1: % Total Body Surface Area Burns (TBSA):less than 20% in adults and less than 10% in children younger than 12 years. Dressing without anesthesia", 
             "Procedure Price": 8200},
            {"Specialty": "Burns Management", "Specialty Code": "BM", "Package Name": "Thermal burns", 
             "Procedure Code": "BM001B", "Procedure Name": "Criteria 2: % Total Body Surface Area Burns (TBSA): Upto 25%; Includes % TBSA skin grafted, flap cover, follow-up dressings etc. as deemed necessary; Surgical procedures are required for deep burns that are not amenable to heal with dressings alone.", 
             "Procedure Price": 40000},
            {"Specialty": "Burns Management", "Specialty Code": "BM", "Package Name": "Thermal burns", 
             "Procedure Code": "BM001C", "Procedure Name": "Criteria 3: % Total Body Surface Area Burns (TBSA): 25-40 %; Includes % TBSA skin grafted, flap cover, follow-up dressings etc. as deemed necessary; Surgical procedures are required for deep burns that are not amenable to heal with dressings alone.", 
             "Procedure Price": 50000},
            {"Specialty": "Emergency Room Packages", "Specialty Code": "ER", "Package Name": "Emergency Care", 
             "Procedure Code": "ER001A", "Procedure Name": "Basic Emergency Care Package", 
             "Procedure Price": 15000},
            {"Specialty": "High-end Diagnostics", "Specialty Code": "HD", "Package Name": "Advanced Imaging", 
             "Procedure Code": "HD001A", "Procedure Name": "MRI with Contrast", 
             "Procedure Price": 25000},
        ]
        return pd.DataFrame(procedures_data)
    except Exception as e:
        st.error(f"Error loading procedures.csv: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_location_data():
    try:
        # Try to load from CSV file first
        return pd.read_csv("location.csv")
    except FileNotFoundError:
        st.error("location.csv file not found. Using sample data.")
        # Fallback to sample data
        location_data = [
            {"State": "Andhra Pradesh", "District": "Alluri Sitharama Raju", "Type": "Aspirational"},
            {"State": "Andhra Pradesh", "District": "Anakapalli", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Ananthapuramu", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Annamayya", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Bapatla", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Chittoor", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Dr. B.R. Ambedkar Konaseema", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "East Godavari", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Eluru", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Guntur", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Kakinada", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Krishna", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Kurnool", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Nandyal", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "NTR", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Palnadu", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Parvathipuram Manyam", "Type": "Aspirational"},
            {"State": "Andhra Pradesh", "District": "Prakasam", "Type": "Non Aspirational"},
            {"State": "Andhra Pradesh", "District": "Srikakulam", "Type": "Non Aspirational"},
            {"State": "Maharashtra", "District": "Mumbai", "Type": "Non Aspirational"},
            {"State": "Karnataka", "District": "Bengaluru Urban", "Type": "Non Aspirational"},
            {"State": "Tamil Nadu", "District": "Chennai", "Type": "Non Aspirational"},
            {"State": "West Bengal", "District": "Kolkata", "Type": "Non Aspirational"},
        ]
        return pd.DataFrame(location_data)
    except Exception as e:
        st.error(f"Error loading location.csv: {str(e)}")
        return pd.DataFrame()

# Load data
procedures_df = load_procedures_data()
location_df = load_location_data()

# Metro cities list
METRO_CITIES = ["Chennai", "Delhi", "Mumbai", "Kolkata", "Bengaluru", "Hyderabad", "Ahmedabad", "Pune"]

# Accreditation fee structures
ENTRY_LEVEL_FEES = {
    (1, 5): 21000,
    (6, 20): 40000,
    (21, 50): 80000,
    (51, 100): 160000,
    (101, 300): 200000
}

FULL_ACCREDITATION_FEES = {
    (1, 50): 227740,
    (51, 100): 304440,
    (101, 300): 466100,
    (301, 500): 619500,
    (501, float('inf')): 802400
}

def get_accreditation_fee(bed_count, accreditation_type):
    fee_structure = ENTRY_LEVEL_FEES if accreditation_type == "Entry Level" else FULL_ACCREDITATION_FEES
    
    for (min_beds, max_beds), fee in fee_structure.items():
        if min_beds <= bed_count <= max_beds:
            return fee
    return 0

def calculate_multiplier(accreditation_type, is_aspirational, is_metro, has_pg_dnb):
    multiplier = 1.0
    
    if accreditation_type == "Entry Level":
        if is_aspirational or is_metro:
            multiplier *= 1.1
        if has_pg_dnb:
            multiplier *= 1.1
    else:  # Full Accreditation
        if is_aspirational:
            multiplier *= 1.15
        elif is_metro:
            multiplier *= 1.1
        if has_pg_dnb:
            multiplier *= 1.1
    
    return multiplier

# Main app
st.markdown("""
<div class="main-header">
    <h1>🏥 Hospital Accreditation ROI Calculator</h1>
    <p>Calculate your return on investment for NABH accreditation</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for the main layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-header"><h3>Hospital Information</h3></div>', unsafe_allow_html=True)
    
    # Location Selection
    st.subheader("📍 Location Details")
    selected_state = st.selectbox("Select State", options=sorted(location_df['State'].unique()))
    
    # Filter districts based on selected state
    districts_in_state = location_df[location_df['State'] == selected_state]['District'].tolist()
    selected_district = st.selectbox("Select District", options=sorted(districts_in_state))
    
    # Get district type
    district_info = location_df[(location_df['State'] == selected_state) & 
                              (location_df['District'] == selected_district)]
    is_aspirational = district_info['Type'].iloc[0] == "Aspirational" if not district_info.empty else False
    
    # City input for metro check
    city_input = st.text_input("Enter your city name")
    is_metro = city_input.strip() in METRO_CITIES
    
    if city_input:
        if is_metro:
            st.success(f"✅ {city_input} is recognized as a metro city")
        else:
            st.info(f"ℹ️ {city_input} is not classified as a metro city")
    
    # Hospital Details
    st.subheader("🏥 Hospital Details")
    bed_count = st.number_input("Number of beds", min_value=1, max_value=1000, value=50)
    has_pg_dnb = st.checkbox("Hospital provides PG/DNB courses")
    
    # Accreditation Type
    accreditation_options = ["Entry Level", "Full Accreditation"]
    if bed_count > 300:
        accreditation_options = ["Full Accreditation"]
        st.warning("⚠️ Entry Level certification is not available for hospitals with more than 300 beds")
    
    accreditation_type = st.selectbox("Select Accreditation Type", options=accreditation_options)

with col2:
    st.markdown('<div class="section-header"><h3>Procedures & Volume</h3></div>', unsafe_allow_html=True)
    
    # Specialty Selection
    st.subheader("🔬 Medical Specialties")
    available_specialties = procedures_df['Specialty'].unique()
    selected_specialties = st.multiselect("Select Specialties you provide", options=available_specialties)
    
    # Store procedure selections
    procedure_selections = []
    
    if selected_specialties:
        for specialty in selected_specialties:
            st.write(f"**{specialty}**")
            
            # Filter packages for this specialty
            specialty_packages = procedures_df[procedures_df['Specialty'] == specialty]['Package Name'].unique()
            selected_packages = st.multiselect(f"Select Packages under {specialty}", 
                                             options=specialty_packages, 
                                             key=f"packages_{specialty}")
            
            if selected_packages:
                for package in selected_packages:
                    # Filter procedures for this specialty and package
                    package_procedures = procedures_df[
                        (procedures_df['Specialty'] == specialty) & 
                        (procedures_df['Package Name'] == package)
                    ]
                    
                    for _, procedure in package_procedures.iterrows():
                        with st.expander(f"{procedure['Procedure Code']} - ₹{procedure['Procedure Price']:,}"):
                            st.write(f"**Procedure:** {procedure['Procedure Name'][:100]}...")
                            monthly_volume = st.number_input(
                                f"Monthly volume for {procedure['Procedure Code']}", 
                                min_value=0, 
                                value=5,
                                key=f"volume_{procedure['Procedure Code']}"
                            )
                            
                            if monthly_volume > 0:
                                procedure_selections.append({
                                    'specialty': specialty,
                                    'package': package,
                                    'procedure_code': procedure['Procedure Code'],
                                    'procedure_name': procedure['Procedure Name'],
                                    'base_price': procedure['Procedure Price'],
                                    'monthly_volume': monthly_volume
                                })

# Calculate ROI
if st.button("Calculate ROI", type="primary"):
    if procedure_selections:
        # Calculate multiplier
        multiplier = calculate_multiplier(accreditation_type, is_aspirational, is_metro, has_pg_dnb)
        
        # Calculate monthly additional income
        total_monthly_additional_income = 0
        
        st.markdown('<div class="section-header"><h3>📊 ROI Calculation Results</h3></div>', unsafe_allow_html=True)
        
        # Display calculation details
        st.subheader("Calculation Details")
        
        col_calc1, col_calc2 = st.columns([1, 1])
        
        with col_calc1:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">Location Benefits</p>
                <p class="metric-value">{'✅ Aspirational District' if is_aspirational else '❌ Non-Aspirational'}</p>
                <p class="metric-value">{'✅ Metro City' if is_metro else '❌ Non-Metro'}</p>
                <p class="metric-value">{'✅ PG/DNB Courses' if has_pg_dnb else '❌ No PG/DNB'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_calc2:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">Total Multiplier</p>
                <p class="metric-value">{multiplier:.2f}x</p>
                <p class="metric-label">Accreditation Type</p>
                <p class="metric-value">{accreditation_type}</p>
            </div>
            """, unsafe_allow_html=True)
            
        
        # Calculate for each procedure
        st.subheader("Procedure-wise Additional Income")
        for procedure in procedure_selections:
            base_price = procedure['base_price']
            enhanced_price = base_price * multiplier
            additional_income_per_procedure = enhanced_price - base_price
            monthly_additional_income = additional_income_per_procedure * procedure['monthly_volume']
            total_monthly_additional_income += monthly_additional_income
            
            st.write(f"**{procedure['procedure_code']}**")
            col_proc1, col_proc2, col_proc3, col_proc4 = st.columns(4)
            
            with col_proc1:
                st.metric("Base Price", f"₹{base_price:,}")
            with col_proc2:
                st.metric("Enhanced Price", f"₹{enhanced_price:,.0f}")
            with col_proc3:
                st.metric("Additional per procedure", f"₹{additional_income_per_procedure:,.0f}")
            with col_proc4:
                st.metric("Monthly Additional", f"₹{monthly_additional_income:,.0f}")
        
        # Calculate accreditation fee
        accreditation_fee = get_accreditation_fee(bed_count, accreditation_type)
        
        # Calculate ROI
        if total_monthly_additional_income > 0:
            months_to_roi = accreditation_fee / total_monthly_additional_income
            years_to_roi = months_to_roi / 12
            
            # Display final results
            st.markdown(f"""
            <div class="roi-result">
                <h2>🎯 ROI Summary</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; margin-top: 2rem;">
                    <div>
                        <div class="roi-number">₹{accreditation_fee:,}</div>
                        <div>Investment Required</div>
                    </div>
                    <div>
                        <div class="roi-number">₹{total_monthly_additional_income:,.0f}</div>
                        <div>Monthly Additional Income</div>
                    </div>
                    <div>
                        <div class="roi-number">{months_to_roi:.1f}</div>
                        <div>Months to Break Even</div>
                    </div>
                </div>
                <div style="margin-top: 2rem; font-size: 1.5rem;">
                    <strong>Time to ROI: {years_to_roi:.1f} years ({months_to_roi:.1f} months)</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Annual projection
            annual_additional_income = total_monthly_additional_income * 12
            st.subheader("📈 Annual Projection")
            
            col_ann1, col_ann2, col_ann3 = st.columns(3)
            with col_ann1:
                st.metric("Annual Additional Income", f"₹{annual_additional_income:,.0f}")
            with col_ann2:
                st.metric("5-Year Additional Income", f"₹{annual_additional_income * 5:,.0f}")
            with col_ann3:
                st.metric("Net Profit (5 years)", f"₹{(annual_additional_income * 5) - accreditation_fee:,.0f}")
        
        else:
            st.error("No procedures selected or monthly volumes are zero.")
    else:
        st.error("Please select at least one procedure with monthly volume greater than 0.")

# Instructions
with st.expander("ℹ️ How to use this calculator"):
    st.markdown("""
    1. **Location**: Select your state and district. Enter your city to check for metro benefits.
    2. **Hospital Details**: Enter bed count and specify if you offer PG/DNB courses.
    3. **Accreditation**: Choose between Entry Level or Full Accreditation.
    4. **Procedures**: Select specialties, packages, and procedures you perform.
    5. **Volume**: Enter monthly volume for each selected procedure.
    6. **Calculate**: Click the button to see your ROI analysis.
    
   """)

# Footerrun
st.markdown("---")
st.markdown("*This calculator provides estimates based on the information provided. Actual results may vary.*")
