#!/usr/bin/env PYTHONIOENCODING=UTF-8 /Users/lstein2/anaconda3/bin/python3

# <bitbar.title>Today's Tweets</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Luke C.D. Stein</bitbar.author>
# <bitbar.author.github>lukestein</bitbar.author.github>
# <bitbar.desc>Display the tweets you've posted today.</bitbar.desc>
# <bitbar.image>http://www.hosted-somewhere/pluginimage</bitbar.image>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/lukestein/bitbar_todays_tweets</bitbar.abouturl>

# See advice at
# https://github.com/matryer/bitbar#writing-plugins
# http://docs.tweepy.org/en/v3.8.0/api.html
# https://www.iconfinder.com/
# https://onlinepngtools.com/convert-png-to-base64

import tweepy
import datetime
import pytz


# %% Twitter API keys
consumer_key        = "KEY"
consumer_secret     = "SECRET"
access_token        = "TOKEN"
access_token_secret = "TOKENSECRET"


# %% Setup

def is_reply(t):
    return (t.in_reply_to_screen_name != None) and (t.in_reply_to_screen_name != screen_name)

twitterlogo = "iVBORw0KGgoAAAANSUhEUgAAACQAAAAkCAYAAADhAJiYAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAArBJREFUWAntlT9rFUEUxV+MkQTFtCIJpE1npUhKJQoWImlThAREK7HwKwhWgn4KEW2sLNKmsBDBT6CWNnbmf3J+++5ZZ5/zdtaImGIvnJ07d+6fs3dmdicGg8GRcGrkzKlhEkR6QqUd6TvUd6jUgdL62ZJDrPOtmujgux8+nM3DiJkMnRzorUKR0ofRZFwgRwwfkLske7JPCYhzDWeZZy5B6uYEJMXXhXM+rL8R7gpLwprwUYDMd+GVkHsZmZviIrkRIthXhaehY7OdNbaJ8bEwKhyJFeGC8EjA70Cg2+g5ZI04Ooji8wLyTHASiPyM+XuNCAToCGfF2yS1kmt6fhaI90s4VzrWBVIjugltS58TLDelsBWp/8NYHCXBFtn2MmLayJCzkTgtgu6tWcdRMj0cqucNPZ8LvPWdyvL7LfItfqJ18u3GOFqnnjsg8jUGnLy+KJ1DS7ewcQ42Axrqw4o9FR/ihdRY0mt2ckx1b9mO7JcjiQswhRiA6Djxd4fbR253PK3T0NuSUZz9PifcExB3DJ01APGcEE/HIHUlHNrqhUuzKw228iAhth/CVQFJuzS05J/uznUtk4Nc7vponXpeYsw6bZ4VNgSkFDP0+uX3IAwQ6vQyNTsF5HRf03eu1CGxrzpbRU46U+xO+GZJpMRIxO3C9kJwh8a9bXrOPkWcXyrNO05vJZR7Kz6K8wKSkkLnAljeSqFo8dsTfhVBkqDkBDJ045uwGQ4fNPKb+BJz4p2DLiAXhdfCssD58/ZJ7SbjWschZO2rcKtDqhn53Bf4sxP3R52JmCO/neZZcZdYhBjd2RLoEOfqvLAgLAm3hUsCQrfSs1QZuzxKhMgBKdClAETYZnAi6ULIiSHlbwlxjsWO/ldEFF+Jk3r+38cTt/ZfMe8JlTrbd6jvUKkDpfVjvG0sZ2IOUeYAAAAASUVORK5CYII="

