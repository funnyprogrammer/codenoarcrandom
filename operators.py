import random as ran
import copy, math

def defineMutationProbability(tasksMutationStartProbability, tasksMutationEndProbability, operatorsMutationStartProbability, operatorsMutationEndProbability, numberOfGenerations, currentGeneration, changeMutationRateType, changeMutationRateExpBase):
    if changeMutationRateType == 0:
        tasksMutationProbability = (((numberOfGenerations * tasksMutationEndProbability) - ((tasksMutationEndProbability - tasksMutationStartProbability) * (numberOfGenerations - currentGeneration))) / numberOfGenerations)
        operatorsMutationProbability = (((numberOfGenerations * operatorsMutationEndProbability) - ((operatorsMutationEndProbability - operatorsMutationStartProbability) * (numberOfGenerations - currentGeneration))) / numberOfGenerations)
    else:
        if changeMutationRateType == 1:
            tasksMutationProbability = (((tasksMutationEndProbability - tasksMutationStartProbability) * (((math.pow(changeMutationRateExpBase, currentGeneration)) + (tasksMutationStartProbability - changeMutationRateExpBase + 1)) - tasksMutationStartProbability)) / (((math.pow(changeMutationRateExpBase, numberOfGenerations)) + (tasksMutationStartProbability - changeMutationRateExpBase + 1)) - tasksMutationStartProbability)) + tasksMutationStartProbability
            operatorsMutationProbability = (((operatorsMutationEndProbability - operatorsMutationStartProbability) * (((math.pow(changeMutationRateExpBase, currentGeneration)) + (operatorsMutationStartProbability - changeMutationRateExpBase + 1)) - operatorsMutationStartProbability)) / (((math.pow(changeMutationRateExpBase, numberOfGenerations)) + (operatorsMutationStartProbability - changeMutationRateExpBase + 1)) - operatorsMutationStartProbability)) + operatorsMutationStartProbability
        else:
            quit(99)
    return (tasksMutationProbability, operatorsMutationProbability)

def rouletteSelection(evaluatedPopulation, sortedEvaluatedPopulation, drivenMutatedIndividuals, drivenMutatedEvaluatedPopulation, drivenMutatedGenerations):
    if drivenMutatedGenerations >= 1:
        limit = ran.random() * drivenMutatedEvaluatedPopulation[0]
        i = 0
        aux = drivenMutatedEvaluatedPopulation[1][i]
        while aux < limit:
            i = i + 1
            aux = aux + drivenMutatedEvaluatedPopulation[1][i]
    else:
        limit = ran.random() * evaluatedPopulation[0]
        i = 0
        aux = evaluatedPopulation[1][i][0]
        while aux < limit:
            i = i + 1
            aux = aux + evaluatedPopulation[1][i][0]
    return (i, drivenMutatedIndividuals[i])

def doubleTournamentSelection(evaluatedPopulation, drivenMutatedIndividuals):
    opponent1 = int(ran.random() * len(evaluatedPopulation[1]))
    opponent2 = int(ran.random() * len(evaluatedPopulation[1]))
    if ((evaluatedPopulation[1][opponent1][0]) * (drivenMutatedIndividuals[opponent1] + 1)) >= ((evaluatedPopulation[1][opponent2][0]) * (drivenMutatedIndividuals[opponent2] + 1)):
        return (opponent1, drivenMutatedIndividuals[opponent1])
    else:
        return (opponent2, drivenMutatedIndividuals[opponent2])

def parentSelection(evaluatedPopulation, sortedEvaluatedPopulation, selectionOp, drivenMutatedIndividuals, drivenMutatedEvaluatedPopulation, drivenMutatedGenerations):
    if selectionOp == 0:
        return rouletteSelection(evaluatedPopulation, sortedEvaluatedPopulation, drivenMutatedIndividuals, drivenMutatedEvaluatedPopulation, drivenMutatedGenerations)
    else:
        if selectionOp == 1:
            return doubleTournamentSelection(evaluatedPopulation, drivenMutatedIndividuals)
        else:
            quit(99)

