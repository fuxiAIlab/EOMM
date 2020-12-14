<!--
 * @
 * 
 * @Author: Linxia GONG 巩琳霞 (linxiagong@gmail.com)
 * @Date: 2020-11-25 11:58:17
 * @LastEditors: Linxia GONG 巩琳霞
 * @LastEditTime: 2020-12-14 17:28:09
-->
# About this repo
**This is a toy reproduction of the paper**  [*(WWW'17) EOMM: An Engagement Optimized Matchmaking*](http://web.cs.ucla.edu/~yzsun/papers/WWW17Chen_EOMM).

We are research engineers working on game matchmaking optimization domain. The idea of EOMM paper is interesting, so we reproduced the framework and the matchmaking procedure, according to the description in the paper.

本项目是对EOMM论文的复现。

# 1. RUN THE CODE / 运行代码

### - First tryout / 快速运行匹配仿真

```shell
$ cd EOMM
$ pip install -r requirements.txt  # use pip3 if you have both python2 and python3 in your environment
$ python main.py  # log file will be generated into ./log folder
```
You can see the simulation result both from your console and log file in `./log` folder.

仿真过程可以从控制台看到，也可以从./log文件夹下找到日志文件。

### - Code files / 代码结构

```shell
EOMM
├── EOMM.py                   # the matchmakers, including WorstMM, SkillMM, RandomMM, EOMM
├── Matchmaking_simulator.py  # the matchmaking simulator
├── main.py                   # the main process to run a simulation
├── log                       # folder to keep log files
```

### - Customize your matchmaking simulation / 修改仿真参数

In the file `main.py`, you can edit the variables 

- matchmakers: the matchmakers to compare in the simulation
- round_num: the round of matchmaking simulation for a given player_num
- player_num: the size of waiting pool of player for simulation

An example: 

```python
round_num=10000, player_num=100
matchmakers = [RandomMM(), SkillMM(), WorstMM(), EOMM()]
```

1. At each round, we create a pool of 100 players;

2. The matchmakers (RandomMM, SkillMM, WorstMM, EOMM) apply on these 100 players; we calculate the retain players of each matchmaker as its performance;
3. We take the average retain of the 10000 matchmaking rounds as the performance of the matchmaker on 100 players

**Now you can play around with the codes.**

# 2. Summary of EOMM algorithm / 论文算法简述

Argument: the intuitive assumption that a fair game is best player experience sometimes fails, and matchmaking based on fairness is not optimal for engagement. 

Goal: maximize overall player engagement

**EOMM:**

- first measures players disengagement by their churn risk after each matchmaking decision;
- secondly models all players who wait in the matchmaking pool as a complete graph, where each player is a node and the edge between two players is their sum churn risks if paired;
- achieven matchmaking desicion by solving a *minimum weight perfect matching* problem that finds non-overlapping pairs with the minimal sum of edge weights on a complete graph.

Limits: it applies to 1-vs-1 matches only.

从匹配系统的角度来说，公平的比赛不一定是用户体验/用户参与度最高的。本文针对最大化用户参与度的目标进行匹配过程的建模。EOMM的匹配过程为：

- 以某次匹配之后用户的流失率作为用户参与度的度量
- 基于等待队列中的所有玩家构建一张Graph，每个玩家作为一个节点，节点间的权重为当这两个玩家被匹配到同一场次时的二人流失率的总和
- 通过在该Graph上求解最小权完美匹配得到玩家间的两两匹配结果

该算法仅适用1-vs-1玩法的匹配。



# 3. Graph Matching implementation / 关于图匹配算法实现

The graph matching problem is sovled by ***networkx*** (see  [max_weight_matching](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.matching.max_weight_matching.html?highlight=max_weight#networkx.algorithms.matching.max_weight_matching) for more details).

- For the ease of graph matching, churn/retain rate values are in percentage (*100%)

- WorstMM (minimize the engagement) is to maximize the total churn weight(i.e. churn rate of p<sub>i</sub> + churn weight of p<sub>j</sub>) of the paired nodes
- EOMM is transformed into max weight matching on the retain weight (i.e. 200-churn weight)