import streamlit as st
import pandas as pd
import pydeck as pdk
from pathlib import Path
from utils import render_logo_header
from universal_viz import load_main_data, load_country_reference_data, setup_sidebar_filters, filter_dataframe_by_selections
from postprocessed import (
    calculate_iffs_as_gdp_percentage, visualize_iffs_as_gdp_percentage,
    calculate_annual_iff_volume, visualize_annual_iff_volume,
    calculate_trade_mispricing, visualize_trade_mispricing,
    calculate_tax_evasion, visualize_tax_evasion,
    calculate_criminal_activities, visualize_criminal_activities,
    calculate_enforcement_effectiveness, visualize_enforcement_effectiveness,
    calculate_corruption_index, visualize_corruption_index
)

render_logo_header()

# === Load Data ===
main_data = load_main_data()
ref_data = load_country_reference_data()

# === Setup Filters ===
filters = setup_sidebar_filters(ref_data, main_data, key_prefix="topic_4_4")

# === Filter Data ===
filtered_data = filter_dataframe_by_selections(main_data, filters, ref_data)

# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "iso3_country_reference.csv"

# === Top Bar ===
col1, col2 = st.columns([0.8, 0.1])
with col1:
    st.title("Topic 4.4: Illicit Financial Flows (IFFs)")
with col2:
    st.page_link("pages/0_home.py", label="Back to Home", use_container_width=True)

# === Overview ===
st.markdown("""
Illicit financial flows (IFFs) represent a significant loss of resources that could fund development.  
They include trade mispricing, tax evasion, corruption, and illegal activity. Tackling IFFs strengthens domestic resource mobilization.
""")

# === Country Selector ===
ref = pd.read_csv(DATA_PATH).rename(columns={"Country or Area": "country_name"})
country_list = sorted(ref["country_name"].dropna().unique())
selected_country = st.selectbox("🔎 Select a country to explore:", country_list)

# === Regional Map ===
st.markdown("### 🌍 Explore by Region")
map_data = ref.copy()
map_data["selected"] = map_data["country_name"] == selected_country
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state=pdk.ViewState(latitude=0, longitude=20, zoom=2),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position="[lon, lat]",
            get_radius=40000,
            get_fill_color="[255, 100, 10, 180]",
            pickable=True,
        )
    ],
    tooltip={"text": "{country_name}"}
))

# === Indicator Tabs ===
st.subheader("Indicator Insights")
tab1, tab2, tab3 = st.tabs([
    "4.4.1: Magnitude of Illicit Financial Flows",
    "4.4.2: Types of IFFs",
    "4.4.3: Detection and Enforcement"
])

# === Tab 1: Magnitude of IFFs ===
with tab1:
    # Indicator 4.4.1.1: IFFs as % of GDP
    with st.container():
        st.markdown("### Indicator 4.4.1.1: IFFs as % of GDP")
        st.caption("Proxied by Global Financial Integrity")
        
        try:
            iffs_viz = visualize_iffs_as_gdp_percentage(
                df=filtered_data,
                selected_iso3=filters["selected_countries"],
                year_range=filters["year_range"]
            )
            
            if iffs_viz and "chart" in iffs_viz:
                st.plotly_chart(iffs_viz["chart"], use_container_width=True, key="tab1_iffs_gdp_chart")
                
                # Display metrics
                if iffs_viz and "metrics" in iffs_viz:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Average IFFs", f"{iffs_viz['metrics']['average_iffs']:.1f}%")
                    with col2:
                        st.metric("Maximum IFFs", f"{iffs_viz['metrics']['max_iffs']:.1f}%")
                    with col3:
                        st.metric("Minimum IFFs", f"{iffs_viz['metrics']['min_iffs']:.1f}%")
            else:
                st.info("No data available for IFFs as % of GDP")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Estimated value of IFFs relative to GDP, showing macro-level impact.  
**Proxy:** Based on GFI trade gap & capital flight data.
            """)

    # Indicator 4.4.1.2: Annual IFF Volume
    with st.container():
        st.markdown("### Indicator 4.4.1.2: Annual IFF Volume")
        st.caption("Proxied by Global Financial Integrity")
        
        try:
            volume_viz = visualize_annual_iff_volume(
                df=filtered_data,
                selected_countries=filters["selected_countries"],
                year_range=filters["year_range"]
            )
            
            if volume_viz and "chart" in volume_viz:
                st.plotly_chart(volume_viz["chart"], use_container_width=True, key="tab1_annual_volume_chart")
                
                # Display metrics
                if volume_viz and "metrics" in volume_viz:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Volume", f"${volume_viz['metrics']['total_volume']:,.0f}")
                    with col2:
                        st.metric("Maximum Volume", f"${volume_viz['metrics']['max_volume']:,.0f}")
                    with col3:
                        st.metric("Minimum Volume", f"${volume_viz['metrics']['min_volume']:,.0f}")
            else:
                st.info("No data available for Annual IFF Volume")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Total illicit outflows per year (USD).  
**Proxy:** GFI estimate of unrecorded transfers, trade mismatches.
            """)

