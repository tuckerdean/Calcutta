import pandas as pd
import numpy as np
import random
from time import sleep

class Calcutta:
    '''
    Class object to run the calcutta draft based on availability pools.
    '''

    def __init__(self, teamsPath, poolPath, randomSeed):
        '''
        Class object
        '''
        random.seed(randomSeed)
        np.random.seed(randomSeed)

        self.round = 1
        self.teams = pd.read_csv(teamsPath)
        self.pools = pd.read_csv(poolPath)

        self.roundTeam = []
        self.auctionWinner = []

        # Setting up the rounds in which seeding pools change
        self.pools['Round_lag'] = self.pools['Teams Eligible (by seed)'].shift()
        self.pools['New Bucket'] = np.where(
            self.pools['Round_lag'] != self.pools['Teams Eligible (by seed)'],
            1,
            0
        )
        self.roundChanges = list(self.pools.loc[self.pools['New Bucket'] == 1]['Round'])
        self.seedMins = list(self.pools.loc[self.pools['New Bucket'] == 1]['Teams Eligible (by seed)'])

        self.ix = 0

        self.currPool = self.seedMins[self.ix]

        #
        self.teamsAvailable = (
            list(
                self.teams
                .loc[
                (self.teams['Bucket'] == self.currPool)
                ]['Team']
            )
        )

    def pick(self):
        '''
        Object that picks a team at random, based on the existing
        pool
        '''
        if self.round >= 57:
            print("Draft Finished")
            return "Draft Finished"
        random.shuffle(self.teamsAvailable)
        team = self.teamsAvailable.pop()
        seed = self.teams.loc[self.teams['Team'] == team]['Seed'].values[0]
        print(f"Round {self.round}: {seed} {team}")
        self.roundTeam.append((self.round, seed, team))
        self.round += 1

        if self.round <= self.roundChanges[-1]:
            if self.round == self.roundChanges[self.ix + 1]:
                # Updating our indexing
                self.ix += 1
                self.currPool = self.seedMins[self.ix]
                newTeams = list(
                    self.teams
                    .loc[
                    (self.teams['Bucket'] == self.currPool)
                    ]['Team']
                )
                for t in newTeams:
                    self.teamsAvailable.append(t)

        if self.round == 57:
            print("Draft Finished")

    def draft(self):
        '''
        Wrapper for pick function that outputs the entire draft
        '''
        while self.round <= 56:
            self.pick()
            winner = ''
            while len(winner) == 0:
                # This is to avoid double clicking enter
                # and jumping to the next round
                print("Winner of the round is: ")
                winner = input()
            self.auctionWinner.append(winner)
