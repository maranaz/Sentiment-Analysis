# -*- coding: utf-8 -*-
"""
Created on Thu May 22 23:30:01 2025

Description:Streamlit application for:
                - Uploading transcripts
                - Displaying per turn sentiment scores, filler ratios, and overall averages.
                - Visulizing sentiment and filler word usage over time

@author: Imara M Nazar
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from analysis import compute_sentiment, compute_filler_ratio


# Page configuration
st.set_page_config(page_title="Sentiment Analysis Dashboard", layout="wide")

#APplication title
st.title("Sentiment Analysis Dashboard")
st.markdown("""
            This Streamlit application allows you to upload transcripts, display sentiment scores and filler ratios per turn,
            compute overall averages, and visualize trends in sentiment and filler word usage over time.""")

# File upload section
st.subheader("Upload Transcript")
uploaded_transcript = st.file_uploader("Choose a text file")

# Set global figure size and font
mpl.rcParams["figure.figsize"] = (5, 3) 
mpl.rcParams["axes.titlesize"] = 4
mpl.rcParams["axes.labelsize"] = 4
mpl.rcParams["xtick.labelsize"] = 3
mpl.rcParams["ytick.labelsize"] = 3
mpl.rcParams["legend.fontsize"] = 4

# Only proceed if a file is uploaded
if uploaded_transcript is not None:
    st.write("Transcript uploaded... ")
    # Read and decode the uploaded file
    transcript_file= uploaded_transcript.read().decode("utf-8")
    # Show raw text
    st.subheader("Transcript Preview")
    st.text(transcript_file)
    data =[]
    # Process lines and compute sentiment values to compute the average
    sentiment_overall = []
    # to compute the ovberall filler ratio
    totalwords_line = []
    filler_line = []
    overall_filler =[]
    #Add button to trigger sentiment analysis
    if st.button("Generate the Report"):
        with st.spinner("Generating the Report..."):
            pass  # Simulating work
            
            for dialog in transcript_file.splitlines():
                if ":" in dialog:
                    speaker, monolog = dialog.strip().split(":", 1)
                    line = monolog.strip()   
                    # Get sentiment stats
                    sentiment_label, sentiment_score = compute_sentiment(line)
                    # Convert to numeric sentiment value
                    sentiment_value = sentiment_score if sentiment_label == 'POSITIVE' else -sentiment_score
                    sentiment_overall.append(sentiment_value)
                    
                    # Get filler stats               
                    filler_ratio, total_words, filler_count, matched_phrases =  compute_filler_ratio(line)
                    totalwords_line.append(total_words)
                    filler_line.append(filler_count)
                    overall_filler.append(matched_phrases)
                    
                    # Store results
                    data.append({
                    "Speaker": speaker,
                    "Line": monolog,
                    "Sentiment Label": sentiment_label,
                    "Sentiment Score": round(sentiment_score, 3),                
                    "Total Words": total_words,
                    "Filler Words": filler_count,
                    "Filler Ratio": round(filler_ratio, 3)
                    })
                    
             # Convert results to DataFrame       
            df = pd.DataFrame(data)
            st.subheader("Analysis Report")
            st.markdown("""
                        This table shows the analysis results for each line of dialogue in a transcript. 
                        It includes the speaker's name, the exact line spoken, and the sentiment label assigned to that line.
                        It also displays the sentiment score, indicating how confidently the sentiment is expressed, along with the total number of words spoken, 
                        the number of filler words used, and the filler ratio, which represents the proportion of filler words to the total words in each line.""")
            st.dataframe(df, use_container_width=True)
            
            #Compute the Overall Metrics
            # Overall sentiment
            overall_sentiment_score = np.mean(sentiment_overall)
            if overall_sentiment_score>0:
                overall_sentiment_label= "Positive"
                emoji = "😊"
            elif overall_sentiment_score<0:
                overall_sentiment_label= "Negative"
                emoji = "😔"
            else:
                overall_sentiment_label= "Neutral"
                emoji = "😑"
                    
            # Overall filler ratio
            overall_filler_ratio = np.sum(filler_line) / np.sum(totalwords_line)
            
            st.subheader("Overall Analysis Results")
            st.markdown("""This section presents the overall metrics summarizing the sentiment and fluency of the entire transcript.
                        The Overall Sentiment indicates the general emotional tone—Positive, Negative, or Neutral—based on the average
                        of all sentiment scores. The Overall Sentiment Score quantifies this tone on a scale from -1 (very negative) to
                        1 (very positive), with values near 0 indicating neutrality. The Overall Filler Ratio measures speaking fluency
                        by calculating the proportion of filler words (like "um", "uh", "you know") to the total words in the transcript. 
                        A higher ratio suggests less fluent or more hesitant speech.""")
            
            # create a three coloum layout to display overall metrices
            col1, col2, col3 = st.columns(3)
    
            with col1:
                st.metric(
                    label="Overall Sentiment",
                    value=f"{overall_sentiment_label}{emoji}")
            with col2:
                st.metric(
                    label="Overall Sentiment Score",
                    value=f"{round(overall_sentiment_score,3)}",
                    help="Ranges from -1 (very negative) to 1 (very positive). Closer to 0 means neutral."
                    )
            with col3:
                st.metric(
                        label="Overall Filler Ratio",
                        value=f"{round(overall_filler_ratio,3)}",
                        help="This value ranges from 0 to 1 and represents the proportion of filler words in the transcript, calculated as: total filler words ÷ total words.")
           
            # Center the plot
            col4, col5 = st.columns(2)
            with col4:
                # Visualize the Speaker-wise Sentiment  Over Time
                st.subheader("Sentiment Variation Across Speakers Over Time")
                st.markdown(""" This plot displays sentiment score trends for each speaker over their respective turns in the conversation.
                            The x-axis represents the turn number, while the y-axis shows sentiment scores ranging from -1 to 1. A score 
                            of -1 indicates a strongly negative sentiment, +1 indicates a strongly positive sentiment, and 0 represents
                            a neutral tone.""" )
                
                fig, ax = plt.subplots()
                speakers = df['Speaker'].unique()
        
                for speaker in speakers:
                    subset = df[df['Speaker'] == speaker]
                    ax.plot(
                        subset.index,
                        [sentiment_overall[i] for i in subset.index],
                        label=speaker,
                        marker='o'
                    )
                
               
                ax.set_xlabel("Turn Number")
                ax.set_ylabel("Sentiment Score")
                ax.set_title("Sentiment Variation Across Speakers")
                ax.legend()
                plt.grid(True)
                plt.tight_layout()
                st.pyplot(fig)
            
            with col5:
                # Visualize the Speaker-wise Filler word usage  Over Time
                st.subheader("Filler words Across Speakers Over Time")
                st.markdown(""" This bar chart visualizes the total and filler word usage per speaking turn for each speaker. 
                            Each bar is divided into two segments: the bottom colored portion (blue or red) represents the
                            number of non-filler words, while the top black segment shows the number of filler words. 
                            The x-axis corresponds to turn numbers, and the y-axis represents the total word count. """ )
                
                # Define speaker-specific colors
                speaker_colors = {
                    speakers[0]: "blue",
                    speakers[1]: "red"
                }
                
                fig, ax = plt.subplots()
                x = np.arange(len(df))  # Turn numbers (0-indexed)
                
                for i, row in df.iterrows():
                    speaker = row["Speaker"]
                    total = row["Total Words"]
                    filler = row["Filler Words"]
                    non_filler = total - filler
                    base_color = speaker_colors.get(speaker, "gray")
                
                    ax.bar(i, non_filler, color=base_color, edgecolor='black')
                    ax.bar(i, filler, bottom=non_filler, color="black")
                
                ax.set_xticks(x)
                ax.set_xticklabels([str(i + 1) for i in x])  
                ax.set_xlabel("Turn Number")
                ax.set_ylabel("Word Count")
                ax.set_title("Filler and Total Word Count per Turn")
                
                handles = [
                    plt.Rectangle((0, 0), 1, 1, color="blue", label=speakers[0]),
                    plt.Rectangle((0, 0), 1, 1, color="red", label=speakers[1]),
                    plt.Rectangle((0, 0), 1, 1, color="black", label="Filler Words")
                ]
                ax.legend(handles=handles)
                plt.grid(True)
                plt.tight_layout()
                st.pyplot(fig)
            