def BVBCrossover(crossoverTasksNumPerc, cromossome1, cromossome2, i, evaluatedPopulation, alphabet):
    offspring1 = copy.deepcopy(cromossome1)
    offspring2 = copy.deepcopy(cromossome2)
    if evaluatedPopulation[1][i][1] >= evaluatedPopulation[1][i + 1][1]:
        incorreclyFiredTasks = evaluatedPopulation[1][i][6]
    else:
        incorreclyFiredTasks = evaluatedPopulation[1][i + 1][6]
    if crossoverTasksNumPerc == -1:
        tasksNum = 1
    else:
        tasksNum = int(crossoverTasksNumPerc * len(alphabet))
    for i in range(tasksNum):
        if (len(incorreclyFiredTasks)) > 0:
            chosenTask = int(ran.choice(incorreclyFiredTasks))
        else:
            chosenTask = int(ran.random() * len(alphabet))
        offspring1[(chosenTask * 2)] = cromossome2[(chosenTask * 2)]
        offspring1[(chosenTask * 2) + 1] = cromossome2[(chosenTask * 2) + 1]
        offspring2[(chosenTask * 2)] = cromossome1[(chosenTask * 2)]
        offspring2[(chosenTask * 2) + 1] = cromossome1[(chosenTask * 2) + 1]
        for j in range(len(offspring1)):
            offspring1[j][(chosenTask * 2)] = cromossome2[j][(chosenTask * 2)]
            offspring1[j][(chosenTask * 2) + 1] = cromossome2[j][(chosenTask * 2) + 1]
            offspring2[j][(chosenTask * 2)] = cromossome1[j][(chosenTask * 2)]
            offspring2[j][(chosenTask * 2) + 1] = cromossome1[j][(chosenTask * 2) + 1]
    return (offspring2, offspring1)

def singleTaskCrossover(crossoverTasksNumPerc, cromossome1, cromossome2, alphabet):
    offspring1 = copy.deepcopy(cromossome1)
    offspring2 = copy.deepcopy(cromossome2)
    if crossoverTasksNumPerc == -1:
        tasksNum = 1
    else:
        tasksNum = int(crossoverTasksNumPerc * len(alphabet))
    for i in range(tasksNum):
        chosenTask = int(ran.random() * len(alphabet))
        offspring1[(chosenTask * 2)] = cromossome2[(chosenTask * 2)]
        offspring1[(chosenTask * 2) + 1] = cromossome2[(chosenTask * 2) + 1]
        offspring2[(chosenTask * 2)] = cromossome1[(chosenTask * 2)]
        offspring2[(chosenTask * 2) + 1] = cromossome1[(chosenTask * 2) + 1]
        for j in range(len(offspring1)):
            offspring1[j][(chosenTask * 2)] = cromossome2[j][(chosenTask * 2)]
            offspring1[j][(chosenTask * 2) + 1] = cromossome2[j][(chosenTask * 2) + 1]
            offspring2[j][(chosenTask * 2)] = cromossome1[j][(chosenTask * 2)]
            offspring2[j][(chosenTask * 2) + 1] = cromossome1[j][(chosenTask * 2) + 1]
    return (offspring2, offspring1)

def uniformCrossoverPerProcess(cromossome1, cromossome2, alphabet):
    offspring1 = copy.deepcopy(cromossome1)
    offspring2 = copy.deepcopy(cromossome2)
    for i in range(0, len(alphabet)):
        if ran.random() < 0.5:
            offspring1[(i * 2)] = cromossome2[(i * 2)]
            offspring1[(i * 2) + 1] = cromossome2[(i * 2) + 1]
            offspring2[(i * 2)] = cromossome1[(i * 2)]
            offspring2[(i * 2) + 1] = cromossome1[(i * 2) + 1]
            for j in range(len(offspring1)):
                offspring1[j][(i * 2)] = cromossome2[j][(i * 2)]
                offspring1[j][(i * 2) + 1] = cromossome2[j][(i * 2) + 1]
                offspring2[j][(i * 2)] = cromossome1[j][(i * 2)]
                offspring2[j][(i * 2) + 1] = cromossome1[j][(i * 2) + 1]
        else:
            offspring1[(i * 2)] = cromossome1[(i * 2)]
            offspring1[(i * 2) + 1] = cromossome1[(i * 2) + 1]
            offspring2[(i * 2)] = cromossome2[(i * 2)]
            offspring2[(i * 2) + 1] = cromossome2[(i * 2) + 1]
            for j in range(len(offspring1)):
                offspring1[j][(i * 2)] = cromossome1[j][(i * 2)]
                offspring1[j][(i * 2) + 1] = cromossome1[j][(i * 2) + 1]
                offspring2[j][(i * 2)] = cromossome2[j][(i * 2)]
                offspring2[j][(i * 2) + 1] = cromossome2[j][(i * 2) + 1]
    return (offspring2, offspring1)

