#!/usr/bin/env python3
from random import shuffle, random, randint
from customio import getInput
from customio import visualize
from pcmax_random import pcmaxRandom
from math import ceil, inf

# START
# Generate the initial population
# Compute fitness
# REPEAT
#     Selection
#     Crossover
#     Mutation
#     Compute fitness
# UNTIL population has converged
# STOP


# Data structure:
# individual = [
#   [processTime1, processTime2], <-- processor0 queue
#   [processTime3, processTime4]  <-- processor1 queue
# ]


GUARD_VALUE = -1
POPULATION_SIZE = 20
MUTATION_PROBABILITY = 0.2
NO_PROGRESS_BAILOUT_COUNT = 10000


def fittness(individual):
  max = 0
  for processor in individual:
    time = sum(processor)
    if time > max:
      max = time
  return -1 * max


def cloning(individual):
  return [list(processor) for processor in individual]


def mutation(individual):
  indices = list(range(len(individual)))
  shuffle(indices)
  [src_processor_index, dest_processor_index] = indices[:2]

  if len(individual[src_processor_index]) < 1:
    return

  src_processor = individual[src_processor_index]
  dest_processor = individual[dest_processor_index]

  process = src_processor[0]
  src_processor.remove(process)
  dest_processor.append(process)


def setup(processesCount, processes):
  initial_population = []

  for i in range(POPULATION_SIZE):
    individual = pcmaxRandom(processesCount, processes)
    initial_population.append(individual)

  return initial_population


def loop(initial_population, generate_random_individual):
  population = initial_population
  best = inf
  no_progress_counter = 0
  generation_counter = 0

  while no_progress_counter < NO_PROGRESS_BAILOUT_COUNT:
    fittest_individual = max(population, key=fittness)
    clone = cloning(fittest_individual)

    population = [fittest_individual, clone]

    for individual in population:
      if random() <= MUTATION_PROBABILITY:
        mutation(individual)

    for i in range(POPULATION_SIZE - len(population)):
      population.append(generate_random_individual())

    current_best = abs(fittness(fittest_individual))
    if current_best < best:
      best = current_best
      no_progress_counter = 0
      print('G ' + str(generation_counter) + ': ' + str(best))
    else:
      no_progress_counter += 1

    generation_counter += 1


def make_pcmaxrandom_generator(processorsCount, processes):
  return lambda : pcmaxRandom(processorsCount, processes)


def main():
  (processorsCount, processesCount, processes) = getInput()

  initial_population = setup(processorsCount, processes)
  generate_random_individual = make_pcmaxrandom_generator(processorsCount, processes)
  loop(initial_population, generate_random_individual)


if __name__ == '__main__':
  main()
