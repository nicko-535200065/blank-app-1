import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score


# Konfigurasi halaman aplikasi Streamlit
st.set_page_config(
    page_title="Streamlit",
#    page_icon="",
)

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    data_path = "Data.csv"  # Sesuaikan path dengan lokasi file CSV Anda
    df = pd.read_csv(data_path)
    return df




# Fungsi untuk menjalankan K-Means Clustering dan menghitung Silhouette Score tiap titik
def run_kmeans(df, n_clusters=3):
    # Memilih fitur untuk clustering (pastikan kolom ini ada dalam Data.csv Anda)
    features = df[['AGV', 'NOL', 'INK', 'KYT', 'MDS', 'BMC', 'HIU', 'NHK', 'GM', 
                   'ASCA', 'ZEUS', 'CAR', 'HBC', 'JPX', 'NJS', 'DYR', 'G2', 'SarungMotor', 
                   'SarungTangan', 'Googles', 'Masker', 'Kaca', 'Aksesoris', 'Lainnya']]
    
    # Menjalankan K-Means Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(features)
    
    # Menghitung jarak titik ke centroid
    distances = np.min(kmeans.transform(features), axis=1)
    
    # Menghitung Silhouette Score untuk tiap titik
    silhouette_vals = silhouette_samples(features, cluster_labels)
    
    # Menambahkan hasil ke DataFrame asli
    df['Cluster'] = cluster_labels
    df['Distance to Centroid'] = distances
    df['Silhouette Score'] = silhouette_vals
    
    # Menghitung Silhouette Score rata-rata untuk semua titik
    silhouette_avg = silhouette_score(features, cluster_labels)
    
    return df, silhouette_avg

# Memuat data
df = load_data()

# Menjalankan K-Means Clustering
st.header("K-Means Clustering dengan Silhouette Score")
n_clusters = st.slider("Pilih jumlah cluster:", 2, 10, 3)
clustered_df, silhouette_avg = run_kmeans(df, n_clusters)

# Menampilkan Silhouette Score rata-rata
st.write(f"### Silhouette Score rata-rata untuk {n_clusters} Cluster: {silhouette_avg:.3f}")

# Menampilkan data dengan cluster, jarak ke centroid, dan Silhouette Score per titik
st.subheader("Data dengan Cluster, Jarak ke Centroid, dan Silhouette Score")
st.write(clustered_df[['Cluster', 'Distance to Centroid', 'Silhouette Score', 'AGV', 'NOL', 'INK', 'KYT', 'MDS', 
                       'BMC', 'HIU', 'NHK', 'GM', 'ASCA', 'ZEUS', 'CAR', 'HBC', 'JPX', 
                       'NJS', 'DYR', 'G2', 'SarungMotor', 'SarungTangan', 
                       'Googles', 'Masker', 'Kaca', 'Aksesoris', 'Lainnya']])

# Menampilkan tabel per cluster
st.subheader("Hasil Clustering per Cluster")
for cluster_num in range(n_clusters):
    st.write(f"### Cluster {cluster_num}")
    cluster_data = clustered_df[clustered_df['Cluster'] == cluster_num]
    st.write(cluster_data[['Distance to Centroid', 'Silhouette Score', 'AGV', 'NOL', 'INK', 'KYT', 'MDS', 
                           'BMC', 'HIU', 'NHK', 'GM', 'ASCA', 'ZEUS', 'CAR', 'HBC', 'JPX', 
                           'NJS', 'DYR', 'G2', 'SarungMotor', 'SarungTangan', 
                           'Googles', 'Masker', 'Kaca', 'Aksesoris', 'Lainnya']])
