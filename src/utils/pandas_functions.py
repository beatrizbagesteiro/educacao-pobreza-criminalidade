import pandas as pd
import logging
logger = logging.getLogger(__name__)

def drop_columns(df: pd.DataFrame, columns_to_drop: list) -> pd.DataFrame:
    logger.info("Iniciando exclusão de colunas...\n")
    try:
        df = df.drop(columns=columns_to_drop)
        return df
    except Exception as e:
        logger.error(f"Erro ao excluir colunas: {e}")
        raise e

def rename_columns(df: pd.DataFrame, columns_to_rename: dict) -> pd.DataFrame:
    logger.info("Iniciando a renomeação de colunas...\n")
    try:
        df = df.rename(columns=columns_to_rename)
        return df
    except Exception as e:
        logger.error(f"Erro ao renomear as colunas: {e}")
        raise e
    
def filter_active_rows(df: pd.DataFrame, column_name: str, active_value) -> pd.DataFrame:
    logger.info(f"Filtrando base onde {column_name} == {active_value}")
    try:
        return df[df[column_name] == active_value]
    except Exception as e:
        logger.error(f"Erro ao filtrar linhas: {e}")
        raise e

def filter_values(df:pd.DataFrame, column_name:str, values:list) -> pd.DataFrame:
    logger.info("Iniciando a filtragem de valores...\n")
    try:
        return df[df[column_name].isin(values)]
    except Exception as e:
        logger.error(f"Erro ao filtrar linhas: {e}")
        raise e

def columns_name_to_lower(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Colocando o nome das colunas em lowercase...\n")
    df.columns = df.columns.str.lower()
    return df

def cast_type(df: pd.DataFrame, columns: list, type) -> pd.DataFrame:
    logger.info("Definindo o tipo das colunas...\n")
    df_copy = df.copy()
    df_copy[columns] = df_copy[columns].astype(type)
    return df_copy