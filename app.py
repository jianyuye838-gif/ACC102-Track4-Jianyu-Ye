# ACC102 Track4 - Corporate Financial Health Analyzer
# WRDS Real Data | Professional Business Analysis
import streamlit as st
import wrds
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------
# PAGE SETUP
# --------------------------
st.set_page_config(
    page_title="Corporate Financial Health Analyzer",
    page_icon="📊",
    layout="wide"
)

# --------------------------
# WRDS CONNECTION (SUPPORTS USERNAME + PASSWORD)
# --------------------------
@st.cache_resource
def connect_wrds(username, password):
    try:
        return wrds.Connection(wrds_username=username, wrds_password=password)
    except Exception as e:
        st.error(f"❌ WRDS Login Failed. Check username or password.")
        return None

# --------------------------
# FETCH REAL WRDS FINANCIAL DATA
# --------------------------
def get_financials(conn, ticker, start_year, end_year):
    query = f"""
        SELECT fyear, revt, ni, at, act, lct, lt, ebitda, epspx, che
        FROM comp.funda
        WHERE tic = '{ticker}'
        AND fyear BETWEEN {start_year} AND {end_year}
        AND indfmt='INDL' AND datafmt='STD' AND consol='C'
        ORDER BY fyear
    """
    df = conn.raw_sql(query)
    df.columns = ["Year", "Revenue", "NetIncome", "TotalAssets",
                  "CurrentAssets", "CurrentLiabilities", "TotalLiabilities",
                  "EBITDA", "EPS", "Cash"]
    return df

# --------------------------
# FULL ACADEMIC RATIOS
# --------------------------
def calculate_full_metrics(df):
    df = df.copy()
    df["Revenue_Growth(%)"] = (df["Revenue"].pct_change() * 100).round(2)
    df["NI_Growth(%)"] = (df["NetIncome"].pct_change() * 100).round(2)
    df["Gross_Margin(%)"] = (df.EBITDA / df.Revenue * 100).round(2)
    df["Net_Margin(%)"] = (df.NetIncome / df.Revenue * 100).round(2)
    df["ROA(%)"] = (df.NetIncome / df.TotalAssets * 100).round(2)
    df["ROE(%)"] = (df.NetIncome / (df.TotalAssets - df.TotalLiabilities) * 100).round(2)
    df["Current_Ratio"] = (df.CurrentAssets / df.CurrentLiabilities).round(2)
    df["Debt_Ratio(%)"] = (df.TotalLiabilities / df.TotalAssets * 100).round(2)
    df["Cash_Ratio"] = (df.Cash / df.CurrentLiabilities).round(2)
    df["Equity"] = (df.TotalAssets - df.TotalLiabilities).round(2)
    df["EPS"] = df["EPS"].round(2)
    return df

# --------------------------
# --------------------------
def plot_single_metric(df, company, col, title):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["Year"], df[col], marker='o', linewidth=2.5, color='#2E86AB')
    ax.set_title(f"{company} | {title}", fontsize=14, weight='bold')
    ax.set_ylabel(col)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    return fig

# --------------------------
# AUTO-GENERATED PROFESSIONAL ANALYSIS
# --------------------------
def generate_pro_analysis(df):
    latest = df.iloc[-1]
    comments = []

    if latest["Net_Margin(%)"] > 15:
        comments.append("✅ **Profitability**: Strong & above industry average.")
    else:
        comments.append("⚠️ **Profitability**: Moderate, room for improvement.")

    if latest["Current_Ratio"] > 1.5:
        comments.append("✅ **Liquidity**: Healthy short-term financial position.")
    else:
        comments.append("⚠️ **Liquidity**: Slightly tight working capital.")

    if latest["Debt_Ratio(%)"] < 50:
        comments.append("✅ **Solvency**: Low financial risk & stable leverage.")
    else:
        comments.append("⚠️ **Solvency**: High debt increases financial risk.")

    if latest["ROE(%)"] > 15:
        comments.append("✅ **Efficiency**: Excellent return to shareholders.")
    else:
        comments.append("⚠️ **Efficiency**: Average return on equity.")

    return comments

