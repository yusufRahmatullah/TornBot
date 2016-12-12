#!/usr/bin/python

import re


class Checker:
    def __init__(self):
        pass

    @staticmethod
    def isLevelUp(page_source):
        return 'Level Up' in page_source


class Url:
    def __init__(self):
        pass
    root = 'http://www.torn.com/'
    crime = root + 'crimes.php'
    gym = root + 'gym.php'
    home = root + 'index.php'


class Util:

    def __init__(self):
        # zero constructor
        pass

    @staticmethod
    def get_pair_int(text):
        try:
            ints = re.findall('[\d,]+', text)
            return int(ints[0]), int(ints[1])
        except ValueError:
            return -1, 100

    @staticmethod
    def get_single_int(text):
        try:
            return int(re.findall('[\d,]+', text)[0])
        except ValueError:
            return -1


class Xpath:
    def __init__(self):
        pass

    class Crime:
        def __init__(self):
            pass
        item = "//ul[@class='item']"
        try_again = "//div[@id='try_again']"

    class Gym:
        def __init__(self):
            pass

        class Data:
            def __init__(self):
                pass
            strength = "//span[@id='strengthTotal']"
            defense = "//span[@id='defenceTotal']"
            speed = "//span[@id='speedTotal']"
            dexterity = "//span[@id='dexterityTotal']"

        class Input:
            def __init__(self):
                pass
            strength = "//input[@name='strength']"
            defense = "//input[@name='defense']"
            speed = "//input[@name='speed']"
            dexterity = "//input[@name='dexterity']"

    class Login:
        def __init__(self):
            pass
        email = "//input[@id='player']"
        password = "//input[@id='password']"
        login = "//input[@class='login'][@type='submit']"

    class Profile:
        def __init__(self):
            pass
        energy = "//div[@id='energy']"
        nerve = "//div[@id='nerve']"
        happy = "//div[@id='happy']"
        life = "//div[@id='life']"
