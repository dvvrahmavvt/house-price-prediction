# -*- coding: utf-8 -*-
"""model random forest.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-yPrNec-2LSRdEKCuYXzB7WFjmUD9F02

1. Import Library
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from google.colab import drive

"""2.Load Dataset"""

data = pd.read_csv( "/content/drive/MyDrive/Project TIA House Prediksi /results_cleaned.csv")
data.head(5)

"""3. Data Understanding

"""

data.info()

jumlah_baris = len(data)
print (f'Jumlah Data: {jumlah_baris}')

"""4. Eksplorasi Data (EDA)"""

print(data.describe())

print("\nJumlah data yang hilang:")
print(data.isnull().sum ())

# Analisis kolom kategorikal
print(data['location'].value_counts())

"""5. Visualization & Pembersihan Dataset

5.1 Menghitung rata-rata harga rumah berdasarkan lokasi
"""

avg_price_by_location = data.groupby('location')['price'].mean().reset_index()
avg_price_by_location = avg_price_by_location.sort_values(by='price', ascending=False)
print(avg_price_by_location)

#visualisasi
plt.figure(figsize=(12, 6))
sns.countplot(y='location', data=data, order=data['location'].value_counts().index)
plt.title('Jumlah Rumah berdasarkan Lokasi')
plt.xlabel('Jumlah Rumah')
plt.ylabel('Lokasi')
plt.show()

"""#Lokasi Bojongloa Kidul, Bandung memiliki jumlah perumahan terbanyak dengan kisaran harga 4 M

