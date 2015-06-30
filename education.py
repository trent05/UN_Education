import pandas as pd
from pandas.io.html import read_html
import sqlite3 as lite
url = 'http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm'
web_data = pd.read_html(url)
len(web_data)
UN_data = web_data[6]
UN_data = UN_data.ix[6:]
UN_data.columns = ['Country or Area', 'Footnote', 'Year', 'Total', 'Men', 'Women']
#del world_billionaires['No']
#type(world_billionaires)
def dfsqlite(dataframe, db_name, tbl_name):
	con = lite.connect(db_name)
	cur = con.cursor()

	wildcards = ','.join(['?'] * len(dataframe.columns))
	data = [tuple(x) for x in dataframe.values]

	cur.execute("drop table if exists %s" % tbl_name)

	col_str = '"' + '","'.join(dataframe.columns) + '"'
	cur.execute("create table %s (%s)" % (tbl_name, col_str))

	cur.executemany("insert into %s values(%s)" % (tbl_name, wildcards), data)

	con.commit()
	con.close()
dfsqlite(UN_data, db_name = "UN_data", tbl_name = "Indicators on Education")
print UN_data