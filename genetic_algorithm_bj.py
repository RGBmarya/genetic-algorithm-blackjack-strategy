"""
START
Generate the initial population
Compute fitness
REPEAT
    Selection
    Crossover
    Mutation
    Compute fitness
UNTIL population has converged
STOP
"""
import random
import ast
import numpy as np

final_table = []

class Individual:

    def __init__(self, player_hard_total):
        self.player_hard_total = player_hard_total
        self.fitness = 100
        self.genes = []
        self.gene_length = 10

        for i in range(self.gene_length):
            self.genes.append(random.randint(0, 1))

    # Calculate and update fitness of individual

    def calc_fitness(self):
        path = ""
        with open(path, 'rb') as f:
            game_data = np.load(f, allow_pickle=True)

        self.fitness = 100

        # i is dealer upcard
        for i in range(1, 13):
            indices = np.where(np.logical_and(game_data.transpose()[
                               2] == self.player_hard_total, game_data.transpose()[4] == (9 if i == 1 else min(i, 10) - 2)))
            if indices[0].size == 0:
                continue
            gene = self.genes[min(i, 10) - 2]
            outcomes = game_data.transpose()[0][indices]
            choices = game_data.transpose()[3][indices]

            num_win_and_gene = len(
                np.where(np.logical_and(outcomes == 1, choices == gene))[0])
            num_gene = len(np.where(choices == gene)[0])
            try:
                prb_win_given_gene = num_win_and_gene / num_gene
            except:
                continue

            if prb_win_given_gene < 0.05:
                self.fitness -= 10
            elif prb_win_given_gene < 0.10:
                self.fitness -= 8
            elif prb_win_given_gene < 0.20:
                self.fitness -= 6
            elif prb_win_given_gene < 0.30:
                self.fitness -= 4
            elif prb_win_given_gene < 0.40:
                self.fitness -= 2


class Population:

    def __init__(self, hard_total):
        self.pop_size = 20
        self.individuals = []
        self.max_fitness = 0
        self.hard_total = hard_total
        self.initialize_pop()

    # Initialize population with "pop_size" individuals
    def initialize_pop(self):
        for i in range(self.pop_size):
            self.individuals.append(Individual(self.hard_total))

    # Return fittest individual object
    # Update max_fitness
    def get_fittest(self):
        fittest = self.individuals[0]
        for indiv in self.individuals:
            if indiv.fitness > fittest.fitness:
                fittest = indiv
        self.max_fitness = fittest.fitness
        return fittest

    # Return second fittest individual object
    def get_second_fittest(self):
        fittest_index = 0
        second_fittest_index = 0
        for i, indiv in enumerate(self.individuals):
            if indiv.fitness > self.individuals[fittest_index].fitness:
                second_fittest_index = fittest_index
                fittest_index = i
            elif indiv.fitness > self.individuals[second_fittest_index].fitness:
                second_fittest_index = i
        return self.individuals[second_fittest_index]

    def get_least_fit_index(self):
        least_fittest_index = 0
        for i, indiv in enumerate(self.individuals):
            if indiv.fitness < self.individuals[least_fittest_index].fitness:
                least_fittest_index = i
        return least_fittest_index

    # Calculate and update fitness for each individual in population
    # Return fittest individual object
    # Update max_fitness

    def calculate_fitness(self):
        for i in self.individuals:
            i.calc_fitness()
        self.get_fittest()


# Create population object
for ht in range(4, 21):
    population = Population(ht)
    print(f"Hard Total: {ht}")


# Select and return two parents (tuple) with greatest fitness


    def selection(pop):
        fittest = pop.get_fittest()
        second_fittest = pop.get_second_fittest()
        return fittest, second_fittest

    # Crossover genes of parents --> offspring produced (fittest = fittest offspring, second_fittest = second fittest offspring)
    def crossover(pop, fittest, second_fittest):
        cross_over_point = random.randint(0, pop.individuals[0].gene_length)
        for i in range(cross_over_point):
            temp = fittest.genes[i]
            fittest.genes[i] = second_fittest.genes[i]
            second_fittest.genes[i] = temp

    # Helper function
    def bit_flip(indiv, index):
        if indiv.genes[index] == 0:
            indiv.genes[index] = 1
        else:
            indiv.genes[index] = 0

    # Randomly mutate single gene in each offspring
    def mutation(pop, fittest, second_fittest, num_mutations):
        for i in range(num_mutations):
            mutation_point = random.randint(
                0, pop.individuals[0].gene_length - 1)
            bit_flip(fittest, mutation_point)

            mutation_point = random.randint(
                0, pop.individuals[0].gene_length - 1)
            bit_flip(second_fittest, mutation_point)

    # Return fittest offspring
    def get_fittest_offspring(fittest, second_fittest):
        if fittest.fitness > second_fittest.fitness:
            return fittest
        return second_fittest

    # Replaces least fit individual in population with fittest offspring
    def add_fittest_offspring(pop, fittest, second_fittest):
        fittest.calc_fitness()
        second_fittest.calc_fitness()

        least_fit_index = pop.get_least_fit_index()
        pop.individuals[least_fit_index] = get_fittest_offspring(
            fittest, second_fittest)

    # Generation Count
    generation_count = 0

    # Calculate and update fitness for each individual in initialized population
    # Update max_fitness of population
    population.calculate_fitness()

    # Repeat until all bits of individual are 1
    while population.max_fitness < 75:
        generation_count += 1

        # Select two parents
        parents = selection(population)

        # Cross over genes of parents
        crossover(population, *parents)

        # offspring produced
        offspring = parents

        # 25% chance of mutation in offspring
        # if random.randint(0, 100) <= 50:
        mutation(population, *offspring, 4)

        # Replaces least fit individual in population with fittest offspring
        add_fittest_offspring(population, *offspring)

        # Calculate and update fitness for each individual in population
        # Update max_fitness
        population.calculate_fitness()

        print(
            f"Generation: {generation_count}   Fittest:{population.max_fitness}")

    final_table.append(population.get_fittest().genes)
    print(f"Genes: {''.join(str(g) for g in population.get_fittest().genes)}")
    print(f"Fitness: {population.max_fitness}\n")

final_table = np.asarray(final_table)
np.save("", final_table)
print(final_table)
