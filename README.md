# genetic-algorithm-blackjack-strategy
UCI COSMOS 2021 - Optimization of Blackjack Strategy through a Genetic Algorithm:
Mihir Arya (RGBmarya), Sharon Chen (23chensharon), Jacob Parmacek, Anirudh Raja (anirudhraja1), Amratha Rao (Amru-13579)

Instructions

	1. Run blackjack_data.py - obtain random game data
		i. Edit file path on line 222
		ii. Edit argument on line 224 to change number of blackjack games simulated
	2. Run genetic_algorithm.py - create optimal strategy table
		i. Edit file path on line 33 (same file path as 1.i.)
		ii. Edit file path on line 216
	3. Run blackjack_plot.py - simulate games and plot game data (optimal strategy table vs. dealer)
		i. Edit file path on line 13 (same file path as 2.ii.)
		ii. Edit file paths on line 213, line 217, and line 235
		iii. Edit argument on line 257 to change number of blackjack games simulated
	
	




**Abstract**

	With high risks and gambling, Blackjack is one of many calculative card games out there. 
	With tensions running high between the dealer and the players, decisions and uncertainties remain constant throughout the rounds. 
	In 1960, Edward O. Thorp, a professor and mathematician at UC Irvine and Blackjack strategist, released the optimal strategy for Blackjack in his book Beat the Dealer. 
	This strategy outlines rules and moves to create the most ideal play for the participants. 
	However, with the rise of AI and Machine learning, the hopes of there being a truly superior strategy have arisen. 
	How can a player maximize their wins in Blackjack through AI?
	Can the Thorp’s Basic Strategy Table be replicated or improved through machine learning? Can Genetic Algorithms provide constructive results?
	By developing a Blackjack strategy through a genetic algorithm, this project offers detailed comparisons between 
	Thorp’s Basic Strategy, the Random Strategy, and the Genetic Algorithm, 
	ultimately concluding a Genetic Algorithm can produce close results to Thorp’s Basic Strategy given sufficient time and compute power.



**Introduction**

 	Blackjack
	    Players try to acquire cards with a value as close to 21 as possible without going over
	    Players can “hit” (receive a card) or “stand” (yield turn)
	    House Rules: Dealer must hit on a hard 17 or more

	Basic Strategy Table: https://images-na.ssl-images-amazon.com/images/I/816DFf5i0EL.jpg 

 	Genetic Algorithm
	    Initial population - Set of solutions to a problem
	    Fitness function - Determines how fit a solution is in comparison to other solutions
	    Selection - Pair of fittest solutions are selected 
	    Crossover - Offspring created by exchanging parent genes until random crossover point
	    Mutation - Some of the offspring’s genes mutate randomly



**Research Questions**

	  How can a player maximize their wins in Blackjack through AI?
	  How effective is the Basic Strategy Table against a dealer? 
	  Can the Basic Strategy Table be replicated or improved through machine learning?



**Methods**

 	Obtain Game Data
    		Simulated ten million Blackjack games with a randomized strategy (equal chance to hit or stand) to obtain game data (hand, decision, upcard, outcome, etc.)

 	Genetic Algorithm
		Used genetic algorithm and game data to create strategy table row-by-row 
		17 populations, each with 20 random rows of length 10 (each population corresponds to hard total)
		Fitness of row in population ∝ probability of winning given current row 
		Evaluated win probability based on stored game data

  	Simulate Games
		Simulated one million games using strategy table against dealer and plotted results


**Results & Conclusion**

	Overall Findings
		Obtained win percentage of 38.4% with 1 million simulations.
		Improved from random strategy (31.60%) but not as successful as Basic Strategy (43.30%)
		Final strategy inclined to standing more than hitting

	Sources of Error
		Limited simulations and compute power
		Arbitrary fitness function and penalty values
		Implementation of the genetic algorithm relies on randomized game data, which may not have had data on every hand
    
	Future work
		Use final strategy table to generate new game data and run genetic algorithm on said data
		Add in soft and hard totals (ace value is 1 or 11)
		Betting functionality in general (add split and double)
    
   
   
**References**

	  Gad, A. (2018, July 3). Introduction to optimization with genetic algorithm. Medium. https://towardsdatascience.com/introduction-to-optimization-with-genetic-algorithm-2f5001d9964b.
	  Gad, A. (2020, May 6). Genetic algorithm implementation in Python. Medium. https://towardsdatascience.com/genetic-algorithm-implementation-in-python-5ab67bb124a6.
	  Hao, K. (2021, April 5). What is machine learning? MIT Technology Review. https://www.technologyreview.com/2018/11/17/103781/what-is-machine-learning-we-drew-you-another-flowchart/.
	  Mallawaarachchi, V. (2020, March 1). Introduction to genetic algorithms - including example code. Medium. https://towardsdatascience.com/introduction-to-genetic-algorithms-including-example-code-e396e98d8bf3.
	  Ponsen, M., Spronck, P., Muñoz-Avila, H., & Aha, D. W. (2007, April 7). Knowledge acquisition for adaptive game ai. Science of Computer Programming. https://www.sciencedirect.com/science/article/pii/S0167642307000548.
	  Sommerville, G. (2019, February 12). Winning blackjack using machine learning. Medium. https://towardsdatascience.com/winning-blackjack-using-machine-learning-681d924f197c.
	  Spronck, P., Ponsen, M., Sprinkhuizen-Kuyper, I., & Postma, E. (2006, March 9). Adaptive game ai with dynamic scripting. Machine Learning. https://link.springer.com/article/10.1007/s10994-006-6205-6.
	  Yakowitz, S., & Kollier, M. (2002, March 21). Machine learning for optimal blackjack counting strategies. Journal of Statistical Planning and Inference. https://www.sciencedirect.com/science/article/abs/pii/0378375892900019. 
	  Images: Mallawaarachchi, V. (2020, March 1). Introduction to genetic algorithms - including example code. Medium. https://towardsdatascience.com/introduction-to-genetic-algorithms-including-example-code-e396e98d8bf3.


