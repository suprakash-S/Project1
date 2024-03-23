import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:", layout="wide")

df = pd.read_csv("/content/drive/MyDrive/supermarket_sales - Sheet1 (2).csv")

st.sidebar.header("Filters")
city = st.sidebar.multiselect(
    "Pick a city : ", options=df["City"].unique(), default=df["City"].unique())
customer = st.sidebar.multiselect(
    "Customer type : ", options=df["Customer_type"].unique(), default=df["Customer_type"].unique())
product = st.sidebar.multiselect(
    "Product line : ", options=df["Product_line"].unique(), default=df["Product_line"].unique())
customerGender = st.sidebar.multiselect(
    "Gender : ", options=df["Gender"].unique(), default=df["Gender"].unique())

df_selection = df.query(
    "City == @city & Customer_type == @customer & Product_line == @product & Gender == @customerGender")

# st.dataframe(df_selection)


st.title(":bar_chart: Sales Dashboard ")
st.markdown("##")

total = round(df_selection["Total"].sum())
avg_sale_transc = round(df_selection["Total"].mean())
avg_rating = round(df_selection["Rating"].mean(), 1)
starRating = ":star:" * int(round(avg_rating, 0))

left, middle, right = st.columns(3)
with left:
    st.subheader("Total Sales : ")
    st.subheader(f"US $ {total:,}")
with middle:
    st.subheader("Average Rating :")
    st.subheader(f"{avg_rating} {starRating}")
with right:
    st.subheader("Average sales per transaction :")
    st.subheader(f"US $ {avg_sale_transc}")

st.markdown("---")

# Sales by Product Graph
sales_by_product = (df_selection.groupby(by=["Product_line"]).sum()["Total"])
fig_product_sale = px.bar(sales_by_product, x="Total", y=sales_by_product.index, orientation="h",
                          template="plotly_white", title="<b>Sales by Product<b>")

#Payment Type
payment_method_type = df_selection.groupby(by=["Payment"]).sum()["Total"]
fig_payment = px.bar(payment_method_type, x="Total", y=payment_method_type.index, orientation="h",template="plotly_white",title="<b>Payment Type<b>")


#Gender Pie Chart

dataFrame = df["Gender"].value_counts()
random_x = [dataFrame[0],dataFrame[1]]
names = ['Female','Male']
fig = px.pie(values=random_x,names = names,title="Overall Gender ratio")


st.plotly_chart(fig_product_sale)
st.markdown("##")
st.plotly_chart(fig_payment)
st.markdown("##")
st.plotly_chart(fig)

# Hiding St contents

hide_st_style = """
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
</style>
"""

st.markdown(hide_st_style,unsafe_allow_html=True)