tweetlogo = "iVBORw0KGgoAAAANSUhEUgAAACQAAAAkCAYAAADhAJiYAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAA8JJREFUWAntl7trVEEUxtdXfKJBxEchKAmijQixEAQTEbEUtdI0NopYaKFgk0ow/gEiKhamsLETrMQmpFBEkIho6QqCoOATxffj++2db5l73bm7N5vCIge+PWfmnsd3zszdTWq1GZmZQHcTmNVdeDKavHME5/8tG/wRKouTVA4MAXNLAuNn1InXjbBU8dl6SkdVxLmYwmJhh9AvkOepMCH8Ekzip2wLscnpLQxejLxTMRn8TwqvBQrEqGt9ULAQc0I4HDZy9ZxwkR5OCluD0/yg2ynHX5OjSfyQ/T2AaXj/iuwLwuew1yuN5Ah5jEN6QOBbYbOA9AgcYUoce0oOxH4VOBoTsIZUTOyD1hzpCqFPQNxYbV62rh2TdgI63Bf2Ufg0A8K+18u0ficQ24qMc6LJy726IdwW7gtLBcT5moSOaJOgL0FjXxKWCBaIMV6CPZ39sl0M3Q4cJT7vhZUCkjsyL3gzcGS0dOoRv5LNZY2Jadk4TvSIQBzdtyPjCfLWcWcRN5at9OlR8eC5YFJod4PN23NR2C0sFyzHZRR9WbeCSR8IwckXh6NA9gpOxFlj01VMjD0u/gNhTLgj2M+xKW1Cw4pB/pkOm36LBmSvEc4IJISQSbkgCX2UcVEfRbzXynbsHuVBfF0aCxPx5qB2Xwo7BS6cj1JmQ/CnI/wpBgkIop1LZlKIca0XSa/IaYvsuKt4OvH+VG1PkaZ9oYtNN3m6w/FAii+4qRZOxfn+3ApVPa2wzCs/3KRtd/JN9nROyS/G0VDaL1KeSbTyjd+mPb573Ol0kHKOT8q7KtT0qYRla2Wn1Xp8XngjQMwJTbKq9nSuKhfi5rNV4tMXjA4eC5PCR6FbQm6Gq9AnIG48W5V8mvk5+UCEznynqk7F/txF7FEBaXt3Mrfs01NidV1wUt4Qd+q9TrSP6gkJg8Q1vFeq44DT8uRnwsWrkPJrDqkNoaLf5rBMK0jEINCj5by3C3cFiHVyhJ4M/kMC4nzZqsPPeDoOobsxwR2XTYlnvjPoQQGpTIavcv8pwHTWC4eEm4KPC50iw9TiqTzSul9AKpHxRNYq8LJQF/hh9a8yJLDplqIGe0wMEuyZNH+8jwiWSmQcZFI92hgWJoS4iIuV6WeKOSv4W1hm85cduyMxEZy5uByHZZ2MXQKXeaNAIf4BJIZp8ebVhYfCuHBPYGoIU8GmgUoSE3IgX4wkYkKxsL9AIIZjglRRIEJc3FjRp3TdipADmBhAKFAsQizP0TTA88oTUUxOygjlHLUo+nZdvFjgv1z/BW5q39C+k8EQAAAAAElFTkSuQmCC"

