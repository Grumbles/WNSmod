#!/usr/bin/env python2.6
"""
/r/WordsnShit Automatic Percolator

An automatic moderator for /r/WordsnShit, the purest Reddit experience available
to date. Logs in and processes the modqueue, approving any and all posts that
meet the strict WNS standards, and deleting all those which don't. This script
should execute at a regular interval (10 minutes, ideally).

Made possible with PRAW, the Python Reddit API Wrapper.

"""

import time

import praw

user_agent = '/r/WordsnShit Automoderator v3.14 by /u/Garythekrampus'
r = praw.Reddit(user_agent=user_agent)

approved_phrases = ["I don't know how I feel about carjackers.",\
                    "I can't believe how tall giraffes really are!",\
                    u"Do you have Die Hard\u2122 on Blu-Ray?",\
                    "Just give me two big ones, please.", ""]

def check_item(item):
    if isinstance(item, praw.objects.Comment):
        check_comment(item)
    elif isinstance(item, praw.objects.Submission):
        check_submission(item)
    else:
        print("I found something weird! " + str(item))
    
def check_comment(comment):
    if comment.body.strip() in approved_phrases:
        print("Approved comment: " + comment.body +\
              " by user " + comment.author.name)
        comment.approve()
    else:
        print("Rejected comment: " + comment.body +\
              " by user " + comment.author.name)
        comment.remove()
        send_rejection_letter(comment.author)

def check_submission(submission):
    if submission.selftext.strip() in approved_phrases\
       and submission.title in approved_phrases:
        print("Approved submission: " + submission.title +\
              " by user " + submission.author.name)
        submission.approve()
    else:
        print("Rejected submission: " + submission.title +\
              " by user " + submission.author.name)
        submission.remove()
        send_rejection_letter(submission.author)

def send_rejection_letter(author):
    fn = open('removal_message', 'r')
    r.send_message(author, 'Mistakes were made', fn.read())
    fn.close()

def main():
    print("Current time: " + time.strftime("%H:%M") +\
          " on " + time.strftime("%m/%d/%Y"))
    print("Logging in...")

    user = open('user.dat', 'r').read().split(':')
    r.login(user[0], user[1])
    sub = r.get_subreddit('WordsnShit')

    print("Done! Checking modqueue...")

    queue = sub.get_mod_queue()
    for item in queue:
        check_item(item)

    print("All done!")

if __name__ == '__main__':
    main()
