# import MySQLdb
import psycopg2
from scrapy.exceptions import DropItem
class Company_listing_Pipeline(object):
	def open_spider(self,spider):
		HostName = "localhost"
		UserName = "postgres"
		Password = "worksmart"
		Database = "bsegnite"
		# HostName = "ec2-107-20-185-27.compute-1.amazonaws.com"
		# UserName = "btsfbrzbpjklbk"
		# Password = "9f21319033b536f72bf58b89e405a731efb875f600ee57e6b5589fb969f1cde5"
		# Database = "d4604o88nokgf4"
		self.connection = psycopg2.connect(host = HostName, user = UserName, password = Password, dbname = Database)
		self.cur = self.connection.cursor()

	def process_item(self, item, spider):
		presql = "SELECT count(c_name) FROM company WHERE c_id= %s"
		preval = (item['s_id'])
		self.cur.execute(presql,preval)
		self.connection.commit()
		decision = self.cur.fetchone()

		if(decision[0]==0):
			presql3 = "INSERT INTO company (c_id,c_acro,c_name,c_isin,c_indus) VALUES (%s,%s,%s,%s,%s)" 
			preval3 = (int(item['s_id'][0]),item['s_acro'][0],item['s_name'][0],item['s_isin'][0],item['s_indus'][0])
			self.cur.execute(presql3,preval3)
			self.connection.commit()
			return item
		
	def close_spider(self,spider):
		self.cur.close()
		self.connection.close()
