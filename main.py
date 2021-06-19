import bs4
from bs4 import BeautifulSoup
import requests
import json



url = 'https://www.midsouthshooterssupply.com'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}

productlinks = []
for x in range(1,3):
  r = requests.get('https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage={x}',headers=headers)
 
  soup = BeautifulSoup(r.content,'lxml')
  productlist = soup.find_all('div',attrs={"class":"product","id":"Div1"})

  for item in productlist:
      for link in item.find_all('a',attrs={"class":"catalog-item-name","href":True}):
          productlinks.append(url + link['href'])


product_info = []

for link in productlinks:
  r = requests.get(link,headers=headers)
 
  soup = BeautifulSoup(r.content,'lxml')
 
  title = soup.find('h1',class_='product-name').text.strip()
  price = soup.find('span',class_='price').text.strip()
  floatPrice = float(price.replace("$",""))
  status = soup.find('span',class_='out-of-stock').text.strip()
  if status == "in-stock":
      stock=(bool(True))
  else:
        stock=(bool())
     


  for div in soup.findAll('div', attrs={'class':'catalog-item-brand-item-number'}):
      manufacturer = (div.find('a').contents[0])
     
  pro_info = {'product-title': title,
              'manufacturer' : manufacturer,
              'price($)' : floatPrice,
              'status of product(stock)': stock
                      }
  product_info.append(pro_info)


print(json.dumps(product_info, indent=2))
