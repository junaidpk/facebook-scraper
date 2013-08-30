facebook-scraper
=================

Simple tool to count the frequency of Facebook Likes for a list of users.

Example:
```
$ fb_scraper.py -f user_ids.txt -a '123456789000|abc123abc123_abc123' -t 5 -l DEBUG
2013-07-24 11:24:46,642 [fb_scraper] INFO - Found 3 user IDs
2013-07-24 11:24:47,036 [fb_scraper] DEBUG - (200, u'100012345678', u'{"success":true}')
2013-07-24 11:24:47,036 [fb_scraper] DEBUG - (200, u'100087654321', u'{"success":true}')
2013-07-24 11:24:47,036 [fb_scraper] WARNING - (404, u'fake_user_abc123', u'{"error":{"message":"(#803) Some of the aliases you requested do not exist: fake_user_abc123","type":"OAuthException","code":803}}')
5,9098498615,Adam Sandler
5,68680511262,NFL
5,128874350565152,Slotomania - Slot Machines
5,314467614927,Angry Birds
5,406433779383,Dwayne The Rock Johnson
```

Requirements
------------

 * [grequests](https://github.com/kennethreitz/grequests)
 * [requests](https://github.com/kennethreitz/requests)
 * [argparse](https://pypi.python.org/pypi/argparse) (if below Python 2.7 or 3.2)
 * Facebook `app access token` ([FB documentation](https://developers.facebook.com/docs/opengraph/howtos/publishing-with-app-token/))

Usage
------------

```
usage: fb_scraper.py [-h] -f RECIPIENTS_FILE [-c MAX_CONCURRENT]
                     [-l LOG_LEVEL] [-t THRESHOLD] -a ACCESS_TOKEN

Scrape the Facebook likes for a list of FB users and count the frequency of
each.

optional arguments:
  -h, --help            show this help message and exit

scraper arguments:
  -f RECIPIENTS_FILE, --recipients-file RECIPIENTS_FILE
                        File containing list of recipients (newline-delimited
                        FB IDs)
  -c MAX_CONCURRENT, --max-concurrent MAX_CONCURRENT
                        Maximum number of concurrent requests (default: 10,
                        max: 100)
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Log level (debug, [default] info, warn, error)
  -t THRESHOLD, --threshold THRESHOLD
                        Minimum Like count to show up in the results

Facebook arguments:
  -a ACCESS_TOKEN, --access-token ACCESS_TOKEN
                        App access token
```

