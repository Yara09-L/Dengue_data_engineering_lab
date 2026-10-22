from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import BadZipFile, ZipFile

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DENGUE_RELEASES = (
    (
        2020,
        "https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/"
        "etv/historicos/2020/datos_abiertos_dengue_311220.zip",
    ),
    (
        2021,
        "https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/"
        "etv/historicos/2021/datos_abiertos_dengue_301221.zip",
    ),
    (
        2022,
        "https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/"
        "etv/historicos/2022/datos_abiertos_dengue_291222.zip",
    ),
    (
        2023,
        "https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/"
        "etv/historicos/2023/datos_abiertos_dengue_271223.zip",
    ),
    (
        2024,
        "https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/"
        "etv/historicos/2024/datos_abiertos_dengue_191224.zip",
    ),
    (
        2025,
        "https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/"
        "etv/historicos/2025/datos_abiertos_dengue_111225.zip",
    ),
    (
        2026,
        "https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/"
        "etv/historicos/2026/datos_abiertos_dengue_151026.zip",
    ),
)


def iter_dengue_csv_chunks(chunksize=50_000):
    """Yield (release_year, CSV chunk) without keeping source ZIPs on disk."""
    if chunksize <= 0:
        raise ValueError("chunksize debe ser un entero positivo.")

    for release_year, url in DENGUE_RELEASES:
        request = Request(url, headers={"User-Agent": "DengueDataEngineeringLab/1.0"})
        print(f"Leyendo corte oficial {release_year}: {url}")
        with urlopen(request, timeout=60) as response:
            archive_bytes = response.read()

        try:
            with ZipFile(BytesIO(archive_bytes)) as archive:
                invalid_member = archive.testzip()
                if invalid_member is not None:
                    raise BadZipFile(
                        f"El ZIP de {release_year} está dañado: {invalid_member}"
                    )

                csv_members = [
                    member
                    for member in archive.namelist()
                    if Path(member.replace("\\", "/")).suffix.lower() == ".csv"
                ]
                if len(csv_members) != 1:
                    raise ValueError(
                        f"El ZIP de {release_year} debe contener exactamente un CSV; "
                        f"encontrados: {len(csv_members)}"
                    )

                with archive.open(csv_members[0]) as csv_file:
                    for chunk in pd.read_csv(
                        csv_file,
                        chunksize=chunksize,
                        low_memory=False,
                    ):
                        chunk["SOURCE_RELEASE_YEAR"] = release_year
                        yield release_year, chunk
        except BadZipFile as error:
            raise BadZipFile(
                f"No se pudo leer el corte oficial de dengue {release_year}."
            ) from error
