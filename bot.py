#commandline: python bot.py hashtag timeCap(in seconds)
import sys, tweepy, time #, xlsxwriter
from twython import TwythonStreamer

from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
#global variables:
searchHashTag = '#'+str(sys.argv[1])
timeCap = int(sys.argv[2])
# Create a workbook and add a worksheet with header labels
#workbook = xlsxwriter.Workbook('TwitterBot.xlsx')
#worksheet = workbook.add_worksheet()
#worksheet.write(0, 0, 'Hashtag: '+searchHashTag)
#worksheet.write(1, 0, 'Username')
#worksheet.write(1, 1, '# of followers')
#worksheet.write(1, 2, 'Tweet')
csv = open('TwitterBot.csv', 'w+')
csv.write('Search parameter: '+searchHashTag+'\n')
csv.write('User that used the hashtag, Number of followers\n')
class MyStreamer(TwythonStreamer):
    #workbook.close()
    #sys.exit()
    def on_success(self, data):
        # The first two rows are for the header labels and filled in manually below
        #row = 2
        for key in data:
            #user is the key for the meta-data that has the screen-name, follower count etc
            if key == 'user':
                userName = data[key]['screen_name']
            #worksheet.write(row, 0, userName) #column 0 is username
                followerCount = data[key]['followers_count']
            #worksheet.write(row, 1, followerCount) #column 1 is follower count
            #tweet = data['text']
            #worksheet.write(row, 2, tweet) #column 2 is the tweet with the hashtag
                csv.write(userName+', '+str(followerCount)+'\n')
                if time.time() - startTime > timeCap:
                    print('Time complete. Exiting now.')
                    csv.close()
                    sys.exit()
            #row+=1

stream = MyStreamer(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
startTime = time.time()
print('Bot will run for '+str(timeCap)+' seconds.')
print('Initiating filter based on the search parameter.')
stream.statuses.filter(track=searchHashTag)