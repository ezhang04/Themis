from a import Model
from a2 import Model2
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
    model2 = Model2()
    if domain in mapping:
        n = 1
        headline, content = fetch_article(
            url,
            mapping[domain][0],
            mapping[domain][1]
        )
        biased, unbiased = model.predict(headline)
        biased2, unbiased2 = model2.predict(headline)
        for paragraph in content:
            n += 1
            p_biased, p_unbiased = model.predict(paragraph)
            biased += p_biased
            unbiased += p_unbiased

            p_biased2, p_unbiased2 = model2.predict(paragraph)
            biased2 += p_biased2
            unbiased2 += p_unbiased2
        biased /= n
        unbiased /= n

        biased2 /= n
        unbiased2 /= n


        print(f"Overall Model 1 Bias Scores - Biased: {biased}, Unbiased: {unbiased}")
        print(f"Overall Model 2 Bias Scores - Biased: {biased2}, Unbiased: {unbiased2}")
        print(f"Overall Bias Scores - Avg Bias: {(biased2 + biased) / 2}, Avg Unbiased: {(unbiased2 + unbiased) / 2}")
        print(f"Overall Bias Scores - Wegihted Bias: {biased2 * .8 + biased * .2}, Avg Unbiased: {unbiased2 *.8 + unbiased *.2}")
        print("-----------------------------------------------------")

    else:
        raise ValueError(f"Domain {domain} not supported.")

predict_from_url("https://www.usatoday.com/story/news/politics/2025/09/27/trump-troops-portland-ice/86390814007/")
predict_from_url("https://www.foxnews.com/politics/obama-center-deposits-just-1m-into-470m-reserve-fund-aimed-to-protect-taxpayers-fueling-new-criticism")
predict_from_url("https://www.msnbc.com/news/news-analysis/democrats-shutdown-trump-rescissions-spending-rcna233554")
predict_from_url("https://www.alternet.org/trump-james-comey-halligan/")
predict_from_url("https://www.breitbart.com/politics/2025/09/27/newsom-attacks-stephen-miller-calls-him-a-fascist/")
predict_from_url("https://www.huffpost.com/entry/united-states-revokes-visa-for-colombias-president-after-he-urges-american-soldiers-to-disobey-trump_n_68d7e7e4e4b085d511c6e2d9?origin=home-latest-news-unit")