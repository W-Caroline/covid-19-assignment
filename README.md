# COVID-19 Global Data Tracker

## Project Description
A Python data analysis project that processes and visualizes global COVID-19 trends. The system loads data from Our World in Data, performs cleaning and analysis, and generates visualizations of cases, deaths, and vaccination progress.

## Objectives
✅ Import and clean COVID-19 dataset  
✅ Analyze time trends in cases and deaths  
✅ Compare metrics across selected countries  
✅ Visualize vaccination progress  
✅ Generate interactive world map visualization  

## Tools & Libraries
- **Python 3** (VS Code environment)
- **Core Libraries**: pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly Express
- **Data Source**: [Our World in Data COVID-19 Dataset](https://covid.ourworldindata.org/data/owid-covid-data.csv)

## Setup Instructions

1. **Clone the repository** (if applicable)
   ```bash
   git clone [your-repository-url]
   cd covid-data-tracker
   
2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install pandas matplotlib seaborn plotly
   
3. **Download the dataset**

   Manually download owid-covid-data.csv

   Place it in a data folder in your project directory

4. **Run the analysis**

   ```bash
   python analysis.py
   
**Expected Outputs**
When you run the analysis script, it will:

- Create an output folder automatically

- Generate these files:

      time_series.png: Comparative charts of cases/deaths

      vaccination.png: Vaccination progress charts

      choropleth.html: Interactive world map (open in browser)

**Key Insights from Analysis**
1. Case Trajectories: Countries show different pandemic wave patterns based on government responses and variants.

2. Vaccination Gaps: Clear disparities visible between developed and developing nations in vaccination rates.

3. Data Challenges:

      Missing early vaccination data for some countries

      Need for careful handling of case/death ratios with small numbers

**Customization Options**

You can modify these aspects in analysis.py:

  - Change target countries in the countries list

  - Adjust date ranges by filtering the DataFrame

  - Modify visualization styles in the plotting functions

**Troubleshooting**
If you get file not found errors:

  - Verify the CSV is in data/owid-covid-data.csv

  - Check the working directory in VS Code

For Plotly errors:

  - Ensure you have the latest version: pip install --upgrade plotly