5.2 Analisis Distribusi Harga Rumah
"""

# Analisis harga
print(data['price'].value_counts())
# Visualisasi distribusi harga rumah
plt.figure(figsize=(8, 5))
sns.histplot(data['price'], bins=30, kde=True)
plt.title('Distribusi Harga Rumah')
plt.xlabel('Price')
plt.ylabel('Frekuensi')
plt.show()

# Menghitung IQR
Q1 = data['price'].quantile(0.25)
Q3 = data['price'].quantile(0.75)
IQR = Q3 - Q1

# Menentukan batas atas dan bawah
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Mengidentifikasi outlier
outliers = data[(data['price'] < lower_bound) | (data['price'] > upper_bound)]
print("Outliers:")
print(outliers)

plt.figure(figsize=(8, 5))
sns.histplot(data['price'], bins=30, kde=True)
plt.axvline(x=lower_bound, color='red', linestyle='--', label='Lower Bound')
plt.axvline(x=upper_bound, color='green', linestyle='--', label='Upper Bound')
plt.title('Distribusi Harga Rumah')
plt.xlabel('Price')
plt.ylabel('Frekuensi')
plt.legend()
plt.show()

# Menghitung statistik deskriptif
price_stats = data['price'].describe()
print(price_stats)
plt.figure(figsize=(8, 5))
sns.boxplot(x=data['price'])
plt.title('Boxplot Harga Rumah')
plt.xlabel('Price')
plt.show()

"""Outlier dapat mempengaruhi estimasi parameter model, menyebabkan model menjadi bias dan tidak akurat.
Outlier dapat menyebabkan distribusi target (misalnya, harga rumah) menjadi tidak normal, yang dapat mempengaruhi asumsi dasar dari banyak algoritma pembelajaran mesin
"""

# Menghapus outlier
#Membuat DataFrame Baru (clenaed)
df= data[(data['price'] >= lower_bound) & (data['price'] <= upper_bound)]

# Visualisasi distribusi harga sebelum penghapusan outlier
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.histplot(data['price'], bins=30, kde=True)
plt.title('Distribusi Harga Rumah (Sebelum Penghapusan Outlier)')
plt.xlabel('Price')
plt.ylabel('Frekuensi')

# Visualisasi distribusi harga setelah penghapusan outlier
plt.subplot(1, 2, 2)
sns.histplot(df['price'], bins=30, kde=True)
plt.title('Distribusi Harga Rumah (Setelah Penghapusan Outlier)')
plt.xlabel('Price')
plt.ylabel('Frekuensi')

plt.tight_layout()
plt.show()

"""5.3 Hubungan Jumlah kamar tidur dengan harga"""

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='bedroom_count', y='price')
plt.title('Distribusi Harga Rumah Berdasarkan Jumlah Kamar Tidur')
plt.xlabel('Jumlah Kamar Tidur')
plt.ylabel('Harga Rumah')
plt.grid(True)
plt.show()

print(df.columns)

"""5.4. Hubungan Luas Tanah dengan Harga rumah"""

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='land_area', y='price', alpha=0.6)
plt.title('Hubungan antara Luas Tanah dan Harga Rumah')
plt.xlabel('Luas Tanah (m²)')
plt.ylabel('Harga Rumah')
plt.grid(True)
plt.show()

"""5.5 Histogram"""

df.hist(bins=50, figsize=(10, 10))

"""5.6 Melihat Persebaran Data pada feature luas bangunan"""

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='building_area (m2)', y='price')
plt.title('Distribusi Harga Rumah Berdasarkan luas bangunan')
plt.xlabel('Luas bangunan')
plt.ylabel('Harga Rumah')
plt.grid(True)
plt.show()

print(df['building_area (m2)'].value_counts())

# Menghitung Q1 dan Q3 untuk building_area
Q1 = df['building_area (m2)'].quantile(0.25)
Q3 = df['building_area (m2)'].quantile(0.75)
IQR = Q3 - Q1

# Menentukan batas bawah dan batas atas
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Menghapus outlier
#Membuat DataFrame baru
df_cleaned = df[(df['building_area (m2)'] >= lower_bound) & (df['building_area (m2)'] <= upper_bound)]

# Visualisasi setelah menghapus outlier
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cleaned, x='building_area (m2)', y='price')
plt.title('Distribusi Harga Rumah Berdasarkan Luas Bangunan')
plt.xlabel('Luas Bangunan (m²)')
plt.ylabel('Harga Rumah')
plt.grid(True)
plt.show()

#Histogram ke 2
df_cleaned.hist(bins=50, figsize=(10, 10))

"""5.7 Melihat Hubungan Carport terhadap harga"""

print(df['carport_count'].value_counts())
#visualisasi
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='carport_count', y='price')
plt.title('Distribusi Harga Rumah Berdasarkan Carport')
plt.xlabel('carport area')
plt.ylabel('Harga Rumah')
plt.grid(True)
plt.show()

# Menghitung Q1 dan Q3 untuk carport_count
Q1 = df['carport_count'].quantile(0.25)
Q3 = df['carport_count'].quantile(0.75)
IQR = Q3 - Q1

# Menentukan batas bawah dan batas atas
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Menghapus outlier carport
data_cleaned = df[(df_cleaned['carport_count'] >= lower_bound) & (df['carport_count'] <= upper_bound)]

# Visualisasi setelah menghapus outlier
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data_cleaned, x='building_area (m2)', y='price', hue='carport_count')
plt.title('Distribusi Harga Rumah Berdasarkan Carport')
plt.xlabel('Luas Bangunan (m²)')
plt.ylabel('Harga Rumah')
plt.grid(True)
plt.show()

#Histogram final
data_cleaned.hist(bins=50, figsize=(10, 10))

#Perbandingan Data sebelum dan sesudah pembersihan
jumlah_baris_sebelum_pembersihan = len(data)
print (f'Jumlah Data: {jumlah_baris_sebelum_pembersihan}')

jumlah_baris_setelah_pembersihan = len(data_cleaned)
print (f'Jumlah Data: {jumlah_baris_setelah_pembersihan}')

"""5.7 Korelasi"""

numeric_df = data_cleaned.select_dtypes(include=['float64', 'int64'])

# Membuat heatmap korelasi antar fitur numerik
plt.figure(figsize=(10, 8))
sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title('Korelasi antar Fitur')
plt.show()

"""7. Pre Processing Data"""

# Memeriksa nilai unik sebelum encoding
print("Unique locations before encoding:", data_cleaned['location'].unique())

from sklearn.preprocessing import LabelEncoder

# Encode kolom location
le = LabelEncoder()
data_cleaned['location_encoded'] = le.fit_transform(data_cleaned['location'])
data_cleaned

# Melihat mapping dari kategori ke nilai yang di-encode
mapping = dict(zip(le.classes_, range(len(le.classes_))))
print(mapping)

"""Andir, Bandung: 0
Antapani, Bandung': 1
Arcamanik, Bandung': 2
Astanaanyar, Bandung': 3
Babakanciparay, Bandung': 4
Bandung Kidul, Bandung: 5
Bandung Kulon, Bandung': 6
Bandung Wetan, Bandung': 7
Batununggal, Bandung': 8
Bojongloa Kidul, Bandung': 9
Buah Batu, Bandung': 10
Cibeunying Kidul, Bandung': 11
Cibiru, Bandung': 12
Cicendo, Bandung': 13
Cidadap, Bandung': 14
Coblong, Bandung': 15
Gede Bage, Bandung': 16
Kiaracondong, Bandung': 17
Lengkong, Bandung': 18
Mandalajati, Bandung': 19
Panyileukan, Bandung': 20
Rancasari, Bandung': 21
Regol, Bandung': 22
Sukajadi, Bandung': 23
Sukasari, Bandung': 24
Sumurbandung, Bandung': 25
Ujungberung, Bandung': 26
"""

# Mengganti nama kolom yang memiliki spasi atau karakter lain
data_cleaned.rename(columns=lambda x: x.replace(" ", "_").replace(",", "").replace("(", "").replace(")", ""), inplace=True)
# Memeriksa kolom yang ada dalam DataFrame setelah mengganti nama
print("Kolom yang ada dalam DataFrame setelah mengganti nama:", data_cleaned.columns)

print(data_cleaned.dtypes)

#KORELASI
correlation_matrix = data_cleaned.select_dtypes(include=['float64', 'int64']).corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f")
plt.show()

"""Hal ini menunjukan luas lahan & luas bangunan memiliki pengaruh yang terbesar terhadap harga properti, kemudian ada jumlah kamar mandi

