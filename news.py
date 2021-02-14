import requests
from bs4 import BeautifulSoup
import re
import sys
import threading

page_count = 15
min_guess = 30
new_guess_ratio = 1.3

#question = sys.argv[1]
parallel = False

print("parallel %s" % parallel)

url = 'https://www.gjopen.com/questions?page='

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7' # Not sure we need this

# May need to update every time
cookies = {
	"_gj_prod_flyover_forecasts_session": "BTUoxrMCoM060rAvVdtg/ycS8dR5/c2SHRHneQPWQijtCxz2qqLpADsiPmZ9lNDYlPSEaDrzHJMjb/uoYLsCbTzABjN6vPvzRtvW6s0Bc4MNLo0iuW5BPj75IrYnNpzY9xUwHMbirvdATcstQx2Em4Lbr0m+BKZXpjCTtg/MDpTaF3bkLR8Z/CUVRjinXOeMSAq7qD0+WmfHbK7K0jw03vTBLlG1WntjhpLgRDq17zJ+ZT4ZZeweWIy1T3M0goXuOAqvoL28t1fIISYtMVPhbzYUSbrdoqqaaHsHZZZEdmw6mCAEydCVxrU4Je2MQ723XkPFz30DzfkmBntb/9caD5b5qqxmppa2vsC7mtUYmulvqSvu3ciEgZg6FMAhSDwiOVVk5F7dMifDy2EJz+UQrSq5aJGYK5XYtHF2G//ikzYoYJi+f6NzPni9FlcpwLgWo6e+an4Fsgpz2uwYXGOW0B7w2rgBW4Ew9gSnJc2f05iL853nzRVUnfWNXm2YnkksidKYMhOqbgGdbFrwunFCWl1XsXapEA1e8Qsz+CL0C7dwXVdNnsToY1v0JVVwzP6wjQU=--kOuvgXr8qHMlFFVJ--20odr4uXq7pSI5ZgFBi5gw==",
}
headers={'User-Agent':user_agent,
'set-cookie': '_gj_prod_flyover_forecasts_session=u6%2BfVXLVDEq9wyYWIteOE7YdyrNvdUV8yyC%2FAR95Wc9AikTrS5r0ueDIr64nyKqkVSo%2BGzHx9z6FiDC3BZkmcKOCG1NOGRPuZ7URqlmuvfpJ1an6HoUSBDVkp0Jvxg9KkYTi3ocwCGq4Ql9V5kbAsVuDxRI317NlT9REN06BzrrzDp729qOIkbtlhN4iJDxATLI%2FcOsFBQVfo0g6DPVPuqn2eopg4ewiScbsb5ThyVYw3AAx3s1obg1JZ34JBjMVM50BL68kA6wV%2BPm1WkJ5giR441lh%2FKUIF7ObKQWl%2FPHPBNnojmGZ5%2Fod4H9SCJYbh9uA93W%2Fna0xq%2BpENOxfBGNWDrVFCK2EMeQnyyUBqPVYmpyU3HOeTUFgyFOuCOzugSM6PVhRmnabDr3zOqZT3X19hzGHXbQBhsKmvN6sLE0%2FVKZsPBJlOt01rIE7uz1YmsSoMhdktjP%2FK4FvUAzssLSq7F2nbpS1dT3%2FBggj2hV1HPLBbYy68cY%2BNTzWQkGq4g7rVdRuovHTW0%2Fj2kYKbn1O0t9b%2FlyKgRZnwRT8wL5MklKBeTxHugJU7V0zvk0Uh6w%3D--X3dO5IcRik%2Bkv8HT--zoRy8PxZiYQi2i%2FNVDRVxg%3D%3D; domain=.gjopen.com; path=/; secure; HttpOnly'}

def fetch_page(page):

    response = requests.get(url + str(page + 1), None, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    questions = soup.find_all(class_ = 'question')

    for question in soup.find_all(class_ = 'question'):
        name = question.get('id')[-4:]

        try:
            with open('gjo-' + name, 'r') as f:
                old_count = len(f.readlines(  ))
                new_count = int(re.search('\d+ Forecasts', question.text).group(0)[:-10])
                #print(f'question {name} had {old_count} now has {new_count}')
                if new_count > old_count * new_guess_ratio:
                    print(f'updates to {name}')
        
            f.close()
        # No file means new question
        except IOError:
            try:
                new_count = int(re.search('\d+ Forecasts', question.text).group(0)[:-10])
                if new_count > min_guess:
                    print(f'new question {name}')
            except AttributeError:
                pass


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

