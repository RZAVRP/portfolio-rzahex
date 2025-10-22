import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd

# Ambil URL dari input pengguna
base_url = input("Masukkan URL target (tanpa parameter query): ").strip()

# Pastikan URL valid (minimal mengandung http:// atau https://)
if not base_url.startswith(('http://', 'https://')):
    print("URL harus diawali dengan http:// atau https://")
    exit()

# Function to extract parameters from a URL (opsional, tidak dipakai langsung di sini)
def extract_parameters(url):
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    return query_params

# Function to scan parameters
def scan_parameters(base_url, params):
    results = []
    for param, values in params.items():
        for value in values:
            # Encode parameter dan value agar aman untuk URL
            encoded_param = urllib.parse.quote(param)
            encoded_value = urllib.parse.quote(value)
            full_url = f"{base_url}?{encoded_param}={encoded_value}"
            
            try:
                response = requests.get(full_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Ganti 'your_tag' dengan tag yang ingin kamu ekstrak, misal 'title', 'p', dll.
                    data = soup.find_all('your_tag')  # <-- Ganti ini sesuai kebutuhan
                    results.append({
                        'parameter': param,
                        'value': value,
                        'status_code': response.status_code,
                        'data': str(data)  # Konversi ke string agar bisa disimpan di CSV
                    })
                else:
                    results.append({
                        'parameter': param,
                        'value': value,
                        'status_code': response.status_code,
                        'data': None
                    })
            except requests.RequestException as e:
                results.append({
                    'parameter': param,
                    'value': value,
                    'status_code': 'Error',
                    'data': str(e)
                })
    return results

# Parameter yang ingin discan (bisa juga diinput dinamis jika diperlukan)
params = {
    'id': ['1', '2', '3'],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': ['25', '30', '35'],
    'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
    'cat': ['dog', 'cat', 'bird']
}

# Jalankan pemindaian
print("Memulai pemindaian...")
results = scan_parameters(base_url, params)

# Konversi ke DataFrame
df = pd.DataFrame(results)
print(df)

# Simpan ke file CSV
output_file = 'parameter_scan_results.csv'
df.to_csv(output_file, index=False)
print(f"Hasil disimpan ke {output_file}")