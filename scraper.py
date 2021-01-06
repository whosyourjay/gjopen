import urllib.request
from bs4 import BeautifulSoup
import re
import sys
import threading

question = sys.argv[1]
guess_count = int(sys.argv[2])
boolean = sys.argv[3].lower() == 'true'
#parallel = sys.argv[4].lower() == 'true'
parallel = False

print("boolean question %s" % boolean)
print("parallel %s" % parallel)

url = 'https://www.gjopen.com/comments?id=junk&filters=&commentable_id=' \
    + question \
    + '&commentable_type=Forecast::Question&page='

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7' # Not sure we need this
headers={'User-Agent':user_agent}

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
