# COVID Article Category Detection - Capstone Project

Welcome to my final capstone project! This project focuses on **automatically detecting and classifying COVID-related articles** using AI techniques like BERT, LDA, and more. It brings together multiple NLP and machine learning methods to understand and sort news/media content related to the pandemic.

---

## Project Files Overview

| File | Description |
|------|-------------|
| `200_samples.xlsx` | Sample dataset of 200 labeled COVID-related articles (used for training/testing). |
| `labels.xlsx` | Contains labeled categories for the articles, used in supervised learning. |
| `bert_implementation.py` | Fine-tunes BERT model for article classification tasks. |
| `lda_implementation.py` | Performs topic modeling using Latent Dirichlet Allocation (LDA). |
| `lc_gridsearch.py` | Uses Grid Search for hyperparameter tuning with Logistic Classifier. |
| `confidential_interval.py` | Calculates confidence intervals for model accuracy and performance. |
| `capstone.py` | Main script that ties everything together; orchestrates data loading, training, and evaluation. |

---

## Objective
To develop a machine learning pipeline that can:
- Detect whether a given article is related to COVID.
- Categorize COVID articles into relevant topics (e.g., health, economy, politics).
- Compare performance of classical ML methods (like LDA + Logistic Regression) vs deep learning (BERT).

---

## Techniques Used
- BERT (Bidirectional Encoder Representations from Transformers)
- LDA (Latent Dirichlet Allocation) for unsupervised topic modeling
- Logistic Regression with Grid Search
- Confidence Interval Analysis for statistical reliability

---

## Dataset
The dataset contains 200 labeled COVID articles, each tagged with a category such as:
- Healthcare
- Economic Impact
- Government Policy
- Social Effects

Note: Due to privacy or licensing reasons, the dataset is limited in size.

---

## How to Run
1. Clone the repository:
```bash
git clone https://github.com/Belle0602Xin/grad-695.git
cd grad-695
```

2. Install dependencies (Python 3.7 or later recommended):
```bash
pip install -r requirements.txt
```

3. Run main script:
```bash
python capstone.py
```

Optional: Run specific components individually:
```bash
python bert_implementation.py
python lda_implementation.py
```

---

## Output Examples
- Classification reports (accuracy, precision, recall)
- Topic clusters with keywords (from LDA)
- Confidence intervals for model reliability

---

## Future Improvements
- Use larger datasets for better generalization
- Integrate web scraping for real-time article input
- Build a simple web dashboard for live classification

---

## About Me
This is my final capstone project for my studies in software engineering and AI. I am passionate about using machine learning to solve real-world problems, especially in public health and social impact.

Feel free to fork, contribute, or ask questions.

---

## License
This project is for educational purposes only.

---

Made with dedication for my capstone project
