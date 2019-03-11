import random as ran
import initialPopulation as initPop
import copy
import cycle

def calculateTPTask(auxCrom, cromossome, i):
    intersectionModelAndLog = 0
    modelSum = 0
    for j in range(2, len(cromossome[i]) - 3, 2):
        if (cromossome[i][j] == 1) or (cromossome[i + 1][j] == 1) or (cromossome[i][j + 1] == 1) or (cromossome[i + 1][j + 1] == 1):
            modelSum = modelSum + 1
            if (auxCrom[i][j] == 1) or (auxCrom[i + 1][j] == 1) or (auxCrom[i][j + 1] == 1) or (auxCrom[i + 1][j + 1] == 1):
                intersectionModelAndLog = intersectionModelAndLog + 1
    if modelSum != 0:
        return (intersectionModelAndLog / modelSum)
    else:
        return 0

def calculateTP(cromossome, referenceCromossome):
    TP = 0
    for i in range(0, len(cromossome) - 5, 2):
        TP = TP + calculateTPTask(referenceCromossome, cromossome, i)
    return TP/((len(cromossome) - 5) / 2)

def countNumberOfANDTokenOutputs(tokens, index1):
    numberOfANDTokenOutputs = 0
    for k in range(len(tokens[index1][1])):
        if isinstance(tokens[index1][1][k], list):
            numberOfANDTokenOutputs = numberOfANDTokenOutputs + 1
    return numberOfANDTokenOutputs

def treatWaitingTokens(waitingTokens, tokens, inputIndexes, index1):
    if len(inputIndexes) > 0:
        for m in range(len(inputIndexes)):
            waitingTokens.append([copy.deepcopy(inputIndexes), copy.deepcopy(tokens[index1])])
    if len(waitingTokens) > 0:
        m = 0
        while m < len(waitingTokens):
            if waitingTokens[m][0].count(tokens[index1][0]) > 0:
                waitingTokens.remove(waitingTokens[m])
                m = m - 1
            m = m + 1
    return waitingTokens

