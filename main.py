import pandas as pd 
import streamlit as st
import Preprocessor

df = pd.read_csv("data.csv") 


# Creating Time Feature

df = Preprocessor.fetch_time_features(df)

#Tittle for Dashboard

st.title("Sales Analytics Dashboard")


# Side bar for filters
st.sidebar.title("Filters")


# Filters 

Selected_years =  Preprocessor.multi_select("Selecte Year",df["Financial_Year"].unique())
Selected_retailers = Preprocessor.multi_select("Select Retailer", df["Retailer"].unique())
Selected_Company = Preprocessor.multi_select("Select company", df["Company"].unique())
Selected_Month = Preprocessor.multi_select("Select  Month", df["Financial_Month"].unique())

filtered_df=df[(df["Financial_Year"].isin(Selected_years))&
            (df["Retailer"].isin(Selected_retailers)) &
            (df["Company"].isin(Selected_Company))&
            (df["Financial_Month"].isin(Selected_Month))]


# KPI - Key performance Indicator
# create columns for display KPIs

col1,col2,col3,col4= st.columns(4)

with col1:
    st.metric(label = "Total Sales", value = f'{int(filtered_df["Amount"].sum())}')


with col2:
    st.metric(label = "Total Margin", value = f'{int(filtered_df["Margin"].sum())}')

with col3:
    st.metric(label = "Total Transactions", value = len(filtered_df))

with col4:
    st.metric(label = "Margin Percentage", value = int((filtered_df["Margin"].sum()*100)/(filtered_df["Amount"].sum())))
    

# Visualization to analyze on month sales trends

yearly_sales = (filtered_df[["Financial_Year","Financial_Month","Amount"]]
               .groupby(["Financial_Year","Financial_Month"])
               .sum()
               .reset_index()
               .pivot(index ="Financial_Month", columns ="Financial_Year", values ="Amount"))

st.line_chart(yearly_sales,x_label = "Financial_Month", y_label = "Total Sales")


# Visualize Retail count by Revenue %

col5 , col6 = st.columns(2)

with col5:
    st.title("Retailer count by Revenue %")
    retailer_count = Preprocessor.fetch_top_revenue_retailers(filtered_df)
    retailer_count.set_index ("percentage revenue", inplace = True)
    st.bar_chart(retailer_count,x_label ="percentage revenue",y_label = "retailer_count" )

# 
with col6:
    st.title("Company count by Revenue %")
    company_count = Preprocessor.fetch_top_revenue_companies(filtered_df)
    company_count.set_index ("percentage revenue", inplace = True)
    st.bar_chart(retailer_count,x_label ="percentage revenue",y_label = "Company_count" )
















