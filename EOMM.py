#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
The Matchmaking Algorithms (i.e. matchmakers)

Author: Linxia GONG 巩琳霞 (linxiagong@gmail.com)
Date: 2020-11-20 14:40:30
LastEditors: Linxia GONG 巩琳霞
LastEditTime: 2020-12-10 17:56:18
'''
import random
import networkx as nx
from networkx.algorithms.matching import max_weight_matching, is_perfect_matching
from matchmaking_simulator import PlayersGraph
from utils.loggingAgent import logger

# TODO 写一个Matchmaker的父类，作为接口类

class RandomMM(object):
    def __repr__(self):
        return "RandomMM"

    def run(self, players):
        pair_num = int(len(players)/2)
        res = []
        players_sort = list(players)
        random.shuffle(players_sort)
        for i in range(pair_num):
            pair = (players_sort.pop().player_id, players_sort.pop().player_id)
            res.append(pair)
        return res


class SkillMM(object):
    def __repr__(self):
        return "SkillMM"

    def run(self, players):
        pair_num = int(len(players)/2)
        res = []
        players_sort = sorted(players, key=lambda p: p.mmr)
        for i in range(pair_num):
            pair = (players_sort.pop().player_id, players_sort.pop().player_id)
            res.append(pair)
        return res


class WorstMM(object):
    def __repr__(self):
        return "WorstMM"

    def run(self, players):
        if not isinstance(players, PlayersGraph):
            players = PlayersGraph().load_players(players)
        return max_weight_matching(players, maxcardinality=False, weight="churn_weight")

class EOMM(object):
    def __repr__(self):
        return "EOMM"

    def run(self, players):
        # logger.info('isinstance(players, PlayerGraph)= '+str(isinstance(players, PlayerGraph)))
        if not isinstance(players, PlayersGraph):
            # logger.info(type(players))
            players = PlayersGraph().load_players(players)
        return max_weight_matching(players, maxcardinality=False, weight="retain_weight")
        # return max_weight_matching(players.G, maxcardinality=False, weight="weight")