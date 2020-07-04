import scrapy
from xbox_games.items import XboxGamesItem
from scrapy.http import Request
from pprint import pprint

class XboxSpider(scrapy.Spider):
    name = 'xbox'
    allowed_domains = ['microsoft.com']
    #start_urls = ['https://www.microsoft.com/en-us/store/top-paid/games/xbox']
    start_urls = ['https://www.microsoft.com/en-us/store/coming-soon/games/xbox']
    base_url = 'https://www.microsoft.com'
    
    # parse game list with default parse method
    def parse(self, response):
        for game in response.css('.m-channel-placement-item'):
            item = XboxGamesItem()
            item['title'] = game.css('h3::text').get()
            link = self.base_url + game.css('a').attrib['href'].split('?')[0]
            item['link'] = link
            item['identifier'] = link.split('/')[-1]
            #print('\nlink: ' + link + '\n identifier: ' + link.split('/')[-1] + '\n title: ' + game.css('h3::text').get())
            
            rating = game.css('span[itemprop="ratingValue"]::text').get()
            if rating is not None:# and rating != '':
                item['rating'] = float(rating)
            else:
                item['rating'] = 0
            # if there's reviews, .c-rating would exist, and its 2nd child span would be review count
            review_count = game.css('.c-rating span:nth-child(4)::text').get()
            #print('\n\n\n\nreview_count: '+ review_count)
            if review_count is not None:# and review_count != '':
                # if no exceptions, review_count should be 3rd word in review_count: There are 11115 reviews
                item['review_count'] = int(review_count.split()[2])
            else:
                item['review_count'] = 0
            yield Request(link, meta={'item':item}, callback=self.parseContent)
        
        next_page = response.css('.m-pagination a[aria-label="next page"]').attrib['href']
        if next_page is not None:
            yield Request(url=self.base_url+next_page, callback=self.parse)
            #pass
        
    # category, release, price_now, price_original, price_premium, description, cover, publisher, developer
    def parseContent(self, response):
        item = response.meta['item']
        game_detail = []
        
        ####
        #### BOTH category and release could be obtained in the bottom code
        ####
        category = response.css('#category-toggle-target a::text').get()
        if category is None:
            category = response.css('#category-toggle-target span::text').get()
        if category is not None:
            category = category.replace(' ','').replace('\r\n','')
        else:
            category = '' # NULL value
        item['category'] = category
        
        release = response.css('#releaseDate-toggle-target>span::text').get()
        if release is None:
            release = '0000-1-1'
        else:
            release = release.replace(' ','').replace('\r\n','').split('/')
            release = release[2]+'-'+release[0]+'-'+release[1]
        item['release'] = release
        
        # ProductPrice_productPrice_PriceContainer>s original price when discount, otherwise not exist
        price_original = response.css('#ProductPrice_productPrice_PriceContainer>s::text').get()
        if price_original is None:  # when an element does not exist, css return None
            price_original = response.css('#ProductPrice_productPrice_PriceContainer>span::text').get()
            price_now = price_original
        else:
            price_now = response.css('#productPrice meta[itemprop="price"]').attrib['content']
        price_premium = response.css('.remediation-cta-label::text').get()
        if price_premium is None:
            price_premium = '' # NULL value
        item['price_original'] = float(price_original.replace('$',''))
        item['price_now'] = float(price_now.replace('$','').replace('"',''))
        item['price_premium'] = price_premium
        
        description = response.css('#product-description::text').get()
        if description is None:
            description = '' # NULL value
        item['description'] = description
        
        cover = response.css('#dynamicImage_image_picture>source:first-child').attrib['srcset']
        if cover is None:
            cover = '' # NULL value
        else:
            cover= cover.split('?')[0]
        item['cover'] = cover
        
        # this could obtain `developer` `publisher` `release` `category`
        developer = '' # NULL value
        publisher = '' # NULL value
        for div in response.css('div[role="dialog"]>div[role="document"]'):
            if div.css('h1::text').get() == "Developed by":
                developer = div.css('div[class="f-dialog-scroll"]::text').get()
            if div.css('h1::text').get() == "Published by":
                publisher = div.css('div[class="f-dialog-scroll"]>span::text').get()
        if publisher is not None or publisher != '': # NULL value:
            publisher = publisher.replace(' ','').replace('\r\n','')
        if developer is not None or developer != '': # NULL value:
            developer = developer.replace(' ','').replace('\r\n','')
        item['publisher'] = publisher
        item['developer'] = developer
        
        game_detail.append(item)
        return game_detail
