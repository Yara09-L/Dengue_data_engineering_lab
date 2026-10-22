# Dengue_data_engineering_lab

## Datos reales y procesamiento con poco almacenamiento

El ETL lee por bloques los ZIP oficiales de dengue de 2020–2026, filtra casos
confirmados y agrega por municipio y semana epidemiológica. Los ZIP/CSV se
mantienen temporalmente en memoria; no se escriben en `data/raw`.

```powershell
python -m src.process_dengue
```

El resultado actual reúne 2020–2026 y se guarda como
`data/processed/dengue_confirmed_weekly_2020_2026.parquet`. La fuente oficial
indica que estas bases históricas se publican desde 2020; por eso, esta fuente
no respalda el periodo 2015–2019 del documento de la actividad.

Para ejecutarlo en Colab y guardar solo el resultado en Drive:

```python
from google.colab import drive
import os

drive.mount("/content/drive")
os.environ["DENGUE_OUTPUT_PATH"] = (
    "/content/drive/MyDrive/dengue_confirmed_weekly_2020_2026.parquet"
)
```

Desde una celda de Colab, ejecuta `!python -m src.process_dengue` desde la
carpeta que contiene `src/`. El código descarga y procesa los ZIP en la sesión
temporal de Colab y escribe únicamente el Parquet final en Drive.

La revisión de calidad encontró 8,798 casos confirmados con fecha de síntomas
posterior a `FECHA_ACTUALIZACION`; se conservan, pero deben revisarse antes de
interpretar resultados. Consulta `metadata/provenance_log.md` para las fuentes,
los cortes utilizados y otras limitaciones.

La salida contiene únicamente datos epidemiológicos reales; ERA5-Land todavía
no está integrado, así que no es el Parquet final dengue-clima.

### Preparación para ERA5-Land

El acceso por API a Copernicus CDS requiere una cuenta y aceptar las condiciones
del dataset. Sigue la [guía oficial de configuración de la API](https://cds.climate.copernicus.eu/how-to-api);
la configuración actual del cliente usa `ECMWF_DATASTORES_URL` y
`ECMWF_DATASTORES_KEY` o el archivo `~/.ecmwfdatastoresrc`, fuera del repositorio.
No guardes ni compartas la clave en GitHub, notebooks o mensajes. La descarga e
integración de clima se implementarán y validarán después de que el acceso de
Copernicus esté configurado en Colab.

Fuente de dengue: [Bases históricas de dengue, Secretaría de Salud](https://www.gob.mx/salud/documentos/datos-abiertos-bases-historicas-de-enfermedades-transmitidas-por-vector).
