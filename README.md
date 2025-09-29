# Themis Bias Detector 🏛️

Themis Bias Detector is a web application designed to analyze news articles for potential political bias.  
Named after **Themis**, the Greek goddess of justice, fairness, and balance, this tool leverages **machine learning** and **AI models** to evaluate article content and provide an easy-to-understand bias assessment.

---

## 🚀 Features
- **URL-based Analysis** → Enter a news article URL and receive an automated bias evaluation.  
- **Bias Breakdown** → Detects linguistic patterns, sentiment, and framing that may indicate bias.  
- **Weighted Bias Score** → Returns a confidence score classifying articles as *Unbiased*, *Somewhat Biased*, or *Biased*.  
- **Interactive Frontend** → Clean web interface built with Flask, and HTML/CSS,.  

---

## 🛠️ How It Works
1. Users submit a news article URL.  
2. The application scrapes and processes the article text.  
3. Text is passed through **two AI models** trained to detect bias.  
4. A **weighted algorithm** combines the outputs into a single bias confidence score.  
5. Results are displayed neatly on the web interface.  

---

## 📂 How To Run
1. git clone entire repo
2. Download .pth file from https://drive.google.com/file/d/1yhWb03_W1m_kJqnT0wfwLFT5_pkYD7HY/view?usp=sharing and put it in your folder
3. in bash terminal: ```source venv/bin/activate```
4. in bash terminal: ```pip install -r requirements.txt```
5. in bash terminal: ```python app.py```
6. in your internet explorer go to http://127.0.0.1:5000
