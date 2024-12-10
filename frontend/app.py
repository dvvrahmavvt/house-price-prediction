import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Konfigurasi halaman
st.set_page_config(page_title="Prediksi Harga Rumah", layout="wide")

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    try:
        # Ganti dengan path dataset Anda
        data = pd.read_csv("results_cleaned.csv")
        return data
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

# Konfigurasi API
BACKEND_URL = "http://localhost:8081/api/predict"

# Memuat dataset
data = load_data()

#DISTRIBUSI HARGA
# Menghitung IQR
Q1 = data['price'].quantile(0.25)
Q3 = data['price'].quantile(0.75)
IQR = Q3 - Q1

# Menentukan batas atas dan bawah
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
#Membuat DataFrame Baru (1)
df= data[(data['price'] >= lower_bound) & (data['price'] <= upper_bound)]

#BUILDING AREA
#Membuat DataFrame Baru (2)
# Menghitung Q1 dan Q3 untuk building_area
Q1 = df['building_area (m2)'].quantile(0.25)
Q3 = df['building_area (m2)'].quantile(0.75)
IQR = Q3 - Q1

# Menentukan batas bawah dan batas atas
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Menghapus outlier
df_cleaned = df[(df['building_area (m2)'] >= lower_bound) & (df['building_area (m2)'] <= upper_bound)]

# CARPORT
#Membuat DataFrame Baru (3)
# Menghitung Q1 dan Q3 untuk carport_count
Q1 = df['carport_count'].quantile(0.25)
Q3 = df['carport_count'].quantile(0.75)
IQR = Q3 - Q1

# Menentukan batas bawah dan batas atas
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Menghapus outlier carport
data_cleaned = df[(df_cleaned['carport_count'] >= lower_bound) & (df['carport_count'] <= upper_bound)]

from sklearn.preprocessing import LabelEncoder

# Encode kolom location
le = LabelEncoder()
data_cleaned['location_encoded'] = le.fit_transform(data_cleaned['location'])
# Mengganti nama kolom yang memiliki spasi atau karakter lain
data_cleaned.rename(columns=lambda x: x.replace(" ", "_").replace(",", "").replace("(", "").replace(")", ""), inplace=True)

#MENAMPILKAN MODEL TERBAIK 
# Fitur yang akan digunakan untuk model
features = ['bedroom_count', 'bathroom_count', 'carport_count', 'land_area', 'building_area_m2', 'location_encoded']
X = data_cleaned[features]

# Target
y = data_cleaned['price']

# Standarisasi
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Membagi dataset menjadi training dan test set
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Inisialisasi dan melatih model Random Forest
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)

# Prediksi menggunakan model Random Forest
y_pred_rf = rf_model.predict(X_test)

