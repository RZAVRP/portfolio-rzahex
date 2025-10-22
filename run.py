import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

# Ambil URL dari input pengguna
base_url = input("Masukkan URL target (tanpa parameter query): ").strip()

if not base_url.startswith(('http://', 'https://')):
    print("URL harus diawali dengan http:// atau https://")
    exit()

def scan_parameters(base_url, params):
    results = []
    for param, values in params.items():
        for value in values:
            encoded_param = urllib.parse.quote(param)
            encoded_value = urllib.parse.quote(value)
            full_url = f"{base_url}?{encoded_param}={encoded_value}"
            
            try:
                response = requests.get(full_url, timeout=10)
                status = response.status_code
                if status == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Ganti 'your_tag' dengan tag yang ingin kamu ekstrak, misal 'title', 'p', dll.
                    data_elements = soup.find_all('your_tag')  # <-- SESUAIKAN DI SINI
                    # Ambil teks dari elemen atau tampilkan strukturnya
                    data_text = ' | '.join([str(el) for el in data_elements])  # Bisa juga el.get_text()
                else:
                    data_text = ''
            except requests.RequestException as e:
                status = 'Error'
                data_text = str(e)

            results.append({
                'parameter': param,
                'value': value,
                'status_code': status,
                'data': data_text
            })
    return results

# Daftar parameter (bisa kamu ubah sesuai kebutuhan)
params = {
    'id': ['1', '2', '3'],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': ['25', '30', '35'],
    'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
    'cat': ['dog', 'cat', 'bird']
}

print("Memulai pemindaian...")
results = scan_parameters(base_url, params)

# Simpan ke CSV tanpa pandas
output_file = 'parameter_scan_results.csv'
with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['parameter', 'value', 'status_code', 'data']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"Hasil disimpan ke {output_file}")

# Opsional: tampilkan hasil di terminal
print("\nRingkasan hasil:")
for r in results:
    print(f"[{r['status_code']}] {r['parameter']}={r['value']}")