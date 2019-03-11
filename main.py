import plotting as plot
import recording as record
import cycle as cycle
import initialPopulation as iniPop
import operators as op
import fitness as fit
import islands as isl
import logs as logs
import multiprocessing
import copy
from ast import literal_eval
from datetime import datetime
from functools import partial

def runRound(par, parameter, population_size, numberOfGenerations, crossoverType, crossoverTasksNumPerc, crossoverProbability, mutationType, mutationTasksNumPerc, tasksMutationStartProbability, tasksMutationEndProbability, operatorsMutationStartProbability, operatorsMutationEndProbability, changeMutationRateType, changeMutationRateExpBase, drivenMutation, drivenMutationPart, limitBestFitnessRepetionCount, numberOfcyclesAfterDrivenMutation, completenessWeight, TPweight, precisenessWeight, simplicityWeight, precisenessStart, simplicityStart, evolutionEnd, completenessAttemptFactor1, completenessAttemptFactor2, elitismPerc, selectionOp, selectionTp, lambdaValue, HammingThreshold, migrationtime, percentageOfBestIndividualsForMigrationPerIsland, percentageOfIndividualsForMigrationPerIsland, alphabet, log, fitnessStrategy, logIndex, num_threads, round, broadcast, islandNumber):
    islandStart = datetime.now()
    highestValueAndPosition = [[0, 0, 0], -1]
    if highestValueAndPosition[0][1] >= precisenessStart:
        precisenessWeight = float(par[parameter][20])
    (population, evaluatedPopulation, referenceCromossome, averageEnabledTasks) = iniPop.initializePopulation(islandNumber, population_size, TPweight, precisenessWeight, simplicityWeight, completenessWeight, completenessAttemptFactor1, completenessAttemptFactor2, selectionOp, alphabet, log)
    fitnessEvolution = []
    (highestValueAndPosition, sortedEvaluatedPopulation) = cycle.chooseHighest(evaluatedPopulation)
    lowestValue = cycle.chooseLowest(sortedEvaluatedPopulation)
    averageValue = cycle.calculateAverage(evaluatedPopulation)
    fitnessEvolution.append([lowestValue, highestValueAndPosition[0][0], averageValue, 0, highestValueAndPosition[0][1], highestValueAndPosition[0][2], highestValueAndPosition[0][3], highestValueAndPosition[0][4], 0, 0, 0, 0])
    if (fitnessEvolution[0][8] >= simplicityStart) and (precisenessWeight > 0):
        simplicityWeight = float(par[parameter][21])
    print('LOG:', logIndex, '| PAR:', parameter, '| RND:', round, '| GEN:', 0, '| TF:', '%.5f' % highestValueAndPosition[0][0], '| C:', '%.5f' % highestValueAndPosition[0][1], '| TP:', '%.5f' % highestValueAndPosition[0][2], '| P:', '%.5f' % highestValueAndPosition[0][3], '| S:', '%.5f' % highestValueAndPosition[0][4], '| REP:', fitnessEvolution[0][3], fitnessEvolution[0][8], fitnessEvolution[0][9], fitnessEvolution[0][10], fitnessEvolution[0][11], '| ISL:', islandNumber)
    drivenMutatedIndividuals = [0 for _ in range(len(population))]
    drivenMutatedGenerations = 0
    for currentGeneration in range(1, numberOfGenerations):
        if highestValueAndPosition[0][1] >= precisenessStart:
            precisenessWeight = float(par[parameter][20])
        (tasksMutationProbability, operatorsMutationProbability) = op.defineMutationProbability(tasksMutationStartProbability, tasksMutationEndProbability, operatorsMutationStartProbability, operatorsMutationEndProbability, numberOfGenerations, currentGeneration, changeMutationRateType, changeMutationRateExpBase)
        (population, evaluatedPopulation, drivenMutatedIndividuals, drivenMutatedGenerations) = cycle.generation(population, referenceCromossome, evaluatedPopulation, crossoverType, crossoverProbability, crossoverTasksNumPerc, mutationType, mutationTasksNumPerc, tasksMutationProbability, operatorsMutationProbability, drivenMutation, drivenMutationPart, limitBestFitnessRepetionCount, fitnessEvolution[currentGeneration - 1][3], drivenMutatedIndividuals, drivenMutatedGenerations, TPweight, precisenessWeight, simplicityWeight, completenessWeight, elitismPerc, sortedEvaluatedPopulation, selectionOp, selectionTp, lambdaValue, HammingThreshold, currentGeneration, completenessAttemptFactor1, completenessAttemptFactor2, numberOfcyclesAfterDrivenMutation, alphabet, log)
        (highestValueAndPosition, sortedEvaluatedPopulation) = cycle.chooseHighest(evaluatedPopulation)
        isl.set_broadcast(population, sortedEvaluatedPopulation, islandNumber,percentageOfBestIndividualsForMigrationPerIsland, broadcast)
        lowestValue = cycle.chooseLowest(sortedEvaluatedPopulation)
        averageValue = cycle.calculateAverage(evaluatedPopulation)
        fitnessEvolution.append([lowestValue, highestValueAndPosition[0][0], averageValue, 0, highestValueAndPosition[0][1], highestValueAndPosition[0][2], highestValueAndPosition[0][3], highestValueAndPosition[0][4], 0, 0, 0, 0])
        if fitnessEvolution[currentGeneration][1] == fitnessEvolution[currentGeneration - 1][1]:
            fitnessEvolution[currentGeneration][8] = fitnessEvolution[currentGeneration - 1][8] + 1
        if fitnessEvolution[currentGeneration][4] == fitnessEvolution[currentGeneration - 1][4]:
            fitnessEvolution[currentGeneration][3] = fitnessEvolution[currentGeneration - 1][3] + 1
        if fitnessEvolution[currentGeneration][5] == fitnessEvolution[currentGeneration - 1][5]:
            fitnessEvolution[currentGeneration][9] = fitnessEvolution[currentGeneration - 1][9] + 1
        if fitnessEvolution[currentGeneration][6] == fitnessEvolution[currentGeneration - 1][6]:
            fitnessEvolution[currentGeneration][10] = fitnessEvolution[currentGeneration - 1][10] + 1
        if fitnessEvolution[currentGeneration][7] == fitnessEvolution[currentGeneration - 1][7]:
            fitnessEvolution[currentGeneration][11] = fitnessEvolution[currentGeneration - 1][11] + 1
        if (fitnessEvolution[currentGeneration][10] >= simplicityStart) and (precisenessWeight > 0):
            simplicityWeight = float(par[parameter][21])
        print('LOG:', logIndex, '| PAR:', parameter, '| RND:', round, '| GEN:', currentGeneration, '| TF:', '%.6f' % highestValueAndPosition[0][0], '| C:', '%.5f' % highestValueAndPosition[0][1], '| TP:', '%.5f' % highestValueAndPosition[0][2], '| P:', '%.5f' % highestValueAndPosition[0][3], '| S:', '%.5f' % highestValueAndPosition[0][4], '| REP:', fitnessEvolution[currentGeneration][8], fitnessEvolution[currentGeneration][3], fitnessEvolution[currentGeneration][9], fitnessEvolution[currentGeneration][10], fitnessEvolution[currentGeneration][11], '| ISL:', islandNumber)
        if ((fitnessStrategy == 0) and ((highestValueAndPosition[0][1] >= 1.0) and (fitnessEvolution[currentGeneration][8] >= evolutionEnd))) or ((fitnessStrategy == 1) and ((highestValueAndPosition[0][1] == 1.0) and (highestValueAndPosition[0][3] > 0) and (highestValueAndPosition[0][4] > 0) and (fitnessEvolution[currentGeneration][10] >= evolutionEnd) and (fitnessEvolution[currentGeneration][11] >= evolutionEnd))):
            broadcast[len(broadcast)-1] = 0
        if (currentGeneration > 0) and (currentGeneration % migrationtime == 0):
            island_fitness = []
            for i in range(len(evaluatedPopulation[1])):
                valor = evaluatedPopulation[1][i]
                island_fitness.append(valor[0])
            isl.do_migration2(population, islandNumber, num_threads, island_fitness, percentageOfIndividualsForMigrationPerIsland, percentageOfBestIndividualsForMigrationPerIsland, broadcast)
            migraNeed = []
            migraNeed.append(broadcast[len(broadcast)-1])
            if migraNeed[0] == 0:
                break
            evaluatedPopulation = fit.evaluationPopulation(population, referenceCromossome, TPweight, precisenessWeight, simplicityWeight, completenessWeight, completenessAttemptFactor1, completenessAttemptFactor2, selectionOp, alphabet, log)
            (highestValueAndPosition, sortedEvaluatedPopulation) = cycle.chooseHighest(evaluatedPopulation)
    cycle.postProcessing(population, alphabet)
    plot.plot_evolution_per_island(fitnessEvolution, str(parameter), str(round), islandNumber)
    prevPlot = []
    with open('results/plotting_{0}.txt'.format(islandNumber), 'r') as plott:
        for line in isl.nonblank_lines(plott):
            prevPlot.append(literal_eval(line))
    plott.close()
    prevPlot.extend(fitnessEvolution)
    with open('results/plotting_{0}.txt'.format(islandNumber), 'w') as plott:
        for ini in range(len(prevPlot)):
            plott.write(str(prevPlot[ini]) + '\n')
    plott.close()
    islandEnd = datetime.now()
    islandDuration = islandEnd - islandStart
    record.record_evolution(log, str(parameter), str(round), par[parameter], islandNumber, highestValueAndPosition[0], fitnessEvolution, alphabet, population[highestValueAndPosition[1]], islandStart, islandEnd, islandDuration, currentGeneration)
    print(islandNumber, islandDuration, '%.5f' % highestValueAndPosition[0][0], '%.5f' % highestValueAndPosition[0][1], '%.5f' % highestValueAndPosition[0][2], '%.5f' % highestValueAndPosition[0][3], alphabet, population[highestValueAndPosition[1]])
    return

