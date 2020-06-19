import tweepy
import time

auth = tweepy.OAuthHandler("nBzN5fIGo7eIac2dXzxEkmJTf",
                           "QyRJWpA7sUwpXa3sMteB5RGXzHi6zEAdIHVUQAVeSOTTmnzEGH")
auth.set_access_token("1272918562403782661-HgpnGSh9kVARsqozKdFI3sjZ4Ozd8o",
                      "6zJNJanh4Y0SS8ffKjIJm28SShwu6J0ZqAUU5zYyGHDdq")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.me()

search = '100DaysOfCode'
nrTweets = 2000
n = 0
for tweet in tweepy.Cursor(api.search, search).items(nrTweets):
    try:

        tweet.favorite()
        tweet.retweet()
        n = n+1
        print('Tweet Liked', n)
        time.sleep(60)
        if n % 100 == 0:
            time.sleep(600)
    except tweepy.TweepError as e:
        print(e.reason)

    except StopIteration:
        break
