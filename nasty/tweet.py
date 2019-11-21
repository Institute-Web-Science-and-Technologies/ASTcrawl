from datetime import datetime
from typing import Any, Dict

import tweepy

from nasty.init import init_nasty
from nasty.util.consts import TWITTER_CREATED_AT_FORMAT


class Tweet:
    """Data class to wrap Tweet JSON objects."""

    class User:
        """Data class to wrap Twitter user JSON objects."""

        def __init__(self, json: Dict):
            self.json = json

        @property
        def id(self):
            return self.json['id_str']

        @property
        def name(self):
            return self.json['name']

        @property
        def screen_name(self):
            return self.json['screen_name']

        @property
        def url(self):
            return 'https://twitter.com/{}'.format(self.screen_name)

        def __repr__(self) -> str:
            return type(self).__name__ + repr({
                'id': self.id,
                'name': self.name,
                'screen_name': self.screen_name,
                'url': self.url,
            })

        def __eq__(self, other: Any) -> bool:
            return (type(self) == type(other)) \
                   and (self.__dict__ == other.__dict__)

        def to_json(self) -> Dict[str, Any]:
            return self.json

        @classmethod
        def from_json(cls, obj: Dict[str, Any]) -> 'Tweet.User':
            return cls(obj)

    def __init__(self, json: Dict[str, Any]):
        self.json = json

    @property
    def created_at(self) -> datetime:
        return datetime.strptime(self.json['created_at'],
                                 TWITTER_CREATED_AT_FORMAT)

    @property
    def id(self) -> str:
        return self.json['id_str']

    @property
    def text(self) -> str:
        return self.json['full_text']

    @property
    def user(self) -> User:
        return self.User(self.json['user'])

    @property
    def url(self):
        return '{}/status/{}'.format(self.user.url, self.id)

    def __repr__(self):
        return type(self).__name__ + repr({
            'created_at': self.created_at,
            'id': self.id,
            'text': self.text,
            'user': self.user,
            'url': self.url,
        })

    def __eq__(self, other: Any) -> bool:
        return (type(self) == type(other)) and (self.__dict__ == other.__dict__)

    def to_json(self) -> Dict[str, Any]:
        return self.json

    @classmethod
    def from_json(cls, obj: Dict[str, Any]) -> 'Tweet':
        return cls(obj)

    def from_tweepy(self) -> 'Tweet':
        config = init_nasty()

        auth = tweepy.OAuthHandler(config['twitter_api']['consumer_key'],
                                   config['twitter_api']['consumer_key_secret'])
        auth.set_access_token(config['twitter_api']['access_token'],
                              config['twitter_api']['access_token_secret'])

        api = tweepy.API(auth)
        return api.statuses_lookup([self.id], tweet_mode='extended')
