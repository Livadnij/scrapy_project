import scrapy


class FactorySpider(scrapy.Spider):
    name = "factoryspider"
    allowed_domains = ["factorio.com"]
    start_urls = ["https://www.factorio.com/blog/"]

    def parse(self, response):
        
        main_url = "https://www.factorio.com/blog/"
        
        max_page = response.css('div.panel-inset div.flex a::text').getall()[-3].strip()
        current_page = response.css('div.panel-inset div.flex a.active::text').get().strip()
        
        posts = response.css('div.blog-card ')
        
        def check_if_none (value):
            if value != ' ' :
                return value
            else:
                return "Not Found"
            
        
        for post in posts:
            name = post.css('h3 a::text').get().replace('\n                    ','').replace("\n                ",'')
            body = post.css('p::text').get().replace('\n            ','')
            url = post.css('h3 a').attrib['href']
            img = post.css('img').attrib['src']
            author = post.css('div.posted-by a::text').get()
            date = post.css('div.posted-by::text').getall()[-1].replace('\n on ', '').strip()
            
            yield{
                 'page_num' : current_page,
                 'name' : check_if_none(name),
                 'body' : check_if_none(body),
                 'url' : check_if_none(url),
                 'img' :  check_if_none(img),
                 'author' : check_if_none(author),
                 'date' : check_if_none(date)
             }       
     
        if int(current_page) < int(max_page) :
                    
            next_page_url = main_url + str(int(current_page) +1)
            yield response.follow(next_page_url, callback = self.parse)
        

# post.css('h3 a::text').get().replace('\n                    ','').replace("\n                ",'')
# post.css('p::text').get()
# post.css('h3 a').attrib['href']

# response.css('div.panel-inset div.flex a::text').getall()[5].strip()