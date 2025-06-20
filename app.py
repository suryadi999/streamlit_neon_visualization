import os
import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode='require'
    )
    return conn

def show_table_data(conn, table_name):
    query = f"SELECT * FROM {table_name} LIMIT 100;"
    df = pd.read_sql_query(query, conn)
    st.subheader(f"Data dari tabel: {table_name}")
    st.dataframe(df)
    if len(df.columns) >= 3 and not df.empty:
        fig = px.bar(df, x=df.columns[1], y=df.columns[2])
        st.plotly_chart(fig)
    elif not df.empty:
        st.write("Data tabel terlalu sedikit kolom untuk visualisasi.")

def main():
    st.title("Visualisasi Data dari Neon PostgreSQL")

    tabel_list = ["orders", "promotions"]

    try:
        conn = get_connection()
        for tabel in tabel_list:
            show_table_data(conn, tabel)
        conn.close()
    except Exception as e:
        st.error(f"Error koneksi atau query: {e}")

if __name__ == "__main__":
    main()
