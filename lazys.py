import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit page configuration
st.set_page_config(page_title="Financial Dashboard", layout="wide")

# Load Excel file
file_path = "Financials.xlsx"
data = pd.read_excel(file_path, sheet_name="Streamlit")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go To", ["Lot Map", "Sales"])

# Lot Map Page
if page == "Lot Map":
    st.title("Lot Map")
    st.write("(Placeholder for Lot Map)")

# Sales Page
elif page == "Sales":
    st.title("\U0001F4CA Financial Sales Dashboard")
    st.markdown("<h4 style='color:gray;'>Interactive Analysis of Sales Data</h4>", unsafe_allow_html=True)

    st.sidebar.header("Filters & Chart Options")

    # Year filter
    years = sorted(data["Year"].dropna().unique())
    years_options = ["All"] + years

    selected_year = st.sidebar.selectbox("Select Year", options=years_options, index=0)

    if selected_year == "All":
        sales_filtered = data.copy()
    else:
        sales_filtered = data[data["Year"] == selected_year]

    # Filter data
    filtered_data = data[data["Year"].isin(selected_years)]

    # X-Axis Options
    x_axis = st.sidebar.selectbox("Select X-Axis", options=["Block", "Variety"])

    # Y-Axis Options
    y_axis = st.sidebar.selectbox("Select Y-Axis", options=[
        "Total Field Boxes", 
        "Field Boxes Per Acre", 
        "Total Bins (tons)", 
        "Bins Per Acre", 
        "$ / Bin", 
        "Total Revenue"
    ])

    # Bar Chart
    st.markdown(f"### Bar Chart: {y_axis} by {x_axis}")
    fig = px.bar(filtered_data, x=x_axis, y=y_axis, color=x_axis, 
                 labels={x_axis: x_axis, y_axis: y_axis},
                 title=f"{y_axis} grouped by {x_axis}")
    fig.update_layout(bargap=0.3, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
