import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)


df = pd.read_csv("data/retail_sales_dataset.csv")
df['Date'] = pd.to_datetime(df['Date'])


st.sidebar.title("🔍 Filters")

category = st.sidebar.multiselect(
    "Select Category",
    options=df['Product Category'].unique(),
    default=df['Product Category'].unique()
)

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)


filtered_df = df[
    (df['Product Category'].isin(category)) &
    (df['Gender'].isin(gender))
]


st.title("📊 Retail Sales Dashboard")
st.markdown("Analyze sales performance, customer behavior, and trends")


total_sales = filtered_df['Total Amount'].sum()
total_orders = filtered_df.shape[0]
avg_sales = filtered_df['Total Amount'].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"₹ {total_sales:,.0f}")
col2.metric("🧾 Total Orders", total_orders)
col3.metric("📈 Avg Order Value", f"₹ {avg_sales:,.0f}")

st.markdown("---")



col1, col2 = st.columns(2)

# Sales by Category
with col1:
    st.subheader("📦 Sales by Category")
    category_sales = filtered_df.groupby('Product Category')['Total Amount'].sum()
    st.bar_chart(category_sales)

# Sales by Gender
with col2:
    st.subheader("👥 Sales by Gender")
    gender_sales = filtered_df.groupby('Gender')['Total Amount'].sum()
    st.bar_chart(gender_sales)


st.subheader("📈 Sales Over Time")

trend = filtered_df.groupby('Date')['Total Amount'].sum()
st.line_chart(trend)


st.markdown("---")
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head(20))


st.markdown("---")

st.markdown("---")
st.subheader("📥 Download Report")


csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📄 Download Filtered Data as CSV",
    data=csv,
    file_name='retail_sales_report.csv',
    mime='text/csv'
)


summary = filtered_df.groupby('Product Category')['Total Amount'].sum().reset_index()

csv_summary = summary.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📊 Download Sales Summary",
    data=csv_summary,
    file_name='sales_summary.csv',
    mime='text/csv'
)