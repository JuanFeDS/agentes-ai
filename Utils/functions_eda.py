"""Modulo de Utils"""
import pandas as pd

def resumen_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Generación de resumen descriptivo de las variables del DataFrame

    Args:
        df (pd.DataFrame): DataFrame original

    Returns:
        pd.DataFrame: DataFrame descriptivo
    """
    df_resume = pd.DataFrame()

    for variable in df.columns:
        variable_name = variable
        tipo_dato = df[variable].dtype
        registros_esperados = len(df)
        registros_disponibles = int(df[variable].count())
        unicos = len(df[variable].unique())
        porc_reg_disponibles = round(registros_disponibles/registros_esperados * 100, 2)
        ejemplos = list(df[variable].sample(3))

        row_resume = pd.DataFrame({
            'Variable': [variable_name],
            'Tipo_Dato': [tipo_dato],
            'Registros_Esperados': [registros_esperados],
            'Registros_Disponibles': [registros_disponibles],
            '%Reg_Disponibles': [porc_reg_disponibles],
            'Valores_Unicos': [unicos],
            'Ejemplos': [ejemplos]
        })

        df_resume = pd.concat([df_resume, row_resume])

    return df_resume
