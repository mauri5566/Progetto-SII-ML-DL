import scrapy
from ..items import ReviewscraperItem
import re
import html
import langid
import brotli

class ReviewSpider(scrapy.Spider):

    name= 'reviews'

    def start_requests(self):
        tripadvisor_urls = [
        'https://www.tripadvisor.it/Restaurants-g187791-Rome_Lazio.html',
        'https://www.tripadvisor.it/Restaurants-g187849-Milan_Lombardy.html',
        'https://www.tripadvisor.it/Restaurants-g187830-Bergamo_Province_of_Bergamo_Lombardy.html',
        'https://www.tripadvisor.it/Restaurants-g187870-Venice_Veneto.html',
        'https://www.tripadvisor.it/Restaurants-g187785-Naples_Province_of_Naples_Campania.html',
        'https://www.tripadvisor.it/Restaurants-g187855-Turin_Province_of_Turin_Piedmont.html',
        'https://www.tripadvisor.it/Restaurants-g187775-Catanzaro_Province_of_Catanzaro_Calabria.html',
        'https://www.tripadvisor.it/Restaurants-g494955-Trapani_Province_of_Trapani_Sicily.html',
        'https://www.tripadvisor.it/Restaurants-g187801-Bologna_Province_of_Bologna_Emilia_Romagna.html'
        'https://www.tripadvisor.it/Restaurants-g187895-Florence_Tuscany.html',
        'https://www.tripadvisor.it/Restaurants-g187890-Palermo_Province_of_Palermo_Sicily.html',
        'https://www.tripadvisor.it/Restaurants-g187823-Genoa_Italian_Riviera_Liguria.html',
        'https://www.tripadvisor.it/Restaurants-g187888-Catania_Province_of_Catania_Sicily.html',
        'https://www.tripadvisor.it/Restaurants-g187871-Verona_Province_of_Verona_Veneto.html',
        'https://www.tripadvisor.it/Restaurants-g187813-Trieste_Province_of_Trieste_Friuli_Venezia_Giulia.html',
        'https://www.tripadvisor.it/Restaurants-g187889-Messina_Province_of_Messina_Sicily.html',
        'https://www.tripadvisor.it/Restaurants-g187867-Padua_Province_of_Padua_Veneto.html',
        'https://www.tripadvisor.it/Restaurants-g187804-Parma_Province_of_Parma_Emilia_Romagna.html',
        'https://www.tripadvisor.it/Restaurants-g194702-Brescia_Province_of_Brescia_Lombardy.html',
        'https://www.tripadvisor.it/Restaurants-g194868-Prato_Province_of_Prato_Tuscany.html'
        ]
        yelp_urls = [
            'https://www.yelp.it/search?find_desc=&find_loc=Roma&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Milano&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Napoli&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Torino&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Venezia&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Firenze&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Palermo&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Genova&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Bologna&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Catania&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Verona&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Trieste&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Messina&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Padova&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Parma&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Brescia&start=0',
            'https://www.yelp.it/search?find_desc=&find_loc=Prato&start=0',            
        ]
        quandoo_urls = [
            'https://www.quandoo.it/en/result?destination=roma',
            'https://www.quandoo.it/en/result?destination=milano',
            'https://www.quandoo.it/en/result?destination=napoli',
            'https://www.quandoo.it/en/result?destination=torino',
            'https://www.quandoo.it/en/result?destination=venezia',
            'https://www.quandoo.it/en/result?destination=firenze',
            'https://www.quandoo.it/en/result?destination=palermo',
            'https://www.quandoo.it/en/result?destination=genova',
            'https://www.quandoo.it/en/result?destination=bologna',
            'https://www.quandoo.it/en/result?destination=catania',
            'https://www.quandoo.it/en/result?destination=verona'
        ]
        #for url in tripadvisor_urls:
            #yield scrapy.Request(url, callback = self.parse_tripadvisor_restaurants)
        for url in yelp_urls:
            yield scrapy.Request(url, callback = self.parse_yelp_restaurants)
        #for url in quandoo_urls:
            #yield scrapy.Request(url, callback = self.parse_quandoo_restaurants)
        
    def parse_tripadvisor_restaurants(self, response):
        #Recupera la lista dei ristoranti nella pagina corrente e invia richieste a ognuno di essi     
        all_restaurants = list(set(response.xpath("//div[contains(@data-test,'_list_item')]//div/div/div/span/a[starts-with(@href,'/Restaurant_Review')]/@href").extract()))
        for restaurant in all_restaurants:
            url = 'https://www.tripadvisor.it' + restaurant
            yield response.follow(url, callback = self.parse_tripadvisor_restaurant, dont_filter=True)
    
    def parse_yelp_restaurants(self, response):
        #Recupera la lista dei ristoranti nella pagina corrente e invia richieste a ognuno di essi  
        all_restaurants = list(set(response.xpath("//span[@class=' css-1egxyvc']/a[@class='css-19v1rkv']/@href").extract()))
        for restaurant in all_restaurants:
            #Per ogni ristorante accedi alla pagina relativa alle recensioni da 1 a 4 stelle.
            for i in range(1,5):
                url = 'https://www.yelp.it' + restaurant + '?rr=' + str(i)
                yield response.follow(url, callback = self.parse_yelp_restaurant, dont_filter=True)
        
        #Ricava la pagina corrente e passa alla prossima pagina, se non si è raggiunta l'ultima (ci sono 24 pagine al massimo)
        current_url = response.request.url
        pattern = r'start=(\d{1,})'
        match = re.search(pattern, current_url)
        if match:
            current_page = int(match.group(1))
        else:
            current_page = 0
        if current_page < 230:
            current_page += 10
            next_page = re.sub(pattern, rf'start={current_page}', current_url)
            yield response.follow(next_page, callback = self.parse_yelp_restaurants, dont_filter=True)
    
    def parse_quandoo_restaurants(self, response):
        #Recupera la lista dei ristoranti nella pagina corrente e invia richieste a ognuno di essi  
        all_restaurants = list(set(response.xpath("//a[@class='zt41a1-0 bFQofF']/@href").extract()))
        #Per ogni ristorante accedi alla sua pagina con recensioni ordinate dalle peggiori (quelle che ci interessano) alle migliori
        for restaurant in all_restaurants:
            url = 'https://www.quandoo.it' + restaurant + '/reviews?reviewSortTypeId=lowest-rating#content'
            yield response.follow(url, callback = self.parse_quandoo_restaurant, dont_filter=True)
        
        #Recupera la pagina corrente
        current_url = response.request.url
        pattern = r'page=(\d+)'
        match = re.search(pattern, current_url)
        if match:
            page_number = int(match.group(1))
        else:
            page_number = 1
        
        #Scorri le prime 5 pagine relative al ristorante, dopo 5 pagine le recensioni sono troppo poche
        if page_number<=5:
            page_number+=1
            #Se il parametro 'page' non è presente nell'url allora sei alla prima pagina, aggiorna l'url in modo dedicato
            if not match:
                next_page = current_url + '&page=' + str(page_number)
                yield response.follow(next_page, callback = self.parse_quandoo_restaurants, dont_filter=True)
            #Se il parametro page esiste e il pulsante 'next page' non è disabilitato allora non sei nè alla prima, nè all'ultima pagina. Aggiorna l'url di conseguenza
            elif match and response.xpath("//button[@class='sc-8sopd8-0 sc-1vrhx70-3 gohXxz'][2]").extract_first() is not None:
                page_number+=1
                next_page = re.sub(pattern, f'page={page_number}', current_url)
                yield response.follow(next_page, callback = self.parse_quandoo_restaurants, dont_filter=True)

    def parse_tripadvisor_restaurant(self, response):

        #Funzione di parsing del singolo ristorante su Tripadvisor
        all_reviews_containers = response.xpath('//div[@class="rev_wrap ui_columns is-multiline"]/div[2]')
        if all_reviews_containers is not None:
            for review_container in all_reviews_containers:
                items = ReviewscraperItem()
                items['restaurant_name'] = response.css('.HjBfq::text').extract_first()
                items['rating'] = 0
                #Il rating è espresso tramite dei pallini a cui corrisponde una classe css
                rating_classes = {
                    'ui_bubble_rating bubble_50': 5,
                    'ui_bubble_rating bubble_40': 4,
                    'ui_bubble_rating bubble_30': 3,
                    'ui_bubble_rating bubble_20': 2,
                    'ui_bubble_rating bubble_10': 1
                }
                rating_class = review_container.css('span::attr(class)').extract_first()
                items['rating'] = rating_classes.get(rating_class)
                items['quote'] = review_container.css('.noQuotes::text').extract_first()
                items['review'] = review_container.css('.partial_entry::text').extract_first()
                items['website'] = 'TripAdvisor'
                yield items
            #Controlla se il pulsante 'next page' è disabilitato ovvero se non si è arrivati all'ultima pagina. Solo in quel caso si invia una richiesta alla successiva
            if response.xpath('//a[@class = "nav next ui_button primary disabled"]').extract_first() is None:
                next_page = 'https://www.tripadvisor.it' + response.xpath('//a[@class = "nav next ui_button primary"]/@href').extract_first()
                yield response.follow(url=next_page, callback = self.parse_tripadvisor_restaurant)

    def parse_yelp_restaurant(self, response):
        
        #Funzione di parsing del singolo ristorante su yelp
        current_url = response.request.url
        pattern1 = r'\?rr=(\d+)' 
        match1 = re.search(pattern1, current_url)
        #Recupera il numero di stelle su cui è settata la pagina corrente
        n_star_filter = match1.group(1)

        #Yelp è un dito ar culo, i dati sono recuperabili solo da un api raggiungibile tramite un id presente nell'hatml della pagina
        bizId = response.xpath("//meta[@name='yelp-biz-id']/@content").extract_first()
        api_url = 'https://www.yelp.it/biz/' + bizId + '/review_feed?rr=' + str(n_star_filter)
        yield response.follow(url=api_url, callback = self.parse_yelp_restaurant_api)

    def parse_yelp_restaurant_api(self, response):

        #Funzione che scarica il file json dell'api corrispondente al ristorante di yelp
        current_url = str(response.request.url)
        jsonresponse = response.json()
        items = ReviewscraperItem()
        current_page = jsonresponse['pagination']['startResult']

        for review in jsonresponse['reviews']:
            items['restaurant_name'] = review['business']['name']
            items['rating'] = review['rating']
            items['quote'] = ''
            items['review'] = html.unescape(review['comment']['text'])
            items['website'] = 'Yelp'
            yield items

        #Il campo 'totalResults' del file json, indica quante recensioni ha il ristorante. Per capire se si è arrivati all'ultima pagina
        #Si fa la differenza tra il numero totale di recensioni e il numero di recensioni analizzate fino ad ora. Diversa gestione
        #Dell'aggiornameno dell'url in base all'esito della differenza
        if jsonresponse['pagination']['totalResults'] > current_page + 10:
            next_page = current_page + 10
            if next_page == 10:
                api_url = current_url + '&start=' + str(next_page)
            else:
                pattern = r'start=(\d{2,})'
                api_url = re.sub(pattern, rf'start={next_page}', current_url)
            yield response.follow(api_url, callback=self.parse_yelp_restaurant_api)

    def parse_quandoo_restaurant(self, response):
        
        #Identificazione pagina corrente
        current_url = response.request.url
        pattern1 = r'Page=(\d+)'
        match = re.search(pattern1, current_url)
        if match:
            page_number = int(match.group(1))
        else:
            page_number = 1

        number_of_reviews_on_page = len(response.xpath("//div[@data-name='shared-review']").extract())

        last_rating = 0
        #Usato range perchè con il metodo classico del recupero della lista dei ristoranti sono stati riscontrati problemi
        for i in range(1,number_of_reviews_on_page+1):
            items = ReviewscraperItem()
            items["restaurant_name"] = response.xpath("//h1[@data-qa='merchant-name']/text()").extract_first()
            #Quandoo offre la possibilità di assegnare un voto da 1 a 6 al ristorante. Si riporta a una scala da 1 a 5.
            quandoo_ratings = {
                6: 5,
                5: 4,
                4: 3,
                3: 3,
                2: 2,
                1: 1
            }
            quandoo_rating = int(response.xpath("//div[@data-name='shared-review']["+str(i)+"]//span[@data-qa='review-score']/text()[1]").extract_first())
            items["rating"] = quandoo_ratings.get(quandoo_rating)
            items["quote"] = response.xpath("//div[@data-name='shared-review']["+str(i)+"]//span[@data-qa='review-score-message']/text()[2]").extract_first()
            items["review"] = response.xpath("//div[@data-name='shared-review']["+str(i)+"]//p[@data-qa='review-description']/span/text()").extract_first()
            items["number"] = number_of_reviews_on_page
            items['website'] = 'Quandoo'
            #Quandoo non offre la possibilità di filtrare recensioni per lingua. L'item viene aggiunto all'output solo se viene riconosciuto come italiano
            if langid.classify(items['review'])[0] == 'it':
                yield items

            #Memorizza l'ultimo rating della pagina per decidere se andare alla prossima, non ci interessano rating alti
            if i == number_of_reviews_on_page:
                last_rating = items["rating"]
        
        #Se l'ultimo rating è minore a 4 allora la prossima pagina potrebbe offrire altre recensioni con voto basso
        if last_rating < 4:
            page_number+=1
            #Se sei alla prima pagina (page_number appena incrementato), aggiorna l'url in modo dedicato.
            if page_number == 2:
                next_page = current_url.replace('rating#content', f'rating&reviewPage={page_number}#content')
                yield response.follow(next_page, callback=self.parse_quandoo_restaurant)
            else:
                pattern = r'(reviewPage=)\d+'
                next_page = re.sub(pattern, f'reviewPage={page_number}', current_url)
                yield response.follow(next_page, callback=self.parse_quandoo_restaurant)
        
        