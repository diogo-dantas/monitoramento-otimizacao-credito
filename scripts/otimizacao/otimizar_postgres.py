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

	def analyze_query(self, query: str) -> Optional[List[tuple]]:
		"""
		Analisa e explica o plano de execução de uma query.

		Args:
			query SQL a ser analisada

		Returns:
			Lista com o resultado da análise ou None em caso de erro.
		"""
		try:
			self.cursor = self.conn.cursor()
			explain_query = self._build_explain_query(query)
			self.cursor.execute(explain_query)
			return self.cursor.fetchall()

		except Exception as e:
			logger.error(f"Erro ao analisar query: {str(e)}") 
			return	None

		finally:
			self._cleanup()

		def _build_explain_query(self, query: str) -> str:
			""" 
			Constrói a query EXPLAIN ANALYZE


			Args:
				query: Query SQL original

			Returns:

				query com EXPLAIN ANALYZE
			"""

			return f"""
			EXPLAIN (FORMAT JSON, ANALYZE, BUFFERS, COSTS, TIMING)
			{query.strip()}
			"""

		def _cleanup(self):
			""" Fecha o cursor se estiver aberto."""
			if self.cursor:
				self.cursor.close()

