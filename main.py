################# ACCOUNT TO LISTEN TO and Slack TOKEN
acc_id = 000000 # Add the twitter account id - You can also opt for a list of accounts
token ="xoxb-"  # Your slack token


################
import tweepy
from tweepy import OAuthHandler
from tweepy import API
from config import  consumer_key ,consumer_secret ,access_token ,access_token_secret,g_daddy_key, g_daddy_sec
import requests
from slack import WebClient

slack_client = WebClient(token)



class goDaddy_handler:
    def __init__(self,key,sec):
        self._key=key
        self._sec =sec
        self._headers = {"Authorization": "sso-key {}:{}".format(self._key, self._sec)}

    def get_availabilt(self,domain):
        try:
            url = "https://api.godaddy.com/v1/domains/available"
            test = requests.get(url, params={'domain':domain}, headers=self._headers)
            available = test.json()['available']
            if available:
                return round(test.json()['price']/10**6,2)
            else:
                return 0
        except Exception as e:
            print('An error detectec, ',e)
            
    def send_tex(self,tex):
        try:
            response = slack_client.chat_postMessage(
                channel="C02EJ3WLG1X",
                text=tex )
        except Exception as e:
            # You will get a SlackApiError if "ok" is False
            print(e)
    def research_domain(self,domaine):
        temp =self.get_availabilt(domaine)
        if temp!=None:
            if temp  == 0:
                print('Domain not available ---',domaine,'---')
                self.send_tex('Domain not available ---'+domaine+'---')
            else:
                print()
                self.send_tex('Domain available and it price on GoDaddy is'+temp+' $')


# Twitter stream handler
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        words= status.text.split(' ')
        for elt in words:
            print('New word has been Tweeted ==>  ',elt)
            temp = elt.lower()
            myDaddy.send_tex('New word has been Tweeted ==>  '+elt)
            myDaddy.research_domain(temp+'.com')


def main():
    myDaddy = goDaddy_handler(g_daddy_key,g_daddy_sec)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    try:
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(follow=[str(acc_id)], is_async=False)

    except Exception as e:
        print('error catch',e)


main()
