import os
from pathlib import Path

import pandas as pd

from src.cleaning import clean_dengue_data
from src.ingestion import PROJECT_ROOT, iter_dengue_csv_chunks
from src.integration import aggregate_weekly_dengue

OUTPUT_PATH = Path(
    os.environ.get(
        "DENGUE_OUTPUT_PATH",
        PROJECT_ROOT / "data" / "processed" / "dengue_confirmed_weekly_2020_2026.parquet",
    )
)


def main():
    raw_records = 0
    confirmed_records = 0
    cleaned_records = 0
    symptom_after_update = 0
    min_symptom_date = None
    max_symptom_date = None
    weekly_chunks = []
    release_records = {}

    for release_year, df_raw in iter_dengue_csv_chunks():
        raw_records += len(df_raw)
        release_records[release_year] = (
            release_records.get(release_year, 0) + len(df_raw)
        )
        confirmed_records += int(
            (pd.to_numeric(df_raw["ESTATUS_CASO"], errors="coerce") == 2).sum()
        )
        df_clean = clean_dengue_data(df_raw)
        cleaned_records += len(df_clean)

        if "FECHA_ACTUALIZACION" in df_clean:
            update_dates = pd.to_datetime(
                df_clean["FECHA_ACTUALIZACION"],
                format="mixed",
                dayfirst=True,
                errors="coerce",
            )
            symptom_after_update += int(
                (df_clean["FECHA_SIGN_SINTOMAS"] > update_dates).sum()
            )

        if not df_clean.empty:
            chunk_min = df_clean["FECHA_SIGN_SINTOMAS"].min()
            chunk_max = df_clean["FECHA_SIGN_SINTOMAS"].max()
            min_symptom_date = (
                chunk_min if min_symptom_date is None else min(min_symptom_date, chunk_min)
            )
            max_symptom_date = (
                chunk_max if max_symptom_date is None else max(max_symptom_date, chunk_max)
            )

        weekly_chunks.append(aggregate_weekly_dengue(df_clean))

    if not weekly_chunks:
        raise RuntimeError("No se obtuvieron registros de los archivos oficiales.")

    for release_year, record_count in sorted(release_records.items()):
        print(
            f"Corte {release_year} procesado: {record_count:,} registros; "
            "no se guardó el CSV original."
        )

    df_weekly = (
        pd.concat(weekly_chunks, ignore_index=True)
        .groupby(["CVE_GEO", "EPI_YEAR", "EPI_WEEK"], as_index=False)[
            "CONFIRMED_CASES"
        ]
        .sum()
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_weekly.to_parquet(OUTPUT_PATH, index=False)

    df_check = pd.read_parquet(OUTPUT_PATH)
    if len(df_check) != len(df_weekly):
        raise RuntimeError("La validación del Parquet no coincide con el resultado ETL.")
    if df_check.duplicated(["CVE_GEO", "EPI_YEAR", "EPI_WEEK"]).any():
        raise RuntimeError("El Parquet contiene claves municipales/semanales duplicadas.")
    if df_check[["CVE_GEO", "EPI_YEAR", "EPI_WEEK", "CONFIRMED_CASES"]].isna().any().any():
        raise RuntimeError("El Parquet contiene nulos en columnas requeridas.")
    if not df_check["CVE_GEO"].str.fullmatch(r"\d{5}").all():
        raise RuntimeError("El Parquet contiene claves geográficas que no tienen 5 dígitos.")
    if not df_check["EPI_WEEK"].between(1, 53).all():
        raise RuntimeError("El Parquet contiene semanas epidemiológicas fuera de rango.")
    if int(df_check["CONFIRMED_CASES"].sum()) != cleaned_records:
        raise RuntimeError("El total semanal no coincide con los casos confirmados limpios.")

    print(f"Registros originales en los cortes: {raw_records:,}")
    print(f"Casos confirmados antes de limpiar: {confirmed_records:,}")
    print(f"Casos confirmados válidos: {cleaned_records:,}")
    print(f"Filas municipio-semana: {len(df_check):,}")
    if min_symptom_date is not None:
        print(f"Periodo de síntomas: {min_symptom_date.date()} a {max_symptom_date.date()}")
    if symptom_after_update:
        print(
            "ADVERTENCIA: hay "
            f"{symptom_after_update:,} casos confirmados cuya fecha de síntomas "
            "es posterior a FECHA_ACTUALIZACION; se conservaron y deben revisarse."
        )
    print(f"Parquet epidemiológico guardado en: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
