import pandas as pd


def clean_dengue_data(df_raw):
    """
    Keep confirmed cases, parse the source's day-first dates, and derive keys.
    """
    required_columns = {
        "ESTATUS_CASO",
        "FECHA_SIGN_SINTOMAS",
        "ENTIDAD_RES",
        "MUNICIPIO_RES",
    }
    missing_columns = required_columns.difference(df_raw.columns)
    if missing_columns:
        raise ValueError(
            "Faltan columnas requeridas en el CSV de dengue: "
            + ", ".join(sorted(missing_columns))
        )

    df = df_raw.copy()

    df["ESTATUS_CASO"] = pd.to_numeric(df["ESTATUS_CASO"], errors="coerce")
    df = df.loc[df["ESTATUS_CASO"] == 2].copy()

    df["FECHA_SIGN_SINTOMAS"] = pd.to_datetime(
        df["FECHA_SIGN_SINTOMAS"],
        format="mixed",
        dayfirst=True,
        errors="coerce",
    )
    df["ENTIDAD_RES"] = pd.to_numeric(df["ENTIDAD_RES"], errors="coerce")
    df["MUNICIPIO_RES"] = pd.to_numeric(df["MUNICIPIO_RES"], errors="coerce")
    df = df.dropna(
        subset=["FECHA_SIGN_SINTOMAS", "ENTIDAD_RES", "MUNICIPIO_RES"]
    ).copy()

    df["ENTIDAD_RES"] = df["ENTIDAD_RES"].astype(int).astype(str).str.zfill(2)
    df["MUNICIPIO_RES"] = df["MUNICIPIO_RES"].astype(int).astype(str).str.zfill(3)
    df["CVE_GEO"] = df["ENTIDAD_RES"] + df["MUNICIPIO_RES"]

    iso_dates = df["FECHA_SIGN_SINTOMAS"].dt.isocalendar()
    df["EPI_YEAR"] = iso_dates["year"].astype("int32")
    df["EPI_WEEK"] = iso_dates["week"].astype("int8")
    return df