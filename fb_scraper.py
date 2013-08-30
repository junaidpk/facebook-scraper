#!/usr/bin/env python

import argparse
import grequests
import requests
import logging
import sys
from collections import defaultdict

BASE_FB_URL = 'https://graph.facebook.com'

def chunks(l, n):
    '''Split l into n-sized chunks'''
    for i in range(0, len(l), n):
        yield l[i:i+n]

def parse_id(url):
    '''Recover the FB ID from the Graph URL'''
    return url.split('/')[3]

def main():
    parser = argparse.ArgumentParser(description='Scrape the Facebook likes for a list of FB users and count the frequency of each.')
    scraper_args = parser.add_argument_group('scraper arguments')
    scraper_args.add_argument('-f', '--recipients-file', type=argparse.FileType('rt'), required=True, help='File containing list of recipients (newline-delimited FB IDs)')
    scraper_args.add_argument('-c', '--max-concurrent', default=10, type=int, help='Maximum number of concurrent requests (default: 10, max: 100)')
    scraper_args.add_argument('-l', '--log-level', default="info", help='Log level (debug, [default] info, warn, error)')
    scraper_args.add_argument('-t', '--threshold', default=3, type=int, help='Minimum Like count to show up in the results')
    
    # Facebook parameters    
    fb_args = parser.add_argument_group('Facebook arguments')            
    fb_args.add_argument('-a', '--access-token', required=True, help='App access token')

    args = parser.parse_args()

    log = logging.getLogger('fb_scraper')
    ch = logging.StreamHandler(sys.stdout)    
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s - %(message)s')    
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.setLevel(getattr(logging, args.log_level.upper()))

    user_ids = args.recipients_file.read().splitlines()
    log.info("Found %s user IDs" % len(user_ids))

    session = requests.session()

    like_freq = defaultdict(int)
    rs = [grequests.get("%s/%s" % (BASE_FB_URL, user_id), session=session, params={
            'fields': 'likes',
            'access_token': args.access_token,
        }) for user_id in user_ids]

    requests_completed = 0
    chunk_size = args.max_concurrent if args.max_concurrent > 100 else 100
    for s in chunks(rs, chunk_size):
        responses = grequests.map(s, size=args.max_concurrent)        
        for r in responses:
            try:
                if r.status_code >= 300:
                    log.warn((r.status_code, parse_id(r.url), r.text))
                else:
                    log.debug((r.status_code, parse_id(r.url), r.text))
                    if 'likes' in r.json():
                        for like in r.json()['likes']['data']:
                            like_freq[like['id']] += 1
            finally:
                r.raw.release_conn()
        requests_completed += len(responses)
        log.info("Completed %s requests" % requests_completed)

    final = dict((k, v) for k, v in like_freq.iteritems() if v >= args.threshold)    
    for k in sorted(final, key=final.get):
        like_url = "%s/%s" % (BASE_FB_URL, k)
        r = requests.get(like_url)
        print("%s,%s,%s" % (final[k], r.json().get('name', "none"), like_url))


if __name__ == "__main__":
    main()