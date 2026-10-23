import logging
from src.silver.cad_unico import data_transformation_cad_unico
from src.silver.censo_escolar import data_transformation_censo_escolar
from src.bronze.load_censo_escolar import load_bronze

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def silver_pipeline():
    logger.info("Iniciando o processamento de toda a camada Silver...")

    try:
        logger.info("Iniciando rotina do CadÚnico...")
        data_transformation_cad_unico()
        
        logger.info("Iniciando rotina do Censo Escolar...")
        data_transformation_censo_escolar()

        logger.info("Processamento da camada Silver finalizado com sucesso!")
        
    except Exception as e:
        logger.error(f"O pipeline falhou: {e}")
        raise e

if __name__ == "__main__":
    load_bronze()
    silver_pipeline()