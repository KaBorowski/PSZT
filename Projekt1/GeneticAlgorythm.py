import random
import math


class GeneticAlg:
    def __init__(self, change, coins, population_length=100, penalty1=10, penalty2=1, mutation_chance=10,
                 iteration=1000, elite=1):
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
        self.elite = elite

    def random_gene(self):
        # TODO
        # OKRESLENIE ILOSCI LOSOWANYCH NOMINALOW
        # a = math.floor(self.change / self.coins[len(self.coins) - 1]) + 3
        a = 3
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
        population_choice_method = 2

        population = []
        for i in range(self.population_length):
            population.append(population_p[i])
            population.append(population_r[i])

        population = self.sort_population(population)

        if population_choice_method == 1:  # mi najlepszych osobnikow
            population = [population[x] for x in range(0, self.population_length)]

        else:  # metoda ruletki
            tmp_population = []
            population_size = len(population)
            for i in range(self.elite):  # Zachowanie elitarnych osobnikow
                tmp_population.append(population[i])
                del population[i]
                population_size = population_size - 1

            tmp = [(1.0 / self.fitness(x), x) for x in population]
            tmp.reverse()
            error_sum = 0
            for i in range(len(tmp)):
                error_sum = error_sum + tmp[i][0]
            tmp = [(x[0] / error_sum, x[1]) for x in tmp]

            sum = 0
            roulette = []
            for i in range(len(tmp)):
                sum = sum + tmp[i][0]
                roulette.append([sum, tmp[i][1]])

            roulette = [(x[0] * 10000, x[1]) for x in roulette]

            for i in range(self.population_length - self.elite):
                rand = -1
                item = self.random_chromosome()
                while rand != -1 and item in tmp_population:
                    rand = random.randint(0, 9999)
                    item = next(x[1] for x in roulette if rand <= x[0])
                tmp_population.append(item)

            population = tmp_population

        return population

    def cross(self, mother, father):

        cross_method = 2
        child1 = []
        child2 = []
        if cross_method == 1:
            locus = random.randint(1, self.chromosome_length - 1)

            for i in range(self.chromosome_length):
                if i < locus:
                    child1.append(mother[i])
                    child2.append(father[i])
                else:
                    child1.append(father[i])
                    child2.append(mother[i])
        else:
            parent = True

            locus_count = math.floor(self.chromosome_length / 3)
            locus = []
            for i in range(locus_count.__int__()):
                tmp = 0
                while tmp in locus:
                    random.randint(1, self.chromosome_length - 1)
            for i in range(self.chromosome_length):
                if i in locus:
                    parent = not parent
                if parent:
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
            # random.shuffle(population_p)
            for i in range(0, self.population_length, 2):
                mother = 0
                father = 1
                children = [self.random_chromosome(), self.random_chromosome()]
                while (mother == father) or (children[0] in population_p) or (children[1] in
                                                                              population_p):
                    mother = random.randint(0, self.population_length - 1)
                    father = random.randint(0, self.population_length - 1)
                    children = self.cross(population_p[mother], population_p[father])
                    children[0] = self.mutate(children[0])
                    children[1] = self.mutate(children[1])

                population_r.append(children[0])
                population_r.append(children[1])

            population_p = self.new_population(population_p, population_r)
            if self.fitness(population_p[0]) < self.fitness(best_x):
                best_x = population_p[0]

        print(population_p)
        return best_x


if __name__ == '__main__':
    ga = GeneticAlg(change=839, coins=[1, 2, 5, 10, 20, 50, 100, 200, 500])
    sum = 0
    ans = ga.run()
    print('ROZKLAD MONET = ')
    print(ans)
    print('WYDANA RESZTA = ')
    for i in range(0, ga.chromosome_length):
        sum = sum + ans[i] * ga.coins[i]
    print(sum)
