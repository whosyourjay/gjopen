import urllib.request
from bs4 import BeautifulSoup
import re
import sys
import threading

question = sys.argv[1]
guess_count = int(sys.argv[2])
boolean = sys.argv[3] == 'True'
parallel = sys.argv[4] == 'True'

print("boolean question %s" % boolean)
print("parallel %s" % parallel)

url = 'https://www.gjopen.com/comments?id=junk&filters=&commentable_id=' \
    + question \
    + '&commentable_type=Forecast::Question&page='

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7' # Not sure we need this
cfduid = 'd8e9b00b9078960925c6921dfc5812f5a1607637346'
flyover = 'iXu2f3vHotIzTgRhtGgRmmXdgQ//CiHTBrY6FAncK7RnJG7dRcQh1S/1oapuPAJqdTx1DAvFix4pigoSsbK3kupjaY593n1jNuccD1YVoQTsk3tz2HyDdOBqeAaD6+bblcrFuslM+ZWFWO8RGavPPawGm0WkKbuoQdWHWTey2iiILbOV6dYAspOR7adsuzD8vetXmy61bR5rL2jHik0qIOkzweesIRek7xr17KRWWuGE5DAu17TXhvneES2L44aVeq9RVxFQs4cJ1qQqrmo7v8cMdGfLtFCJ5S6iV/glflqipu6C66df9LmNPKxxZhIw4LlONxNx3Ss7usrzTuwznsgLrXUzwuuTKgg5th5BoJJB6HXZmwZ0wHMJ5AIB13J9db8B2P48NnE8Y4ISogV3agkQqG68AraV8lNVqW7MbnksBugqD8JfzuoUTll0QcOijSsOP9voQZSOHkHRMWnx7FDLnm91vbCqCKp6Wku/yvTAeoYK4kQ8BdWLWKp2K6UEWcuJBYFkpj8IpoCTeg27Jh01+8JXz9tQQPgKyBFHrjMnrDKvBQJobscsEi93gKeax3I=--qI9m2g9uk+sEbM+C--VeHD16MgEtkxLObbhqMb7g=='
cookie = '__cfduid =' + cfduid \
    + '; _gj_prod_flyover_forecasts_session =' + flyover
headers={'User-Agent':user_agent,
        'Cookie':cookie}

page_count = (guess_count + 9)//10 # Round up
guesses = [[] for _ in range(page_count)]
def fetch_page(page):

    request = urllib.request.Request(url + str(page + 1), None, headers)
    response = urllib.request.urlopen(request)
    data = response.read().decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')

    if soup.find(class_ = 'empty-text'):
        print("empty page")
        return []

    for guess in soup.find_all(class_ = 'prediction-set-info'):
        user = guess.find(class_ = 'membership-username').text
        # Toss the header row
        vals = guess.find_all(class_ = 'row-condensed')[1:]

        percents = []
        for val in vals:
            # Grab the first number
            percents.append(int(re.search('\d+', val.text).group(0)))
        if boolean:
            percents.append(100 - percents[0])
        
        guesses[page].append((user, tuple(percents)))

    print("page %d done" % page)

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

# Flatten
guesses = [item for page in guesses for item in page]
guesses.reverse()
# Discard extras on last page
# Todo Smarter merge
guesses = guesses[-guess_count:]

with open('gjo-' + question, 'a') as f:
    for user, vals in guesses:
        f.write("%s %s\n" % (user, ' '.join(map(str, vals))))

f.close()
