#!/usr/bin/python
import json
from threading import Thread
import time

import selenium.webdriver as wd

from config import Config
from util import Checker, Util, Url, Xpath


class Torn:
    def __init__(self):
        self.timer = 0
        self.config = Config()
        if self.config.client == Config.PHANTOM:
            self.b = wd.PhantomJS()
        elif self.config.client == Config.CHROME:
            self.b = wd.Chrome()
        elif self.config.client == Config.FIREFOX:
            self.b = wd.Firefox()
        self.b.set_window_position(0, 0)
        self.b.set_window_size(1366, 768)
        self.isRun = False

    def _crime(self, max_crime_idx=21):
        self._debug('[crime] visit crime with idx={}'.format(max_crime_idx))
        self.b.get(Url.crime)
        if Checker.isLevelUp(self.b.page_source):
            self.b.get(Url.crime)
        if Checker.isBotDetected(self.b.page_source):
            _temp = self.b.find_elements_by_xpath(Xpath.Captcha.image_tab)
            if len(_temp) > 0:
                _temp[0].click()
            _time = time.gmtime()
            _time_str = 'bot_{}-{}-{}_{}-{}-{}.png'.format(_time.tm_year, _time.tm_mon,
            _time.tm_mday, _time.tm_hour, _time.tm_min, _time.tm_sec)
            self.b.save_screenshot(_time_str)
            return
        uls = self.b.find_elements_by_tag_name('ul')
        # max_crime_idx must in range 20-36
        # cost is start from 2 for idx 20 and 18 for idx 36
        if 19 <= max_crime_idx <= 36:
            uls[max_crime_idx].click()
            time.sleep(1)
            items = self.b.find_elements_by_xpath(Xpath.Crime.item)
            if len(items) > 0:
                self._debug('[crime] item found')
                items[0].click()
                time.sleep(1)
                cost = max_crime_idx - 18
                available_crime = self.nerve[0]/cost
                self._debug('[crime] cost: {}'.format(cost))
                self._debug('[crime] available crime: {}'.format(available_crime))
                for i in xrange(available_crime):
                    t.b.find_element_by_xpath(Xpath.Crime.try_again).click()
                    time.sleep(1)

    def _debug(self, text):
        if self.config.isDebug:
            print(text)

    def _get_profile_info(self):
        self._debug('[info] call get profile info')
        self.b.get(Url.gym)
        _temp = self.b.find_elements_by_xpath(Xpath.Profile.energy)
        if len(_temp) > 0:
                self.energy = Util.get_pair_int(_temp[0].text)
        else:
                self.energy = (-1, 100)
        _temp = self.b.find_elements_by_xpath(Xpath.Profile.nerve)
        
        if len(_temp) > 0:
                self.nerve = Util.get_pair_int(_temp[0].text)
        else:
                self.nerve = (-1, 100)
        _temp = self.b.find_elements_by_xpath(Xpath.Profile.happy)
        
        if len(_temp) > 0:
                self.happy = Util.get_pair_int(_temp[0].text)
        else:
                self.happy = (-1, 100)
        
        _temp = self.b.find_elements_by_xpath(Xpath.Profile.life)
        if len(_temp) > 0:
                self.life = Util.get_pair_int(_temp[0].text)
        else:
                self.life = (-1,100)
        
        _temp = self.b.find_elements_by_xpath(Xpath.Gym.Data.strength)
        if len(_temp) > 0:
                self.strength = float(_temp[0].text)
        else:
                self.strength = -1.0
        
        _temp = self.b.find_elements_by_xpath(Xpath.Gym.Data.defense)
        if len(_temp) > 0:
                self.defense = float(_temp[0].text)
        else:
                self.defense = -1.0
        
        _temp = self.b.find_elements_by_xpath(Xpath.Gym.Data.speed)
        if len(_temp) > 0:
                self.speed = float(_temp[0].text)
        else:
                self.speed - -1.0
        
        _temp = self.b.find_elements_by_xpath(Xpath.Gym.Data.dexterity)
        if len(_temp) > 0:
                self.dexterity = float(_temp[0].text)
        else:
                self.dexterity = -1.0

        _temp = self.b.find_elements_by_class_name('info-money')
        if len(_temp) > 0:
                self.money = Util.get_single_int(_temp[0].text)
        else:
                self.money = -1
                
        _temp = self.b.find_elements_by_class_name('info-level')
        if len(_temp) > 0:
                self.level = Util.get_single_int(_temp[0].text)
        else:
                self.level = -1

        if self.energy[0] == -1 or self.nerve[0] == -1 or self.happy[0] == -1:
                self.timer = 0
                return
        energy_diff = self.energy[1] - self.energy[0]
        self._debug('[info] energy diff: {}'.format(energy_diff))
        energy_timer = energy_diff/5 * 15 * 60    # wait n x 15 minutes
        self._debug('[info] energy timer: {}'.format(energy_timer))

        nerve_diff = self.nerve[1] - self.nerve[0]
        self._debug('[info] nerve diff: {}'.format(nerve_diff))
        nerve_timer = nerve_diff * 5 * 60   # wait n x 5 minutes
        self._debug('[info] nerve timer: {}'.format(nerve_timer))

        if self.happy[0] < 10:
            happy_diff = self.happy[1] - self.happy[0]
            self._debug('[info] happy diff: {}'.format(happy_diff))
            happy_timer = happy_diff/5 * 15 * 60
            self._debug('[info] happy timer: {}'.format(happy_timer))
        else:
            happy_timer = 100 * 15 * 60

        self.timer = min(energy_timer, nerve_timer, happy_timer)

    def _gym(self):
        values = self.config.gym_values
        self._debug('[gym] call gym with value: {}, {}, {}, {}'.format(values[0], values[1], values[2], values[3]))
        if self.energy[0] < self.energy[1]:
            self._debug('[gym] energy not enough: {}/{}'.format(self.energy[0], self.energy[1]))
            return
        self.b.get(Url.gym)
        if Checker.isLevelUp(self.b.page_source):
            self.b.get(Url.gym)
        strength = self.b.find_element_by_xpath(Xpath.Gym.Input.strength)
        defense = self.b.find_element_by_xpath(Xpath.Gym.Input.defense)
        speed = self.b.find_element_by_xpath(Xpath.Gym.Input.speed)
        dexterity = self.b.find_element_by_xpath(Xpath.Gym.Input.dexterity)

        strength.clear()
        strength.send_keys(values[0])
        defense.clear()
        defense.send_keys(values[1])
        speed.clear()
        speed.send_keys(values[2])
        dexterity.clear()
        dexterity.send_keys(values[3])

        buttons = self.b.find_elements_by_link_text('TRAIN')
        for btn in buttons:
            btn.click()

    def _login(self):
        self._debug('[login] call login')
        self.b.get(Url.root)
        email = self.b.find_element_by_xpath(Xpath.Login.email)
        password = self.b.find_element_by_xpath(Xpath.Login.password)
        login = self.b.find_element_by_xpath(Xpath.Login.login)
        self._debug('email= {}'.format(self.config.email))
        self._debug('password= {}'.format(self.config.password))
        email.send_keys(self.config.email)
        password.send_keys(self.config.password)
        login.click()

    def _print_profile_info(self):
        self._get_profile_info()
        print('==================')
        print('Profile Info')
        print('------------------')
        print('Money: {}'.format(self.money))
        print('Level: {}'.format(self.level))
        print('Energy: {}/{}'.format(self.energy[0], self.energy[1]))
        print('Nerve: {}/{}'.format(self.nerve[0], self.nerve[1]))
        print('Happy: {}/{}'.format(self.happy[0], self.happy[1]))
        print('Life: {}/{}'.format(self.life[0], self.life[1]))
        print('------------------')
        print('Strength: {}'.format(self.strength))
        print('Defense: {}'.format(self.defense))
        print('Speed: {}'.format(self.speed))
        print('Dexterity: {}'.format(self.dexterity))
        print('==================')

    def run(self):
        self._login()
        while True:
            self._print_profile_info()
            self._gym()
            self._crime()
            self._print_profile_info()
            self._debug('[run] sleep for {} seconds'.format(self.timer))
            time.sleep(self.timer)

if __name__ == '__main__':
    t = Torn()
    t.run()