if __name__ == '__main__':
    par = []
    with open('input-parameters-v.csv', 'r') as parameters:
        for line in isl.nonblank_lines(parameters):
            par.append(line.split(';'))
    parameters.close()
    for parameter in range(1,len(par)):
        numberOfRounds = int(par[parameter][0])
        population_size = int(par[parameter][1])
        numberOfGenerations = int(par[parameter][2])
        crossoverType = int(par[parameter][3])
        crossoverTasksNumPerc = float(par[parameter][4])
        crossoverProbability = float(par[parameter][5])
        mutationType = int(par[parameter][6])
        mutationTasksNumPerc = float(par[parameter][7])
        tasksMutationStartProbability = float(par[parameter][8])
        tasksMutationEndProbability = float(par[parameter][9])
        operatorsMutationStartProbability = float(par[parameter][10])
        operatorsMutationEndProbability = float(par[parameter][11])
        changeMutationRateType = int(par[parameter][12])
        changeMutationRateExpBase = float(par[parameter][13])
        drivenMutation = int(par[parameter][14])
        drivenMutationPart = float(par[parameter][15])
        limitBestFitnessRepetionCount = int(par[parameter][16])
        numberOfcyclesAfterDrivenMutation = int(par[parameter][17])
        completenessWeight = float(par[parameter][18])
        TPweight = float(par[parameter][19])
        precisenessStart = float(par[parameter][22])
        simplicityStart = int(par[parameter][23])
        evolutionEnd = int(par[parameter][24])
        completenessAttemptFactor1 = int(par[parameter][25])
        completenessAttemptFactor2 = float(par[parameter][26])
        elitismPerc = float(par[parameter][27])
        selectionOp = int(par[parameter][28])
        selectionTp = int(par[parameter][29])
        lambdaValue = int(par[parameter][30])
        HammingThreshold = int(par[parameter][31])
        migrationtime = int(par[parameter][32])
        num_threads = int(par[parameter][33])
        percentageOfBestIndividualsForMigrationPerIsland = float(par[parameter][34])
        percentageOfIndividualsForMigrationPerIsland = float(par[parameter][35])
        logIndex = int(par[parameter][36])
        fitnessStrategy = int(par[parameter][37])
        if fitnessStrategy == 0:
            precisenessWeight = float(par[parameter][20])
            simplicityWeight = float(par[parameter][21])
        else:
            precisenessWeight = 0
            simplicityWeight = 0
        globalStart = datetime.now()
        alphabet = []
        log = []
        log = copy.deepcopy(logs.logList[logIndex])
        logSizeAndMaxTraceSize = [0, float('inf'), 0]
        iniPop.createAlphabet(log, alphabet)
        iniPop.processLog(log, logSizeAndMaxTraceSize)
        #print('Para', num_threads, 'threads:', 'logs = ', logIndex)
        num_islands = []
        for thread in range(num_threads):
            num_islands.append(thread)
        p = multiprocessing.Pool(num_threads)
        m = multiprocessing.Manager()
        broadcast = m.list()
        func = partial(runRound, par, parameter, population_size, numberOfGenerations, crossoverType,
                       crossoverTasksNumPerc, crossoverProbability, mutationType, mutationTasksNumPerc,
                       tasksMutationStartProbability,
                       tasksMutationEndProbability, operatorsMutationStartProbability, operatorsMutationEndProbability,
                       changeMutationRateType,
                       changeMutationRateExpBase, drivenMutation, drivenMutationPart, limitBestFitnessRepetionCount,
                       numberOfcyclesAfterDrivenMutation,
                       completenessWeight, TPweight, precisenessWeight, simplicityWeight, precisenessStart,
                       simplicityStart, evolutionEnd, completenessAttemptFactor1,
                       completenessAttemptFactor2, elitismPerc, selectionOp, selectionTp, lambdaValue, HammingThreshold,
                       migrationtime, percentageOfBestIndividualsForMigrationPerIsland,
                       percentageOfIndividualsForMigrationPerIsland, alphabet, log, fitnessStrategy, logIndex, num_threads)
        time = open('results/time.txt', 'w')
        time.close()
        for round in range(numberOfRounds):
            for thread in range(num_threads):
                new_thread = []
                broadcast.append(new_thread)
            broadcast.append(1)
            func2 = partial(func, round, broadcast)
            p.map(func2, num_islands)
            p.close()
            plot.plot_evolution_integrated(str(parameter), str(round), num_threads)
            globalEnd = datetime.now()
            globalDuration = globalEnd - globalStart
            print('Global Start:    ', globalStart)
            print('Global End:      ', globalEnd)
            print('Global Duration: ', globalDuration)

            times = []
            with open('results/time.txt', 'r') as timer:
                for line in isl.nonblank_lines(timer):
                    times.append(literal_eval(line))
            timer.close()
            times.extend(globalDuration)
            with open('results/time.txt', 'w') as timer:
                for ini in range(len(times)):
                    timer.write(str(times[ini]) + '\n')
            timer.close()

