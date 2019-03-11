import matplotlib.pyplot as plt
import islands as isl
from ast import literal_eval
plt.switch_backend('agg')

def plot_evolution_per_island(vetor_fitness, parameter, round, islandNumber):
    v_min = [i[0] for i in vetor_fitness]
    v_max = [i[1] for i in vetor_fitness]
    v_avg = [i[2] for i in vetor_fitness]
    plt.figure(1)
    plt.plot(v_min, label="Lowest fitness", linestyle=':', linewidth=1.0, color="red")
    plt.plot(v_avg, label="Average fitness", linewidth=2.0, color="orange")
    plt.plot(v_max, label="Highest fitness", linewidth=2.0, color="green")
    plt.ylabel("Fitness")
    plt.xlabel("Generation")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, mode="expand", borderaxespad=0., prop={'size': 10})
    plt.ylim([0, 1.02])
    plt.draw()
    name = 'graphs/' 'graph-' + parameter + '-' + round + '-' + str(islandNumber) + '.png'
    plt.savefig(name)
    plt.clf()
    return

def plot_evolution_integrated(parameter, round, numberrOfIslands):
    vetorOfVetor_fitness = []
    for i in range(numberrOfIslands):
        vetor_fitness = []
        with open('island_files/plotting_{0}.txt'.format(i), 'r') as plott:
            for line in isl.nonblank_lines(plott):
                vetor_fitness.append(literal_eval(line))
            vetorOfVetor_fitness.append(vetor_fitness)
        plott.close()

    v_min = []
    v_max = []
    v_ave = []
    for j in range(numberrOfIslands):
        v_min.append([i[0] for i in vetorOfVetor_fitness[j]])
        v_max.append([i[1] for i in vetorOfVetor_fitness[j]])
        v_ave.append([i[2] for i in vetorOfVetor_fitness[j]])

    plt.figure(1)
    for j in range(numberrOfIslands):
        plt.plot(v_min[j], label='Lowest fitness', linestyle=':', linewidth=1.0, color="red")
        plt.plot(v_ave[j], label='Average fitness', linewidth=2.0, color="orange")
        plt.plot(v_max[j], label='Highest fitness', linewidth=2.0, color="green")

    plt.ylabel("Fitness")
    plt.xlabel("Generation")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, mode="expand", borderaxespad=0., prop={'size': 10})
    plt.ylim([0, 1.02])
    plt.draw()
    name = 'graphs/' 'graph-' + parameter + '-' + round + '-' + 'I' + '.png'
    plt.savefig(name)
    plt.clf()
    return