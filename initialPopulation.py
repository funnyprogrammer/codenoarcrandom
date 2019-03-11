import random as ran
import fitness as fitn
import islands as isl
import copy

def getTaskID(task, alphabet):
    i = 0
    while alphabet[i] != task:
        i = i + 1
    return i

def createEmptyIndividualTask(alphabet):
    task = [0 for _ in range((2 * len(alphabet)) + 3)]
    return task

def createAuxiliaryCromossome(usedLog, alphabet):
    auxCrom = [createEmptyIndividualTask(alphabet) for _ in range((2 * len(alphabet)) + 3)]
    for i in range(len(alphabet)):
        for j in range(len(usedLog)):
            for k in range(len(usedLog[j]) - 1):
                if usedLog[j][k] == alphabet[i]:
                    auxCrom[(i * 2)][(getTaskID(usedLog[j][k + 1], alphabet) * 2)] = 1
                    auxCrom[(i * 2)][(getTaskID(usedLog[j][k + 1], alphabet) * 2) + 1] = 1
                    auxCrom[(i * 2) + 1][(getTaskID(usedLog[j][k + 1], alphabet) * 2)] = 1
                    auxCrom[(i * 2) + 1][(getTaskID(usedLog[j][k + 1], alphabet) * 2) + 1] = 1
    enabledTasks = 0
    for j in range(len(auxCrom) - 2):
        for k in range(1, len(auxCrom[j]) - 1):
            if auxCrom[j][k] == 1:
                enabledTasks = enabledTasks + 1
    return (auxCrom, enabledTasks / 4)

def DMmeasures(t1, t2, log):
    l2l = 0 #the number of times that the substring "t1t2t1" occurs in a log.
    follows = 0 #the number of times that a task is directly followed by another one. That is, how often the substring "t1t2" occurs in a log.
    for i in range(len(log)):
        for j in range(len(log[i]) - 2):
            if (log[i][j] == t1) and (log[i][j + 1] == t2):
                follows = follows + 1
                if (log[i][j + 2] == t1):
                    l2l = l2l + 1
    return (l2l, follows)

def dependencyMeasure(t1, t2, log):
    dependencyMeasure = 0
    (l2l_t1_t2, follows_t1_t2) = DMmeasures(t1, t2, log)
    (l2l_t2_t1, follows_t2_t1) = DMmeasures(t2, t1, log)
    if (t1 == t2):
        dependencyMeasure = (follows_t1_t2 / (follows_t1_t2 + 1))
    else:
        if (t1 != t2):
            if (l2l_t1_t2 == 0):
                dependencyMeasure = ((follows_t1_t2 - follows_t2_t1) / (follows_t1_t2 + follows_t2_t1 + 1))
            else:
                if (l2l_t1_t2 > 0):
                    dependencyMeasure = ((l2l_t1_t2 + l2l_t2_t1) / (l2l_t1_t2 + l2l_t2_t1 + 1))
                else:
                    quit()
    return dependencyMeasure

def createInitialIndividual(auxCrom, alphabet, log):
    influenceControl = 2 #control the "influence" of the dependency measure in the probability of setting a causality relation. Higher values for p lead to the inference of fewer causality relations among the tasks in the event log, and vice-versa.
    for i in range(len(alphabet) - 1):
        for j in range(1, len(alphabet)):
            if ran.random() < pow(dependencyMeasure(alphabet[i], alphabet[j], log), influenceControl):
                if ran.random() < 0.5:
                    if ran.random() < 0.5:
                        auxCrom[(i * 2)][(j * 2)] = 1
                    else:
                        auxCrom[(i * 2)][(j * 2) + 1] = 1
                else:
                    if ran.random() < 0.5:
                        auxCrom[(i * 2) + 1][(j * 2)] = 1
                    else:
                        auxCrom[(i * 2) + 1][(j * 2) + 1] = 1
    for i in range(len(alphabet)):
        if ran.random() < 0.5:
            auxCrom[i * 2][-3] = 1
        if ran.random() < 0.5:
            auxCrom[i * 2][-2] = 1
        if ran.random() < 0.5:
            auxCrom[i * 2][-1] = 1
        if ran.random() < 0.5:
            auxCrom[-3][i * 2] = 1
        if ran.random() < 0.5:
            auxCrom[-2][i * 2] = 1
        if ran.random() < 0.5:
            auxCrom[-1][i * 2] = 1
    return auxCrom

def initializeIndividual(alphabet):
    individual = [createEmptyIndividualTask(alphabet) for _ in range((2 * len(alphabet)) + 3)]
    return individual

def createAlphabet(log, alphabet):
    k = 0
    for i in range(len(log)):
        for j in range(len(log[i])):
            if alphabet.count(log[i][j]) == 0:
                alphabet.append(log[i][j])
            k = k + 1
    alphabet.sort()
    alphabet.insert(0,'Begin')
    alphabet.append('End')
    return

def processLog(log, logSizeAndMaxTraceSize):
    for i in range(len(log)):
        log[i].insert(0,'Begin')
        log[i].append('End')
        if logSizeAndMaxTraceSize[1] > len(log[i]):
            logSizeAndMaxTraceSize[1] = len(log[i])
        if logSizeAndMaxTraceSize[2] < len(log[i]):
            logSizeAndMaxTraceSize[2] = len(log[i])
    logSizeAndMaxTraceSize[0] = len(log)
    return logSizeAndMaxTraceSize

def initializePopulation(island, population_size, TPweight, precisenessWeight, simplicityWeight, evaluatePrecisenesscompletenessWeight, completenessAttemptFactor1, completenessAttemptFactor2, selectionOp, alphabet, log):
    population = [initializeIndividual(alphabet) for _ in range(population_size)]
    (referenceCromossome, averageEnabledTasks) = createAuxiliaryCromossome(log, alphabet)
    for i in range(len(population) - 1):
        population[i] = createInitialIndividual(population[i], alphabet, log)
    #population[-1] = copy.deepcopy(referenceCromossome)
    #for i in range(len(population)): #usado para teste com uma população inicial específica
    #    population[i] = copy.deepcopy(testCrom)
    return (population, fitn.evaluationPopulation(population, referenceCromossome, TPweight, precisenessWeight, simplicityWeight, evaluatePrecisenesscompletenessWeight, completenessAttemptFactor1, completenessAttemptFactor2, selectionOp, alphabet, log), referenceCromossome, averageEnabledTasks)