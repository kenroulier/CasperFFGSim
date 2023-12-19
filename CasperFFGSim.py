"""
    Description: Python progam to simulate the Proof of Stake Consensus Algo (Casper FFG)

    Casper FFG consists of two layers:
    1. The bottom layer is the tree of transactions.
    2. The top layer is the sub-tree of checkpoints extracted from the tree of transactions.

    Instructions:
            1. There are 10 validators in the system. The set of the validators are fixed. The deposits of the validators are given.
            2. The checkpoint tree is a full binary tree.
            3. Each node/checkpoint in the checkpoint tree has a number associated with it. Given a node of number 𝑛,
                its left child is 2𝑛+1, and its right child is 2𝑛+2. The root node is labeled 0.  This is the node index in the code below.
            4. The length of the link contained in each vote is always 1.
            5. For each vote, the probability of selecting the left child as the target is the same as the probability
                of selecting the right child.
            6. If the sum of the deposits of the validators voting for a link L exceeds 1/2 of the total deposit,
                L is the supermajority link. (Note: this is different from the 2/3 rule used in real Casper FFG.)

            Starting from the genesis node, this will run the Proof-of-Stake (PoS)-based voting 10 rounds,
            which yields 10 supermajority links

    Notes:
      Checkpoint spacing is 1 so that every block has to go through consensus
    --------------------------------------------------------------------------------
"""

from random import randint
import sys
import argparse

class CheckTreeNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.index = None
        self.desc = None
        self.parent = None

    def insertnode(self, lindex, rindex, parent):

        if self.index is None:
            self.index = 0
            self.desc = "Root"
            self.parent = parent
            self.state = "Finalized"

        else:
            self.right = CheckTreeNode()
            self.right.index = rindex
            self.right.desc = "Right"
            self.right.parent = parent

            self.left = CheckTreeNode()
            self.left.index = lindex
            self.left.desc = "Left"
            self.left.parent = parent

    def printtree(self):
        print("Index,", self.left.index, "is the ", self.left.desc, "child with parent index", self.left.parent)
        print("Index,", self.right.index, "is the ", self.right.desc, "child with parent index", self.right.parent)


"""-------------------------------------------------------------------------"""

def get_a_winner(Validators):

    voteleft = 0
    voteright = 0

    # total up the balances so we know when 1/2 of deposits are achieved to determine a supermajority
    bal_total = 0
    tmp = 0
    
    for x in Validators:
        bal_total = bal_total + Validators[tmp][1]
        tmp = tmp + 1

    bal_to_win = bal_total / 2

    # begin the voting
    print("\nStarting voting to find winning child\n")

    print("\n        Left Voter:                          Right Voter:")
    print("   ______________________________     ____________________________\n")

    votecount = 0

    for x in Validators:

        valname = Validators[votecount][0]
        valbal = Validators[votecount][1]
        votecount = votecount + 1

        randomvote = randint(0, 1)

        if randomvote == 0:
            print("  ", valname, "bal=", valbal)
            voteleft = voteleft + valbal
        else:
            voteright = voteright + valbal
            print("                                    ", valname, "bal=",valbal)            

        if voteleft > bal_to_win:
            winner = "left"
            print("\nTotal balance of deposits for winning vote=",voteleft, "out of",bal_total)
            return (winner)

        if voteright > bal_to_win:
            winner = "right"
            print("\nTotal balance of deposits for winning vote=",voteright, "out of",bal_total)
            return (winner)

"""-----------------------------"""
def main():

    def print_tree_state(winindex, loseindex, parent, sl):
        print("Index", winindex, "is now Justified (1st vote) and Index", loseindex, "does not move forward")
        print("Parent Index", parent, "is now Finalized (2nd vote)")
        print("Superlink", sl, ": (source)", parent,"->",winindex,"(target) has been established\n")


    #allow the user to pass in the number of voting rounds
    argParser = argparse.ArgumentParser()
    argParser.add_argument("votes", help="enter number of rounds to vote",type=int)
    args = argParser.parse_args()

    if args.votes <= 0:
        voterounds = 10     #default to 10
    else:
        voterounds =  args.votes

    print("\n***** Simulation will perform ", args.votes,"rounds of voting ****\n")

    #create a list of validators
    Validators = [("validator0",500),("validator1",100),("validator2",300),
                  ("validator3",250),("validator4",150),("validator5",500),
                  ("validator6",650),("validator7",300),("validator8",200),
                  ("validator9",150)]

    #create the root
    root = CheckTreeNode()
    root.insertnode(lindex=None, rindex=None, parent=None)
    print("\n\n========  Created the root ========\n")

    n = 0   # this is the tree height so we can do (2n + 1) and (2n + 2) logic

    #create the children to the parent in pairs (left and right)
    lindex = 2*n+1
    rindex = 2*n+2
    prevparent = 0

    while (n <= voterounds):

        if (n == 0):
            print("========  creating children for Root ========\n")
            root.insertnode(lindex, rindex, parent=n)
            root.printtree()
            n = 1  # go ahead and put move to the 1st height in the tree

        # we can start with picking the previous winner of the children
        winner = get_a_winner(Validators)

        lparent = lindex        #establish the left parent
        rparent = rindex        #establish the right parent

        lindex = 2*n+1
        rindex = 2*n+2

        if (winner == "left"):

            print("\nHeight", n, "winner, index:",lparent,"-",winner,"child\n")
            print_tree_state(lparent, rparent, prevparent, n)
            prevparent = lparent

            #build left node in pairs.  Use lparent for printing since lindex has already advanced

            if (n < voterounds): #only get next set of children if more voting is needed
                print("\n========  creating children for height ", n, "========\n")
                root.left.insertnode(lindex, rindex, lparent)
                root.left.printtree()

        if (winner == "right"):

            print("\nHeight", n, "winner is index:",rparent,"-",winner,"child\n")
            print_tree_state(rparent, lparent, prevparent, n)
            prevparent = rparent

            #build left node in pairs
            if (n < voterounds): #only get next set of children if more voting is needed
                print("\n========  creating children for height ", n, "========\n")
                root.right.insertnode(lindex, rindex, rparent)
                root.right.printtree()

        n = n + 1

#                print("Parent", self.left.parent, "is Finalized")

if __name__ == '__main__':
    main()
