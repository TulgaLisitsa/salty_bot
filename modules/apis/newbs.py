#! /usr/bin/env python2.7

import modules.apis.api_base as api

class NewbsAPI(api.API):

    def __init__(self, session = None):
        super(NewbsAPI, self).__init__("https://leagueofnewbs.com/api", session)

    def add_textutil(self, channel, text_type, data, **kwargs):
        endpoint = "/users/{0}/{1}s".format(channel, text_type)
        success, response = self.post(endpoint, data, **kwargs)
        return success, response

    def show_textutil(self, channel, text_type, limit = 1, **kwargs):
        endpoint = "/users/{0}/{1}s?limit={2}".format(channel, text_type, limit)
        success, response = self.get(endpoint, **kwargs)
        return success, response

    def get_song(self, channel, **kwargs):
        endpoint = "/users/{}/songs".format(channel)
        success, response = self.get(endpoint, **kwargs)
        return success, response
