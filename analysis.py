# analysis.py
"""
Created on Thu May 22 23:27:02 2025
Description:Contains helper functions for:
            - Sentiment analysis using HuggingFace transformers
            - Filler word identification and ratio computation using spaCy

@author: Imara M Nazar
"""

from transformers import pipeline
import spacy 
from spacy.matcher import PhraseMatcher


#-------Sentiment Analysis------------#

# Initialize HuggingFace sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", device = -1)
def compute_sentiment(line):   
     sentiment_result = sentiment_pipeline(line)[0]
     label = sentiment_result["label"]
     score = sentiment_result["score"]
     return label, score
 

#-------Filler word Analysis------------#

# Load spaCy model only once
nlp = spacy.load("en_core_web_sm")

# Common filler phrases
filler_phrase =['like','um', 'basically', 'well', 'actually', 'I mean', 
              'just', 'so','uh', 'oh', 'okay', 'right', 'er','literally', 'totally','really', 'honestly','Ah', 'I guess', 
              'or something', 'at the end of the day', 'hmm', 'for sure', 'seriously','probably', 'similarly', 
              'absolutely', 'almost', 'definitely', 'yeah', 'you know', 'maybe']


        
def compute_filler_ratio(line):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    phrases = [nlp(filler_word) for filler_word in filler_phrase]
    matcher.add("fillersList", phrases)
    
    line_lower = nlp(line.lower())  # lower case processing
    matches = matcher(line_lower)
    matched_phrases = [line_lower[start:end].text for match_id, start, end in matches]
    
    #print(f"Line  {matched_phrases} | Count: {len(matched_phrases)}")    
    
    total_words = len([token for token in line_lower if token.is_alpha])
    filler_count = 0
    for match_id, start, end in matches:
           filler_count += end - start

    #Filler word ratio
    if total_words > 0:
        filler_ratio = filler_count / total_words
    else:
        filler_ratio = 0
    return filler_ratio, total_words, filler_count, matched_phrases


