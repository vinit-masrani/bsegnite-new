import MySQLdb
from scrapy.exceptions import DropItem
class Company_listing_Pipeline(object):
	def open_spider(self,spider):
		HostName = "localhost"
		UserName = "root"
		Password = ""
		Database = "bsegnite"
		self.connection = MySQLdb.connect(host = HostName, user = UserName, passwd = Password, database = Database)
		self.cur = self.connection.cursor()

	def process_item(self, item, spider):
		presql = "SELECT count(c_name) FROM company WHERE c_id= %s"
		preval = (item['s_id'])
		self.cur.execute(presql,preval)
		decision = self.cur.fetchone()

		if(decision[0]==0):
			presql3 = "INSERT INTO company (c_id,c_acro,c_name,c_isin,c_indus) VALUES (%s,%s,%s,%s,%s)" 
			preval3 = (item['s_id'],item['s_acro'],item['s_name'],item['s_isin'],item['s_indus'])
			self.cur.execute(presql3,preval3)
			self.connection.commit()
			return item
		
	def close_spider(self,spider):
		self.cur.close()
		self.connection.close()
