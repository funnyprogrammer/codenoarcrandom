from random import randint
import cycle as cycle

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def set_broadcast(population, sortedEvaluatedPopulation, islandNumber, percentageOfBestIndividualsForMigrationPerIsland, broadcast):
    allBests = []
    for i in range(int((len(population)) * percentageOfBestIndividualsForMigrationPerIsland)):
        allBests.append([population[sortedEvaluatedPopulation[i][5]], [sortedEvaluatedPopulation[i][0]]])
    broadcast[islandNumber] = allBests

def isMigrationNeed(broadcast):
    migraNeed = broadcast[len(broadcast)-1]
    return migraNeed

def find_island(island_number, island_size, num_islands, broad_size, migration_index):
    island = randint(0, num_islands - 1)
    while island == island_number or migration_index[island] >= int(broad_size*island_size):
        island = randint(0, num_islands - 1)
    return island

def do_migration2(island_content, island_number, num_islands, island_fitness, mig_policy_size, broad_size, broadcast):
    if isMigrationNeed(broadcast) == 0:
        return
    else:
        migration_index = []
        for i in range(num_islands):
            broadcast[i] = sorted(broadcast[i], reverse=False, key=cycle.takeSecond)
            migration_index.append(0)
        worst_gen_list = []
        count = 0
        for individuo in range(len(island_fitness)):
            worst_gen_list.append([island_fitness[individuo], count])
            count += 1
        #print('Migrating', island_number)
        sorted_worst_gen_list = sorted(worst_gen_list, reverse=False, key=cycle.takeFirst)
        sorted_island = find_island(island_number, len(island_content), num_islands, broad_size, migration_index)
        iter = 0
        while iter < mig_policy_size*(len(island_content)):
            if migration_index[sorted_island] >= int(broad_size*len(island_content)):
                sorted_island = find_island(island_number, len(island_content), num_islands, broad_size, migration_index)
            worst_fit = sorted_worst_gen_list[iter][0]
            island_selected = broadcast[sorted_island]
            best_ind = island_selected[migration_index[sorted_island]]
            best_fit = best_ind[1][0]
            migration_index[sorted_island] += 1
            if worst_fit < best_fit:
                island_content[sorted_worst_gen_list[iter][1]] = best_ind[0]
            iter = iter + 1
        #print('Migration', island_number, 'concluded')
        return