retweetlogo = "iVBORw0KGgoAAAANSUhEUgAAACQAAAAkCAYAAADhAJiYAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAABIlJREFUWAntl01olFcUhuc3MeA0FIyhKLEuoq02f4YGAy4iXQVsd5FqC920Ci660V2hIrhRdNWCuLFdFIqEuiwIirE/C5uGJIuAMSmEUklKoCUm0MnMZL4+78m942fmm5lMsbs5cOecOffcc9773nPvJLFYQxoMNBj4fxmI15E+QWzghpYlRkZGqq4fHR1VfFHBL1sExotAVAXiA6UBnawnfjuJBabY39/fsba29vfs7OyqCvX29r5eLBbbU6lUIQiCyDzML05PTz9VPGJ5Ns3Kn6nKUzZjSbq6ul7d2NiYb2lpuYv3Xc0A4nhTU9OtQqEQxBGL3vKBO9fT03Mnm82ecRupCUoBFQVWRHcsmUxeYaQTicQJCpyQj51/BZhHMBQJRjFIGtDvs5F7m1+tn6rFG40u9kWls5+YmMh3d3cfYaefwFBBEdhXUQYUli4A6in6CWPejd/Qc4zfiY3ncrksoAc44o+1fmhoyNbKjpKKDLkbEoOV6wxbS0/kSf4mLH0qByz9NDU1tbezs/MQ+iDjDWnYPIzeR8hN7B2sU/hxfdSSSEDsQr1VpPBJEg45duRLYivnJY5zlwwkDng5VVV6I5PJ6LpLxiHJDBhrltHW1ubnzL/1IwpQfGxsrCBQJLvsdufXKV5HkAHYJTkBJqCqWhqrq6uGAhA7FBOW5eVlmwv7wnYZIFcgtrKycqG5ublTO2SoqHamG2VFAHWO/npLfYZfeWxe2jNEbN2Pogq9IBSwJOzuR67rdyR9RsA76A4FwtgvqMeM9XQ6vSQfsu3CtY6sDBDJ1QdxmvJntEaMXvqWxu4AVIyjusHc1/I70RGE+0LflVcPZukEWG9HNT4+nnbxkZsoLSAoLCqQoI/seEjW5CcpslP24OBgCyoKTEAPZl38mtNiNid7YWFBcwJjAOULSxRDfr4IveoPJQu4beYHnF0z+ktzW5kJ6KvdxOit0iYO+EsBu8d4i77Bl8G+Pjk5+QO2klo+tEklhmyy1o1wObyyXBRrA/xHjFMA64dRE/x7+f4BG3kPx1Et4gKV1S9z+OyVNMlsjbvaot0P/QCneSxnYOVLrSdWx2Pz2OqpGC/3Y3rwmua5QPb6y/ZSFVDUjSDpP1rsrnbpquMKfAGKXqT5V/CpB0vNC0M6/s/kc49v+Mhxb74fZkR9+COD7nXNa4ckHZDtGFIPaOiPtc0m48vMzMxfrPnc9Z16pICd4nfvPgzeUaweX/xlUq2pw8EPAHI6n89n0WdpzmEYWEeLYdvl3Nxcke87AXKahn3I+ILvZ4g/DCsFNTf2+XDSKDvy6oUCNW8FSf6Ih3AAUBX//hEjsPArPfK2cvT19Q0D8HuAyK/365z6zL3uoTLPzRLNz11llrHQ2tp6m+T7GQcZketgIeAnZU97e/sfS0tLk4x57F78+wA7vLi4uM5QgbLe8VW3c2RqyoT7i+8Ur/YeAL3mE4Q1TAQ0dAr9p/cD5kOYfQVW1OTaXKnJfcx/1fFw424jiX8OfGjVG+2DavWQjwvrev/98cBeGjNhMA27wUCDgXoZ+BfqkvlK9fmwTwAAAABJRU5ErkJggg=="

replylogo = "iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAYAAACoPemuAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAAoRJREFUWAntl81qFEEUhaNRA5HgMmg2MeJGyNKFDyC4DfoWPkfIOmSRPIRugiCuhMGFIYqib5CQTXCtJlGT8zF15NI/M1WTOBOkL5yu21V17z11qrp7Zmqqs06BToH/R4ErWgq4VHY1sIl+6B6/O51KzqhdFW6Mn0K9okkx0hP205SJbmkk9UqEToWdSROLpF4nUhD7lIhNpGki9T2RMzHOGfPGtqVNpI5E4Fci9lFt1a6pI8ZVx7PuByVg7HfKwvY9EY4F1PE7bE7+A2Ep9R2qPRHYZuJ5leBfmEXCPlMoRRHjT/Ddt6e+TeGhYEPBC9niHFImAjlUBKjrfto3QiQY82qozJDe1qZULF71IVclue6EalGv2Cz3dUW+FSha3b4qkUH3nDWr+EX+HQEj/1CLCg2dXDjBZ4vFLQtfhfsChLPIad5fi0RH2co2Ba38N1W6naoVn7kYMIycDz8qAN5vbF/TE2tynzVu8/Hx/dA2h1xT8agYRKsPwk/1MccPROvDMIgx5Fg9hnLxBUtyYtmaF8KscEuYFxYEDnpcHEpiEGFBHJlHwnuBPo/LzbOYPG6rP0m7DWn4nXZPeCZsCXuClURFq9aTj8Vz3e/JvDaR80ec84JyPGXMa9oBPmErwjvBBH8k/7FarHVL+8Pt1yZyFPGvCxOiBahAsepr4an6DgQT3JaPxfz9noJrDC75oQhRSHrLOI8vBcih3KKAebx/V3iN5HqK3U/xFM+xqOCaAiD3PAXGsZxctTkmN+qfEeKtzqb8D6mC89YKlnQ4MTHRz82BwlZ5Q/7dFDhKrlrNmLw2mNFhEjc1dz7NN9mM8H87xeSocmlIecnnVd55urZToEiBMwks0+sAjBfRAAAAAElFTkSuQmCC"


