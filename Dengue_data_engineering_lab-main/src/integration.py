import pandas as pd

INTEGRATION_KEYS = ["CVE_GEO", "EPI_YEAR", "EPI_WEEK"]


def aggregate_weekly_dengue(df_clean):
    """Count confirmed dengue cases for each municipality and epi-week."""
    required_columns = set(INTEGRATION_KEYS)
    missing_columns = required_columns.difference(df_clean.columns)
    if missing_columns:
        raise ValueError(
            "Faltan columnas para agregar dengue por semana: "
            + ", ".join(sorted(missing_columns))
        )

    return (
        df_clean.groupby(INTEGRATION_KEYS, as_index=False)
        .size()
        .rename(columns={"size": "CONFIRMED_CASES"})
    )


def integrate_with_climate(dengue_weekly, climate_weekly):
    """Join weekly dengue and climate data using their shared geographic keys."""
    required_climate_columns = {"PRECIPITATION_MM", "TEMP_CELSIUS"}
    missing_climate_columns = required_climate_columns.difference(
        climate_weekly.columns
    )
    if missing_climate_columns:
        raise ValueError(
            "Faltan variables meteorológicas requeridas: "
            + ", ".join(sorted(missing_climate_columns))
        )

    for name, frame in (
        ("dengue", dengue_weekly),
        ("clima", climate_weekly),
    ):
        missing_columns = set(INTEGRATION_KEYS).difference(frame.columns)
        if missing_columns:
            raise ValueError(
                f"Faltan claves de integración en {name}: "
                + ", ".join(sorted(missing_columns))
            )
        if frame.duplicated(INTEGRATION_KEYS).any():
            raise ValueError(
                f"El dataset de {name} tiene claves CVE_GEO/año/semana duplicadas."
            )

    return pd.merge(
        dengue_weekly,
        climate_weekly,
        on=INTEGRATION_KEYS,
        how="inner",
        validate="one_to_one",
    )