# --------------------------
# RISK RATING
# --------------------------
def get_rating(df):
    l = df.iloc[-1]
    score = 0
    if l["Net_Margin(%)"] > 10: score += 1
    if l["ROA(%)"] > 8: score +=1
    if l["Current_Ratio"] > 1.2: score +=1
    if l["Debt_Ratio(%)"] < 60: score +=1
    rating = ["Poor", "Average", "Good", "Very Good", "Excellent"]
    return rating[score]

# --------------------------
# MAIN INTERFACE
# --------------------------
st.title("📊 CORPORATE FINANCIAL HEALTH ANALYZER")
st.markdown("## ACC102 TRACK4 | WRDS Real Data | Business Performance Analysis")
st.divider()

# SIDEBAR
with st.sidebar:
    st.subheader("🔐 WRDS LOGIN")
    username = st.text_input("WRDS Username")
    password = st.text_input("WRDS Password", type="password")
    
    st.subheader("🏢 COMPANY COMPARISON")
    ticker1 = st.text_input("Main Company", "AAPL")
    ticker2 = st.text_input("Peer Company", "MSFT")
    
    st.subheader("🗓️ YEAR RANGE")
    start = st.slider("From", 2010, 2024, 2016)
    end = st.slider("To", start, 2024, 2024)
    
    run = st.button("🚀 RUN ANALYSIS", type="primary")

# --------------------------
# RUN ANALYSIS
# --------------------------
if run:
    conn = connect_wrds(username, password)
    if not conn:
        st.stop()

    with st.spinner("Loading WRDS data..."):
        df1 = get_financials(conn, ticker1, start, end)
        df2 = get_financials(conn, ticker2, start, end)

    df1 = calculate_full_metrics(df1)
    df2 = calculate_full_metrics(df2)

    st.success(f"✅ ANALYSIS READY: {ticker1} vs {ticker2}")

    # ----------------------
    # 1. DATA TABLES
    # ----------------------
    st.subheader("📋 Financial Metrics Table")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {ticker1}")
        st.dataframe(df1.round(2), use_container_width=True)
    with col2:
        st.markdown(f"### {ticker2}")
        st.dataframe(df2.round(2), use_container_width=True)

    st.divider()

    # ----------------------
    # ----------------------
    st.subheader(f"📈 {ticker1} — Key Financial Trends (Full Size)")
    
    metrics = [
        ("Net_Margin(%)", "Net Profit Margin"),
        ("ROA(%)", "Return on Assets"),
        ("ROE(%)", "Return on Equity"),
        ("Current_Ratio", "Current Ratio"),
        ("Debt_Ratio(%)", "Debt Ratio"),
        ("EPS", "Earnings Per Share")
    ]
    
    for col, title in metrics:
        st.pyplot(plot_single_metric(df1, ticker1, col, title))

    st.divider()

    st.subheader(f"📈 {ticker2} — Key Financial Trends (Full Size)")
    for col, title in metrics:
        st.pyplot(plot_single_metric(df2, ticker2, col, title))

    st.divider()

    # ----------------------
    # 3. ANALYSIS & RECOMMENDATION
    # ----------------------
    st.subheader("💡 Professional Financial Analysis")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"### {ticker1} | {get_rating(df1)}")
        for line in generate_pro_analysis(df1):
            st.write(line)
    with c2:
        st.markdown(f"### {ticker2} | {get_rating(df2)}")
        for line in generate_pro_analysis(df2):
            st.write(line)

    st.subheader("🏆 Final Comparison & Recommendation")
    r1 = df1.iloc[-1]["ROE(%)"]
    r2 = df2.iloc[-1]["ROE(%)"]
    winner = ticker1 if r1 > r2 else ticker2

    st.success(f"""
    **FINAL INVESTMENT RECOMMENDATION**:  
    **{winner}** is financially stronger, more efficient, and less risky.  
    It shows better profitability, liquidity, and solvency.
    """)

st.caption("📊 ACC102 Track4 | WRDS Financial Dashboard | Academic Use Only")