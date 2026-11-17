from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.operators.python_operator import PythonOperator
import scrapy
import logging
from Crypto_nlp.Scraper.Scraper.items import ZrozumiecbitcSpiderItem, BitcoinSpiderItem

# Name of the spider as mentioned in the "genspider" command
name = 'bitcoin_magazine_spider'
# Domains allowed for scraping, as mentioned in the "genspider" command
allowed_domains = ['www.bitcoinmagazine.com', 'bitcoinmagazine.com']
# URL(s) to scrape as mentioned in the "genspider" command
# The scrapy spider, starts making  requests, to URLs mentioned here
start_urls = ['https://bitcoinmagazine.com/business']
custom_settings = {"FEEDS": {"Scraper/Scraper/spiders/Scraped_data.json": {"format": "jsonlines"}}, 'FEED_EXPORTERS': {
    'jsonlines': 'scrapy.exporters.JsonItemExporter'}, 'FEED_EXPORT_ENCODING': 'utf-8'}



# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="spider_dag", start_date=datetime(2023, 3, 29), schedule=@once) as dag:
    @task()
    def parse(self, response):
        base_url = 'https://bitcoinmagazine.com/business'
        bitcoin_magazine_spider = response.xpath(
            '//*[@id="main-content"]/section[3]/phoenix-hub/section[1]/phoenix-non-personalized-recommendations-tracking/div[1]/phoenix-super-link/phoenix-card/div[2]/phoenix-ellipsis')
        # for bitc in bitcoin_magazine_spider:
        title = bitcoin_magazine_spider.xpath(".//a/h2//text()").get()
        link = bitcoin_magazine_spider.xpath(".//a/@href").get()
        full_url = base_url + link
        # yield {"link": link, "title": title}
        # yield {"meta": response}
        yield response.follow(url=link, callback=self.parse_bitcoin_magazine_spider,
                              meta={'bitcoin_magazine_spider_title': title, 'bitcoin_magazine_spider_link': full_url})

    # Tasks are represented as operators
    spider_first_task = PythonOperator(task_id="parse", python_callable=parse)
    # Set dependencies between tasks
    spider_first_task >> airflow()