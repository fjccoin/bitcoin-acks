from github_twitter.scripts.get_pull_requests import insert_response
from github_twitter.scripts.send_tweet import send_tweet

if __name__ == '__main__':
    insert_response()
    send_tweet()