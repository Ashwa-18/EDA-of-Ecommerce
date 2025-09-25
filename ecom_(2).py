# -*- coding: utf-8 -*-
"""ecom (2).ipynb



**Name** : **Ashwa Asghar**

**Roll No**: **FA23-BST-018**

**Section** : **BST-B**

**Instructor**: **Dr.Noman**

**Title**: **Ecommerce Analysis**

#  Ecommerce Analysis

##  <u>Introduction</u>

This DataSet focuses on Ecommerce Analysis using EDA(Exploratory Data Analysis) data visualization techniques.

##  Ecommerce Dataset Overview

- The dataset contains **transactional data** of ecommerce orders.
###  Columns
1. `order_date`: Date when the order was placed  
2. `price`: Price of a single unit of the product  
3. `quantity`: Number of units ordered  
4. `discount`: Discount applied on the order  
5. `sales`: Derived column = `price * quantity * (1 - discount)`  

###  Target Variable:
- sales

# Importing all required libraries
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import io


"""#  Load Data"""

st.title("📂 Upload Your Ecommerce Dataset")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())
    
    st.write("Shape of dataset:", df.shape)
else:
    st.warning("Please upload a CSV file to proceed.")



st.header(" Exploratory Data Analysis (EDA)")

st.subheader("Descriptive Analysis")


buffer = io.StringIO()
df.info(buf=buffer)     # capture df.info() output into the buffer
info_str = buffer.getvalue()
st.text(info_str)   

st.write("Missing Values:")
st.write(df.isnull().sum())

st.write("Duplicate Records:")
st.write(df.duplicated().sum())

st.subheader("Data Cleaning and Processing")

#### I do not want Price in Float(decimal) data type .I have to convert it into int.


df["price"]=df["price"].astype("int")
df["price"]

df["sales"]=df["price"]*df["quantity"]*(1-df["discount"])

df["sales"]=df["sales"].astype("int")
st.dataframe(df.head())

df["order_date"]=pd.to_datetime(df["order_date"])
df["order_date"]

st.subheader("Data Analysis") 

st.write(df["category"].value_counts())


st.subheader("I want to see how many orders belong to each category, so that's why I plotted this bar chart.")


category_counts=df["category"].value_counts().reset_index()
category_counts.columns = ["category" , "count"]
fig=px.bar(category_counts, x="category",y="count",title =" Category counts ",text="count",color="category")
st.plotly_chart(fig)


st.subheader("I want to see the share of sales from each region, so I used a pie chart to visualize it.")


fig= px.pie(df,names=df["region"],values=df["sales"],title="category By price")
st.plotly_chart(fig)

st.subheader("I want to analyze total sales for each month, so that's why I plotted this bar chart.")


df["month"] = df["order_date"].dt.month_name()

fig, ax = plt.subplots()
sns.barplot(data=df, x="month", y="sales", estimator=sum, ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)



st.subheader("I want to Total Quantity Sold by Category, so that's why I plotted this bar plot")

fig, ax = plt.subplots()
sns.barplot(df,x="category", y="quantity",estimator=sum,hue="category", palette="viridis")
plt.xticks(rotation=90)
plt.title("Total Quantity Sold by Category")
st.pyplot(fig)


st.subheader("I want to understand the distribution of sales across different categories, so I plotted a box plot to visualize the spread, median, and outliers for each category")

fig,ax = plt.subplot()
sns.boxplot(df,x="category", y="sales",hue="category", palette="Set2")

plt.title("Distribution of Sales by Category")
st.pyplot(fig)


st.subheader("I want to analyze the relationship between product categories and payment methods, so I plotted a heatmap showing the number of transactions for each category–payment method combination.")

fig,ax = plt.subplots()
heatmap_grouped = pd.crosstab(df["category"],df["payment_method"])
sns.heatmap(heatmap_grouped,cmap="Blues",annot=True,fmt="d")
plt.xticks(rotation=45)
plt.title("category VS Payment Method")
st.pyplot(fig)


st.subheader("I want to see how total sales vary across the days of the week, so I plotted a bar chart showing the sum of sales for each weekday.")

fig,ax=plt.subplots()
df["day_name"]=df["order_date"].dt.day_name()
cswgroup=df.groupby(["day_name"])["sales"].sum().reset_index()
sns.barplot(cswgroup,x="day_name", y="sales",hue="day_name", palette="pastel")
plt.xticks(rotation=90)
plt.title("Total Sales by Week days")
st.pyplot(fig)


st.subheader("I want to compare total sales across different categories,so that's why I plotted this horizontal bar chart")


cswgroup=df.groupby(["category", "region"])["sales"].sum().reset_index()
fig,ax=plt.subplots()
sns.barplot(cswgroup,y="category", x="sales", hue="region", palette="tab10")
plt.xticks(rotation=90)
plt.title("Total Sales by category across Regions")
st.pyplot(fig)

