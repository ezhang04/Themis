from a import Model
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

mapping = {"www.usatoday.com": ("h1.gnt_ar_hl", "p.gnt_ar_b_p"),
           "www.msnbc.com": ("h1.article-hero-headline__htag.lh-none-print.black-print", "p.body-graf"),
           "www.alternet.org": ("h1.headline.h1", "p"),
           "www.breitbart.com": ("h1", "p"),
           "www.huffpost.com": ("h1.headline", "p"),
           "www.foxnews.com": ("h1.headline.speakable", "p.speakable")}

def fetch_article(url, headline_selector, content_selector):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    headline = soup.select_one(headline_selector)
    if not headline:
        raise ValueError(f"Headline not found with selector: {headline_selector}")
    headline = headline.get_text(strip=True)

    content_els = soup.select(content_selector)
    if not content_els:
        raise ValueError(f"Content not found with selector: {content_selector}")
    content = [p.get_text(strip=True) for p in content_els]
    
    return headline, content

def predict_from_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    model = Model()
    if domain in mapping:
        print(domain,mapping[domain][0],mapping[domain][1])
        headline, content = fetch_article(
            url,
            mapping[domain][0],
            mapping[domain][1]
        )
        print("Headline:", headline)
        print("Content:", content[0])
        # gets bias & unbiased score from headline
        biased, unbiased = model.predict(headline)
        print(f"Headline Bias Scores - Biased: {biased}, Unbiased: {unbiased}")
        for paragraph in content:
            p_biased, p_unbiased = model.predict(paragraph)
            print(f"Content Bias Scores - Biased: {p_biased}, Unbiased: {p_unbiased}")
    else:
        raise ValueError(f"Domain {domain} not supported.")

predict_from_url("https://www.usatoday.com/story/news/politics/2025/09/27/trump-troops-portland-ice/86390814007/")