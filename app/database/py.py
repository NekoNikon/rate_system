import psycopg2

from psycopg2.extras import DictCursor ,RealDictCursor ,RealDictRow

dsn = "dbname='rate_system' user='postgres' host='localhost' password='jojodio' port='5432'"

psql = psycopg2

def Connect():
    conn = psql.connect(dsn)
    curs = conn.cursor()
    return  curs

conn = psql.connect(dsn)
curs = conn.cursor()
for s in range(4):
	for t in range(5):
		for i in range(33):
			curs.execute("INSERT INTO rate(rate_value , rate_indicator_id, rate_teacher_id, rate_season_id) VALUES(0.0 , %i , %i , %i)" % (i+1 , t+1 , s+1))
			conn.commit()
			print('%i-%i-%i' % (s+1 , t+1 , i+1))
