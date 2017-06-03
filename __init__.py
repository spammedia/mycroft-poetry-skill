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

from os.path import dirname, realpath
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
        self.styles = ["blackmetal", "deathmetal","scifi","viking"]
        self.path = dirname(realpath(__file__))
        self.minsize = 10
        self.maxsize = 20
        self.mode = 1

    def initialize(self):
        self.load_data_files(dirname(__file__))

        viking_poetry_intent = IntentBuilder("ReciteVikingPoetryIntent") \
            .require("viking").build()
        self.register_intent(viking_poetry_intent,
                             self.handle_viking_poetry_intent)

        gore_poetry_intent = IntentBuilder("ReciteGorePoetryIntent") \
            .require("gore").build()
        self.register_intent(gore_poetry_intent,
                             self.handle_gore_poetry_intent)

        satanic_poetry_intent = IntentBuilder("ReciteSatanicPoetryIntent") \
            .require("satanic").build()
        self.register_intent(satanic_poetry_intent,
                             self.handle_satanic_poetry_intent)

        sci_poetry_intent = IntentBuilder("ReciteSciFiPoetryIntent") \
            .require("science").build()
        self.register_intent(sci_poetry_intent,
                             self.handle_science_poetry_intent)

        poetry_intent = IntentBuilder("RecitePoetryIntent")\
            .require("poetry").build()
        self.register_intent(poetry_intent,
                             self.handle_poetry_intent)

    def handle_science_poetry_intent(self, message):
        style = "scifi"
        poem = self.poetry(style)
        self.save(style, poem)
        # speak
        self.speak(poem)

    def handle_gore_poetry_intent(self, message):
        style = "deathmetal"
        poem = self.poetry(style)
        self.save(style, poem)
        # speak
        self.speak(poem)

    def handle_viking_poetry_intent(self, message):
        style = "viking"
        poem = self.poetry(style)
        self.save(style, poem)
        # speak
        self.speak(poem)

    def handle_satanic_poetry_intent(self, message):
        style = "blackmetal"
        poem = self.poetry(style)
        self.save(style,poem)
        # speak
        self.speak(poem)

    def handle_poetry_intent(self, message):
        #self.speak_dialog("poetry")
        # choose style (black metal, death metal, trash metal)
        style = random.choice(self.styles)
        poem = self.poetry(style)
        self.save(style,poem)
        # speak
        self.speak(poem)


    def poetry(self, style):
        # style = "shakespeare"
        path = self.path + "/styles/" + style + ".txt"
        # init dicionares
        poemFreqDict = {}
        poemProbDict = addToDict(path, poemFreqDict, self.mode)
        # choose seed word
        f = open(path, 'r')
        self.words = re.sub("\n", " \n", f.read()).lower().split(' ')
        startWord = random.choice(self.words)

        # generate poem
        return makepoem(startWord, poemProbDict, self.mode, self.minsize, self.maxsize)

    def save(self, style, poem):
        # save
        path = self.path + "/results/" + style + "_" + poem[:20] + ".txt"
        wfile = open(path, "w")
        wfile.write(poem)
        wfile.close()

    def stop(self):
        pass


def create_skill():
    return PoetrySkill()

# freqDict is a dict of dict containing frequencies
def addToDict(fileName, freqDict, mode = 1):
    f = open(fileName, 'r')
    # phrases
    if mode == 1:
        words = re.sub("\n", " \n", f.read()).lower().split('\n')
    else:
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

def markov_next( curr, probDict):
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

def makepoem(curr, probDict, mode=1, minsize=8, maxsize=20):
    if mode == 1:
        T = random.choice(range(minsize,maxsize))
    else:
        T = random.choice(range(minsize*20, maxsize*5))
    poem = [curr]
    for t in range(T):
        poem.append(markov_next(poem[-1], probDict))
        if mode == 1:
            poem.append(",\n")
    return " ".join(poem)
