#!/usr/bin/python

import json


class Config:

    PHANTOM = 'phantom'
    CHROME = 'chrome'
    FIREFOX = 'firefox'

    def __init__(self, config_file='config.json'):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.client = self.config["client"]
        self.email = self.config["email"]
        self.gym_values = self.config["gym_values"]
        self.isDebug = self.config["debug"]
        self.password = self.config["password"]
