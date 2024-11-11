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