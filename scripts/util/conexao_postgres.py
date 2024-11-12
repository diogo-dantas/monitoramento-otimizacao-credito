import logging
from typing import Optional, List, Tuple, Any
import pandas as pd
import psycopg2
from psycopg2 import sql

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# subclasse de Exception
class DatabaseError(Exception):
    """Exceção customizada para erros relacionados ao banco de dados."""
    pass

@dataclass 
class DatabaseConfig:
    """Configurações de conexão com o banco de dados."""
    dbname: str
    user: str
    password: str
    host: str = 'localhost'
    port: str = '5432'

class PostgresDatabase:
    """Classe para gerenciar operações com banco de dados PostgreSQL."""
    
    def __init__(self, config: DatabaseConfig):
        """
        Inicializa a conexão com o banco de dados.
        
        Args:
            config: Configurações do banco de dados
        """
        self.config = config
        self._conn = None

    def connect(self) -> None:
        """
        Estabelece conexão com o banco de dados.
        
        Raises:
            DatabaseError: Se houver erro na conexão
        """
        try:
            self._conn = psycopg2.connect(
                dbname=self.config.dbname,
                user=self.config.user,
                password=self.config.password,
                host=self.config.host,
                port=self.config.port
            )
            logger.info("Conexão com o PostgreSQL estabelecida com sucesso!")
        except Exception as e:
            error_msg = f"Erro ao conectar ao PostgreSQL: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
            
    def close(self) -> None:
        """Fecha a conexão com o banco de dados."""
        if self._conn:
            self._conn.close()
            self._conn = None
            logger.info("Conexão com o PostgreSQL encerrada com sucesso.")