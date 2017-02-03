# mycroft-poetry-skill
make poems/lyrics based on Hidden Markov Model

usage:
- recite a poem
- recite viking poetry
- recite evil poem
- write gore poem
- write scifi poem
- recite shakespeare poetry

based on the following video: https://www.youtube.com/watch?v=yE0dcDNRZjw

originally meant to make rap lyrics now makes metal lyrics, styles can be added by collecintg lyrics and making a new txt file and adding the name to init.py, should have put this in cnfig file but im lazy :P

add following (or your equivalent) to config file

 "PoetrySkill": {
    "path": "/home/user/mycroft-core/mycroft/skills/Poetry/"
  }
  
  
  this is teh folder whre you have the styles.txt and the poems will be saved
