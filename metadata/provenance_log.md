# Registro de procedencia

## Casos de dengue

- Fuente: Dirección General de Epidemiología, Secretaría de Salud, [bases
  históricas de enfermedades transmitidas por vector](https://www.gob.mx/salud/documentos/datos-abiertos-bases-historicas-de-enfermedades-transmitidas-por-vector).
- La fuente indica que publica estas bases históricas desde el 3 de diciembre
  de 2020. No se localizaron cortes 2015–2019 en este portal.
- El proceso consulta los siguientes cortes oficiales, uno por año:

| Año | Publicación seleccionada | URL del ZIP |
|---|---:|---|
| 2020 | 31-12-2020 | [datos_abiertos_dengue_311220.zip](https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/etv/historicos/2020/datos_abiertos_dengue_311220.zip) |
| 2021 | 30-12-2021 | [datos_abiertos_dengue_301221.zip](https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/etv/historicos/2021/datos_abiertos_dengue_301221.zip) |
| 2022 | 29-12-2022 | [datos_abiertos_dengue_291222.zip](https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/etv/historicos/2022/datos_abiertos_dengue_291222.zip) |
| 2023 | 27-12-2023 | [datos_abiertos_dengue_271223.zip](https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/etv/historicos/2023/datos_abiertos_dengue_271223.zip) |
| 2024 | 19-12-2024 | [datos_abiertos_dengue_191224.zip](https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/etv/historicos/2024/datos_abiertos_dengue_191224.zip) |
| 2025 | 11-12-2025 | [datos_abiertos_dengue_111225.zip](https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/etv/historicos/2025/datos_abiertos_dengue_111225.zip) |
| 2026 | 15-10-2026 | [datos_abiertos_dengue_151026.zip](https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/etv/historicos/2026/datos_abiertos_dengue_151026.zip) |

- Los archivos CSV de los ZIP se leen por bloques desde memoria; el ETL no
  guarda los originales en `data/raw`.
- Resultado verificado: 1,239,045 registros fuente, 247,174 casos confirmados
  válidos y 54,435 filas municipio-semana, con síntomas entre 2020-01-01 y
  2026-10-07.
- Calidad pendiente: 8,798 casos confirmados tienen fecha de síntomas posterior
  a `FECHA_ACTUALIZACION`. Se conservaron y se reportan como advertencia; no se
  imputaron ni descartaron automáticamente.
- Salida: `data/processed/dengue_confirmed_weekly_2020_2026.parquet`.
- La salida cubre solo 2020–2026; no representa el periodo 2015–2026 completo.

## Clima e integración

ERA5-Land/Copernicus y el catálogo geográfico de INEGI aún no se han descargado
ni integrado. No hay variables meteorológicas en la salida actual. La
integración final requiere alinear el clima a municipio y semana y validar las
claves antes de generar el Parquet dengue-clima.
