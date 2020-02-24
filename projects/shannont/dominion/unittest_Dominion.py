# -*- coding: utf-8 -*-
"""
Created on  January 19th 2020

@author: shannont
"""
from unittest import TestCase
import testUtility
import Dominion

class TestCard(TestCase):

    def setUp(self):
        #Data setup
        self.players = testUtility.getPlayers()
        self.nV = testUtility.getCurses(self.players)
        self.nC = testUtility.getVictoryCards(self.players)
        self.box = testUtility.GetBoxes(self.nV)
        self.supply_order = testUtility.supplyOrder()
        self.supply = testUtility.fillSupply(self.supply_order,self.nV,self.nC,self.players)
        self.trash = []
        self.player = Dominion.Player('Annie')

    def test_init(self):
        #init the test data
        self.setUp()
        cost = 1
        buypower = 5
        card = Dominion.Coin_card(self.player.name,cost,buypower)

        self.assertEqual('Annie',card.name)
        self.assertEqual(buypower,card.buypower)
        self.assertEqual(cost,card.cost)
        self.assertEqual("coin",card.category)
        self.assertEqual(1,card.vpoints)


    def test_gameover(self):
        self.setUp()

        #test that game is not over because province cards are still in supply
        self.assertEqual(Dominion.gameover(self.supply),False)

        #test that the game is over because at least three of supplies are depleted
        self.supply["Gold"] = []
        self.supply["Duchy"] = []
        self.supply["Estate"] = []
        self.assertEqual(Dominion.gameover(self.supply), True)
        #set supply to zero to test first branch
        self.supply["Province"] = []
        self.assertEqual(Dominion.gameover(self.supply),True)


    def test_react(self):
        pass



class TestActionCard(TestCase):
    def test_initialization(self):
        # first create an aciton card
        card = Dominion.Action_card
        # create test variables for init function of action card
        testName = "Woodcutter"
        testCost = 3
        testActions = 0
        testCards = 0
        testBuys = 1
        testCoins = 2

        card.__init__(card,testName,testCost,testActions,testCards,testBuys,testCoins)

        #test results of init
        self.assertEqual(card.name,testName)
        self.assertEqual(card.cost,testCost)
        self.assertEqual(card.actions,testActions)
        self.assertEqual(card.cards,testCards)
        self.assertEqual(card.buys,testBuys)
        self.assertEqual(card.coins,testCoins)
    def test_use(self):
        #first lets make a player
        player = Dominion.Player('Annie')

        #first lets put an action card in the players hand
        player.hand = [Dominion.Smithy()]

        #now lets 'use' this card
        player.hand[0].use(player,[])

        #the player should have discarded and have no remaining cards in hand
        self.assertEqual(player.hand,[])

        #the players list of played card should no longer be none
        self.assertIsNotNone(player.played)

    def test_augment(self):
        # first lets make a player
        player = Dominion.Player('Annie')

        # give player a basline of buys, actions, and purse to start
        player.actions = 0
        player.buys = 0
        player.purse = 0
        # first lets put an action card in the players hand
        player.hand = [Dominion.Smithy()]

        # now augmenting the card
        player.hand[0].augment(player)

        # check to make sure the augment made correct player changes
        self.assertEqual(player.actions, Dominion.Smithy().actions)
        self.assertEqual(player.buys, Dominion.Smithy().buys)
        self.assertEqual(player.purse, Dominion.Smithy().coins)

    def test_game_over(self):
        self.setUp()


class TestPlayer(TestCase):
    def test_action_balance(self):
        #first make a player
        player = Dominion.Player('Annie')

        #the player has no action cards yet so action balance should return 0
        self.assertEqual(0.0, player.action_balance())

        #giving the player some action cards means the action_balance should return a negative number
        player.deck = [Dominion.Moat()]*10
        self.assertGreater(0.0,player.action_balance())

    def test_calcpoints(self):
        #first make a player
        player = Dominion.Player('Annie')

        #first check that the player should have 3 points to start
        self.assertEqual(player.calcpoints(),3)

        #next lets add a garden to increase the points
        player.hand.append(Dominion.Gardens())
        self.assertGreater(player.calcpoints(),3)

        #now lets add some victory point cards to test it can add properly
        player.hand.append(Dominion.Province())
        player.hand.append(Dominion.Duchy())

        #the total should be 13 points
        self.assertEqual(player.calcpoints(),13)

    def test_draw(self):
        #first make a player
        player = Dominion.Player('Annie')

        #first lets check its able to replenish the deck if a hand is empty
        player.discard = player.deck
        player.deck = []
        self.assertEqual(player.deck,[])
        player.draw()

        #the deck should be resuffled and not empty
        self.assertNotEqual(player.deck,[])

        #now lets check that it make sure it add a card to the players hand
        player.hand = []
        self.assertEqual(player.hand, [])
        player.draw()

        #the player's hand should no longer be empty
        self.assertNotEqual(player.hand,[])

        #check to make sure a card is removed from deck
        player.deck = []
        self.assertEqual(player.deck,[])
        player.deck.append(Dominion.Copper())
        self.assertNotEqual(player.deck,[])
        player.draw()

        #the decks only copper card should have been removed from deck
        self.assertEqual(player.deck,[])

    def test_draw_coverage(self):
        player = Dominion.Player('Annie')
        self.assertNotEqual('NotACard',player.draw().name)
        discardSize = len(player.discard)
        player.deck = []
        player.draw()
        self.assertEqual(discardSize,len(player.deck))
    def test_cardsummary(self):
        # first make a player
        player = Dominion.Player('Annie')
        #player should have 7 copper and 3 estate to start
        summary = player.cardsummary()

        #check to make sure it has 7 coppers
        self.assertEqual(summary['Copper'],7)

        #check to make sure it has 3 estates
        self.assertEqual(summary['Estate'],3)

        #There should be 3 VICTORY POINTS
        self.assertEqual(summary['VICTORY POINTS'],3)

        # Make sure a dictionary is returned
        self.assertEqual(type(summary),type({}))

        #check to make sure its only 0 victory points are returned with an empty stack
        player.hand = []
        player.deck = []

        self.assertEqual(player.cardsummary(),{'VICTORY POINTS': 0})




