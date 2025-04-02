import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

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

    st.title("Sales")
    st.sidebar.header("Filters & Chart Options")

    # Get current year
    current_year = datetime.now().year

    # Year filter (Multi-select)
    years = sorted(data["Year"].dropna().unique())
    default_years = [current_year] if current_year in years else [years[-1]]  # fallback to latest if current year not present

    selected_years = st.sidebar.multiselect(
        "Select Year(s)",
        options=years,
        default=default_years
    )

    # Y-Axis options
    y_axis_options = {
        "Total Field Boxes": "Total Field Boxes",
        "Field Boxes Per Acre": "Field Boxes Per Acre",
        "Total Bins (Tons)": "Total Bins (Tons)",
        "Bins Per Acre": "Bins per Acre",
        "$ / Bin": "$ / Bin",
        "Total Revenue": "Total Revenue"
    }

    y_axis_label = st.sidebar.selectbox("Select Y-Axis", options=list(y_axis_options.keys()))

    # Define custom color map
    color_map = {
        "Clementine": "turquoise",
        "Tango": "red",
        "Washington": "orange",
        "Atwood": "orange",
        "Cara Cara": "orange",
        "Powell": "orange",
        "Valencia": "purple",
        "Lemon": "yellow",
        "Grapefruit": "pink",
        "Late Lane": "orange"
    }

    # Custom block order
    custom_block_order = [
        "1 (OLD)", "2 (OLD)", "1", "2A", "2B", "3", "4", "5", "6", "7", "8", "9",
        "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"
    ]

    # Filter data based on year selection
    sales_filtered = data[data["Year"].isin(selected_years)]

    # === Fix: remove facet_col when only one year is selected ===
    if len(selected_years) > 1:
        fig = px.bar(
            sales_filtered,
            x="Block",
            y=y_axis_options[y_axis_label],
            color="Variety",
            color_discrete_map=color_map,
            category_orders={"Block": custom_block_order},
            facet_col="Year",
            labels={"Block": "Block", y_axis_options[y_axis_label]: y_axis_label},
        )
    else:
        fig = px.bar(
            sales_filtered,
            x="Block",
            y=y_axis_options[y_axis_label],
            color="Variety",
            color_discrete_map=color_map,
            category_orders={"Block": custom_block_order},
            labels={"Block": "Block", y_axis_options[y_axis_label]: y_axis_label},
        )

    fig.update_layout(
        bargap=0.3,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title_x=0.5,
        margin=dict(t=30)
    )

    st.plotly_chart(fig, use_container_width=True)
