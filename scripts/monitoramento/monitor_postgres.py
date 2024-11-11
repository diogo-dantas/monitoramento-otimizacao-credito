import psycopg2
import pandas as pd

class PostgresMetricsCollector:
	def __init__(
		self.conn = None
		dbname: str,
        user: str,
        password: str,
        host: str = 'localhost',
        port: str = '5432'
        ):

	# Validação de None
    if any(param is None for param in [dbname, user, password]):
        raise TypeError("Credenciais do banco não podem ser None")
    
    # Validação de tipo string
    if not all(isinstance(param, str) for param in [dbname, user, password, host, port]):
        raise TypeError("Credenciais do banco devem ser strings")
    
    """ Inicializa o conector com PostgreSQL """

    self.credentials = {
        'dbname': dbname,
        'user': user,
        'password': password,
        'host': host,
        'port': port
    }


	def connect(self):
		try:
            conn = psycopg2.connect(**self.credentials)
            return conn
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

	def close_connection(self):
		if self.conn:
			self.conn.close()


