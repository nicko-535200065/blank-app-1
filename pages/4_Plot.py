import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import numpy as np
from matplotlib.ticker import FuncFormatter
 
# Konfigurasi halaman aplikasi Streamlit
st.set_page_config(
    page_title="Streamlit",
#    page_icon="",
)

# Fungsi untuk mengonversi tanggal dengan nama bulan dalam bahasa Indonesia
def convert_indonesian_date_column(df, date_column):
    # Ganti nama bulan Indonesia dengan bahasa Inggris
    bulan_mapping = {
        'Januari': 'January', 'Februari': 'February', 'Maret': 'March', 
        'April': 'April', 'Mei': 'May', 'Juni': 'June', 
        'Juli': 'July', 'Agustus': 'August', 'September': 'September', 
        'Oktober': 'October', 'November': 'November', 'Desember': 'December'
    }

    for indo_bulan, eng_bulan in bulan_mapping.items():
        df[date_column] = df[date_column].str.replace(indo_bulan, eng_bulan, regex=False)
    
    # Konversi kolom menjadi datetime dengan dayfirst=True
    df[date_column] = pd.to_datetime(df[date_column], dayfirst=True, errors='coerce')
    return df

# Load data and clustering function
@st.cache_data
def load_data():
    data_path = "Data.csv"
    df = pd.read_csv(data_path)


    # Konversi kolom tanggal yang berformat Indonesia
    df = convert_indonesian_date_column(df, 'Tanggal')
    return df


# Function to run KMeans
def run_kmeans(df, n_clusters=3):
    produk_kategori = ['AGV', 'NOL', 'INK', 'KYT', 'MDS', 'BMC', 'HIU', 'NHK', 'GM', 
                       'ASCA', 'ZEUS', 'CAR', 'HBC', 'JPX', 'NJS', 'DYR', 'G2', 'SarungMotor', 
                       'SarungTangan', 'Googles', 'Masker', 'Kaca', 'Aksesoris', 'Lainnya']
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(df[produk_kategori])
    df['Cluster'] = cluster_labels
    return df, cluster_labels, kmeans

# Load and run clustering
df = load_data()
n_clusters = st.slider("Jumlah cluster:", 2, 10, 3)
clustered_df, cluster_labels, kmeans = run_kmeans(df, n_clusters)

# Calculate total sales per product per cluster
st.subheader("Total Penjualan per Produk di Masing-masing Cluster")
produk_kategori = ['AGV', 'NOL', 'INK', 'KYT', 'MDS', 'BMC', 'HIU', 'NHK', 'GM', 
                   'ASCA', 'ZEUS', 'CAR', 'HBC', 'JPX', 'NJS', 'DYR', 'G2', 'SarungMotor', 
                   'SarungTangan', 'Googles', 'Masker', 'Kaca', 'Aksesoris', 'Lainnya']
cluster_sales = clustered_df.groupby('Cluster')[produk_kategori].sum()

# Konversi kolom 'Tanggal' ke tipe datetime
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df['Bulan'] = df['Tanggal'].dt.to_period("M")

# Menghitung total pendapatan bulanan
monthly_revenue = df.groupby('Bulan')['Pendapatan'].sum()
#monthly_revenue

# Plot total pendapatan bulanan
st.subheader("Pendapatan Bulanan")
fig, ax = plt.subplots(figsize=(10, 6))
monthly_revenue.plot(ax=ax, marker='o', color='blue')
ax.set_title("Total Pendapatan Bulanan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Pendapatan")

# Mengatur format sumbu y agar menampilkan nilai asli tanpa disingkat
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

plt.xticks(rotation=45)
st.pyplot(fig)

# Plot total sales per cluster per product
fig, ax = plt.subplots(figsize=(10, 6))
cluster_sales.plot(kind='bar', stacked=True, ax=ax, color=plt.cm.tab20.colors)
ax.set_title("Total Penjualan per Produk di Setiap Cluster")
ax.set_xlabel("Cluster")
ax.set_ylabel("Total Penjualan")
st.pyplot(fig)

# Calculate and plot average sales per cluster
st.subheader("Rata-rata Penjualan di Setiap Cluster")
cluster_avg_sales = cluster_sales.mean(axis=1)
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(cluster_avg_sales.index, cluster_avg_sales.values, color='coral')
ax.set_title("Rata-rata Penjualan per Cluster")
ax.set_xlabel("Cluster")
ax.set_ylabel("Rata-rata Penjualan")
st.pyplot(fig)

# Plot sales per product in each cluster
st.subheader("Penjualan per Produk di Setiap Cluster")
for produk in produk_kategori:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(cluster_sales.index, cluster_sales[produk], color='skyblue')
    ax.set_title(f"Penjualan Produk '{produk}' di Setiap Cluster")
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Total Penjualan")
    st.pyplot(fig)
    
# Plot silhouette scores for each cluster
st.subheader("Silhouette Score untuk Masing-masing Cluster")
silhouette_vals = silhouette_samples(df[produk_kategori], cluster_labels)
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(range(len(silhouette_vals)), silhouette_vals, color='teal')
ax.set_title("Silhouette Score per Cluster")
ax.set_xlabel("Data Point Index")
ax.set_ylabel("Silhouette Score")
st.pyplot(fig)

# Konversi kolom 'Tanggal' ke tipe datetime
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df['Bulan'] = df['Tanggal'].dt.to_period("M")

# Menghitung total penjualan bulanan untuk setiap cluster
monthly_sales = df.groupby(['Bulan', 'Cluster'])[produk_kategori].sum().sum(axis=1).unstack()

# Plot total penjualan bulanan per cluster
fig, ax = plt.subplots(figsize=(10, 6))
monthly_sales.plot(ax=ax, marker='o')
ax.set_title("Total Penjualan Bulanan per Cluster")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penjualan")
plt.xticks(rotation=45)
st.pyplot(fig)

# Pastikan kolom 'Tanggal' sudah dalam format datetime
#df['Tanggal'] = pd.to_datetime(df['Tanggal'])
#df['Bulan'] = df['Tanggal'].dt.to_period("M")

# Tentukan rentang bulan penuh dari data yang tersedia
#all_months = pd.period_range(df['Bulan'].min(), df['Bulan'].max(), freq='M')

# Hitung total penjualan bulanan untuk setiap cluster dan isi dengan 0 untuk bulan yang kosong
#monthly_sales = df.groupby(['Bulan', 'Cluster'])[produk_kategori].sum().sum(axis=1).unstack().reindex(all_months, fill_value=0)

# Plot total penjualan bulanan per cluster
#fig, ax = plt.subplots(figsize=(10, 6))
#monthly_sales.plot(ax=ax, marker='o')
#ax.set_title("Total Penjualan Bulanan per Cluster")
#ax.set_xlabel("Bulan")
#ax.set_ylabel("Total Penjualan")
#plt.xticks(rotation=45)
#st.pyplot(fig)

# Plot monthly total sales per cluster
#st.subheader("Total Penjualan Setiap Bulan untuk Setiap Cluster")
#df['Tanggal'] = pd.to_datetime(df['Tanggal'])
#df['Bulan'] = df['Tanggal'].dt.to_period("M")
#monthly_sales = df.groupby(['Cluster', 'Bulan'])[produk_kategori].sum().sum(axis=1).unstack()
#fig, ax = plt.subplots(figsize=(10, 6))
#monthly_sales.plot(ax=ax, marker='o')
#ax.set_title("Total Penjualan Bulanan per Cluster")
#ax.set_xlabel("Bulan")
#ax.set_ylabel("Total Penjualan")
#st.pyplot(fig)

