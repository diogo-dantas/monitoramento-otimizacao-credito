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

		def get_optimization_suggestions(self, execution_plan: List[tuple]) -> List[str]:
			"""
			Analisa o plano de execução e retorna sugestões de otimização.

			Args:
				execution_plan: Resultado da EXPLAIN ANALYZE

			Returns:
				Lista de sugestões para otimização
			"""
			suggestions = []

			if not execution_plan:
				return ["Não foi possível gerar sugestões: plano de execução vazio."]

			# Analisa o tempo total de execução
			execution_time = self._extract_execution_time(execution_plan)
			if execution_time > 1000:  # mais de 1 segundo
				suggestions.append(f"Query demorada: {execution_time:.2f}ms. Considere criar índices apropriados.")

			# Identifica operações de sequential scan
			if self._has_sequential_scan(execution_plan)	:
				suggestions.append("Detectado Sequential Scan. Considere criar índices apropriados.")

			return suggestions

		def _extract_execution_time(self, execution_plan: List[tuple]) -> float:
			"""
			Extrai o tempo total de execução do plano.

			Args:
				execution_plan: Resultado da análise EXPLAIN ANALYSE

			Returns:
				Tempo de execução em milisegundos
			"""
			try:
				for row in execution_plan:
					if 'Execution Time' in str(row):
						return float(str(row).split(':')[1].strip().replace('ms', ''))
			except Exception:
				return 0.0		

		def _has_sequential_scan(self, execution_plan: List[tuple]) -> bool:
			"""
			Verifica se há Sequential Scan no plano de execução.

			Args:
				execution_plan: Resultado da análise EXPLAIN ANALYSE

			Returns:
				True se encontrar Sequential Scan, False caso contrário.
			"""
			return any('Seq Scan' in str(row) for row in execution_plan)

		def _cleanup(self):
			""" Fecha o cursor se estiver aberto."""
			if self.cursor:
				self.cursor.close()

