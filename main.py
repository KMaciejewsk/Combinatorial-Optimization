import random
import itertools
import time

def generateGraph(n,max_distance=1000):
    max_edges = n*(n-1)
    edges = []
    for i in range(n):
        for j in range(n):
            if i!=j:
                temp = [i,j]
                edges.append(temp)
    graph = [[0] * n for _ in range(n)]
    for j in range(len(edges)):
        x = edges[j][0]
        y = edges[j][1]
        d = random.randint(1, max_distance)
        graph[x][y] = d
        graph[y][x] = d
    return graph


def bruteForce(matrix):
    num_locations = len(matrix)
    min_distance = float('inf')
    best_routes = None

    for routes in itertools.permutations(range(num_locations)):
        distance = 0
        for i in range(int(num_locations/2) - 1):
            distance += matrix[routes[i]][routes[i + 1]]
        distance += matrix[routes[int(num_locations/2) - 1]][routes[0]]
        for i in range(int(num_locations/2), num_locations-1):
            distance += matrix[routes[i]][routes[i + 1]]
        distance += matrix[routes[int(num_locations) - 1]][routes[int(num_locations/2)]]
        if distance < min_distance:
            min_distance = distance
            best_routes = routes

    return min_distance, best_routes

def nearestNeighbour(matrix):
    route1 = []
    route2 = []
    distance = 0
    available_nodes = [i for i in range(len(matrix))]
    route1.append(random.choice(available_nodes))
    available_nodes.remove(route1[0])
    route2.append(random.choice(available_nodes))
    available_nodes.remove(route2[0])
    while len(available_nodes) > 1:
        min_distance = float('inf')
        for i in available_nodes:
            if matrix[route1[-1]][i] < min_distance:
                min_distance = matrix[route1[-1]][i]
                next_node = i
        route1.append(next_node)
        distance += min_distance
        available_nodes.remove(next_node)
        min_distance = float('inf')
        for i in available_nodes:
            if matrix[route2[-1]][i] < min_distance:
                min_distance = matrix[route2[-1]][i]
                next_node = i
        route2.append(next_node)
        distance += min_distance
        available_nodes.remove(next_node)
    if len(available_nodes) == 1:
        if matrix[route1[-1]][available_nodes[0]] < matrix[route2[-1]][available_nodes[0]]:
            route1.append(available_nodes[0])
            distance += matrix[route1[-2]][available_nodes[0]]
        else:
            route2.append(available_nodes[0])
            distance += matrix[route2[-2]][available_nodes[0]]
    distance += matrix[route1[-1]][route1[0]]
    distance += matrix[route2[-1]][route2[0]]
    return distance, route1, route2

def generate_chromosome(matrix):
    chromosome = []
    available_nodes = [i for i in range(len(matrix))]

    while len(available_nodes) > 0:
        chromosome.append(random.choice(available_nodes))
        available_nodes.remove(chromosome[-1])
    return chromosome

def crossover(chromosome1, chromosome2):
    crossover_point = random.randint(1, len(chromosome1)-2)
    new_chromosome1 = chromosome1[:crossover_point]
    new_chromosome2 = chromosome2[:crossover_point]
    for i in chromosome2:
        if i not in new_chromosome1:
            new_chromosome1.append(i)
    for i in chromosome1:
        if i not in new_chromosome2:
            new_chromosome2.append(i)
    return new_chromosome1, new_chromosome2

def mutation(chromosome, matrix):
    mutation_point1 = random.randint(0, len(chromosome)-1)
    mutation_point2 = random.randint(0, len(chromosome)-1)
    chromosome[mutation_point1], chromosome[mutation_point2] = chromosome[mutation_point2], chromosome[mutation_point1]
    return chromosome

def fitness(chromosome, matrix):
    distance = 0
    for i in range(int(len(chromosome) / 2) - 1):
        distance += matrix[chromosome[i]][chromosome[i + 1]]
    distance += matrix[chromosome[int(len(chromosome) / 2) - 1]][chromosome[0]]
    for i in range(int(len(chromosome) / 2), len(chromosome) - 1):
        distance += matrix[chromosome[i]][chromosome[i + 1]]
    distance += matrix[chromosome[int(len(chromosome)) - 1]][chromosome[int(len(chromosome) / 2)]]
    return distance, chromosome


def geneticAlgorithm(matrix):
    population = []
    fitnesses = []
    for i in range(100):
        population.append(generate_chromosome(matrix))
    best_distance = float('inf')
    best_chromosome = None
    for i in range(400):
        new_population = []
        for j in range(100):
            chromosome1 = random.choice(population)
            chromosome2 = random.choice(population)
            new_chromosome1, new_chromosome2 = crossover(chromosome1, chromosome2)
            new_chromosome1 = mutation(new_chromosome1, matrix)
            new_chromosome2 = mutation(new_chromosome2, matrix)
            new_population.append(new_chromosome1)
            new_population.append(new_chromosome2)
            fitnesses.append(fitness(new_chromosome1, matrix))
            fitnesses.append(fitness(new_chromosome2, matrix))
        fitnesses.sort(key=lambda x: x[0])
        if fitnesses[0][0] < best_distance:
            best_distance = fitnesses[0][0]
            best_chromosome = fitnesses[0][1]
        population = [i[1] for i in fitnesses[:100]]
    return best_distance, best_chromosome
