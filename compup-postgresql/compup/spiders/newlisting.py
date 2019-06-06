# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from compup.items import CompanyItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
import os
import json
import pandas as pd
df = pd.read_csv('../temp/newlisting.csv', header = 0, skip_blank_lines = True)
urls = []
Cdata = {}
for i in df['company_id']:
	temp = "https://api.bseindia.com/BseIndiaAPI/api/ComHeader/w?quotetype=EQ&scripcode="+str(i)+"&seriesid="
	urls.append(temp)
for index,row in df.iterrows():
	Cdata.update({row['company_id']:row['company_name']})
os.remove('../temp/newlisting.csv')


class NewlistingSpider(scrapy.Spider):
    name = 'newlisting'
    allowed_domains = ['https://api.bseindia.com']
    start_urls = urls[0]
    def start_requests(self):
    	for url in urls: 
            yield SplashRequest(url,self.parse,endpoint='render.html',args={'wait':2},)


    def parse(self, response):
        raw_data = str(response.xpath('//pre/text()').extract_first())
        data = json.loads(raw_data)
        comp_loader = ItemLoader(item=CompanyItem(), selector = data)
        comp_loader.add_value('s_id', data["SecurityCode"])
        comp_loader.add_value('s_name', Cdata[int(data["SecurityCode"])])
        comp_loader.add_value('s_acro', data["SecurityId"])
        comp_loader.add_value('s_isin', data["ISIN"])
        comp_loader.add_value('s_indus', data["Industry"])

        yield comp_loader.load_item()
