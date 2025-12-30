#Youtube comment downloader schema resources. Defines objects and their conversions to tables and fields.
#Purpose: Accept a youtube link, download and display comments
#Usage: python prxyYT_CommentDL_gui.py

import os   #used to handle files
import json #used for data storage/handling
import operator #Used for sorts
import datetime # Used to display dates


class user:
    def __init__(self, form=None):
        self.user_id = ""
        self.num_comments = ""
        self.list_comment_cids = ""
        self.list_comment_vids = ""
        self.user_comment_sent = ""
        self.sent_per_vid = ""
        self.bot_chance = ""
        pass

    def getUserID(self):
        return self.user_id
        pass


class video:
    def __init__(self):
        self.video_id = ""
        self.title = ""
        self.channel = ""
        self.time_posted = ""
        self.time_lastChecked
        self.num_comments
        self.num_likes = ""
        self.description = ""
        self.comment_dict = {}
        pass
        
    def getVideoID(self):
        return self.video_id
        pass


class comment:
    def __init__(self):
        self.cid = ""
        self.text = ""
        self.time = ""
        self.author = ""
        self.channel = ""
        self.votes = ""
        self.replies = ""
        self.photo = ""
        self.heart = ""
        self.reply = ""
        self.time_parsed = ""
        pass
        
    def getCID(self):
        return self.cid
        pass
