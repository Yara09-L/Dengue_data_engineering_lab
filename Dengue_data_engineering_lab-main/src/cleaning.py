import pandas as pd

def clean_dengue_data(df_raw):
    """
    Cleans raw dengue dataset by filtering confirmed cases, casting dates,
    and generating 5-digit INEGI GEO codes.
    """
    df = df_raw.copy()
    
    # CLEAN-01: Filter confirmed cases
    df = df[df['ESTATUS_CASO'] == 2]
    
    # CLEAN-02: Convert date strings to datetime
    df['FECHA_SIGN_SINTOMAS'] = pd.to_datetime(df['FECHA_SIGN_SINTOMAS'])
    
    # CLEAN-03: Create zero-padded 5-digit CVE_GEO
    df['ENTIDAD_RES'] = df['ENTIDAD_RES'].astype(str).str.zfill(2)
    df['MUNICIPIO_RES'] = df['MUNICIPIO_RES'].astype(str).str.zfill(3)
    df['CVE_GEO'] = df['ENTIDAD_RES'] + df['MUNICIPIO_RES']
    
    return df