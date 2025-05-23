# Sentiment-Analysis
This Streamlit application allows you to upload transcripts, display sentiment scores and filler ratios per turn, compute overall averages, and visualize trends in sentiment and filler word usage over time. 

# ----Features---- #
- Sentiment classification using HuggingFace Transformers
- Filler word detection using spaCy
- Visualizations of speaker sentiment and filler usage for individual speakers

# ---- Requirements---- #

streamlit---Recommended Version: >= 1.0.0
pandas
matplotlib---Recommended Version: >= 3.5
spaCy---Recommended Version: >= 3.0
transformers---Recommended Version: >= 4.0.0
torch
numpy---Recommended Version: >=1.21,<2.0


# ---- How to install---- #

pip install -r requirements.txt
streamlit run app.py
