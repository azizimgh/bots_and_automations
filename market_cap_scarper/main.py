import requests
from bs4 import BeautifulSoup
import time

##########################

start_page = 1
end_page = 30  
export_file ="market_caps.txt"


#Thr file is opened in "add mode" this will not remove previous data
def write_to_file(line):
    with open(export_file,'a') as fl:
        fl.write(line +'\n')


def scrape_one_page(number):
    url =  "https://www.coingecko.com/en?page="+str(number)
    content = requests.get(url)
    soup = BeautifulSoup(content.content, 'html.parser')

    table = soup.find('table', {'class':'sort table mb-0 text-sm text-lg-normal table-scrollable'})
    lines_of_coins = table.find('tbody').findAll('tr')
    for title in lines_of_coins:
        try:

            elements_of_line = title.findAll('td')
            id = title.find('td', {'class':'table-number text-center text-xs'}).text.strip()
            name = title.find('a', {'class':'d-lg-none font-bold'}).text.strip()
            market_cap = title.find('td', {'class':'td-market_cap cap col-market cap-price text-right'}).find('span').text.strip()        
            print('    Page: ',number,'id:',id,'token: ', name ,'mkt cap: ',market_cap)
            write_to_file(",".join([id, name , market_cap]))

        except Exception as e :
            print('error: ', str(e))

def main():
    print("Market cap data scarpint has started")
    for i in range(start_page, end_page+1):
        print(" Page ",i)
        scrape_one_page(i)
        time.sleep(0.5)


main()