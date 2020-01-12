import tweepy  # imports the whole library so if you want "Stream" you must type tweepy.Stream... but if you import API from tweepy like below you don't need tweepy.API, just API()
from tweepy import API  # API is a tweepy class that provides methods like user_timeline
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import twitter_credentials
from googletrans import Translator

# # # # AUTHENTICATION INFORMATION # # # #

auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_KEY, twitter_credentials.ACCESS_SECRET)
api = API(auth)


# Function to take out retweets from tweet pool. Retweets + comments are still included but just the simple "retweet click"
def analyze_status(example_text):
    if 'RT' in example_text[0:8]:  # 0-->8 because " TEXT: RT Blah blah"
        return True
    else:
        return False


# # # # TWITTER STREAM LISTENER # # # #

#  Basic listener class that prints received tweets to stdout & writing it to a file (built in natural loop in tweepy (on_status keeps looping)
#  StreamListener - inherited class provides methods that we can directly override (on_status, on_data, on_error)

#  This class filters for no retweets (sans-comment), gets full text out of ALL tweets and tweet w/keyword replies/comments, takes away random blank spaces in tweets, writes to file.txt in uniform lines easy for data analysis, precautions for errors. Info from tweets: Text, Time, Follower count, User name

class TwitterListener(StreamListener):
    def on_status(self, status):  # class method that takes in parameter data - status (tweets)
        if not analyze_status(status.text):  # if not evaluates for true or false so basically "if false"
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text

            try:
                location = status.user.location
            except None:
                location = "None"

# translator = Translator()  # Class variable
# trans = translator.translate(text, dest='en')  # Object of the translator class - assigning values
# h = trans.text
# EVERYTHING WORKS PERFECTLY WITHOUT THIS CODE. CHANGE .join(text.split())) to h.split and figure out how to put this in without the 1 column error.
# Then apply the NLP layer on top of the text in the txt_analysis file

            try:
                with open('tweets.txt', 'a', encoding="utf-8") as tf:  # 'a' means append, because we want to continually add the tweets as they are streamed && Opens the file with built in function open(), and names the long open(location and append and encoding) as variable "tf"
                    tf.write(' TEXT: ' + (" ".join(text.split())) + '\n' + ' LOCN: ' + status.user.location + '\n' + ' SUBS: ' + str(status.user.followers_count) + '\n' + ' TIME: ' + str(status.created_at) + '\n' + ' JOIN: ' + str(status.user.created_at) + '\n' + ' USER: ' + status.user.screen_name + '\n')  # splits the text into a list of indivdual words and then joins each word in list with a space. - cuts out unnecessary tweet spaces
                    print('\n' + ' TEXT: ' + (" ".join(text.split())) + '\n' + ' LOCN: ' + location + '\n' + ' SUBS: ' + str(status.user.followers_count) + '\n' + ' TIME: ' + str(status.created_at) + '\n' + ' JOIN: ' + str(status.user.created_at) + '\n' + ' USER: ' + status.user.screen_name + '\n')  # Status gives all the tweet information so narrow it down to .text
                return True
            except BaseException as e:  # general exception line
                print("Custom - Error on_status: %s" % str(e))

#  %s is a format specifier %str is also a format specifier telling interpreter that the error print of 'e' will be string

    def on_error(self, status):
        if status == 420:
# Error code 420 is twitter saying that they want you to stop (rate limit) or you're kicked so just kill the connection return "False"
            return False
        print(status)


class TweetAnalyzer():
    def tweets_to_df(self, tweets):
        pass
# Can we import the other analysis script here and set a timer for the tweet stream so that when its over it immediately runs this analysis class?


if __name__ == '__main__':

    myStreamListener = TwitterListener()

    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener, tweet_mode='extended')  # this is an object... also: Use tweepy(library).Stream(function) because we didn't directly do: from tweepy import Stream

    myStream.filter(track=['Donald Trump'], is_async=['true'])  # Around 40 tweets/min
    # Baseball keywords: ['Baseball', 'MLB', 'Trades', 'Mike Trout', 'Major League Baseball']
    # Tech Keywords: ['Tech', 'IP', 'Technology', 'Samsung', 'Apple', 'Huawei', '5G', 'Phones', 'Smartphones']
    # Apple Keywords: ['Apple', 'iPhone', 'Macbook', 'iPad']
    # Middle East Keywords: ['Muslim', 'Arab', 'Middle East', 'Hijab']
    # print(twitter_client.get_user_timeline_tweets(1))  # Instantiate a client object from --> def get_user_timeline_tweets --> the method (function in a class) requires an argument (num_tweets) which is why we specify a number when we call that method