def processTokensToOutpus(parsedTasks, enabledTasks, numberOfANDTokenOutputs, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, inputIndexes, topInputIndexes, bottomInputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, index2, i, l, side, activityFoundInxORorANDOutputToken, log, alphabet):
    if centralInputGatewayType == 0:
        if topInputGatewayType == 0:
            if bottomInputGatewayType == 0:
                if inputIndexes.count(tokens[index1][0]) > 0:  # 1
                    if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                        for m in range(len(tokens[index1][1][side])):
                            if tokens[index1][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                    tokens.remove(tokens[index1])
                    availableToken = 1
                    properlyParsedTasks = properlyParsedTasks + 1
                    return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
            else:
                if bottomInputGatewayType == 1:
                    if topInputIndexes.count(tokens[index1][0]) > 0:  # 2
                        if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                            for m in range(len(tokens[index1][1][side])):
                                if tokens[index1][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                    tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                        tokens.remove(tokens[index1])
                        availableToken = 1
                        properlyParsedTasks = properlyParsedTasks + 1
                        return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
                    else:
                        if bottomInputIndexes.count(tokens[index1][0]) > 0:
                            if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                for m in range(len(tokens[index1][1][side])):
                                    if tokens[index1][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                        tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                            bottomInputIndexes.remove(tokens[index1][0])
                            waitingTokens = treatWaitingTokens(waitingTokens, tokens, bottomInputIndexes, index1)
                            tokens.remove(tokens[index1])
                            if len(bottomInputIndexes) == 0:
                                availableToken = 1
                                properlyParsedTasks = properlyParsedTasks + 1
                                return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
        else:
            if topInputGatewayType == 1:
                if bottomInputGatewayType == 0:
                    if topInputIndexes.count(tokens[index1][0]) > 0:  # 3
                        if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                            for m in range(len(tokens[index1][1][side])):
                                if tokens[index1][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                    tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                        topInputIndexes.remove(tokens[index1][0])
                        waitingTokens = treatWaitingTokens(waitingTokens, tokens, topInputIndexes, index1)
                        tokens.remove(tokens[index1])
                        if len(topInputIndexes) == 0:
                            availableToken = 1
                            properlyParsedTasks = properlyParsedTasks + 1
                            return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
                    else:
                        if bottomInputIndexes.count(tokens[index1][0]) > 0:
                            if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                for m in range(len(tokens[index1][1][side])):
                                    if tokens[index1][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                        tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                            tokens.remove(tokens[index1])
                            availableToken = 1
                            properlyParsedTasks = properlyParsedTasks + 1
                            return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
                else:
                    if bottomInputGatewayType == 1:
                        if topInputIndexes.count(tokens[index1][0]) > 0:  # 4
                            if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                for m in range(len(tokens[index1][1][side])):
                                    if tokens[index1][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                        tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                            topInputIndexes.remove(tokens[index1][0])
                            waitingTokens = treatWaitingTokens(waitingTokens, tokens, topInputIndexes, index1)
                            tokens.remove(tokens[index1])
                            if len(topInputIndexes) == 0:
                                availableToken = 1
                                properlyParsedTasks = properlyParsedTasks + 1
                                return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
                        else:
                            if bottomInputIndexes.count(tokens[index1][0]) > 0:
                                if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                    for m in range(len(tokens[index1][1][side])):
                                        if tokens[index1][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                            tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                bottomInputIndexes.remove(tokens[index1][0])
                                waitingTokens = treatWaitingTokens(waitingTokens, tokens, bottomInputIndexes, index1)
                                tokens.remove(tokens[index1])
                                if len(bottomInputIndexes) == 0:
                                    availableToken = 1
                                    properlyParsedTasks = properlyParsedTasks + 1
                                    return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
    else:
        if centralInputGatewayType == 1:
            if topInputGatewayType == 1:
                if bottomInputGatewayType == 1:
                    if (((topInputIndexes.count(tokens[index1][0]) > 0) or topInputIndexes == [-1]) and ((bottomInputIndexes.count(tokens[index2][0]) > 0) or bottomInputIndexes == [-1])):  # 5
                        if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                            if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                if len(tokens[max(index1, index2)][1]) > 1:
                                    if isinstance(tokens[max(index1, index2)][1][side], list):
                                        for m in range(len(tokens[max(index1, index2)][1][side])):
                                            if tokens[max(index1, index2)][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                                tokens.append([tokens[max(index1, index2)][0], [tokens[max(index1, index2)][1][side][m]]])
                                if index1 != index2:
                                    if len(tokens[min(index1, index2)][1]) > 1:
                                        if isinstance(tokens[min(index1, index2)][1][side], list):
                                            for m in range(len(tokens[min(index1, index2)][1][side])):
                                                if tokens[min(index1, index2)][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                                    tokens.append([tokens[min(index1, index2)][0], [tokens[min(index1, index2)][1][side][m]]])
                            else:
                                if (topInputIndexes != [-1]) and (bottomInputIndexes == [-1]):
                                    if len(tokens[index1][1]) > 1:
                                        if isinstance(tokens[index1][1][side], list):
                                            for m in range(len(tokens[index1][1][side])):
                                                if tokens[index1][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                                    tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                else:
                                    if (topInputIndexes == [-1]) and (bottomInputIndexes != [-1]):
                                        if len(tokens[index2][1]) > 1:
                                            if isinstance(tokens[index2][1][side], list):
                                                for m in range(len(tokens[index2][1][side])):
                                                    if tokens[index2][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                                        tokens.append([tokens[index2][0], [tokens[index2][1][side][m]]])
                        if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                            topInputIndexes.remove(tokens[index1][0])
                            bottomInputIndexes.remove(tokens[index2][0])
                            waitingTokens = treatWaitingTokens(waitingTokens, tokens, topInputIndexes, index1)
                            waitingTokens = treatWaitingTokens(waitingTokens, tokens, bottomInputIndexes, index2)
                            tokens.remove(tokens[max(index1, index2)])
                            if index1 != index2:
                                tokens.remove(tokens[min(index1, index2)])
                        else:
                            if (topInputIndexes != [-1]) and (bottomInputIndexes == [-1]):
                                topInputIndexes.remove(tokens[index1][0])
                                waitingTokens = treatWaitingTokens(waitingTokens, tokens, topInputIndexes, index1)
                                bottomInputIndexes.remove(-1)
                                tokens.remove(tokens[index1])
                            else:
                                topInputIndexes.remove(-1)
                                bottomInputIndexes.remove(tokens[index2][0])
                                waitingTokens = treatWaitingTokens(waitingTokens, tokens, bottomInputIndexes, index2)
                                tokens.remove(tokens[index1])
                        if (len(topInputIndexes) == 0) and (len(bottomInputIndexes) == 0):
                            availableToken = 1
                            properlyParsedTasks = properlyParsedTasks + 1
                            return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
                else:
                    if bottomInputGatewayType == 0:
                        if (((topInputIndexes.count(tokens[index1][0]) > 0) or topInputIndexes == [-1]) and ((bottomInputIndexes.count(tokens[index2][0]) > 0) or bottomInputIndexes == [-1])):  # 6
                            if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                    if len(tokens[max(index1, index2)][1]) > 1:
                                        if isinstance(tokens[max(index1, index2)][1][side], list):
                                            for m in range(len(tokens[max(index1, index2)][1][side])):
                                                if tokens[max(index1, index2)][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                                    tokens.append([tokens[max(index1, index2)][0], [tokens[max(index1, index2)][1][side][m]]])
                                    if index1 != index2:
                                        if len(tokens[min(index1, index2)][1]) > 1:
                                            if isinstance(tokens[min(index1, index2)][1][side], list):
                                                for m in range(len(tokens[min(index1, index2)][1][side])):
                                                    if tokens[min(index1, index2)][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                                        tokens.append([tokens[min(index1, index2)][0], [tokens[min(index1, index2)][1][side][m]]])
                            if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                topInputIndexes.remove(tokens[index1][0])
                                waitingTokens = treatWaitingTokens(waitingTokens, tokens, topInputIndexes, index1)
                                if (len(topInputIndexes) > 0):
                                    tokens.remove(tokens[index1])
                                else:
                                    tokens.remove(tokens[max(index1, index2)])
                                    if index1 != index2:
                                        tokens.remove(tokens[min(index1, index2)])
                            if len(topInputIndexes) == 0:
                                availableToken = 1
                                properlyParsedTasks = properlyParsedTasks + 1
                                return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
            else:
                if topInputGatewayType == 0:
                    if bottomInputGatewayType == 1:
                        if (((topInputIndexes.count(tokens[index1][0]) > 0) or topInputIndexes == [-1]) and ((bottomInputIndexes.count(tokens[index2][0]) > 0) or bottomInputIndexes == [-1])):  # 7
                            if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                    if len(tokens[max(index1, index2)][1]) > 1:
                                        if isinstance(tokens[max(index1, index2)][1][side], list):
                                            for m in range(len(tokens[max(index1, index2)][1][side])):
                                                if tokens[max(index1, index2)][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                                    tokens.append([tokens[max(index1, index2)][0], [tokens[max(index1, index2)][1][side][m]]])
                                    if index1 != index2:
                                        if len(tokens[min(index1, index2)][1]) > 1:
                                            if isinstance(tokens[min(index1, index2)][1][side], list):
                                                for m in range(len(tokens[min(index1, index2)][1][side])):
                                                    if tokens[min(index1, index2)][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                                        tokens.append([tokens[min(index1, index2)][0], [tokens[min(index1, index2)][1][side][m]]])
                            if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                bottomInputIndexes.remove(tokens[index2][0])
                                waitingTokens = treatWaitingTokens(waitingTokens, tokens, bottomInputIndexes, index1)
                                if len(bottomInputIndexes) > 0:
                                    tokens.remove(tokens[index2])
                                else:
                                    tokens.remove(tokens[max(index1, index2)])
                                    if index1 != index2:
                                        tokens.remove(tokens[min(index1, index2)])
                            if len(bottomInputIndexes) == 0:
                                availableToken = 1
                                properlyParsedTasks = properlyParsedTasks + 1
                                return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
                    else:
                        if bottomInputGatewayType == 0: # 8
                            if (((topInputIndexes.count(tokens[index1][0]) > 0) or topInputIndexes == [-1]) and ((bottomInputIndexes.count(tokens[index2][0]) > 0) or bottomInputIndexes == [-1])):
                                if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                    if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                        if len(tokens[max(index1, index2)][1]) > 1:
                                            if isinstance(tokens[max(index1, index2)][1][side], list):
                                                for m in range(len(tokens[max(index1, index2)][1][side])):
                                                    if tokens[max(index1, index2)][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                                        tokens.append([tokens[max(index1, index2)][0], [tokens[max(index1, index2)][1][side][m]]])
                                        if index1 != index2:
                                            if len(tokens[min(index1, index2)][1]) > 1:
                                                if isinstance(tokens[min(index1, index2)][1][side], list):
                                                    for m in range(len(tokens[min(index1, index2)][1][side])):
                                                        if tokens[min(index1, index2)][1][side][m] != initPop.getTaskID(log[i][l], alphabet):
                                                            tokens.append([tokens[min(index1, index2)][0], [tokens[min(index1, index2)][1][side][m]]])
                                if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                    tokens.remove(tokens[max(index1, index2)])
                                    if index1 != index2:
                                        tokens.remove(tokens[min(index1, index2)])
                                availableToken = 1
                                properlyParsedTasks = properlyParsedTasks + 1
                                return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
    return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 0, parsedTasks, enabledTasks)

def addressSpecificInputType(tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, completenessAttemptFactor1, completenessAttemptFactor2, incorrectlyFiredTasks, log, alphabet):
    count = 0
    while (len(tokens) > 0) and (count < (completenessAttemptFactor1 + pow(len(tokens), completenessAttemptFactor2))):
        count = count + 1
        index1 = ran.randrange(0, len(tokens))
        index2 = ran.randrange(0, len(tokens))
        numberOfANDTokenOutputs = countNumberOfANDTokenOutputs(tokens, index1)
        if len(topInputIndexes) == 0:
            topInputIndexes.append(-1)
        if len(bottomInputIndexes) == 0:
            bottomInputIndexes.append(-1)
        if len(inputIndexes) == 0:
            inputIndexes.append(-1)
        if numberOfANDTokenOutputs == 0:
            if tokens[index1][1].count(initPop.getTaskID(log[i][l], alphabet)) > 0:
                (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, breakSignal, parsedTasks, enabledTasks) = processTokensToOutpus(parsedTasks, enabledTasks, numberOfANDTokenOutputs, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, inputIndexes, topInputIndexes, bottomInputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, index2, 0, 0, 0, 0, log, alphabet)
                if breakSignal == 1:
                    break
        else:
            if numberOfANDTokenOutputs == 1:
                if tokens[index1][1][0].count(initPop.getTaskID(log[i][l], alphabet)) > 0:
                    (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, breakSignal, parsedTasks, enabledTasks) = processTokensToOutpus(parsedTasks, enabledTasks, numberOfANDTokenOutputs, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, inputIndexes, topInputIndexes, bottomInputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, index2, i, l, 0, 1, log, alphabet)
                    if breakSignal == 1:
                        break
                else:
                    if tokens[index1][1].count(initPop.getTaskID(log[i][l], alphabet)) > 0:
                        (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, breakSignal, parsedTasks, enabledTasks) = processTokensToOutpus(parsedTasks, enabledTasks, numberOfANDTokenOutputs, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, inputIndexes, topInputIndexes, bottomInputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, index2, i, l, 0, 0, log, alphabet)
                        if breakSignal == 1:
                            break
            else:
                if numberOfANDTokenOutputs == 2:
                    if tokens[index1][1][0].count(initPop.getTaskID(log[i][l], alphabet)) > 0:
                        (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, breakSignal, parsedTasks, enabledTasks) = processTokensToOutpus(parsedTasks, enabledTasks, numberOfANDTokenOutputs, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, inputIndexes, topInputIndexes, bottomInputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, index2, i, l, 0, 0, log, alphabet)
                        if breakSignal == 1:
                            break
                    else:
                        if tokens[index1][1][1].count(initPop.getTaskID(log[i][l], alphabet)) > 0:
                            (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, breakSignal, parsedTasks, enabledTasks) = processTokensToOutpus(parsedTasks, enabledTasks, numberOfANDTokenOutputs, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, inputIndexes, topInputIndexes, bottomInputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, index2, i, l, 1, 0, log, alphabet)
                            if breakSignal == 1:
                                break
    if availableToken == 0:
        if incorrectlyFiredTasks.count(l) == 0:
            incorrectlyFiredTasks.append(initPop.getTaskID(log[i][l], alphabet))
        if centralInputGatewayType == 0:
            missingLocalTokens = missingLocalTokens + 1
        else:
            if centralInputGatewayType == 1:
                missingLocalTokens = missingLocalTokens + len(inputIndexes)
    return (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks, incorrectlyFiredTasks)

def checkEnabledTasks(cromossome, parsedTasks, enabledTasks, tasks, alphabet):
    parsedTasks.append(tasks[0])
    for j in range(len((tasks[1]))):
        if isinstance(tasks[1][j], list):
            for k in range(len(tasks[1][j])):
                inputTTasks = []
                inputBTasks = []
                for i in range(len(alphabet)):
                    if ((cromossome[(i * 2)][(tasks[1][j][k] * 2)]) == 1) or ((cromossome[(i * 2)][(tasks[1][j][k] * 2) + 1]) == 1):
                        inputTTasks.append(i)
                    if ((cromossome[(i * 2) + 1][(tasks[1][j][k] * 2)]) == 1) or ((cromossome[(i * 2) + 1][(tasks[1][j][k] * 2) + 1]) == 1):
                        inputBTasks.append(i)
                if (len(inputTTasks) == 0) and (len(inputBTasks) == 0):
                    enabledTasks.append(tasks[1][j][k])
                else:
                    inputTTasksInParsedTasks = 0
                    inputBTasksInParsedTasks = 0
                    for l in range(len(inputTTasks)):
                        if parsedTasks.count(inputTTasks[l]) > 0:
                            inputTTasksInParsedTasks = inputTTasksInParsedTasks + 1
                    for l in range(len(inputBTasks)):
                        if parsedTasks.count(inputBTasks[l]) > 0:
                            inputBTasksInParsedTasks = inputBTasksInParsedTasks + 1
                    if (len(inputTTasks) <= 1) and (len(inputBTasks) <= 1):
                        if (len(inputTTasks) == 1) and (len(inputBTasks) == 0):
                            if ((cromossome[-2][(tasks[1][j][k] * 2)] == 1) and (inputTTasksInParsedTasks == len(inputTTasks))) or ((cromossome[-2][(tasks[1][j][k] * 2)] == 0) and (inputTTasksInParsedTasks > 0)):
                                enabledTasks.append(tasks[1][j][k])
                        if (len(inputTTasks) == 0) and (len(inputBTasks) == 1):
                            if ((cromossome[-1][(tasks[1][j][k] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j][k] * 2)] == 0) and (inputBTasksInParsedTasks > 0)):
                                enabledTasks.append(tasks[1][j][k])
                        if (len(inputTTasks) == 1) and (len(inputBTasks) == 1):
                            if (((cromossome[-3][(tasks[1][j][k] * 2)] == 1) and ((inputTTasksInParsedTasks > 0) and (inputBTasksInParsedTasks > 0))) or ((cromossome[-3][(tasks[1][j][k] * 2)] == 0) and ((inputTTasksInParsedTasks > 0) or (inputBTasksInParsedTasks > 0)))):
                                enabledTasks.append(tasks[1][j][k])
                    else:
                        if (len(inputTTasks) == 0) or (len(inputBTasks) == 0):
                            if (len(inputTTasks) > 0) and (len(inputBTasks) == 0):
                                if ((cromossome[-2][(tasks[1][j][k] * 2)] == 1) and (inputTTasksInParsedTasks == len(inputTTasks))) or ((cromossome[-2][(tasks[1][j][k] * 2)] == 0) and (inputTTasksInParsedTasks > 0)):
                                    enabledTasks.append(tasks[1][j][k])
                            if (len(inputTTasks) == 0) and (len(inputBTasks) > 0):
                                if ((cromossome[-1][(tasks[1][j][k] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j][k] * 2)] == 0) and (inputBTasksInParsedTasks > 0)):
                                    enabledTasks.append(tasks[1][j][k])
                        else:
                            if cromossome[-3][(tasks[1][j][k] * 2)] == 0:
                                if ((((cromossome[-2][(tasks[1][j][k] * 2)] == 1) and (inputTTasksInParsedTasks == len(inputTTasks))) or ((cromossome[-2][(tasks[1][j][k] * 2)] == 0) and (inputTTasksInParsedTasks > 0))) or (((cromossome[-1][(tasks[1][j][k] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j][k] * 2)] == 0) and (inputBTasksInParsedTasks > 0)))):
                                    enabledTasks.append(tasks[1][j][k])
                            if cromossome[-3][(tasks[1][j][k] * 2)] == 1:
                                if ((((cromossome[-2][(tasks[1][j][k] * 2)] == 1) and (inputTTasksInParsedTasks == len(inputTTasks))) or ((cromossome[-2][(tasks[1][j][k] * 2)] == 0) and (inputTTasksInParsedTasks > 0))) and (((cromossome[-1][(tasks[1][j][k] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j][k] * 2)] == 0) and (inputBTasksInParsedTasks > 0)))):
                                    enabledTasks.append(tasks[1][j][k])
        else:
            inputTTasks = []
            inputBTasks = []
            for i in range(len(alphabet)):
                if ((cromossome[(i * 2)][(tasks[1][j] * 2)]) == 1) or ((cromossome[(i * 2)][(tasks[1][j] * 2) + 1]) == 1):
                    inputTTasks.append(i)
                if ((cromossome[(i * 2) + 1][(tasks[1][j] * 2)]) == 1) or ((cromossome[(i * 2) + 1][(tasks[1][j] * 2) + 1]) == 1):
                    inputBTasks.append(i)
            if (len(inputTTasks) == 0) and (len(inputBTasks) == 0):
                enabledTasks.append(tasks[1][j])
            else:
                inputTTasksInParsedTasks = 0
                inputBTasksInParsedTasks = 0
                for l in range(len(inputTTasks)):
                    if parsedTasks.count(inputTTasks[l]) > 0:
                        inputTTasksInParsedTasks = inputTTasksInParsedTasks + 1
                for l in range(len(inputBTasks)):
                    if parsedTasks.count(inputBTasks[l]) > 0:
                        inputBTasksInParsedTasks = inputBTasksInParsedTasks + 1
                if (len(inputTTasks) <= 1) and (len(inputBTasks) <= 1):
                    if (len(inputTTasks) == 1) and (len(inputBTasks) == 0):
                        if ((cromossome[-2][(tasks[1][j] * 2)] == 1) and (inputTTasksInParsedTasks == len(inputTTasks))) or ((cromossome[-2][(tasks[1][j] * 2)] == 0) and (inputTTasksInParsedTasks > 0)):
                            enabledTasks.append(tasks[1][j])
                    if (len(inputTTasks) == 0) and (len(inputBTasks) == 1):
                        if ((cromossome[-1][(tasks[1][j] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j] * 2)] == 0) and (inputBTasksInParsedTasks > 0)):
                            enabledTasks.append(tasks[1][j])
                    if (len(inputTTasks) == 1) and (len(inputBTasks) == 1):
                        if (((cromossome[-3][(tasks[1][j] * 2)] == 1) and ((inputTTasksInParsedTasks > 0) and (inputBTasksInParsedTasks > 0))) or ((cromossome[-3][(tasks[1][j] * 2)] == 0) and ((inputTTasksInParsedTasks > 0) or (inputBTasksInParsedTasks > 0)))):
                            enabledTasks.append(tasks[1][j])
                else:
                    if (len(inputTTasks) == 0) or (len(inputBTasks) == 0):
                        if (len(inputTTasks) > 0) and (len(inputBTasks) == 0):
                            if ((cromossome[-2][(tasks[1][j] * 2)] == 1) and (inputTTasksInParsedTasks == len(inputTTasks))) or ((cromossome[-2][(tasks[1][j] * 2)] == 0) and (inputTTasksInParsedTasks > 0)):
                                enabledTasks.append(tasks[1][j])
                        if (len(inputTTasks) == 0) and (len(inputBTasks) > 0):
                            if ((cromossome[-1][(tasks[1][j] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j] * 2)] == 0) and (inputBTasksInParsedTasks > 0)):
                                enabledTasks.append(tasks[1][j])
                    else:
                        if cromossome[-3][(tasks[1][j] * 2)] == 0:
                            if ((((cromossome[-2][(tasks[1][j] * 2)] == 1) and (inputTTasksInParsedTasks == len(inputTTasks))) or ((cromossome[-2][(tasks[1][j] * 2)] == 0) and (inputTTasksInParsedTasks > 0))) or (((cromossome[-1][(tasks[1][j] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j] * 2)] == 0) and (inputBTasksInParsedTasks > 0)))):
                                enabledTasks.append(tasks[1][j])
                        if cromossome[-3][(tasks[1][j] * 2)] == 1:
                            if ((((cromossome[-2][(tasks[1][j] * 2)] == 1) and (inputTTasksInParsedTasks == len(inputTTasks))) or ((cromossome[-2][(tasks[1][j] * 2)] == 0) and (inputTTasksInParsedTasks > 0))) and (((cromossome[-1][(tasks[1][j] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j] * 2)] == 0) and (inputBTasksInParsedTasks > 0)))):
                                enabledTasks.append(tasks[1][j])
    return (parsedTasks, enabledTasks)

def calculateCompletenessAndPreciseness(cromossome, completenessAttemptFactor1, completenessAttemptFactor2, log, alphabet):
    tracesInLog = len(log)
    tasksInLog = 0
    properlyParsedTasks = 0
    missingTokens = 0
    extraTokensLeftBehind = 0
    tracesWithMissingTokens = 0
    tracesWithExtraTokensLeftBehind = 0
    enabledTasks = []
    incorrectlyFiredTasks = []
    for i in range(len(log)):
        parsedTasks = []
        missingLocalTokens = 0
        tokens = [[-1, [0]]]
        parsedTasks, enabledTasks = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, tokens[0], alphabet)
        waitingTokens = []
        for l in range(0, len(log[i])):
            tasksInLog = tasksInLog + 1
            availableToken = 0
            topInputIndexes = []
            bottomInputIndexes = []
            for j in range(0, len(alphabet)):
                if (cromossome[(j * 2)][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 1) or (cromossome[(j * 2)][(initPop.getTaskID(log[i][l], alphabet) * 2) + 1] == 1):
                    topInputIndexes.append(j)
                if (cromossome[(j * 2) + 1][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 1) or (cromossome[(j * 2) + 1][(initPop.getTaskID(log[i][l], alphabet) * 2) + 1] == 1):
                    bottomInputIndexes.append(j)
            inputIndexes = topInputIndexes + bottomInputIndexes
            if (cromossome[-3][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 0):
                if (cromossome[-2][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 0):
                    if (cromossome[-1][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 0):
                        (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks, incorrectlyFiredTasks) = addressSpecificInputType(tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 0, 0, 0, completenessAttemptFactor1, completenessAttemptFactor2, incorrectlyFiredTasks, log, alphabet)
                    else:
                        if (cromossome[-1][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 1):
                            (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks, incorrectlyFiredTasks) = addressSpecificInputType(tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 0, 0, 1, completenessAttemptFactor1, completenessAttemptFactor2, incorrectlyFiredTasks, log, alphabet)
                else:
                    if (cromossome[-2][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 1):
                        if (cromossome[-1][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 0):
                            (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks, incorrectlyFiredTasks) = addressSpecificInputType(tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 0, 1, 0, completenessAttemptFactor1, completenessAttemptFactor2, incorrectlyFiredTasks, log, alphabet)
                        else:
                            if (cromossome[-1][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 1):
                                (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks, incorrectlyFiredTasks) = addressSpecificInputType(tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 0, 1, 1, completenessAttemptFactor1, completenessAttemptFactor2, incorrectlyFiredTasks, log, alphabet)
            else:
                if (cromossome[-3][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 1):
                    if (cromossome[-2][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 1):
                        if (cromossome[-1][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 1):
                            (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks, incorrectlyFiredTasks) = addressSpecificInputType(tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 1, 1, 1, completenessAttemptFactor1, completenessAttemptFactor2, incorrectlyFiredTasks, log, alphabet)
                        else:
                            if (cromossome[-1][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 0):
                                (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks, incorrectlyFiredTasks) = addressSpecificInputType(tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 1, 1, 0, completenessAttemptFactor1, completenessAttemptFactor2, incorrectlyFiredTasks, log, alphabet)
                    else:
                        if (cromossome[-2][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 0):
                            if (cromossome[-1][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 1):
                                (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks, incorrectlyFiredTasks) = addressSpecificInputType(tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 1, 0, 1, completenessAttemptFactor1, completenessAttemptFactor2, incorrectlyFiredTasks, log, alphabet)
                            else:
                                if (cromossome[-1][(initPop.getTaskID(log[i][l], alphabet) * 2)] == 0):
                                    (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks, incorrectlyFiredTasks) = addressSpecificInputType(tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 1, 0, 0, completenessAttemptFactor1, completenessAttemptFactor2, incorrectlyFiredTasks, log, alphabet)
            if initPop.getTaskID(log[i][l], alphabet) != (len(alphabet) - 1):
                outputLIndexes = []
                outputRIndexes = []
                for j in range(len(alphabet)):
                    if (cromossome[(initPop.getTaskID(log[i][l], alphabet) * 2)][(j * 2)] == 1) or (cromossome[(initPop.getTaskID(log[i][l], alphabet) * 2) + 1][(j * 2)] == 1):
                        outputLIndexes.append(j)
                    if (cromossome[(initPop.getTaskID(log[i][l], alphabet) * 2)][(j * 2) + 1] == 1) or (cromossome[(initPop.getTaskID(log[i][l], alphabet) * 2) + 1][(j * 2) + 1] == 1):
                        outputRIndexes.append(j)
                if cromossome[(initPop.getTaskID(log[i][l], alphabet)) * 2][-3] == 1:
                    if cromossome[(initPop.getTaskID(log[i][l], alphabet)) * 2][-2] == 1:
                        for j in range(len(outputLIndexes)):
                            tokens.append([initPop.getTaskID(log[i][l], alphabet), [outputLIndexes[j]]])
                            (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(log[i][l], alphabet), [outputLIndexes[j]]], alphabet)
                    else:
                        if cromossome[(initPop.getTaskID(log[i][l], alphabet)) * 2][-2] == 0:
                            xORoutputs = []
                            for j in range(len(outputLIndexes)):
                                xORoutputs.append(outputLIndexes[j])
                            if xORoutputs != []:
                                tokens.append([initPop.getTaskID(log[i][l], alphabet), xORoutputs])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(log[i][l], alphabet), xORoutputs], alphabet)
                    if cromossome[(initPop.getTaskID(log[i][l], alphabet)) * 2][-1] == 1:
                        for j in range(len(outputRIndexes)):
                            tokens.append([initPop.getTaskID(log[i][l], alphabet), [outputRIndexes[j]]])
                            (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(log[i][l], alphabet), [outputRIndexes[j]]], alphabet)
                    else:
                        if cromossome[(initPop.getTaskID(log[i][l], alphabet)) * 2][-1] == 0:
                            xORoutputs = []
                            for j in range(len(outputRIndexes)):
                                xORoutputs.append(outputRIndexes[j])
                            if xORoutputs != []:
                                tokens.append([initPop.getTaskID(log[i][l], alphabet), xORoutputs])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(log[i][l], alphabet), xORoutputs], alphabet)
                else:
                    if cromossome[(initPop.getTaskID(log[i][l], alphabet)) * 2][-3] == 0:
                        xORLoutputs = []
                        xORRoutputs = []
                        ANDLoutputs = []
                        ANDRoutputs = []
                        if cromossome[(initPop.getTaskID(log[i][l], alphabet)) * 2][-2] == 0:
                            for j in range(len(outputLIndexes)):
                                xORLoutputs.append(outputLIndexes[j])
                        else:
                            if cromossome[(initPop.getTaskID(log[i][l], alphabet)) * 2][-2] == 1:
                                for j in range(len(outputLIndexes)):
                                    ANDLoutputs.append(outputLIndexes[j])
                        if cromossome[(initPop.getTaskID(log[i][l], alphabet)) * 2][-1] == 0:
                            for j in range(len(outputRIndexes)):
                                xORRoutputs.append(outputRIndexes[j])
                        else:
                            if cromossome[(initPop.getTaskID(log[i][l], alphabet)) * 2][-1] == 1:
                                for j in range(len(outputRIndexes)):
                                    ANDRoutputs.append(outputRIndexes[j])
                        if ((len(xORLoutputs) > 0) and (len(xORRoutputs) > 0) and (len(ANDLoutputs) == 0) and (len(ANDRoutputs) == 0)) or ((len(xORLoutputs) > 0) and (len(xORRoutputs) == 0) and (len(ANDLoutputs) == 0) and (len(ANDRoutputs) == 0)) or ((len(xORLoutputs) == 0) and (len(xORRoutputs) > 0) and (len(ANDLoutputs) == 0) and (len(ANDRoutputs) == 0)):
                            tokens.append([initPop.getTaskID(log[i][l], alphabet), xORLoutputs + xORRoutputs])
                            (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(log[i][l], alphabet), xORLoutputs + xORRoutputs], alphabet)
                        else:
                            if (len(xORLoutputs) == 0) and (len(xORRoutputs) == 0) and (len(ANDLoutputs) > 0) and (len(ANDRoutputs) > 0):
                                tokens.append([initPop.getTaskID(log[i][l], alphabet), [ANDLoutputs] + [ANDRoutputs]])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(log[i][l], alphabet), [ANDLoutputs] + [ANDRoutputs]], alphabet)
                            if (len(xORLoutputs) == 0) and (len(xORRoutputs) > 0) and (len(ANDLoutputs) > 0) and (len(ANDRoutputs) == 0):
                                tokens.append([initPop.getTaskID(log[i][l], alphabet), [ANDLoutputs] + xORRoutputs])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(log[i][l], alphabet), [ANDLoutputs] + xORRoutputs], alphabet)
                            if (len(xORLoutputs) > 0) and (len(xORRoutputs) == 0) and (len(ANDLoutputs) == 0) and (len(ANDRoutputs) > 0):
                                tokens.append([initPop.getTaskID(log[i][l], alphabet), [ANDRoutputs] + xORLoutputs])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(log[i][l], alphabet), [ANDRoutputs] + xORLoutputs], alphabet)
                            if (len(xORLoutputs) == 0) and (len(xORRoutputs) == 0) and (len(ANDLoutputs) > 0) and (len(ANDRoutputs) == 0):
                                tokens.append([initPop.getTaskID(log[i][l], alphabet), [ANDLoutputs]])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(log[i][l], alphabet), [ANDLoutputs]], alphabet)
                            if (len(xORLoutputs) == 0) and (len(xORRoutputs) == 0) and (len(ANDLoutputs) == 0) and (len(ANDRoutputs) > 0):
                                tokens.append([initPop.getTaskID(log[i][l], alphabet), [ANDRoutputs]])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(log[i][l], alphabet), [ANDRoutputs]], alphabet)
                            if (len(xORLoutputs) == 0) and (len(xORRoutputs) == 0) and (len(ANDLoutputs) == 0) and (len(ANDRoutputs) == 0):
                                tokens.append([initPop.getTaskID(log[i][l], alphabet), []])
        if missingLocalTokens > 0:
            tracesWithMissingTokens = tracesWithMissingTokens + 1
            missingTokens = missingTokens + missingLocalTokens
        if (len(tokens) + len(waitingTokens)) > 0:
            tracesWithExtraTokensLeftBehind = tracesWithExtraTokensLeftBehind + 1
            extraTokensLeftBehind = extraTokensLeftBehind + len(tokens) + len(waitingTokens)
            for l in range(len(tokens)):
                if incorrectlyFiredTasks.count(tokens[l][0]) == 0:
                    incorrectlyFiredTasks.append(tokens[l][0])
            for l in range(len(waitingTokens)):
                if incorrectlyFiredTasks.count(waitingTokens[l][0][0]) == 0:
                    incorrectlyFiredTasks.append(waitingTokens[l][0][0])
    punishment = ((missingTokens / (tracesInLog - tracesWithMissingTokens + 1)) + (extraTokensLeftBehind / (tracesInLog - tracesWithExtraTokensLeftBehind + 1)))
    completeness = ((properlyParsedTasks - punishment) / tasksInLog)
    precisenessAKM = len(enabledTasks) / len(alphabet)
    if len(enabledTasks) > 0:
        precisenessBVB = 1 / len(enabledTasks)
    else:
        precisenessBVB = 1
    return (completeness, precisenessAKM, precisenessBVB, incorrectlyFiredTasks)

def calculateSimplicity(cromossome, alphabet):
    enabledOuputTasks = 0
    outputInternalANDGateways = 0
    outputInternalXORGateways = 0
    outputExternalANDGateways = 0
    outputExternalXORGateways = 0
    for i in range(len(alphabet)):
        enabledLOuputTasks = 0
        enabledROuputTasks = 0
        for j in range(1, len(alphabet)):
            if (cromossome[i * 2][j * 2] == 1) or (cromossome[(i * 2) + 1][j * 2] == 1):
                enabledLOuputTasks = enabledLOuputTasks + 1
            if (cromossome[i * 2][(j * 2) + 1] == 1) or (cromossome[(i * 2) + 1][(j * 2) + 1] == 1):
                enabledROuputTasks = enabledROuputTasks + 1
        enabledOuputTasks = enabledOuputTasks + enabledLOuputTasks + enabledROuputTasks
        if enabledLOuputTasks > 1:
            if cromossome[i * 2][-2] == 0:
                outputInternalXORGateways = outputInternalXORGateways + 1
            else:
                outputInternalANDGateways = outputInternalANDGateways + 1
        if enabledROuputTasks > 1:
            if cromossome[i * 2][-1] == 0:
                outputInternalXORGateways = outputInternalXORGateways + 1
            else:
                outputInternalANDGateways = outputInternalANDGateways + 1
        if (enabledLOuputTasks > 0) and (enabledROuputTasks > 0):
            if cromossome[i * 2][-3] == 0:
                outputExternalXORGateways = outputExternalXORGateways + 1
            else:
                outputExternalANDGateways = outputExternalANDGateways + 1
    enabledInputTasks = 0
    inputInternalANDGateways = 0
    inputInternalXORGateways = 0
    inputExternalANDGateways = 0
    inputExternalXORGateways = 0
    for i in range(len(alphabet)):
        enabledTInputTasks = 0
        enabledBInputTasks = 0
        for j in range(len(alphabet) - 1):
            if (cromossome[j * 2][i * 2] == 1) or (cromossome[j * 2][(i * 2) + 1] == 1):
                enabledTInputTasks = enabledTInputTasks + 1
            if (cromossome[(j * 2) + 1][i * 2] == 1) or (cromossome[(j * 2) + 1][(i * 2) + 1] == 1):
                enabledBInputTasks = enabledBInputTasks + 1
        enabledInputTasks = enabledInputTasks + enabledTInputTasks + enabledBInputTasks
        if enabledTInputTasks > 1:
            if cromossome[-2][i * 2] == 0:
                inputInternalXORGateways = inputInternalXORGateways + 1
            else:
                inputInternalANDGateways = inputInternalANDGateways + 1
        if enabledBInputTasks > 1:
            if cromossome[-1][i * 2] == 0:
                inputInternalXORGateways = inputInternalXORGateways + 1
            else:
                inputInternalANDGateways = inputInternalANDGateways + 1
        if (enabledTInputTasks > 0) and (enabledBInputTasks > 0):
            if cromossome[-3][i * 2] == 0:
                inputExternalXORGateways = inputExternalXORGateways + 1
            else:
                inputExternalANDGateways = inputExternalANDGateways + 1
    if (enabledOuputTasks + enabledInputTasks + inputInternalXORGateways + inputExternalXORGateways + inputInternalANDGateways + inputExternalANDGateways + outputInternalXORGateways + outputExternalXORGateways + outputInternalANDGateways + outputExternalANDGateways) == 0:
        return 0
    else:
        return (1 / (enabledOuputTasks + enabledInputTasks + inputInternalXORGateways + inputExternalXORGateways + inputInternalANDGateways + inputExternalANDGateways + outputInternalXORGateways + outputExternalXORGateways + outputInternalANDGateways + outputExternalANDGateways))

def adaptCromossome(cromossome, alphabet):
    for i in range(len(alphabet)):
        numberOfL1 = 0
        numberOfR1 = 0
        for j in range(len(alphabet)):
            if (cromossome[i * 2][j * 2] == 1) or (cromossome[(i * 2) + 1][j * 2] == 1):
                numberOfL1 = numberOfL1 + 1
                if numberOfL1 == 2:
                    break
        for j in range(len(alphabet)):
            if (cromossome[i * 2][(j * 2) + 1] == 1) or (cromossome[(i * 2) + 1][(j * 2) + 1] == 1):
                numberOfR1 = numberOfR1 + 1
                if numberOfR1 == 2:
                    break
        if (cromossome[i * 2][-1] == 1) and (numberOfR1 <= 1):
            cromossome[i * 2][-1] = 0
        if (cromossome[i * 2][-2] == 1) and (numberOfL1 <= 1):
            cromossome[i * 2][-2] = 0
        if (cromossome[i * 2][-3] == 1) and ((numberOfL1 == 0) or (numberOfR1 == 0)):
            cromossome[i * 2][-3] = 0
    for i in range(len(alphabet)):
        numberOfT1 = 0
        numberOfB1 = 0
        for j in range(len(alphabet)):
            if (cromossome[j * 2][i * 2] == 1) or (cromossome[j * 2][(i * 2) + 1] == 1):
                numberOfT1 = numberOfT1 + 1
                if numberOfT1 == 2:
                    break
        for j in range(len(alphabet)):
            if (cromossome[(j * 2) + 1][i * 2] == 1) or (cromossome[(j * 2) + 1][(i * 2) + 1] == 1):
                numberOfB1 = numberOfB1 + 1
                if numberOfB1 == 2:
                    break
        if (cromossome[-1][i * 2] == 1) and (numberOfB1 <= 1):
            cromossome[-1][i * 2] = 0
        if (cromossome[-2][i * 2] == 1) and (numberOfT1 <= 1):
            cromossome[-2][i * 2] = 0
        if (cromossome[-3][i * 2] == 1) and ((numberOfT1 == 0) or (numberOfB1 == 0)):
            cromossome[-3][i * 2] = 0
    return cromossome

def evaluateIndividual(cromossome, referenceCromossome, TPweight, precisenessWeight, simplicityWeight, completenessWeight, i, completenessAttemptFactor1, completenessAttemptFactor2, alphabet, log):
    TP = calculateTP(cromossome, referenceCromossome)
    completeness = 0
    precisenessAKM = 0
    precisenessBVB = 0
    simplicity = 0
    temporaryAdaptedCromossome = adaptCromossome(copy.deepcopy(cromossome), alphabet)
    (completeness, precisenessAKM, precisenessBVB, incorrectlyFiredTasks) = calculateCompletenessAndPreciseness(temporaryAdaptedCromossome, completenessAttemptFactor1, completenessAttemptFactor2, log, alphabet)
    if (simplicityWeight > 0):
        simplicity = calculateSimplicity(cromossome, alphabet)
    if (precisenessWeight == 0):
        precisenessAKM = 0
        precisenessBVB = 0
    fitnessAKM = ((((completeness * completenessWeight) + (TP * TPweight)) - (precisenessAKM * precisenessWeight) - (simplicity * simplicityWeight)), completeness, TP, precisenessAKM, simplicity, i, incorrectlyFiredTasks)
    fitnessBVB = ((((completeness * completenessWeight) + (TP * TPweight)) - ((1 - precisenessBVB) * precisenessWeight) - ((1 - simplicity) * simplicityWeight)), completeness, TP, precisenessBVB, simplicity, i, incorrectlyFiredTasks)
    return fitnessBVB

def normalizeTotalFitness(evaluationValues):
    sortedEvaluationValues = sorted(evaluationValues, reverse=True, key=cycle.takeFirst)
    maxValue = sortedEvaluationValues[0][0]
    minValue = sortedEvaluationValues[-1][0]
    if maxValue > 0:
        newMaxValue = maxValue
    else:
        newMaxValue = 0.00001
    if minValue > 0:
        newMinValue = minValue
    else:
        newMinValue = 0
    normalizedEvaluationValues = []
    for i in range(len(evaluationValues)):
        normalizedEvaluationValues.append([(newMaxValue - newMinValue) / (maxValue - minValue) * (evaluationValues[i][0] - maxValue) + newMaxValue, evaluationValues[i][1], evaluationValues[i][2], evaluationValues[i][3], evaluationValues[i][4], evaluationValues[i][5]])
    evaluationValues = copy.deepcopy(normalizedEvaluationValues)
    return evaluationValues

def evaluationPopulation(population, referenceCromossome, TPweight, precisenessWeight, simplicityWeight, completenessWeight, completenessAttemptFactor1, completenessAttemptFactor2, selectionOp, alphabet, log):
    evaluationSum = 0
    evaluationValues = []
    for i in range(len(population)):
        evaluationValues.append(evaluateIndividual(population[i], referenceCromossome, TPweight, precisenessWeight, simplicityWeight, completenessWeight, i, completenessAttemptFactor1, completenessAttemptFactor2, alphabet, log))
        evaluationSum = evaluationSum + evaluationValues[i][0]
    if selectionOp == 0:
        evaluationValues = normalizeTotalFitness(evaluationValues)
    return (evaluationSum, evaluationValues)