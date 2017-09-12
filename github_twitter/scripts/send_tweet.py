import datetime
import os

from twython import Twython

from github_twitter.database.session_scope import session_scope
from github_twitter.models import PullRequests
from github_twitter.models.tweets import Tweets


def send_tweet():
    with session_scope() as session:
        now = datetime.datetime.utcnow()
        yesterday = now - datetime.timedelta(days=1)
        twitter = Twython(os.environ['BTC_TWITTER_APP_KEY'],
                          os.environ['BTC_TWITTER_APP_SECRET'],
                          os.environ['BTC_TWITTER_OAUTH_TOKEN'],
                          os.environ['BTC_TWITTER_OAUTH_TOKEN_SECRET']
                          )
        next_pull_request = (
            session
            .query(PullRequests)
            .order_by(PullRequests.merged_at.asc())
            .filter(PullRequests.merged_at > yesterday)
            .filter(PullRequests.tweet_id.is_(None))
            .first()
        )
        status = f'Merged PR from {next_pull_request.author}: ' \
                 f'{next_pull_request.title} {next_pull_request.url}'
        tweet = twitter.update_status(status=status)
        new_tweet = Tweets()
        new_tweet.id = tweet['id']
        new_tweet.pull_request_id = next_pull_request.id
        session.add(new_tweet)
        next_pull_request.tweet_id = tweet['id']


if __name__ == '__main__':
    send_tweet()