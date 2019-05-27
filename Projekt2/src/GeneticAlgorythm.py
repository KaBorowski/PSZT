import random
import math
from Network import Network


class GeneticAlg:
    def __init__(self, change, coins, population_length=200, penalty1=10, penalty2=1, mutation_chance=10,
                 iteration=1000, elite=10):
        """
        Inicjalizacja algorytmu
        :param change: reszta do wydania
        :param coins: zbior nominalow waluty
        :param population_length: wielkosc populacji P i R osobnikow
        :param penalty1: wspolczynnik kary niepoprawnej reszty
        :param penalty2: wspolczynnik kary nieoptymalnego rozkladu
        :param mutation_chance: szansa na mutacje osobnika w %
        :param iteration: liczba iteracji algorytmu (brak warunku stopu)
        :param elite: liczba osobnikow elitarnych
        """
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
        """
        funkcja losujaca pojedynczy gen chromosomu, czyli liczbe sztuk danego nominalu
        :return: Ilosc sztuk danego nominalu
        """
        # TODO
        # OKRESLENIE ILOSCI LOSOWANYCH NOMINALOW
        a = math.floor(self.change / self.coins[len(self.coins) - 1]) + 2
        # a = 3
        # print(a)
        x = random.randint(0, a)
        return x

    def random_chromosome(self):
        """
        funkcja losujaca chromoson, czyli zestaw genow, ktorymi jest rozklad nominalow waluty
        :return: Tablica z iloscia sztuk poszczegolnych nominalow
        """
        genes = []
        for i in range(self.chromosome_length):
            genes.append(self.random_gene())

        return genes

    def create_population(self):
        """
        Funkcja tworzaca losowa populacje startowa
        :return: Losowa populacja dla k=1
        """
        population = []
        for i in range(self.population_length):
            population.append(self.random_chromosome())

        return population

    def fitness(self, chromosome):
        """
        Funkcja liczaca funkcje celu dla danego zestawu monet
        :param chromosome: chromosom (zestaw monet), ktorego jakosc sprawdzamy
        :return: Jakosc danego chromosomu
        """
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
        """
        Sortowanie populacji od najlepszego genotypu do najgorszego
        :param population: populacja do posortowania
        :return: posortowana populacja
        """
        tmp = [(self.fitness(x), x) for x in population]
        tmp = sorted(tmp)
        tmp = [x[1] for x in tmp]
        population = tmp

        return population

    def new_population(self, population_p, population_r):
        """
        Tworzenie nowej populacji z populacji P i R. Jesli population_choice_method == 1, to wybor population_length
        najlepszych osobnikow (rozwiazanie slaby w naszym przypadku); w p.p. metoda ruletki, losujaca nowa populacje
        z prawdopodobienstwem zaleznym od jakosci rozwiazania. Dodatkowo implementacja strategii elitarnej
        :param population_p: populacja rodzicow P
        :param population_r: populacja potomkow R
        :return: nowa populacja
        """
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
        """
        Funkcja krzyzujaca dwa genotypy i tworzaca dwa osobniki potomne
        :param mother:
        :param father:
        :return: nowe osobniki potomne
        """

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
        """
        Funkcja mutujaca dany genotym z szansa mutation_chance
        :param child: mutowany genotyp
        :return: zmutowany, badz nie genotyp
        """
        for i in range(0, self.chromosome_length):
            if random.randint(1, 100) <= self.mutation_chance:
                child[i] = self.random_gene()
        return child

    def run(self):
        """
        Funckja uruchamiajaca algorytm genetyczny wyliczajacy reszte i ilosc wydanych monet
        :return: rozklad waluty
        """
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
    network = Network()
    network = network.get_Network()
    # for net in network:
    #     print(net)
    #     for demand in network[net].demandlist:
    #         # print(demand)
    #         for demandpath in demand:
    #             print(demandpath)
