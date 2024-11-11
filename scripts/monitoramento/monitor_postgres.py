import psycopg2
import pandas as pd

class PostgresMetricsCollector:
	def __init__(self, dbname, user, password, host, port):
		self.conn = None
		self.dbname = dbname
		self.user = user
		self.password = password
		self.host = host 
		self. port = port

	def connect(self):
		try:
			self.conn = psycopg2.connect(
			dbname = self.dbname,
			user = self.user,
			password = self.password,
			host = self.host,
			port = self.port
			)
		except Exception as e:
			print("Erro ao conectar ao banco de dados: ", e)

	def collect_metrics(self):
		if not self.conn:
			self.connect()

		cursor = self.conn.cursor()
		cursor.execute("SELECT * FROM pg_stat_activity;")
		data = cursor.fetchall()
		columns = [desc[0] for desc in cursor.description]
		df = pd.DataFrame(data, columns = columns)
		cursor.close()
		return df

	# O método collect_metrics consulta a tabela pg_stat_activity para obter informações sobre as conexões ativas 
	# e atividades atuais no banco de dados, retornando os dados em um DataFrame do Pandas.