# Evaluasi Model
mae_rf = mean_absolute_error(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

# Fungsi preprocessing
def preprocess_location(data):
    # Encode lokasi jika belum di-encode
    location_mapping = {loc: idx for idx, loc in enumerate(data['location'].unique())}
    return location_mapping

# Sidebar navigasi
def sidebar_navigation():
    st.sidebar.title("Menu Navigasi")
    menu = st.sidebar.radio("Pilih Menu", 
        ["Beranda", "Dataset", "Eksplorasi Data", "Visualisasi", "Model","Prediksi Harga"]
    )
    return menu

# Halaman Beranda
def home_page():
    st.title("Sistem Prediksi Harga Rumah")
    st.markdown("""
    ### Selamat Datang di Aplikasi Prediksi Harga Rumah
    
    Aplikasi ini menggunakan Machine Learning Random Forest untuk memprediksi harga rumah 
    berdasarkan berbagai fitur seperti:
    - Jumlah Kamar Tidur
    - Jumlah Kamar Mandi
    - Luas Lahan
    - Luas Bangunan
    - Lokasi
    """)

    # Tampilkan statistik ringkas
    if not data.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Data", len(data))
        with col2:
            st.metric("Harga Rata-rata", f"Rp {data['price'].mean():,.0f}")
        with col3:
            st.metric("Lokasi Unik", len(data['location'].unique()))

#Halaman Dtaaset
def dataset_page():
    st.title("Dataset")
    st.subheader("Tabel Dataset Rumah")
    st.dataframe(data)

# Halaman Eksplorasi Data
def eda_page():
    st.title("Eksplorasi Data")
    
    # Pilihan visualisasi
    viz_type = st.selectbox("Pilih Jenis Visualisasi", 
        ["Distribusi Harga","Histogram Semua Fitur", "Korelasi Fitur", "Boxplot Harga per Lokasi"]
    )
    
    if viz_type == "Distribusi Harga":
        fig = px.histogram(df, x='price', 
            title='Distribusi Harga Rumah')
        st.plotly_chart(fig)

    elif viz_type == "Histogram Semua Fitur":
        st.subheader("Histogram Semua Fitur")
        # Membuat histogram untuk semua fitur numerik
        num_cols = data.select_dtypes(include=np.number).columns  # Pilih kolom numerik
        fig, axes = plt.subplots(len(num_cols), 1, figsize=(10, 10))
        
        if len(num_cols) == 1:
            axes = [axes]  
        
        for i, col in enumerate(num_cols):
            axes[i].hist(data[col], bins=50, color='skyblue', edgecolor='black')
            axes[i].set_title(f'Histogram {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Frekuensi')
        
        plt.tight_layout() 
        st.pyplot(fig)    
    
    elif viz_type == "Korelasi Fitur":
        st.subheader("Heatmap Korelasi antar Fitur")
        
        # Mengambil kolom numerik untuk korelasi
        numeric_df = data_cleaned.select_dtypes(include=['float64', 'int64'])
        
        # Menghitung matriks korelasi antar fitur numerik
        correlation_matrix = numeric_df.corr()
        
        # Membuat heatmap korelasi antar fitur
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")  # annot=True untuk menampilkan angka korelasi
        plt.title("Korelasi antar Fitur")
        
        # Menampilkan heatmap dengan Streamlit
        st.pyplot(plt)
    
    elif viz_type == "Boxplot Harga per Lokasi":
        fig = px.box(data, x='location', y='price', 
            title='Distribusi Harga Rumah per Lokasi')
        st.plotly_chart(fig)
        

# Halaman Visualisasi Data
def visualisasi_page():
    st.title("Visualisasi Distribusi Setiap Fitur terhadap Harga (Price)")

    # Set tema dan gaya visualisasi
    sns.set_theme(style="whitegrid")  # Menggunakan tema whitegrid untuk tampilan bersih dan modern

    # 1. Boxplot - Jumlah Kamar Tidur terhadap Harga
    st.subheader("Distribusi Harga Rumah Berdasarkan Jumlah Kamar Tidur")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=data_cleaned, x='bedroom_count', y='price', ax=ax1, palette="coolwarm")
    ax1.set_title('Distribusi Harga Rumah Berdasarkan Jumlah Kamar Tidur', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Jumlah Kamar Tidur', fontsize=12)
    ax1.set_ylabel('Harga Rumah', fontsize=12)
    ax1.grid(color='lightgray', linestyle='--', linewidth=0.5)
    st.pyplot(fig1)

    # 2. Boxplot - Jumlah Kamar Mandi terhadap Harga
    st.subheader("Distribusi Harga Rumah Berdasarkan Jumlah Kamar Mandi")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=data_cleaned, x='bathroom_count', y='price', ax=ax2, palette="viridis")
    ax2.set_title('Distribusi Harga Rumah Berdasarkan Jumlah Kamar Mandi', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Jumlah Kamar Mandi', fontsize=12)
    ax2.set_ylabel('Harga Rumah', fontsize=12)
    ax2.grid(color='lightgray', linestyle='--', linewidth=0.5)
    st.pyplot(fig2)

    # 3. Scatter Plot - Luas Lahan terhadap Harga
    st.subheader("Distribusi Harga Rumah Berdasarkan Luas Lahan")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=data_cleaned, x='land_area', y='price', ax=ax3, color='dodgerblue', alpha=0.7, s=70)
    ax3.set_title('Distribusi Harga Rumah Berdasarkan Luas Lahan', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Luas Lahan (m²)', fontsize=12)
    ax3.set_ylabel('Harga Rumah', fontsize=12)
    ax3.grid(color='lightgray', linestyle='--', linewidth=0.5)
    st.pyplot(fig3)

    # 4. Scatterplot - Luas Bangunan terhadap Harga
    st.subheader("Distribusi Harga Rumah Berdasarkan Luas Bangunan")
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=data_cleaned, x='building_area_m2', y='price', ax=ax4, color='seagreen', alpha=0.7, s=70)
    ax4.set_title('Distribusi Harga Rumah Berdasarkan Luas Bangunan', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Luas Bangunan (m²)', fontsize=12)
    ax4.set_ylabel('Harga Rumah', fontsize=12)
    ax4.grid(color='lightgray', linestyle='--', linewidth=0.5)
    st.pyplot(fig4)

    # 5. Scatterplot - Jumlah Carport terhadap Harga
    st.subheader("Distribusi Harga Rumah Berdasarkan Carport")
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
    data=data_cleaned, 
    x='building_area_m2', 
    y='price', 
    hue='carport_count', 
    palette='coolwarm', 
    alpha=0.7, 
    s=70, 
    ax=ax5
    )
    ax5.set_title('Distribusi Harga Rumah Berdasarkan Carport', fontsize=14, fontweight='bold')
    ax5.set_xlabel('Luas Bangunan (m²)', fontsize=12)
    ax5.set_ylabel('Harga Rumah', fontsize=12)
    ax5.legend(title="Jumlah Carport", fontsize=10, title_fontsize=11)  
    ax5.grid(color='lightgray', linestyle='--', linewidth=0.5)
    st.pyplot(fig5)

    # 6. Boxplot - Lokasi terhadap Harga
    st.subheader("Distribusi Harga Rumah Berdasarkan Lokasi")
    fig6, ax6 = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=data_cleaned, x='location', y='price', ax=ax6, palette="cubehelix")
    ax6.set_title('Distribusi Harga Rumah Berdasarkan Lokasi', fontsize=14, fontweight='bold')
    ax6.set_xlabel('Lokasi', fontsize=12)
    ax6.set_ylabel('Harga Rumah', fontsize=12)
    ax6.set_xticklabels(ax6.get_xticklabels(), rotation=90, fontsize=10)  # Memutar label lokasi agar lebih rapi
    ax6.grid(color='lightgray', linestyle='--', linewidth=0.5)
    st.pyplot(fig6)