# === Tab 2: Types of IFFs ===
with tab2:
    # Indicator 4.4.2.1: Trade Mispricing
    with st.container():
        st.markdown("### Indicator 4.4.2.1: Trade Mispricing")
        st.caption("Proxied by GFI Trade Gap Data")
        
        try:
            trade_viz = visualize_trade_mispricing(
                df=filtered_data,
                selected_countries=filters["selected_countries"],
                year_range=filters["year_range"]
            )
            
            if trade_viz and "chart" in trade_viz:
                st.plotly_chart(trade_viz["chart"], use_container_width=True, key="tab2_trade_mispricing_chart")
                
                # Display metrics
                if trade_viz and "metrics" in trade_viz:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Average Value", f"${trade_viz['metrics']['average_value']:,.0f}")
                    with col2:
                        st.metric("Maximum Value", f"${trade_viz['metrics']['max_value']:,.0f}")
                    with col3:
                        st.metric("Minimum Value", f"${trade_viz['metrics']['min_value']:,.0f}")
            else:
                st.info("No data available for Trade Mispricing")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Manipulating trade values to illegally shift capital.  
**Proxy:** GFI's bilateral trade mismatch analysis.
            """)

    # Indicator 4.4.2.2: Tax Evasion
    with st.container():
        st.markdown("### Indicator 4.4.2.2: Tax Evasion")
        st.caption("Proxied by IMF Tax Registration Data")
        
        try:
            tax_viz = visualize_tax_evasion(
                df=filtered_data,
                selected_countries=filters["selected_countries"],
                year_range=filters["year_range"]
            )
            
            if tax_viz and "chart" in tax_viz:
                st.plotly_chart(tax_viz["chart"], use_container_width=True, key="tab2_tax_evasion_chart")
                
                # Display metrics
                if tax_viz and "metrics" in tax_viz:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Average Value", f"${tax_viz['metrics']['average_value']:,.0f}")
                    with col2:
                        st.metric("Maximum Value", f"${tax_viz['metrics']['max_value']:,.0f}")
                    with col3:
                        st.metric("Minimum Value", f"${tax_viz['metrics']['min_value']:,.0f}")
            else:
                st.info("No data available for Tax Evasion")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Illegally avoiding taxes via underreporting or offshore hiding.  
**Proxy:** Share of taxpayers vs. population (IMF compliance benchmark).
            """)

    # Indicator 4.4.2.3: Criminal Activities
    with st.container():
        st.markdown("### Indicator 4.4.2.3: Criminal Activities")
        st.caption("Proxied by UNODC Crime Flow Data")
        
        try:
            crime_viz = visualize_criminal_activities(
                df=filtered_data,
                selected_countries=filters["selected_countries"],
                year_range=filters["year_range"]
            )
            
            if crime_viz and "chart" in crime_viz:
                st.plotly_chart(crime_viz["chart"], use_container_width=True, key="tab2_criminal_activities_chart")
                
                # Display metrics
                if crime_viz and "metrics" in crime_viz:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Average Value", f"${crime_viz['metrics']['average_value']:,.0f}")
                    with col2:
                        st.metric("Maximum Value", f"${crime_viz['metrics']['max_value']:,.0f}")
                    with col3:
                        st.metric("Minimum Value", f"${crime_viz['metrics']['min_value']:,.0f}")
            else:
                st.info("No data available for Criminal Activities")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** IFFs generated from organized crime, trafficking, and corruption.  
**Proxy:** UNODC estimates on proceeds from criminal activity.
            """)

# === Tab 3: Detection and Enforcement ===
with tab3:
    # Indicator 4.4.3.1: Anti-IFF Enforcement Effectiveness
    with st.container():
        st.markdown("### Indicator 4.4.3.1: Anti-IFF Enforcement Effectiveness")
        st.caption("Proxied by WJP & CPIA Ratings")
        
        try:
            enforcement_viz = visualize_enforcement_effectiveness(
                df=filtered_data,
                selected_countries=filters["selected_countries"],
                year_range=filters["year_range"]
            )
            
            if enforcement_viz and "chart" in enforcement_viz:
                st.plotly_chart(enforcement_viz["chart"], use_container_width=True, key="tab3_enforcement_chart")
                
                # Display metrics
                if enforcement_viz and "metrics" in enforcement_viz:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Average Score", f"{enforcement_viz['metrics']['average_score']:.1f}")
                    with col2:
                        st.metric("Maximum Score", f"{enforcement_viz['metrics']['max_score']:.1f}")
                    with col3:
                        st.metric("Minimum Score", f"{enforcement_viz['metrics']['min_score']:.1f}")
            else:
                st.info("No data available for Enforcement Effectiveness")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Number of successful investigations and prosecutions.  
**Proxy:** Governance & transparency scores from WJP and CPIA.
            """)

    # Indicator 4.4.3.2: Corruption & Bribery
    with st.container():
        st.markdown("### Indicator 4.4.3.2: Corruption & Bribery")
        st.caption("Proxied by WJP & World Bank Governance Indicators")
        
        try:
            corruption_viz = visualize_corruption_index(
                df=filtered_data,
                selected_countries=filters["selected_countries"],
                year_range=filters["year_range"]
            )
            
            if corruption_viz and "chart" in corruption_viz:
                st.plotly_chart(corruption_viz["chart"], use_container_width=True, key="tab3_corruption_chart")
                
                # Display metrics
                if corruption_viz and "metrics" in corruption_viz:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Average Score", f"{corruption_viz['metrics']['average_score']:.1f}")
                    with col2:
                        st.metric("Maximum Score", f"{corruption_viz['metrics']['max_score']:.1f}")
                    with col3:
                        st.metric("Minimum Score", f"{corruption_viz['metrics']['min_score']:.1f}")
            else:
                st.info("No data available for Corruption Index")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Perceptions and incidents of corruption in public/private sectors.  
**Proxy:** Control of Corruption index, WJP bribery prevalence score.
            """)
