import numpy as np
import math
import matplotlib.pyplot as plt

# SEIR states
susceptible = 0
exposed = 8
infectious = 10
recovered = 4

# temp use
exposed_temp = -1
infectious_temp = -2

N = 660000 # 总人口
N_infected = 26  # 初始感染人口
N_recovered = 517440  # 群体免疫阈值
beta = 0.3 # 传染率
gamma = 1 / 10 # 恢复率
sigma = 1 / 5 # 暴露人员变为感染的概率

# the number of each state during the simulation
susceptible_list = []
exposed_list = []
infectious_list = []
recovered_list = []


# count the number of each state
def count_susceptible(population: np.ndarray):
    return int(np.sum(population == susceptible))


def count_exposed(population: np.ndarray):
    return int(np.sum(population == exposed))


def count_infectious(population: np.ndarray):
    return int(np.sum(population == infectious))


def count_recovered(population: np.ndarray):
    return int(np.sum(population == recovered))


# init U.K. population
def init_pop(num: int, num_infected: int, num_recovered: int = 0):
    length = math.floor(math.sqrt(num))
    population = np.zeros((length, length))
    population += susceptible
    if num_recovered:  # init recovered people
        rows = np.random.choice(range(length), num_recovered)
        columns = np.random.choice(range(length), num_recovered)
        for i in range(num_recovered):
            population[rows[i]][columns[i]] = recovered
    rows = np.random.choice(range(length), num_infected)
    columns = np.random.choice(range(length), num_infected)
    for i in range(num_infected):  # init infected people
        population[rows[i]][columns[i]] = infectious
    return population


# infect one cell
def infect(population: np.ndarray, i: int, j: int):
    if population[i][j] != susceptible:  # if this cell is not susceptible, just return
        return
    elif np.random.binomial(n=1, p=beta):
        population[i][j] = exposed_temp


# infect around cells
def infect_around(population: np.ndarray, i: int, j: int):
    size = population.shape[0]
    if i != 0:
        infect(population, i - 1, j)
    if j != 0:
        infect(population, i, j - 1)
    if i < size - 1:
        infect(population, i + 1, j)
    if j < size - 1:
        infect(population, i, j + 1)


# spread by day
def daily_spread(population: np.ndarray, day: int):
    size = population.shape[0]
    print("At day {}, only {} people are never infected.".format(day, count_susceptible(population)))
    for i in range(size):
        for j in range(size):
            if population[i][j] == susceptible or population[i][j] == recovered:
                continue
            if population[i][j] == exposed or population[i][j] == infectious:
                infect_around(population, i, j)
                if population[i][j] == infectious:
                    if np.random.binomial(n=1, p=gamma):
                        population[i][j] = recovered
                elif population[i][j] == exposed:
                    if np.random.binomial(n=1, p=sigma):
                        population[i][j] = infectious_temp
    population[population == exposed_temp] = exposed
    population[population == infectious_temp] = infectious
    susceptible_list.append(count_susceptible(population))
    exposed_list.append(count_exposed(population))
    infectious_list.append(count_infectious(population))
    recovered_list.append(count_recovered(population))


def spread_by_days(population: np.ndarray, days: int):
    plt.figure()
    plt.ion()
    for day in range(days):
        daily_spread(population, day)
        if day % 10 == 0:
            plt.imshow(population, cmap="Greys")
            plt.show()


def spread_until_convergence(population: np.ndarray):
    plt.figure()
    plt.ion()
    day = -1
    while True:
        day += 1
        daily_spread(population, day)
        if day % 10 == 0:
            plt.imshow(population, cmap="OrRd")
            plt.show()
        if day > 30 and (infectious_list[-1] + exposed_list[-1]) < population.size * 1e-3:
            return


def draw():
    plt.figure()
    plt.grid(True)
    plt.xlabel("day")
    plt.ylabel("cases")
    plt.plot(susceptible_list)
    plt.plot(exposed_list)
    plt.plot(infectious_list)
    plt.plot(recovered_list)
    plt.legend(["susceptible", "exposed", "infectious", "recovered"])
    plt.show()


#模拟群体免疫
def herd_immune():
    pop = init_pop(N, N_infected, N_recovered)
    spread_by_days(pop, 90)


#模拟实际情况
def simulate():
    pop = init_pop(N, N_infected)
    spread_until_convergence(pop)


if __name__ == "__main__":
    simulate()
