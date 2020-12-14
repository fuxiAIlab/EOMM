#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
A toy implement of EOMM.

Author: Linxia GONG 巩琳霞 (linxiagong@gmail.com)
Date: 2020-11-20 16:26:44
LastEditors: Linxia GONG 巩琳霞
LastEditTime: 2020-12-14 15:25:37
'''
from utils.loggingAgent import logger
from matchmaking_simulator import MatchmakingSimulator
from EOMM import RandomMM, SkillMM, WorstMM, EOMM

# initialize the matchmakers
matchmakers = [RandomMM(), SkillMM(), WorstMM(), EOMM()]
round_num = 10000
for players_num in [100, 200, 300, 400, 500]:
    avg_retrain = [0,0,0,0]
    for r in range(round_num):
        simulator = MatchmakingSimulator(players_num)  # In each round, matchmakng algorithms are run on the same pool of players
        for m in range(len(matchmakers)):
            matchmaker = matchmakers[m]
            retain_players_num = simulator.run(matchmaker)
            logger.debug('{matchmaker} - round {r} - retain_players_num {retain}'.format(matchmaker=matchmaker, r=r, retain=retain_players_num))
            # -----------------------------------------------------------------
            # We compare different matchmaking methods by the average number of 
            # their retained players per round, i.e., the players who continue 
            # playing in the next eight hours
            # -----------------------------------------------------------------
            avg_retrain[m] = (avg_retrain[m]*r + retain_players_num)/(r+1)
    logger.info('SETTING: players_num: {}, rounds:{} | RESULT: avg_retain of {}: {}'.format(players_num, r+1, matchmakers, avg_retrain))