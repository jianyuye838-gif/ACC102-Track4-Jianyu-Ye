# ACC102 Track4: Corporate Financial Health Analyzer
An interactive Python financial analysis tool using real WRDS Compustat data.

## 1. Purpose
This tool helps users compare the financial health of two public companies by analyzing key ratios including profitability, liquidity, solvency, and efficiency.

## 2. Data Source
- Database: WRDS Compustat (funda)
- Access Date: April 2026
- Variables: Revenue, Net Income, Assets, Liabilities, EPS, Cash

## 3. Core Functions
- Connect to WRDS with username and password
- Pull real annual financial data
- Calculate professional financial ratios
- Visualize trends with full-size charts
- Auto-generate analysis and comparison

## 4. How to Run
1. Install dependencies:
pip install -r requirements.txt

2. Run the tool:
streamlit run app.py

3. Enter WRDS credentials and run analysis.

## 5. Project Structure
- app.py: Main Streamlit application
- ACC102_Track4.ipynb: Analysis notebook
- README.md: Project documentation
- requirements.txt: Dependencies

## 6. Limitations
- Requires valid WRDS account
- Only annual data supported
- WRDS login restricted to campus network / local terminal
