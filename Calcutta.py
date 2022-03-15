import pandas as pd
import numpy as np
import random
import sys
from time import sleep

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}Round {self.round}: {seed} {team}{bcolors.ENDC}")
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
                print(f"{bcolors.WARNING}Winner of the round is: {bcolors.ENDC}")
                winner = input(f'{bcolors.FAIL}')
            self.auctionWinner.append(winner)

if __name__ == "__main__":
    random_seed = int(sys.argv[1])
    c = Calcutta('teams_2022.csv', 'round_eligibility_2022.csv', random_seed)
    c.draft()
