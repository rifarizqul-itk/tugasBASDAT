import streamlit as st
import pandas as pd
from datetime import datetime

from config import *

st.set_page_config("Dashboard", page_icon="", layout="wide")

result_customers = view_customers()
df_customers = pd.DataFrame(result_customers, columns=[
    "customer_id", "name", "email", "phone", "address", "birthdate"
])

df_customers["birthdate"] = pd.to_datetime(df_customers["birthdate"])
df_customers["Age"] = (datetime.now() - df_customers["birthdate"]).dt.days // 365

result_products = view_products()
df_products = pd.DataFrame(result_products, columns=[
    "product_id", "name", "description", "price", "stock"
])

result_orders = view_orders_with_customers()
df_orders = pd.DataFrame(result_orders, columns=[
    "order_id", "order_date", "total_amount", "customer_name", "phone"
])

result_order_details = view_order_details_with_info()
df_order_details = pd.DataFrame(result_order_details, columns=[
    "order_detail_id", "order_id", "order_date", "customer_id", "customer_name",
    "product_id", "product_name", "unit_price", "quantity", "subtotal",
    "order_total", "phone"
])


@st.cache_data
def to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def tabelCustomers_dan_export():
    total_customers = df_customers.shape[0]

    col1, _, _ = st.columns(3)
    with col1:
        st.metric("📦 Total Pelanggan", total_customers)

    st.sidebar.header("Filter Rentang Usia")
    min_age = int(df_customers["Age"].min())
    max_age = int(df_customers["Age"].max())

    age_range = st.sidebar.slider(
        "Pilih Rentang Usia",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )

    filtered = df_customers[df_customers["Age"].between(*age_range)]

    st.markdown("### 📋 Tabel Data Pelanggan")
    show_cols = st.multiselect(
        "Pilih Kolom Pelanggan",
        options=filtered.columns,
        default=filtered.columns
    )

    st.dataframe(filtered[show_cols], use_container_width=True)

    st.download_button(
        "⬇️ Download CSV",
        to_csv(filtered[show_cols]),
        "customers.csv",
        "text/csv"
    )


def tabelProducts_dan_export():
    total_products = df_products.shape[0]

    col1, _ = st.columns(2)
    with col1:
        st.metric("Total Produk", total_products)

    st.markdown("### 📦 Data Produk")
    show_cols = st.multiselect(
        "Pilih Kolom Produk",
        options=df_products.columns,
        default=df_products.columns
    )

    st.dataframe(df_products[show_cols], use_container_width=True)

    st.download_button(
        "⬇️ Download Produk CSV",
        to_csv(df_products[show_cols]),
        "products.csv",
        "text/csv"
    )


def tabelOrders_dan_export():
    total_orders = df_orders.shape[0]
    total_revenue = df_orders["total_amount"].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Order", total_orders)
    with col2:
        st.metric("Total Pendapatan", f"Rp {total_revenue:,.0f}")

    st.markdown("### 🧾 Data Orders")
    show_cols = st.multiselect(
        "Pilih Kolom Orders",
        options=df_orders.columns,
        default=df_orders.columns
    )

    st.dataframe(df_orders[show_cols], use_container_width=True)

    st.download_button(
        "⬇️ Download Orders CSV",
        to_csv(df_orders[show_cols]),
        "orders.csv",
        "text/csv"
    )


def tabelOrderDetails_dan_export():
    total_detail = df_order_details.shape[0]

    st.metric("Total Detail Transaksi", total_detail)
    st.markdown("### 🧩 Data Order Details")

    show_cols = st.multiselect(
        "Pilih Kolom Order Detail",
        options=df_order_details.columns,
        default=df_order_details.columns
    )

    st.dataframe(df_order_details[show_cols], use_container_width=True)

    st.download_button(
        "⬇️ Download Order Details CSV",
        to_csv(df_order_details[show_cols]),
        "order_details.csv",
        "text/csv"
    )


st.sidebar.success("Pilih Tabel:")

if st.sidebar.checkbox("Tampilkan Pelanggan", key="show_customers"):
    tabelCustomers_dan_export()

if st.sidebar.checkbox("Tampilkan Products", key="show_products"):
    tabelProducts_dan_export()

if st.sidebar.checkbox("Tampilkan Orders", key="show_orders"):
    tabelOrders_dan_export()

if st.sidebar.checkbox("Tampilkan Order Details", key="show_order_details"):
    tabelOrderDetails_dan_export()