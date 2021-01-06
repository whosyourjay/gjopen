import urllib.request
from bs4 import BeautifulSoup
import re
import sys
import threading

page_count = 12
new_guess_ratio = 1.2

#question = sys.argv[1]
parallel = False

print("parallel %s" % parallel)

url = 'https://www.gjopen.com/questions?page='

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7' # Not sure we need this

# May need to update every time
cookie = 'referring_url=https%3A%2F%2Fwww.gjopen.com%2F; landing_url=https%3A%2F%2Fwww.gjopen.com%2F; __cfduid=d8e9b00b9078960925c6921dfc5812f5a1607637346; _gj_prod_flyover_forecasts_session=vP%2FxpDiKh8Z3ah7IIqHIojSdXzvwpP5eluxe1yXBvve%2FK028TqNJHI%2F8%2BBC8VCgG5hF1y%2FpsPl%2BGGnMGapSPD2jkazMl4bxJvAmsiTYM%2FX5BYheBNgNxb38CTSLoDkOSCNSZvFQfWsUIyPU29l3nQg5Bl4BYWs9E4fKTyEJdjzsYiLeGZz7KeOuvRArawwAexSkxvBDZBUfWqOFdnPVoLynEGpo3%2FTdrVbrdmPcXbLP73n4nB77M8tbLqFl61EwWhV6VGyn8NTumi44rovybYzHn3OIJe0ixECBMg8sIdor8nH6Vh7Ll8LnK%2F3KHTdjlGPusHt3liyYEsug%2FqmzrGAWVwtigbvg4MOMX1xddsnwVnp3pv4Un0iy0WsT8iG5obUCoOBBi4mlaRnLwWehFMV1r1FHXO2nn4pl%2FHZ4cdNShSTP0%2FoTh%2BXjiyosqs2YdAIGcbiVOmMyZ6gGPLL5E4mMSrvX%2FCskTzv8OMs%2FEv2%2BxwVoRW6r5ZqsT1s6EOgv3EbAPZ%2BbMaBEqD7cI%2FX1UJz%2BKIE7QMX%2ByfZzRMA00c1nKbsre66LWtUSxIXUoyEqCOIM%3D--rj98lvmCw06H1PCa--67SqXu1LlToa%2B3Sv9gyJJQ%3D%3D; randomization_seed=0.28373514239737885'
headers={'User-Agent':user_agent,
        'Cookie':cookie}

def fetch_page(page):

    request = urllib.request.Request(url + str(page + 1), None, headers)
    response = urllib.request.urlopen(request)
    data = response.read().decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')

    questions = soup.find_all(class_ = 'question')

    for question in soup.find_all(class_ = 'question'):
        name = question.get('id')[-4:]

        try:
            with open('gjo-' + name, 'r') as f:
                old_count = len(f.readlines(  ))
                new_count = int(re.search('\d+ Forecasts', question.text).group(0)[:-10])
                if new_count > old_count * new_guess_ratio:
                    print(f'updates to {name}')
        
        # No file means new question
        except IOError:
            print(f'new question {name}')

        f.close()

    print(f'page {page} done')

if parallel:
    threads = [threading.Thread(target=fetch_page, args=(page,))
        for page in range(page_count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
else:
    for page in range(page_count):
        fetch_page(page)

