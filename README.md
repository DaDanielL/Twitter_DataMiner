# Twitter Data Miner

### This GUI is made to allow its users to stream tweets from Twitter within a few steps and perform sentiment analysis on the tweets they collect

---

Getting Started:
1. [Install Python](https://www.python.org/downloads/)
2. [Download Files](https://github.com/DaDanielL/Twitter_DataMiner/releases)
3. Single-click the address bar of the folder in file explorer and type 'cmd' to access the command prompt
4. Install all the required packages by entering ```pip install -r requirements.txt```
5. Lastly, enter ```python main.py``` to run the program.

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
![Graphs 2](/demo/graphs2.PNG)