#Halaman Model
def model_page():
    st.title("Model Pembelajaran Mesin Terbaik: Random Forest")
    
    # Menampilkan evaluasi model
    st.subheader("Evaluasi Model Random Forest")
    st.write(f"**MAE** (Mean Absolute Error): {mae_rf:.2f}")
    st.write(f"**MSE** (Mean Squared Error): {mse_rf:.2f}")
    st.write(f"**R²** (Koefisien Determinasi): {r2_rf:.2f}")
    
    # Visualisasi: Actual vs Predicted Prices (Random Forest)
    st.subheader("Visualisasi Perbandingan Harga Aktual dan Prediksi (Random Forest)")
    
    # Menghitung error prediksi
    error = y_test - y_pred_rf
    
    # Membuat scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(y_test, y_pred_rf, c=error, cmap='coolwarm', alpha=0.7)
    ax.set_xlabel("Harga Aktual")
    ax.set_ylabel("Harga Prediksi")
    ax.set_title("Perbandingan Harga Aktual dan Prediksi (Random Forest)")

    # Menambahkan garis y=x untuk referensi
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)

    # Menambahkan colorbar untuk error
    cbar = plt.colorbar(scatter)
    cbar.set_label('Prediction Error (Aktual - Prediksi)')
    
    # Menampilkan plot di Streamlit
    st.pyplot(fig)

# Halaman Prediksi
def prediction_page():
    st.title("Prediksi Harga Rumah")
    
    # Mapping lokasi
    location_mapping = preprocess_location(data)
    
    # Input fitur
    col1, col2 = st.columns(2)
    
    with col1:
        bedroom_count = st.number_input("Jumlah Kamar Tidur", min_value=1, max_value=10, value=3)
        bathroom_count = st.number_input("Jumlah Kamar Mandi", min_value=1, max_value=10, value=2)
        carport_count = st.number_input("Jumlah Carport", min_value=0, max_value=5, value=1)
    
    with col2:
        land_area = st.number_input("Luas Lahan (m²)", min_value=10.0, max_value=10000.0, value=100.0)
        building_area = st.number_input("Luas Bangunan (m²)", min_value=10.0, max_value=5000.0, value=80.0)
        location_name = st.selectbox("Lokasi", options=list(location_mapping.keys()))
    
    location_encoded = location_mapping[location_name]
    
    if st.button("Prediksi Harga"):
        payload = {
            "bedroomCount": bedroom_count,
            "bathroomCount": bathroom_count,
            "carportCount": carport_count,
            "landArea": land_area,
            "buildingArea": building_area,
            "locationEncoded": location_encoded
        }
        
        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if "predictedPrice" in result:
                prediction = result["predictedPrice"]
                st.success(f"### Prediksi Harga Rumah: Rp {prediction:,.2f}")
                
                # Bandingkan dengan data historis
                similar_houses = data[
                    (data['bedroom'] == bedroom_count) & 
                    (data['bathroom'] == bathroom_count) & 
                    (data['location'] == location_name)
                ]
                
                if not similar_houses.empty:
                    st.info(f"Harga Rumah Serupa: Rp {similar_houses['price'].mean():,.2f}")
            else:
                st.error("Format respons tidak valid")
        
        except requests.exceptions.RequestException as req_err:
            st.error(f"Kesalahan Jaringan: {req_err}")
        except Exception as e:
            st.error(f"Kesalahan tidak terduga: {e}")

# Halaman Utama
def main():
    menu = sidebar_navigation()
    
    if menu == "Beranda":
        home_page()
    elif menu == "Dataset":
        dataset_page()    
    elif menu == "Eksplorasi Data":
        eda_page()
    elif menu == "Visualisasi":
        visualisasi_page()    
    elif menu == "Model":  
        model_page()  
    elif menu == "Prediksi Harga":
        prediction_page()

if __name__ == "__main__":
    main()
