import json
import pandas as pd

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

            except ValueError:
                pass
        
        df = pd.DataFrame(data=data)
        df_to_csv = df.to_csv('data/tweets.csv', index=True)

        return pd.DataFrame(data=data)
    

DataAnalyzer = DataAnalyzer('data/tweets.json')
DataAnalyzer.create_dataframe()
