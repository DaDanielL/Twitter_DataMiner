import json
import pandas as pd
from textblob import TextBlob
import re

class DataAnalyzer():


    def __init__(self, file_path):
        self.file = open(file_path,'r')


    def create_dataframe(self):
        data = {
            'tweet' : [],
            'created_at': []
        }

        for line in self.file:
            try:
                tweet = json.loads(line)

                # if 'extended_tweet' is in the tweet
                try:
                    data['tweet'].append(tweet['extended_tweet']['full_text'])

                # if 'extended_tweet' does not exist in the tweet
                except KeyError:
                    data['tweet'].append(tweet['text'])

                data['created_at'].append(tweet['created_at'])

            except:
                pass
        
        self.df = pd.DataFrame(data=data)
    

    def sentiment_analysis(self):
        self.df['cleaned_tweet'] = self.df['tweet'].apply(self.cleanText)

        def getSubjectivity(text):
            return TextBlob(text).sentiment.subjectivity
        def getPolarity(text):
            return TextBlob(text).sentiment.polarity
        def getEval(val):
            if val > 0:
                return 'Positive'
            elif val < 0:
                return 'Negative'
            else:
                return 'Neutral'

        self.df['subjectivity'] = self.df['cleaned_tweet'].apply(getSubjectivity)
        self.df['polarity'] = self.df['cleaned_tweet'].apply(getPolarity)
        self.df['evaluation'] = self.df['polarity'].apply(getEval)
        
        
    

    def cleanText(self,text):
        text = re.sub(r'@[A-Za-z0-9_]+', '', text) # removes @ mentions
        text = re.sub(r'#', '', text) # removes #
        text = re.sub(r'RT','',text) # removes RT
        text = re.sub(r'https?:\/\/\S+', '', text) #removes hyper link
        text = re.sub(r'\:','',text)

        return text
    