def twoPointCrossoverPerProcess(cromossome1, cromossome2, alphabet):
    offspring1 = copy.deepcopy(cromossome1)
    offspring2 = copy.deepcopy(cromossome2)
    cutpoint1 = int(ran.random() * len(alphabet))
    cutpoint2 = int(ran.random() * (len(alphabet) - cutpoint1))
    cutpoint2 = cutpoint2 + cutpoint1
    for i in range(0, cutpoint1):
        offspring1[(i * 2)] = cromossome2[(i * 2)]
        offspring1[(i * 2) + 1] = cromossome2[(i * 2) + 1]
        offspring2[(i * 2)] = cromossome1[(i * 2)]
        offspring2[(i * 2)] = cromossome1[(i * 2)]
        for j in range(len(cromossome1)):
            offspring1[j][(i * 2)] = cromossome2[j][(i * 2)]
            offspring1[j][(i * 2) + 1] = cromossome2[j][(i * 2) + 1]
            offspring2[j][(i * 2)] = cromossome1[j][(i * 2)]
            offspring2[j][(i * 2) + 1] = cromossome1[j][(i * 2) + 1]
    for i in range(cutpoint2 + 1, len(alphabet)):
        offspring1[(i * 2)] = cromossome2[(i * 2)]
        offspring1[(i * 2) + 1] = cromossome2[(i * 2) + 1]
        offspring2[(i * 2)] = cromossome1[(i * 2)]
        offspring2[(i * 2) + 1] = cromossome1[(i * 2) + 1]
        for j in range(len(cromossome1)):
            offspring1[j][(i * 2)] = cromossome2[j][(i * 2)]
            offspring1[j][(i * 2) + 1] = cromossome2[j][(i * 2) + 1]
            offspring2[j][(i * 2)] = cromossome1[j][(i * 2)]
            offspring2[j][(i * 2) + 1] = cromossome1[j][(i * 2) + 1]
    return (offspring2, offspring1)

def singlePointCrossover(cromossome1, cromossome2, alphabet):
    offspring1 = copy.deepcopy(cromossome1)
    offspring2 = copy.deepcopy(cromossome2)
    cutpoint = int(ran.random() * len(alphabet))
    for i in range(((cutpoint * 2) + 1) + 1, (len(cromossome1) - 3)):
        offspring1[i] = cromossome2[i]
        offspring2[i] = cromossome1[i]
        for j in range(len(cromossome1)):
            offspring1[j][i] = cromossome2[j][i]
            offspring2[j][i] = cromossome1[j][i]
    return (offspring2, offspring1)

def crossoverPerProcess(crossoverType, crossoverProbability, crossoverTasksNumPerc, cromossome1, cromossome2, i, evaluatedPopulation, alphabet):
    if ran.random() < crossoverProbability:
        if crossoverType == 0:
            (cromossome1, cromossome2) = singlePointCrossover(cromossome1, cromossome2, alphabet)
        else:
            if crossoverType == 1:
                (cromossome1, cromossome2) = twoPointCrossoverPerProcess(cromossome1, cromossome2, alphabet)
            else:
                if crossoverType == 2:
                    (cromossome1, cromossome2) = uniformCrossoverPerProcess(cromossome1, cromossome2, alphabet)
                else:
                    if crossoverType == 3:
                        (cromossome1, cromossome2) = singleTaskCrossover(crossoverTasksNumPerc, cromossome1, cromossome2, alphabet)
                    else:
                        if crossoverType == 4:
                            (cromossome1, cromossome2) = BVBCrossover(crossoverTasksNumPerc, cromossome1, cromossome2, i, evaluatedPopulation, alphabet)
                        else:
                            quit(99)
    return (cromossome1, cromossome2)

def mutationBVB(mutationTasksNumPerc, cromossome, alphabet):
    if mutationTasksNumPerc == -1:
        tasksNum = 1
    else:
        tasksNum = int(mutationTasksNumPerc * len(alphabet))
        if tasksNum < 1:
            tasksNum = 1
    for i in range(tasksNum):
        chosenTask = int(ran.random() * len(alphabet))
        chosenType = ran.random()
        if chosenType < 1/3:
            position1 = ran.randrange(0, 1 + 1)
            position2 = ran.randrange(0, 1 + 1)
            newInput = int(ran.random() * len(alphabet))
            if cromossome[(newInput * 2) + position1][(chosenTask * 2) + position2] == 0:
                cromossome[(newInput * 2) + position1][(chosenTask * 2) + position2] = 1
            else:
                cromossome[(newInput * 2) + position1][(chosenTask * 2) + position2] = 0
        else:
            if chosenType > 2/3:
                position1 = ran.randrange(0, 1 + 1)
                position2 = ran.randrange(0, 1 + 1)
                newOutput = int(ran.random() * len(alphabet))
                if cromossome[(chosenTask * 2) + position1][(newOutput * 2) + position2] == 0:
                    cromossome[(chosenTask * 2) + position1][(newOutput * 2) + position2] = 1
                else:
                    cromossome[(chosenTask * 2) + position1][(newOutput * 2) + position2] = 0
            else:
                newOperator1 = ran.randrange(0, 1 + 1)
                newOperator2 = ran.randrange(1, 3 + 1)
                if newOperator1 == 0:
                    if cromossome[(chosenTask * 2)][-newOperator2]== 0:
                        cromossome[(chosenTask * 2)][-newOperator2] = 1
                    else:
                        cromossome[(chosenTask * 2)][-newOperator2] = 0
                else:
                    if newOperator1 == 1:
                        if cromossome[-newOperator2][(chosenTask * 2)]== 0:
                            cromossome[-newOperator2][(chosenTask * 2)] = 1
                        else:
                            cromossome[-newOperator2][(chosenTask * 2)] = 0
    return

