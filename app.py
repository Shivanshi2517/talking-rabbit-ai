import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Talking Rabbit AI", page_icon="🐰", layout="wide")

# ---------- Custom CSS ----------
st.markdown("""
<style>

/* Gradient Background */
.stApp {
background: linear-gradient(135deg,#e0f2fe,#dbeafe,#bfdbfe,#93c5fd);
}

/* Title */
.main-title{
font-size:50px;
font-weight:800;
color:#1e3a8a;
}

/* Subtitle */
.subtitle{
color:#1e293b;
font-size:18px;
}

/* Metrics Card */
[data-testid="metric-container"]{
background:white;
border-radius:12px;
padding:15px;
}

/* Buttons */
.stButton>button{
background:#2563eb;
color:white;
border-radius:10px;
padding:10px 20px;
border:none;
}

/* File uploader button */
[data-testid="stFileUploader"] button {
background-color: #2563eb;
color: white;
border-radius: 8px;
border: none;
padding: 8px 16px;
}

/* Hover effect */
[data-testid="stFileUploader"] button:hover {
background-color: #1d4ed8;
color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
col_logo, col_title = st.columns([1,6])

with col_logo:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
        width=95
    )

with col_title:
    st.markdown(
        "<h1 class='main-title'>Talking Rabbit AI</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p class='subtitle'>Ask questions from your business data instantly</p>",
        unsafe_allow_html=True
    )

st.divider()

# ---------- Upload ----------
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # ---------- Dataset Information ----------
    st.subheader("📊 Dataset Information")

    colA, colB = st.columns(2)

    with colA:
        st.write("Rows:", df.shape[0])
        st.write("Columns:", df.shape[1])

    with colB:
        st.write("Column Names:")
        st.write(df.columns.tolist())

    st.divider()

    # ---------- Metrics ----------
    total_revenue = df["Revenue"].sum()
    avg_revenue = df["Revenue"].mean()
    max_revenue = df["Revenue"].max()

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Revenue", total_revenue)
    col2.metric("📊 Average Revenue", round(avg_revenue,2))
    col3.metric("🚀 Highest Revenue", max_revenue)

    st.divider()

    # ---------- Layout ----------
    left, right = st.columns([2,1])

    with left:
        st.subheader("📋 Dataset Preview")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)

        st.download_button(
            label="⬇ Download Dataset",
            data=csv,
            file_name="dataset.csv",
            mime="text/csv"
        )

    with right:
        st.subheader("🤖 Ask Your Data")

        question = st.text_input("Ask a question")

        st.info("🐰 Tip: Try asking 'highest revenue', 'lowest revenue', or 'total revenue'")

        if question:

            if "highest revenue" in question.lower():
                row = df.loc[df["Revenue"].idxmax()]
                st.success(f"🏆 {row['Region']} has highest revenue: {row['Revenue']}")

            elif "lowest revenue" in question.lower():
                row = df.loc[df["Revenue"].idxmin()]
                st.warning(f"📉 {row['Region']} has lowest revenue: {row['Revenue']}")

            elif "total revenue" in question.lower():
                st.info(f"💰 Total revenue is {df['Revenue'].sum()}")

            else:
                st.error("Sorry, I can't answer that yet.")

    st.divider()

    # ---------- Bar Chart ----------
    st.subheader("📈 Revenue by Region")

    fig, ax = plt.subplots(figsize=(5,3))

    df.groupby("Region")["Revenue"].sum().plot(
        kind="bar",
        color=["red","yellow","green","orange"],
        ax=ax
    )

    ax.set_ylabel("Revenue")
    ax.set_xlabel("Region")

    st.pyplot(fig)

    # ---------- Pie Chart ----------
    st.subheader("🥧 Revenue Distribution")

    fig2, ax2 = plt.subplots(figsize=(4,4))

    df.groupby("Region")["Revenue"].sum().plot(
        kind="pie",
        autopct='%1.1f%%',
        colors=["red","yellow","green","orange"],
        ax=ax2
    )

    ax2.set_ylabel("")

    st.pyplot(fig2)