7.1 Normalisasi
"""

from sklearn.preprocessing import StandardScaler

# memilih fitur untuk model
features = ['bedroom_count', 'bathroom_count', 'carport_count', 'land_area', 'building_area_m2', 'location_encoded']
X = data_cleaned[features]

# Target
y = data_cleaned['price']

# Standarisasi
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X

y

"""8. Modeling"""

#8.1 Linier Regression

#Split Dataset ( membagi data menjadi data latih dan uji)
from sklearn.model_selection import train_test_split

# Membagi dataset
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

#Melatih model
from sklearn.linear_model import LinearRegression
# Inisialisasi model
lr_model = LinearRegression()

# Latih model
lr_model.fit(X_train, y_train)

# Prediksi LinierRegression
y_pred_lr = lr_model.predict(X_test)

"""8.2 Random Forest"""

# Inisialisasi model
rf_model = RandomForestRegressor(random_state=42)

# Latih model Random forest
rf_model.fit(X_train, y_train)

# Prediksi
y_pred_rf = rf_model.predict(X_test)

"""9. Evaluasi Model"""

# Evaluasi Linear Regression
mae_lr = mean_absolute_error(y_test, y_pred_lr)
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)
# Evaluasi Random Forest
mae_rf = mean_absolute_error(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Random Forest - MAE: {mae_rf}, MSE: {mse_rf}, R²: {r2_rf}")

print(f"Linear Regression - MAE: {mae_lr}, MSE: {mse_lr}, R²: {r2_lr}")

"""#Kesimpulan
Model Random Forest memiliki Mean Absolute Error (MAE) dan Mean Squared Error (MSE) lebih rendah dan nilai R-kuadrat(R2) yang lebih tinggi bila di bandingkan dnegan linier regression.

Dalam hal ini, model Random Forest menjelaskan sekitar 81,9% dari varians, sedangkan model Regresi Linier hanya menjelaskan 58,1%.

Visualisasai Model Random Forest Predict
"""

# Menghitung selisih antara nilai aktual dan prediksi
error = y_test - y_pred_rf
# Membuat scatter plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(y_test, y_pred_rf, c=error, cmap='coolwarm', alpha=0.7)

# Menambahkan colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('Prediction Error (Actual - Predicted)')

# Menambahkan label dan judul
plt.xlabel("Actual Prices")
plt.ylabel("Predicted Prices")
plt.title("Actual vs Predicted Prices (Random Forest)")

# Menambahkan garis y=x untuk referensi
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)

plt.show()

"""10. Menyimpan Model Terbaik"""

import pickle

# Menyimpan model ke file .pkl
with open('rf_model.pkl', 'wb') as file:
    pickle.dump(rf_model, file)

print("Model telah disimpan ke rf_model.pkl")

# Memuat model dari file .pkl
with open('rf_model.pkl', 'rb') as file:
    model_random_forest_loaded = pickle.load(file)

#prediction
predictions = model_random_forest_loaded.predict(X_test)

from google.colab import files

# Memindahkan file model ke Google Colab file system
!cp rf_model.pkl /content/rf_model.pkl

# Mengunduh model ke komputer lokal
files.download('/content/rf_model.pkl')