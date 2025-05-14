"""
COVID-19 GLOBAL DATA TRACKER
Analysis of cases, deaths, and vaccinations worldwide
"""

# SECTION 1: SETUP AND DATA LOADING
# =================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px # type: ignore
from datetime import datetime

# Explanation: 
# We import essential libraries:
# - pandas for data manipulation
# - matplotlib/seaborn for static visualizations
# - plotly for interactive maps
# - datetime for date handling

def load_data():
    """Load and prepare COVID-19 dataset"""
    try:
        # Try loading from Our World in Data directly
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        df = pd.read_csv(url)
        print("✅ Successfully loaded live data from OWiD")
    except Exception as e:
        print(f"⚠️ Online load failed: {e}\nLoading local file...")
        df = pd.read_csv('data/owid-covid-data.csv')
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    return df

# Explanation:
# This function attempts to load fresh data directly from the source
# Falls back to local file if internet connection fails
# Automatically converts dates to datetime objects for easier time-based analysis

# SECTION 2: DATA CLEANING
# ========================

def clean_data(df, countries=None):
    """Clean and prepare COVID data for analysis"""
    if not countries:
        countries = ['United States', 'India', 'Brazil', 'Germany', 'Kenya', 'South Africa']
    
    # Filter selected countries
    df_clean = df[df['location'].isin(countries)].copy()
    
    # Handle missing values in critical columns
    critical_cols = ['total_cases', 'total_deaths', 'total_vaccinations', 'population']
    df_clean = df_clean.dropna(subset=critical_cols[:2], how='all')
    
    # Forward fill missing values within each country's data
    df_clean[critical_cols] = df_clean.groupby('location')[critical_cols].fillna(method='ffill')
    
    # Calculate derived metrics
    df_clean['death_rate'] = df_clean['total_deaths'] / df_clean['total_cases']
    df_clean['cases_per_million'] = (df_clean['total_cases'] / df_clean['population']) * 1e6
    df_clean['vaccination_per_hundred'] = (df_clean['total_vaccinations'] / df_clean['population']) * 100
    
    return df_clean

# Explanation:
# - Filters data to only selected countries for focused analysis
# - Drops rows missing both cases and deaths data
# - Uses forward-fill to handle missing values in time series
# - Calculates important derived metrics like death rate and per-capita measures

# SECTION 3: EXPLORATORY DATA ANALYSIS
# ===================================

def plot_time_series(df, countries):
    """Generate time series plots for cases, deaths, and vaccinations"""
    plt.style.use('seaborn')
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Total Cases
    for country in countries:
        country_data = df[df['location'] == country]
        axes[0,0].plot(country_data['date'], country_data['total_cases'], label=country)
    axes[0,0].set_title('Total COVID-19 Cases', fontsize=12)
    axes[0,0].set_ylabel('Cases', fontsize=10)
    axes[0,0].legend(fontsize=8)
    
    # Plot 2: Total Deaths
    for country in countries:
        country_data = df[df['location'] == country]
        axes[0,1].plot(country_data['date'], country_data['total_deaths'], label=country)
    axes[0,1].set_title('Total COVID-19 Deaths', fontsize=12)
    axes[0,1].set_ylabel('Deaths', fontsize=10)
    
    # Plot 3: New Cases (7-day average)
    for country in countries:
        country_data = df[df['location'] == country]
        axes[1,0].plot(country_data['date'], 
                      country_data['new_cases'].rolling(7).mean(), 
                      label=country)
    axes[1,0].set_title('7-Day Average of New Cases', fontsize=12)
    axes[1,0].set_ylabel('New Cases', fontsize=10)
    
    # Plot 4: Death Rate
    for country in countries:
        country_data = df[df['location'] == country]
        axes[1,1].plot(country_data['date'], 
                      country_data['death_rate'].rolling(7).mean(), 
                      label=country)
    axes[1,1].set_title('7-Day Average Death Rate', fontsize=12)
    axes[1,1].set_ylabel('Death Rate', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('output/time_series.png', dpi=300)
    plt.close()
    print("📈 Saved time series plots to output/time_series.png")

# Explanation:
# - Creates a 2x2 grid of plots showing different aspects of the pandemic
# - Uses rolling averages for smoother trends in new cases and death rates
# - Saves output to file rather than showing interactively (better for reports)
# - Customizes fonts and layout for professional appearance

# SECTION 4: VACCINATION ANALYSIS
# ==============================

def plot_vaccination(df, countries):
    """Analyze and visualize vaccination progress"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Total Vaccinations
    for country in countries:
        country_data = df[df['location'] == country].dropna(subset=['total_vaccinations'])
        axes[0].plot(country_data['date'], country_data['total_vaccinations'], label=country)
    axes[0].set_title('Total Vaccinations', fontsize=12)
    axes[0].set_ylabel('Vaccinations', fontsize=10)
    axes[0].legend(fontsize=8)
    
    # Plot 2: Vaccination Percentage
    for country in countries:
        country_data = df[df['location'] == country].dropna(subset=['vaccination_per_hundred'])
        axes[1].plot(country_data['date'], country_data['vaccination_per_hundred'], label=country)
    axes[1].set_title('Vaccinations per 100 People', fontsize=12)
    axes[1].set_ylabel('% Population Vaccinated', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('output/vaccination.png', dpi=300)
    plt.close()
    print("💉 Saved vaccination plots to output/vaccination.png")

# Explanation:
# - Shows both absolute vaccination numbers and population-adjusted rates
# - Drops missing values specifically for vaccination data
# - Uses consistent styling with the previous plots
# - Saves to separate file for modular reporting

# SECTION 5: GLOBAL CHOROPLETH MAP
# ================================

def generate_choropleth(df):
    """Create interactive world map visualization"""
    latest_date = df['date'].max()
    latest_global = df[df['date'] == latest_date]
    
    fig = px.choropleth(latest_global,
                        locations="iso_code",
                        color="total_cases_per_million",
                        hover_name="location",
                        hover_data=["total_cases", "total_deaths"],
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title=f"COVID-19 Cases per Million (as of {latest_date})",
                        labels={'total_cases_per_million': 'Cases per Million'})
    
    fig.write_html("output/choropleth.html")
    print("🌍 Saved interactive choropleth to output/choropleth.html")

# Explanation:
# - Uses Plotly Express for interactive visualization
# - Shows latest available data with hover information
# - Saves as HTML file that can be opened in any browser
# - Uses a perceptually uniform color scale (Plasma)

# SECTION 6: MAIN EXECUTION
# =========================

if __name__ == "__main__":
    print("\nCOVID-19 DATA ANALYSIS STARTED")
    print("=============================")
    
    # Create output directory
    import os
    os.makedirs("output", exist_ok=True)
    
    # Load and clean data
    raw_data = load_data()
    cleaned_data = clean_data(raw_data)
    
    # Get list of countries actually present in cleaned data
    available_countries = cleaned_data['location'].unique().tolist()
    
    # Generate visualizations
    plot_time_series(cleaned_data, available_countries)
    plot_vaccination(cleaned_data, available_countries)
    generate_choropleth(raw_data)  # Use raw data for global view
    
    print("\nANALYSIS COMPLETE")
    print("=================")
    print("Generated files in /output directory:")
    print("- time_series.png: Case/death trends")
    print("- vaccination.png: Vaccination progress")
    print("- choropleth.html: Interactive world map")

# Explanation:
# - Main execution block ensures code only runs when script is executed directly
# - Creates necessary output directory
# - Shows progress messages in console
# - Handles case where some countries might have been filtered out during cleaning
