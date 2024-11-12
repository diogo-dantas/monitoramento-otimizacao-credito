from typing import List, Optional
import logging
from psycopg2.extensions import cursor, connection

# Configura as definições básicas para o registro de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryOptimizer:
	def__init__(self,connection : connection)
	"""
	Inicializa o otimizador de queries.

	Args:
		connection: Conexão com o banco de dados Postgresql

	"""

	self.conn = connection
	self.cursor = None

