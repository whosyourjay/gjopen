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
	"__cfduid": "d1888c96138eae27a3b3c457323ec288f1610236038",
	"_gj_prod_flyover_forecasts_session": "b8IRwtGO2Gc0/Mw9BvI79/fW57IuipxLZLtE3462S65fN0NVl4VQymDZRuajHMteiWzjYOkQJC0gCdihYYUmYenBY5p2nlTSjYvkX698AjnJKRHgONn40LiVUPDGtyMrmdeqjF89ojYZyRdtSY0uwp1tj8WG6Ki//KSRX1Dyt5SSD7Rs4JF1rFVp5xvY7Uw2ZAnZ2JYlxfpuoOOsHq5dQ/mROI4xhfX4293xCY/95m/DVj6nN/bGNWFMO3WvkYVegL7oS1IaaNDc28LBZwSKfkhZIsb1th42ktG/8tBUCekGa447bk40maZR3eA5pfWm5htqm98/7onhQw+2R+Ybv0AWvkIPohPlgHB1K2uV+BAm5ASMcFGO/ZTfZMS2Rq6RWy1WXiraGtIZnSOnCLHDF5QjpNY4inR5peoFgDscovrQaKeH8c8V139K/o0ZiSqVxkrAM2uGMIJwFoXf5JXE6nNZfrLGQm7+kaH+lzIJoz/Wxz1U0rGpkzrrTPHlb6zw/PsOv923ffq6Sl/KZtSYK5XDp4IeY5usnvziQekSlhzXfmqMLwGf2KoNxPkLEaDlmuY=--ocPXmjeheRJSyHgR--eQus5nXXqHCWxbh3CrFkUQ==",
	"landing_url": "https://www.gjopen.com/",
	"randomization_seed": "0.5925377311652286",
	"referring_url": "https://www.gjopen.com/",
	"remember_user_token": "eyJfcmFpbHMiOnsibWVzc2FnZSI6IlcxczVOalU1TWwwc0lpUXlZU1F4TUNSaU9FNUxNblk1Y3pJMVZFNHZTRkpzU2t0T2FtNTFNV0l3TVRobFlXSm1NMk16TW1OalpqaGlaR05qWkdVek1XSXdZakU0TUdFaUxDSXhOakV4T0RjMU5qQXlMamt4TWpRMU5EUWlYUT09IiwiZXhwIjoiMjAyMS0wMi0xMVQyMzoxMzoyMi45MTJaIiwicHVyIjoiY29va2llLnJlbWVtYmVyX3VzZXJfdG9rZW4ifX0=--dea30f02fae3b220bb36b762abcbd24d78c63303"
}
headers={'User-Agent':user_agent,
        'Cookie':cookies}

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

