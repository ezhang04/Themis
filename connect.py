from a import Model
from a2 import Model2
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

mapping = {
    "www.usatoday.com": ("h1.gnt_ar_hl", "p.gnt_ar_b_p"),
    "www.msnbc.com": ("h1.article-hero-headline__htag.lh-none-print.black-print", "p.body-graf"),
    "www.alternet.org": ("h1.headline.h1", "p"),
    "www.breitbart.com": ("h1", "p"),
    "www.huffpost.com": ("h1.headline", "p"),
    "www.foxnews.com": ("h1.headline.speakable", "p.speakable"),
}

def fetch_article(url, headline_selector, content_selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
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

    model1 = Model()
    model2 = Model2()

    if domain not in mapping:
        raise ValueError(f"Domain {domain} not supported.")

    n = 1
    headline, content = fetch_article(url, mapping[domain][0], mapping[domain][1])

    # Run headline
    biased1, unbiased1 = model1.predict(headline)
    biased2, unbiased2 = model2.predict(headline)
    max_bias_content = headline
    max_bias = max(biased1, biased2)

    # Run paragraphs
    for paragraph in content:
        n += 1
        p_biased1, p_unbiased1 = model1.predict(paragraph)
        biased1 += p_biased1
        unbiased1 += p_unbiased1

        p_biased2, p_unbiased2 = model2.predict(paragraph)
        biased2 += p_biased2
        unbiased2 += p_unbiased2
        if p_biased1 > max_bias or p_biased2 > max_bias:
            max_bias_content = paragraph

    results = {
        "domain": domain,
        "Weighted Bias Score": (biased1 / n) * .2 + (biased2 / n) * .8,
        "Weighted Unbiased Score": (unbiased1 / n) * .2 + (unbiased2 / n) * .8,
        "Most Biased Excerpt": max_bias_content
    }
    return results
