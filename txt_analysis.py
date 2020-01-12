"""
RATING SYSTEM:
if subjectivity > 0.5:
    +10% weightage...
if subjectivity < -0.5
    + 5% weightage (Less beacause negative opinions contain more sentiment usually so it's biased to the negative aready.)
if tweet_likes > 100
    + 5% weightage

if retweet_count > 0:
    + 5% weight of user (more important/more influential tweet)
elif retweet_count > 100
    + 15% weight
"""

import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from geopy.geocoders import Nominatim
import folium
from nltk.sentiment.vader import SentimentIntensityAnalyzer


text = []
location = []
followers = []
time = []
join_date = []
user = []
sentiment = []


# we can use starts with because it is a read string from the file. didn't add to a list beforehand.. could also use .contains function for sorting string.__contains__()

with open('tweets.txt', 'r', encoding='UTF-8') as file:
    for line in file:
        if line.startswith(' TEXT: '):
            text.append(line.replace(' TEXT: ', '').replace('\n', ''))
        elif line.startswith(' LOCN: '):
            location.append(line.replace(' LOCN: ', '').replace('\n', ''))
        elif line.startswith(' SUBS: '):
            followers.append(line.replace(' SUBS: ', '').replace('\n', ''))
        elif line.startswith(' TIME: '):
            time.append(line.replace(' TIME: ', '').replace('\n', ''))
        elif line.startswith(' JOIN: '):
            join_date.append(line.replace(' JOIN: ', '').replace('\n', ''))
        elif line.startswith(' USER: '):
            user.append(line.replace(' USER: ', '').replace('\n', ''))
        else:
            print("Empty Line")


# # # # SENTIMENT ANALYSIS # # # #

subjectivity = []

for line in text:
# Class from the Vader lexicon library that outputs a dictionary of pos,neg,neu,and compound the avg of all of them
    a = SentimentIntensityAnalyzer().polarity_scores(line)
    b = TextBlob(line).sentiment.subjectivity
    sentiment.append(a['compound'])
    subjectivity.append(b)

# Getting subjectivity from TextBlob analysis to allow better analysis... subjectivity means opinion and only opinion will be considered in sentiment analysis.
# See text analysis and tests between IBM Watson, Vader Lexicon and TextBlob


# Use TextBlob subjectivty to organize still, but use vader lexicon to analyze sentiment... see sentiment score with only textblob vs with half textblob and half vader lexicon.
# Vader Sentiment Analysis works better for with texts from social media and in general as well. It is based on lexicons of sentiment-related words. Each words in the lexicon is rated whether it is positive or negative.
# When it comes to analysing comments or text from social media, the sentiment of the sentence changes based on the emoticons. Vader takes this into account along with slang, capitalization etc and hence a better option when it comes to tweets analysis and their sentiments.




# # # # DATA FRAME CREATION - CONCAT AND DATA ALLOCATION + STATS ABOUT SENTIMENT # # # #
df_text = pd.DataFrame(data=text, columns=['TWEETS'])
df_locn = pd.DataFrame(data=location, columns=['LOCATION'])
df_subs = pd.DataFrame(data=followers, columns=['FOLLOWERS'])
df_time = pd.DataFrame(data=time, columns=['TIME'])
df_join = pd.DataFrame(data=join_date, columns=['JOIN DATE'])
df_user = pd.DataFrame(data=user, columns=['USER'])
df_sent = pd.DataFrame(data=sentiment, columns=['SENTIMENT'])
df_subj = pd.DataFrame(data=subjectivity, columns=['SUBJECTIVITY'])

frames = [df_text, df_locn, df_subs, df_time, df_join, df_user, df_sent, df_subj]
df_result = pd.concat(frames, axis=1, sort=False)

# Filtering for all tweets with subjectivity = 0 (deleting and creating a new DF because those tweets produce no sentiment..) Objectivity is fact, so no sentiment/opinion goes with that


df_filtered = (df_result.loc[df_result['SUBJECTIVITY'] > 0.000001].reset_index(drop=True))  # ensures that only tweets with subjectivity - meaning opinion based tweets can pass through (subjectivity must be > 0).. exact number because some values had just 0.000001 below this value
print(df_filtered)


print('\n' + str(df_sent.describe()))


subjectivity_filtered_list = df_filtered["SUBJECTIVITY"].tolist()  # Column of the non-zero subjectivity from the new filtered dataframe
sentiment_filtered_list = df_filtered["SENTIMENT"].tolist()  # Column from the new data frame (with only subjectivity above 0 included - df_filtered) conversion --> to list.


# # # # CLASSIFYING SENTIMENT INTO 3 CATEGORIES & CREATING PIE CHART # # # #

pos = 0
neg = 0
neu = 0

for o in sentiment_filtered_list:
    if o > 0:
        pos += 1
    elif o < 0:
        neg += 1
    else:
        neu += 1

labels = ['Positive', 'Negative', 'Neutral']
sizes = [pos, neg, neu]
fig1, ax = plt.subplots()
ax.set_title('Overall Sentiment Dispersion')
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()


# # # # LOCATION TO COORDINATES CONVERSION AND THEN MAPPING BASED ON SENTIMENT AND LOCATION # # # #

def loc_to_coord(x):
    locator = Nominatim(user_agent="twitter_bot", timeout=10000000)
    location = locator.geocode(x)
    return location.latitude, location.longitude


location_filtered_list = df_filtered["LOCATION"].tolist()
# Column from the new data frame (with only subjectivity above 0 included - df_filtered) conversion --> to list.

map = folium.Map(location=[44.052085, -33.062728], zoom_start=3)

count = 0

for p in location_filtered_list:
    try:
        s = sentiment_filtered_list[count]  # returns a number
        count += 1  # increment count for the next iteration

        if s > 0:
            folium.Marker(location=loc_to_coord(p), popup=p, icon=folium.Icon(icon='twitter', color='blue', prefix='fa')).add_to(map)
        elif s < 0:
            folium.Marker(location=loc_to_coord(p), popup=p, icon=folium.Icon(icon='twitter', color='red', prefix='fa')).add_to(map)
        else:
            folium.Marker(location=loc_to_coord(p), popup=p, icon=folium.Icon(icon='twitter', color='lightgray', prefix='fa')).add_to(map)
    except AttributeError:
        continue

map.save('index.html')

# if TextBlob(line).detect_language() != 'en':
#     line = TextBlob(line).translate(to='en')

# Filter out 0's - don't want neutral sentiment?
# sentiment = filter(lambda goo: goo != 0.0, sentiment)
# print(sentiment)


# add function in the end after you get dataframe to print full data needed to write: ' blank space ' in the .txt so it doesn't buildup data in two spots

# df.describe() <== find mean, standard deviations etc.
# df.sort_values('column', ascending=False)
# Different functions and usages with data analysis - https://www.youtube.com/watch?v=e60ItwlZTKM


