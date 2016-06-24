#! /usr/bin/env python2.7

import time

from modules import irc

class TwitchIRC(irc.IRC):

    def __init__(self, username, oauth, callback = None):
        if not oauth.startswith("oauth:"):
            oauth = "oauth:{0}".format(oauth)
        super(TwitchIRC, self).__init__(
            "irc.chat.twitch.tv",
            6667,
            username,
            oauth=oauth,
            use_ssl=False,
            callback=callback
        )
        self.total_messages = 0
        self.sent_messages = 0
        self.message_limit = 30
        self.last_reset = time.time()

    @property
    def rate_limited(self):
        return self.sent_messages >= self.message_limit

    def clear_limit(self):
        if time.time() - self.last_reset >= 30:
            self.sent_messages = 0

    def privmsg(self, channel, msg):
        self.clear_limit()
        if not self.rate_limited:
            super(TwitchIRC, self).privmsg(channel, msg)
            self.sent_messages += 1
            self.total_messages += 1