# %% Authenticate to Twitter:
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# %% Create API object
api = tweepy.API(auth)
screen_name = api.me().screen_name
#print("User @%s successfully authorized the app." % screen_name)

#print(api.me().followers_count)
#print(api.me().friends_count)


# %% Get timeline

tweets = []

for i in tweepy.Cursor(api.user_timeline).items():
    # process status here
    if ((i.created_at.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).month == datetime.datetime.now().month) and
        (i.created_at.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).day   == datetime.datetime.now().day)):
        tweets.append(i)
        #print(i.text)
    else:
        break

#timeline = api.user_timeline()
#tweets = [i for i in timeline if (i.created_at.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).month == datetime.datetime.now().month) and
#                                 (i.created_at.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).day   == datetime.datetime.now().day)]


# %% Print counts
prefix = ""
#prefix = "≥" if len(tweets) == 20 else ""

print(prefix + "%d+%d+%d (💕%d) | templateImage=%s" % (
  sum(1 for t in tweets if not t.retweeted and not is_reply(t)),
  sum(1 for t in tweets if     t.retweeted),
  sum(1 for t in tweets if not t.retweeted and     is_reply(t)),
  sum(t.favorite_count for t in tweets),
  twitterlogo))

# %% Print tweets
print("---")

print(prefix + "%d Tweets (💕%d) |   href=https://twitter.com/%s image=%s"               % (sum(1 for t in tweets if not t.retweeted and not is_reply(t)),
                                                                                            sum(t.favorite_count for t in tweets if not t.retweeted and not is_reply(t)),
                                                                                            screen_name,
                                                                                            tweetlogo))
for t in tweets:
    if not t.retweeted and not is_reply(t):
        print("--%d💕 %s | size=12 length=60 href=https://twitter.com/%s/status/%d" % (t.favorite_count, t.text.replace('\n', ' ').replace('\r', ''), t.user.screen_name, t.id))

print(prefix + "%d Retweets | href=https://twitter.com/%s image=%s"               % (sum(1 for t in tweets if t.retweeted), screen_name, retweetlogo))
for t in tweets:
    if t.retweeted:
        print("--%s | size=12 length=60 href=https://twitter.com/%s/status/%d" % (t.text[3:].replace('\n', ' ').replace('\r', ''), t.user.screen_name, t.id))

print(prefix + "%d Replies: (💕%d) | href=https://twitter.com/%s/with_replies image=%s"  % (sum(1 for t in tweets if not t.retweeted and is_reply(t)), sum(t.favorite_count for t in tweets if not t.retweeted and is_reply(t)), screen_name, replylogo))
for t in tweets:
    if not t.retweeted and is_reply(t):
        print("--%d💕 %s | size=12 length=60 href=https://twitter.com/%s/status/%d" % (t.favorite_count, t.text.replace('\n', ' ').replace('\r', ''), t.user.screen_name, t.id))


print("---")
print("%d Followers| href=https://twitter.com/%s/followers" % (api.me().followers_count, screen_name))
print("%d Following | href=https://twitter.com/%s/following" % (api.me().friends_count, screen_name))
print("Analytics | href=https://analytics.twitter.com/user/%s/tweets" % screen_name)