def basicMutation(cromossome, tasksMutationProbability, operatatorsMutationProbability):
    for i in range(0, len(cromossome) - 5):
        for j in range(2, len(cromossome[i]) - 3):
            if ran.random() < tasksMutationProbability:
                if cromossome[i][j] == 0:
                    cromossome[i][j] = 1
                else:
                    cromossome[i][j] = 0
    for i in range(0, len(cromossome) - 5, 2):
        for j in range(1, 4):
            if ran.random() < operatatorsMutationProbability:
                if cromossome[i][-j] == 0:
                    cromossome[i][-j] = 1
                else:
                    cromossome[i][-j] = 0
    for i in range(2, len(cromossome[-1]) - 3, 2):
        for j in range(1, 4):
            if ran.random() < operatatorsMutationProbability:
                if cromossome[-j][i] == 0:
                    cromossome[-j][i] = 1
                else:
                    cromossome[-j][i] = 0
    return

def mutation(cromossome, tasksMutationProbability, operatatorsMutationProbability, mutationType, mutationTasksNumPerc, alphabet):
    if mutationType == 0:
        basicMutation(cromossome, tasksMutationProbability, operatatorsMutationProbability)
    else:
        if mutationType == 1:
            mutationBVB(mutationTasksNumPerc, cromossome, alphabet)
        else:
            quit(99)

def drivenMutation(auxPopulation, sortedEvaluatedAuxPopulation, drivenMutationPart, mutatedIndividuals):
    N_BetterIndividuals = int(drivenMutationPart * len(auxPopulation))
    dominantSchema = copy.deepcopy(auxPopulation[0])
    for i in range(len(dominantSchema)):
        for j in range(len(dominantSchema[i])):
            dominantSchema[i][j] = 1
    for i in range(N_BetterIndividuals - 1):
        mutatedIndividuals[sortedEvaluatedAuxPopulation[i][5]] = 1
        for j in range(len(dominantSchema)):
            for k in range(len(dominantSchema[j])):
                if auxPopulation[sortedEvaluatedAuxPopulation[i][5]][j][k] != auxPopulation[sortedEvaluatedAuxPopulation[i + 1][5]][j][k]:
                    dominantSchema[j][k] = 0
    mutatedIndividuals[sortedEvaluatedAuxPopulation[i + 1][5]] = 1
    for i in range(N_BetterIndividuals):
        for j in range(len(dominantSchema)):
            for k in range(len(dominantSchema[j])):
                if dominantSchema[j][k] == 1:
                    if auxPopulation[sortedEvaluatedAuxPopulation[i][5]][j][k] == 0:
                        auxPopulation[sortedEvaluatedAuxPopulation[i][5]][j][k] = 1
                    else:
                        auxPopulation[sortedEvaluatedAuxPopulation[i][5]][j][k] = 0
    return mutatedIndividuals

def elitism(population, elitismPerc, sortedEvaluatedAuxPopulation, sortedEvaluatedPopulation, auxPopulation, drivenMutatedIndividuals):
    for i in range(round(len(population) * elitismPerc)):
        if sortedEvaluatedAuxPopulation[len(sortedEvaluatedAuxPopulation) - 1 - i][0] < sortedEvaluatedPopulation[i][0]:
            auxPopulation[sortedEvaluatedAuxPopulation[len(sortedEvaluatedAuxPopulation) - 1 - i][5]] = copy.deepcopy(population[sortedEvaluatedPopulation[i][5]])
            drivenMutatedIndividuals[sortedEvaluatedAuxPopulation[len(sortedEvaluatedAuxPopulation) - 1 - i][5]] = 0
        else:
            break
    return