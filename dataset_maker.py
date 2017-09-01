# Makes dataset for bot_detector

import praw

reddit = praw.Reddit(client_id='kI3FZaNn2yH3FA', client_secret='HHv8tHON3HrQN6NFIwWW__9B7fc', user_agent='test_bot')

import pandas as pd

# Import current dataset
current = pd.read_csv('bot_list.csv')

users = set()

# Gather users
for submission in reddit.subreddit('all').hot(limit=5):
    for comment in submission.comments:
        try:
            name = comment.author.name.lower()
        except:
            continue
        if 'auto' not in comment.author.name.lower():
            print(name)
            users.add(comment.author)
            if len(users) % 80 == 79:
                break

# Assemble new data set
new_set = pd.DataFrame([[u,0] for u in users], columns=current.columns)

# Combine sets
combined = current.append(new_set)

# Save dataset
combined.to_csv('raw.csv')

def get_vocabulary(generator, post_type):
    vocab = set()
    num_listing = 0
    for listing in generator:
        if post_type == 'submission':
            vocab.update([x for x in listing.title.split(' ')])
            vocab.update([x for x in listing.selftext.split(' ')])
        elif post_type == 'comment':
            vocab.update([x for x in listing.body.split(' ')])
        num_listing += 1
    return num_listing, len(vocab)

def get_data(redditor):
    if type(redditor) is str:
        redditor = reddit.redditor(redditor)
    num_submissions, submission_vocab = get_vocabulary(redditor.submissions.new(limit=None), 'submission')
    num_comments, comment_vocab = get_vocabulary(redditor.comments.new(limit=None), 'comment')
    return (redditor.link_karma,
            redditor.comment_karma,
            num_submissions,
            submission_vocab,
            num_comments,
            comment_vocab,
            len(list(redditor.gilded())),
            len(redditor.multireddits()),
            redditor.created_utc,
            redditor.has_subscribed,
            redditor.has_verified_email,
            redditor.hide_from_robots,
            redditor.is_employee,
            redditor.is_gold,
            redditor.is_mod,
            redditor.pref_show_snoovatar,
            redditor.verified)

# Create preprocessed data set
raw = pd.read_csv('raw.csv').iloc[:,1:]
num_success = 0
with open('assembled.csv', 'w') as f:
    f.write('bot,link_karma,comment_karma,num_submissions,submission_vocab,')
    f.write('num_comments,comment_vocab,num_gilded,num_subreddits,')
    f.write('created_utc,has_subscribed,verified_email,hide_from_robots,')
    f.write('is_employee,is_gold,is_mod,pref_show_snoovatar,verified,is_bot\n')
    for i in range(len(raw.iloc[:,0])):
        name = raw.iloc[i,0]
        try:
            data = get_data(name)
            f.write(name + ',' + ''.join([str(float(x))+',' for x in data]) + str(raw.iloc[i,1]) + '\n')
            print('Collected data for: ' + name)
            num_success += 1
        except:
            print('Failed to collect data for: ' + name)