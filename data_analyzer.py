import json
import pandas as pd
from textblob import TextBlob
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image
import numpy as np
import seaborn as sns

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
        self.df['cleaned_tweet'] = self.df['tweet'].apply(self.clean_text)

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
        

    def clean_text(self,text):
        text = re.sub(r'@[A-Za-z0-9_]+', '', text) # removes @ mentions
        text = re.sub(r'#', '', text) # removes #
        text = re.sub(r'RT','',text) # removes RT
        text = re.sub(r'https?:\/\/\S+', '', text) #removes hyper link
        text = re.sub(r'\:','',text)

        return text

    def create_graphs(self):
        #wordcloud
        self.create_wc()
        #piechart
        self.create_pie()
        #timechart    
        self.create_line()

    def create_wc(self):
        posdf = self.df[self.df.polarity > 0]
        negdf = self.df[self.df.polarity < 0]

        posword = ' '.join([tweets for tweets in posdf['tweet']])
        negword = ' '.join([tweets for tweets in negdf['tweet']])

        stopwords = list(STOPWORDS) + ['RT','co','https']

        custom_mask_smile = np.array(Image.open('img/smile.png'))
        custom_mask_sad = np.array(Image.open('img/sad.png'))

        pos_wordcloud = WordCloud(width=600, height=600,random_state=5, # random_state related to color
                            stopwords=stopwords, font_path='font/WhitneyBold.ttf',mask=custom_mask_smile,
                            colormap = 'Greens',mode='RGBA',background_color=None, min_word_length=2)
        neg_wordcloud = WordCloud(width=600, height=600,random_state=5, # random_state related to color
                            stopwords=stopwords, font_path='font/WhitneyBold.ttf',mask=custom_mask_sad,
                            colormap = 'Reds',mode='RGBA',background_color=None, min_word_length=2)

        pos_wordcloud.generate(posword)
        neg_wordcloud.generate(negword)

        wc1 = plt.imshow(pos_wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('graphs/pos.png',transparent=True)
        plt.clf()

        wc2 = plt.imshow(neg_wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('graphs/neg.png',transparent=True)
        plt.clf()


    def create_pie(self):
        posTweets = self.df[self.df.polarity > 0]
        negTweets = self.df[self.df.polarity < 0]
        neuTweets = self.df[self.df.polarity == 0]

        val = [posTweets.shape[0],negTweets.shape[0],neuTweets.shape[0]]

        plt.figure(figsize=(8,8))
        plt.pie(val,colors=['#2eb82e','#ee412b','#efe8b5'],labels=['Positive','Negative','Neutral'],
                autopct = lambda p: '{:.0f}%'.format(p), shadow=True, explode=[0.02,0.04,0.015],
                textprops={'color': '#ffffff', 'weight':'bold'})
        plt.title('Sentiment Percentages', fontdict={'color':'#ffffff'})

        plt.savefig('graphs/pie.png',transparent=True)
        plt.clf()

    
    def create_line(self):
        sns.set(style='darkgrid',)
        full_data = self.df['polarity']
        num_points = 200
        n = int(len(full_data)/num_points)

        all_time = self.df['created_at']
        start = all_time[0].split()
        middle = all_time[len(all_time)//2].split()
        end = all_time[len(all_time)-1].split()

        data = []

        for i in range(num_points):
            x = full_data[i*n:(i+1)*n]
            data.append(sum(x)/n)

        ax = sns.lineplot(data=data)
        ax.set_xticks([0,num_points/2, num_points])
        ax.set_xticklabels([f'{start[1]} {start[2]} {start[5]} at {start[3]}',
                            f'{middle[1]} {middle[2]} {middle[5]} at {middle[3]}',
                            f'{end[1]} {end[2]} {end[5]} at {end[3]}'])
        ax.tick_params(axis='x', colors="white")

        ax.set_ylabel = 'Sentiment Value'
        ax.tick_params(axis='y', colors="white")
        plt.ylim(-1,1)

        plt.axhline(y=0, color = '#808080', linestyle=':', linewidth=4)
        plt.savefig('graphs/line.png', transparent=True)



Dm = DataAnalyzer('data/tweets.json')
Dm.create_dataframe()
Dm.sentiment_analysis()
Dm.create_graphs()
    