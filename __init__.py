# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from os.path import dirname
import random
import re

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'jarbas'

logger = getLogger(__name__)


class PoetrySkill(MycroftSkill):

    def __init__(self):
        super(PoetrySkill, self).__init__(name="PoetrySkill")
        self.styles = ["blackmetal", "deathmetal"]
        self.path = self.config.get["path"]

    def initialize(self):
        self.load_data_files(dirname(__file__))

        poetry_intent = IntentBuilder("RecitePoetryIntent")\
            .require("poetry").build()
        self.register_intent(poetry_intent,
                             self.handle_poetry_intent)

    def handle_poetry_intent(self, message):
        self.speak_dialog("poetry")
        # choose style (black metal, death metal, trash metal)
        style = random.choice(self.styles)
        path = "/home/user/mycroft-core/mycroft/skills/Facebook/styles/" + style + ".txt"
        #init dicionares
        poemFreqDict = {}
        poemProbDict = self.addToDict(path,
                                          poemFreqDict)
        # choose seed word
        f = open(path, 'r')
        self.words = re.sub("\n", " \n", f.read()).lower().split(' ')
        startWord = random.choice(self.words)

        #generate poem
        poem = self.makepoem(startWord, poemProbDict)
        self.speak(poem)

    # freqDict is a dict of dict containing frequencies
    def addToDict(self, fileName, freqDict):
        f = open(fileName, 'r')
        words = re.sub("\n", " \n", f.read()).lower().split(' ')

        # count frequencies curr -> succ
        for curr, succ in zip(words[1:], words[:-1]):
            # check if curr is already in the dict of dicts
            if curr not in freqDict:
                freqDict[curr] = {succ: 1}
            else:
                # check if the dict associated with curr already has succ
                if succ not in freqDict[curr]:
                    freqDict[curr][succ] = 1;
                else:
                    freqDict[curr][succ] += 1;

        # compute percentages
        probDict = {}
        for curr, currDict in freqDict.items():
            probDict[curr] = {}
            currTotal = sum(currDict.values())
            for succ in currDict:
                probDict[curr][succ] = currDict[succ] / currTotal
        return probDict

    def markov_next(self, curr, probDict):
        if curr not in probDict:
            return random.choice(list(probDict.keys()))
        else:
            succProbs = probDict[curr]
            randProb = random.random()
            currProb = 0.0
            for succ in succProbs:
                currProb += succProbs[succ]
                if randProb <= currProb:
                    return succ
            return random.choice(list(probDict.keys()))

    def makepoem(self, curr, probDict, T=50):
        poem = [curr]
        for t in range(T):
            poem.append(self.markov_next(poem[-1], probDict))
        return " ".join(poem)

    def stop(self):
        pass


def create_skill():
    return PoetrySkill()