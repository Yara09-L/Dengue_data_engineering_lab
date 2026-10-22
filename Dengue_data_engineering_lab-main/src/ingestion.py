import os
import requests

# URL oficial de Datos Abiertos de la Secretaría de Salud (Dengue)
DATA_URL = "https://www.gob.mx/salud/documentos/datos-abiertos-bases-historicas-de-enfermedades-transmitidas-por-vector"
RAW_FILE_PATH = "data/raw/dengue_abierto.csv"

def download_latest_dengue_data(url=DATA_URL, output_path=RAW_FILE_PATH):
    """
    Descarga o actualiza de forma automatizada el dataset de Dengue 
    directamente desde el portal oficial de datos abiertos.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"Descargando datos actualizados desde: {url}...")
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        print(f"✔ Archivo actualizado guardado exitosamente en: {output_path}")
    else:
        print(f"❌ Error al descargar datos. Código HTTP: {response.status_code}")

if __name__ == "__main__":
    download_latest_dengue_data()