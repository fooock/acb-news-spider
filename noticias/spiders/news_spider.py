import scrapy

from scrapy.utils.markup import remove_tags


class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = ["http://www.acb.com/"]
    allowed_domains = ["acb.com"]

    def parse(self, response):
        for link in response.css('div.titulo a::attr(href)').extract():
            if not link.startswith(self.start_urls[0]):
                continue
            yield scrapy.Request(link, callback=self.parse_content)

    def parse_content(self, response):
        titulo = response.css('div.tituloreal::text').extract_first()
        contenido = response.css('div.cuerpoarticulo').extract_first()
        yield {'titulo': titulo, 'contenido': remove_tags(contenido)}

        # get related news
        for related in response.css('div.cuerpoarticulo2 a.negro::attr(href)').extract():
            yield response.follow(related, callback=self.parse_content)

        # top news
        for top in response.css('div.menucontenido3 a.blanco::attr(href)').extract():
            yield response.follow(top, callback=self.parse_content)
