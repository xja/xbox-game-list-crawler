# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql 


class XboxGamesPipeline:
    def process_item(self, item, spider):
        self.insert_db(item)
        return item
    
    def open_spider(self, spider):
        # connect database
        db = spider.settings.get('MYSQL_DB_NAME','scrapy_db')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '123456')

        self.db_conn =pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()

    # close database
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()
        
    def insert_db(self, item):
        values = (
            item['title'],
            item['category'],
            item['release'],
            item['rating'],
            item['review_count'],
            item['price_now'],
            item['price_original'],
            item['price_premium'],
            item['identifier'],
            item['description'],
            item['cover'],
            item['link'],
            item['publisher'],
            item['developer']
        )
        sql = 'INSERT INTO `xbox` (`title`,`category`,`release`,`rating`,`review_count`,`price_now`,`price_original`,`price_premium`,`identifier`,`description`,`cover`,`link`,`publisher`,`developer`,`tag`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"Coming Soon");'
        result = self.db_cur.execute(sql, values)
