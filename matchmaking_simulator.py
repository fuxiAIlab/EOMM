#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''


Author: Linxia GONG 巩琳霞 (linxiagong@gmail.com)
Date: 2020-11-20 14:41:14
LastEditors: Linxia GONG 巩琳霞
LastEditTime: 2020-12-14 16:10:32
'''
import random
import time
import math
import uuid
import networkx as nx
from utils.loggingAgent import logger

# ************************************
# Player
# ************************************
class Player(object):
    def __init__(self, player_id=None, **param):
        self._player_id = str(uuid.uuid1()) if player_id is None else player_id
        self._mmr = random.randint(1,100)
        self._latest_win_seq = [random.choice([1,-1]) for i in range(2)]

    @property
    def player_id(self):
        return self._player_id

    @property
    def mmr(self):
        # the MMR property.
        return self._mmr

    @property
    def latest_win_seq(self):
        # win:1, lose:-1, draw:0
        return self._latest_win_seq

# ************************************
# PlayersGraph: 
# A complete graph (each pair of players are connected)
# for solving the minimum weight perfect matching problem
# ************************************
class PlayersGraph(nx.Graph):
    def __init__(self):
        super().__init__()

    def load_players(self, players):
        self._add_players(players)
        self._calc_link_weight(players)
        return self

    def _add_players(self, players):
        for p in players:
            self.add_node(p.player_id)

    def _calc_link_weight(self, players):
        for i in range(len(players)):
            pi = players[i]
            for j in range(i+1,len(players)):
                pj = players[j]
                churn_rate= predict_pair_churn(pi, pj)
                self.add_edge(pi.player_id, pj.player_id, churn_weight=churn_rate, retain_weight=200-churn_rate)

# ************************************
# A simplified(temporary) method to calculate the churn weight in the PlayersGraph
# ************************************
def predict_win(pi, pj):
    '''
    Description: predict win rate of player pi, against player pj. 
        Here we adopt ELO algorthm for the ease of computation.
    Param:
        pi,pj: Player instance
    Return:
        Pi_win, Pi_draw, Pi_lose
    '''
    # assert isinstance(pi, Player)
    # assert isinstance(pj, Player)
    Pi_win = 1/(1+math.pow(10, (pj.mmr-pi.mmr)/400))
    Pi_draw = 0
    Pi_lose = 1-Pi_win-Pi_draw
    return Pi_win, Pi_draw, Pi_lose

def predict_individual_churn(p, next_outcome):
    '''
    Description: To simplify the churn prediction of individual player, the churn probability
        is set to be statistical churn_rate(*100%) according to the latest+predicted match outcomes.
    Param: 
		p: the player
        next_outcome: predicted match outcome, 1 for win, -1 for lose, 0 for drawn
    Return: 
		churn_rate: churn rate(*100%)  of p with the given predicted outcome
    '''
    # assert isinstance(p, Player)
    outcome_seq = p.latest_win_seq[-2:] + [next_outcome]
    if outcome_seq == [1,1,1]:
        churn_rate = 37
    elif outcome_seq == [1,1,-1]:
        churn_rate = 49
    elif outcome_seq == [1,-1,1]:
        churn_rate = 46
    elif outcome_seq == [-1,1,1]:
        churn_rate = 43
    elif outcome_seq == [-1,1,-1]:
        churn_rate = 37
    elif outcome_seq == [-1,-1,1]:
        churn_rate = 27
    elif outcome_seq == [1,-1,-1]:
        churn_rate = 56
    elif outcome_seq == [-1,-1,-1]:
        churn_rate = 61
    else:
        churn_rate = 50
    return churn_rate

def predict_pair_churn(pi, pj):
    '''
    Description: predict the churn weight when a pair of players are assigned together
    Param: 
		pi, pj: the pair of players
    Return: 
		churn: pairwise churn weight 
    '''
    # assert isinstance(pi, Player)
    # assert isinstance(pj, Player)
    Pi_win, Pi_draw, Pi_lose = predict_win(pi, pj)
    churn = Pi_win*(predict_individual_churn(pi, next_outcome=1)+predict_individual_churn(pj, next_outcome=-1)) \
        + 0 \
            +Pi_lose*(predict_individual_churn(pi, next_outcome=-1)+predict_individual_churn(pj, next_outcome=1))
    return churn
# ************************************
# Matchmakers
# ************************************
# The 4 matchmakers are written in EOMM.py

# ************************************
# MatchmakingSimulator
# ************************************
class MatchmakingSimulator(object):
    def __init__(self, players_num=100):
        # 1. Create a waiting pool of P players, whose player states are
        #   sampled from the player state collection.
        self.players_num =  players_num
        self.get_players(players_num)

    def get_players(self, players_num):
        self.players_dict = {id_:Player(player_id=id_) for id_ in range(players_num)}
        self.players = list(self.players_dict.values())
        logger.info('players: '+str([p.player_id for p in self.players]))
        self.players_graph = PlayersGraph().load_players(self.players)
        logger.debug('self.players_graph.nodes(): '+str(self.players_graph.nodes()))
        logger.debug('self.players_graph.edges(): '+str(self.players_graph.edges.data()))

    def get_matches(self):
        pass

    def evaluate(self):
        # success rate
        # match quality
        pass

    def run(self, matchmaker):
        # -----------------------------------------------------------------
        # 1. Create a waiting pool of P players, whose player states are
        #   sampled from the player state collection.
        # WE MOVED THIS STEP TO THE INITIALIZATION OF THE SIMULATOR, TO 
        # MAKE THE P PLAYERS SHARED BY THOSE MATCHMAKERS, FOR COMPARISON PURPOSE.
        # -----------------------------------------------------------------
        # self.get_players(players_num)
        
        # -----------------------------------------------------------------
        # 2. Use M to determine the pair assignment (matchmaking).
        # -----------------------------------------------------------------
        if matchmaker in ['EOMM', 'WorstMM']:
            res = matchmaker.run(self.players_graph)
        else:
            res = matchmaker.run(self.players)
        logger.info(str(matchmaker)+' matchmaking res: '+str(res))
        # -----------------------------------------------------------------
        # 3. Simulate match outcomes according to the win/lose/draw probability predicted by the skill model
        # 4. For each player, simulate if he will churn according to the predicted churn probability by churn model.
        # 5. Record the number of retained players
        # WE SIMPLIFIED THIS PROCESS BY PICKING THE CALCULATED PAIRWISE RETAIN WEIGHTS
        # -----------------------------------------------------------------
        retain_players_num = 0
        retain = nx.get_edge_attributes(self.players_graph,'retain_weight')
        # logger.info(retain)
        for pair in res:
            if pair not in retain.keys():
                pair = (pair[1], pair[0])
            # logger.info(retain[pair])
            retain_players_num += retain[pair]/100
        return retain_players_num