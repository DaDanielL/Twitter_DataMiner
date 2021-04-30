# Twitter Data Miner

### This GUI is made to allow its users to stream tweets from Twitter within a few steps and perform sentiment analysis on the tweets they collect

Sentiment analysis help us determine the emotions and the opinions of the general public in order to gather insightful information. This application uses the Textblob library and a lexicon-based approach to sentiment analysis. In other words, the sentiment of the tweets will be determined based on a pre-defined, approximately 3000 word dictionary where each word is assigned a polarity, subjectivity, and intensity value. 

Polarity (a value ranging from -1 to 1) is the main determining factor of sentiment with -1 meaning most negative and 1 meaning most positive.

Subjectivity (as the name implies) define how subjective a word is. A 0 stands for most objective and a 1 stands for most subjective.

Intensity (a value ranging from 0 to 1) represents how much the word influences the other words around it. For example, 'not' has a intensity value of 1, a polarity value of -1 and can greatly reduce the polarity of neighboring words ('good' vs 'not good')

[Dictionary](https://github.com/sloria/TextBlob/blob/dev/textblob/en/en-sentiment.xml)

---

Getting Started:
1. [Install Python](https://www.python.org/downloads/)
2. [Download Source Code (zip)](https://github.com/DaDanielL/Twitter_DataMiner/releases)
3. Extract the folder from the zip file
4. Single click the address bar of the extracted folder in the file explorer and enter ```cmd``` to access the command prompt
5. Install all the required packages by entering ```pip install -r requirements.txt``` in the command prompt
6. Lastly, enter ```python main.py``` in the command prompt to run the program.

---

How To Use:

After running the program, you will be greeted by this screen:

![Main Screen](/demo/mainsc.PNG)

To stream tweets, click the circle underneath 'Collect Data' and you will come across this screen:

![Stream Screen 1](/demo/streamsc1.PNG)

Enter any keywords in the 'Keyword Filter' box. You will only collect tweets that contain any of the keywords you enter. Keywords may come in the forms of words, hashtags, url, @mentions, and more.

After entering your keywords and clicking the 'Start Stream' button, you will be asked to authorize the application with your Twitter account. In order to authorize the application, follow the instruction on the newly opened tab and enter the code here:

![Auth](/demo/authensc.PNG)

If the authentication is successful, you will see the following at the bottom right of the application:

![Auth Success](/demo/authsuccess.PNG)

After successfully authorizing the application, you can finally start streaming tweets :clap: :clap: !!

![Stream Screen 2](/demo/streamsc2.PNG)

Upon stoping the stream, you will be returned to the main menu screen, where you can click on 'Analyze Data' to view the sentiment data of the tweets
you just collected :clap: :clap: !!

![Graphs 1](/demo/graphs1.PNG)

The above are two wordclouds. The green wordcloud contains words with positive sentiments while the red wordcloud contains words with negative sentiment. The size of the words are determined by how often they are used in the set of tweets you collected.

![Graphs 2](/demo/graphs2.PNG)

The above is a line graph shows the trend in sentiment throughout the period of time you streamed your tweets. Red stands for negative and green stands for positive sentiments.
