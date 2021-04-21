# bitbar_todays_tweets
A plugin to show today’s tweets in Mac menubar using [SwiftBar](https://swiftbar.app) or [xbar](https://xbarapp.com) (which have replaced BitBar).

![Screenshot](todays_tweets.png)

Requires python3, [tweepy](https://www.tweepy.org/), and [Twitter developer API](https://developer.twitter.com/) access (which is easy to request).

## Installation instructions

1. Set up [SwiftBar](https://swiftbar.app) or [xbar](https://xbarapp.com)
2. Ensure [tweepy](https://www.tweepy.org/) is installed
3. Download the [todays_tweets script](todays_tweets.30m.py) (`todays_tweets.30m.py`)
4. Set up the todays_tweets script by editing `todays_tweets.30m.py`
   1. Replace `/usr/local/bin/python3` in the first line with the path to your python3 installation
   2. Replace `KEY`, `SECRET`, `TOKEN`, and `TOKENSECRET` with your [Twitter developer API](https://developer.twitter.com/) keys
5. Rename `todays_tweets.30m.py` if you want it to run at a frequency other than every 30 minutes
6. Move `todays_tweets.30m.py` into your [SwiftBar](https://swiftbar.app) or [xbar](https://xbarapp.com) plugin folder, and ensure it can be executed using `chmod +x plugin.sh`

## Caveats

This is very much a work-in-progress, toy project by a highly amateur Python programmer. Also, there is currently no error handling.
