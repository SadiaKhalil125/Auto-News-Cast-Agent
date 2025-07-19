import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from nodes.newsstate import NewsState
# nltk.download('punkt')
# nltk.download('stopwords')


def get_headlines_bbc():
    url = 'https://www.bbc.com/news'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    # Try to extract headlines
    
    headlines = []
    for single_line in soup.find_all('a'):
        text = single_line.get_text(strip=True)
        if text and len(text.strip()) > 4:
            headlines.append(text.strip())

    return list(set(headlines))



def get_headlines_cnn():
    url = 'https://edition.cnn.com/world'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    headlines = [span.text.strip() for span in soup.find_all('a')]
    return list(set([h for h in headlines if len(h.split()) > 4]))


def get_headlines_aljazeera():
    url = 'https://www.aljazeera.com/news/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    headlines = [a.text.strip() for a in soup.find_all('a')]
    return list(set([h for h in headlines if len(h.split()) > 4]))

# Normalize and tokenize
# def clean_and_tokenize(text):
#     stop_words = set(stopwords.words('english'))
#     tokens = word_tokenize(text.lower())
#     return [w for w in tokens if w.isalnum() and w not in stop_words]

# Simple similarity based on token overlap
# def is_similar(headline1, headline2):
#     tokens1 = set(clean_and_tokenize(headline1))
#     tokens2 = set(clean_and_tokenize(headline2))
#     return len(tokens1 & tokens2) >= 3  # At least 3 common words

# Find common news topics
# def find_common_headlines(all_headlines):
#     common = []
#     for h1 in all_headlines[0]:
#         for h2 in all_headlines[1]:
#             if is_similar(h1, h2):
#                 for h3 in all_headlines[2]:
#                     if is_similar(h1, h3):
#                         common.append(h1)
#     return list(set(common))

def scrape_and_return(state:NewsState):

    bbc = get_headlines_bbc()
    cnn = get_headlines_cnn()
    aljazeera = get_headlines_aljazeera()
    
    return {'bbc_headlines': bbc,
            'cnn_headlines': cnn,
            'al_jazeera_headlines': aljazeera,}

