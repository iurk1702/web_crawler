import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_flipkart_laptops(urls, data_frame):
    cnt = 0
    for url in urls:    
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('div', {'class': '_2B099V'})
       # print(products)
       
       
       
      
        for product in products:
            try:
                
                
                
                
                
                name = product.find('a', {'class': 'IRpwTa'}).text.strip() if product.find('a', {'class': 'IRpwTa'}) else 'N/A'
                print(name)
                price = product.find('div', {'class': '_30jeq3'}).text.strip() if product.find('div', {'class': '_30jeq3'}) else 'N/A'
                print(price)
                rating = product.find('div', {'class': '_3LWZlK'}).text.strip() if product.find('div', {'class': '_3LWZlK'}) else 'N/A'
                print(rating)
                reviews = product.find('span', {'class': '_2_R_DZ'}).text.strip() if product.find('span', {'class': '_2_R_DZ'}) else 'N/A'
                print(reviews)
                sizes_ul = product.find('ul', {'class': '_1xgFaf'})
                sizes = [size.text.strip() for size in sizes_ul.find_all('li')]
                print(sizes)        
                
                data_frame = data_frame.append({
                    'Name': name,
                    'Price': price,
                    'Rating': rating,
                    'Reviews': reviews,
                    'Sizes': sizes
                }, ignore_index=True)
                #print(data_frame)
            except AttributeError:
                continue

        next_page = soup.find('a', {'class': '_1LKTO3'})
        if next_page is None:
            break
        
        next_page_url = 'https://www.flipkart.com' + next_page.get('href')
        scrape_flipkart_laptops([next_page_url], data_frame)
        
        cnt += 1
    
    print(f"Scraped {cnt} pages")
    return data_frame

urls = ['https://www.flipkart.com/search?q=uspa+polo+shirts']

df = pd.DataFrame(columns=['Name', 'Price', 'Rating', 'Reviews', 'Sizes'])
df = scrape_flipkart_laptops(urls, df)
df.to_excel('x.xlsx', index=False)
