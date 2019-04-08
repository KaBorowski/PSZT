import random
import math


class GeneticAlg:
    def __init__(self, change, coins, population_length=100, penalty1=1000, penalty2=1000, mutation_chance=10,
                 iteration=100):
        self.change = change
        self.coins = coins
        self.chromosome_length = len(coins)
        self.population_length = population_length
        if self.population_length % 2 != 0:
            self.population_length = population_length + 1
        self.penalty1 = penalty1
        self.penalty2 = penalty2
        self.mutation_chance = mutation_chance
        self.iteration = iteration

        print('test')

    def random_gene(self):
        # TODO
        # OKRESLENIE ILOSCI LOSOWANYCH NOMINALOW
        a = math.floor(self.change/self.coins[len(self.coins)-1])
        # print(a)
        x = random.randint(0, a)
        return x

    def random_chromosome(self):
        genes = []
        for i in range(self.chromosome_length):
            genes.append(self.random_gene())

        return genes

    def create_population(self):
        population = []
        for i in range(self.population_length):
            population.append(self.random_chromosome())

        return population

    def fitness(self, chromosome):
        sum = 0
        coin_count = 0
        for i in range(0, self.chromosome_length):
             sum = sum + chromosome[i] * self.coins[i]
             coin_count = coin_count + chromosome[i]

        err = self.change - sum

        # print(err)
        # print(coin_count)

        return self.penalty1 * err ** 2 + self.penalty2 * coin_count

    def sort_population(self, population):
        tmp = [(self.fitness(x), x) for x in population]
        tmp = sorted(tmp)
        tmp = [x[1] for x in tmp]
        population = tmp

        return population

    def new_population(self, population_p, population_r):
        # population = population_p
        # population.append(population_r)
        population = []
        for i in range(self.population_length):
            population.append(population_p[i])
            population.append(population_r[i])

        population = self.sort_population(population)
        population = [population[x] for x in range(0, self.population_length)]

        return population

    def cross(self, mother, father):
        locus_count = 1
        # locus = []
        # for i in range(locus_count):
        #     tmp = 0
        #     while tmp in locus:
        #         tmp = random.randint(1, self.chromosome- 1)
        #     locus.append(tmp)
        # for i in range(locus_count):
        locus = random.randint(1, self.chromosome_length - 1)
        child1 = []
        child2 = []

        for i in range(self.chromosome_length):
            if i < locus:
                child1.append(mother[i])
                child2.append(father[i])
            else:
                child1.append(father[i])
                child2.append(mother[i])

        return [child1, child2]

    def mutate(self, child):
        for i in range(0, self.chromosome_length):
            if random.randint(1, 100) <= self.mutation_chance:
                child[i] = self.random_gene()
        return child

    def run(self):
        population_p = self.create_population()
        population_p = self.sort_population(population_p)
        best_x = population_p[0]
        for k in range(self.iteration):
            population_r = []
            random.shuffle(population_p)
            for i in range(0, self.population_length, 2):
                children = self.cross(population_p[i], population_p[i - 1])
                population_r.append(children[0])
                population_r.append(children[1])

            for i in range(0, self.population_length):
                population_r[i] = self.mutate(population_r[i])
            population_p = self.new_population(population_p, population_r)
            if self.fitness(population_p[0]) < self.fitness(best_x):
                best_x = population_p[0]

        print(population_p)
        return best_x


if __name__ == '__main__':
    ga = GeneticAlg(change=749, coins=[1, 2, 5, 10, 20, 50, 100, 200, 500])
    # ans = ga.create_population()
    # print(ga.fitness(ans[0]))
    sum = 0
    ans = ga.run()
    print('ROZKLAD MONET = ')
    print(ans)
    print('WYDANA RESZTA = ')
    for i in range(0, ga.chromosome_length):
        sum = sum + ans[i] * ga.coins[i]
    print(sum)
