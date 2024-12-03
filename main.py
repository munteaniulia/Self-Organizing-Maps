import math
import random
from copy import deepcopy
from random import randint
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000000)

file_name = 'coord_X_coord_Y_index_Zona.txt'
centroizi_file_name = "Centroizi.txt"

nrOfCentroizi = randint(2, 10)
zona1 = {"name": "zona1", "mx": 180, "my": 220, "sigmax": 10, "sigmay": 10}
zona2 = {"name": "zona2", "mx": -100, "my": 110, "sigmax": 15, "sigmay": 10}
zona3 = {"name": "zona3", "mx": 210, "my": -150, "sigmax": 5, "sigmay": 20}

W, X, poz_neuroni = [], [], []
omega = 0
N = 20
int_max = float('inf')

def alege_valoarea_pt_coord():
    return randint(-300, 300)

def convertire(coord, zona, xORy):
    return np.exp(-((zona[f"m{xORy}"] - coord) ** 2) / (2 * (zona[f"sigma{xORy}"] ** 2)))

def verificare_nr_puncte():
    with open(file_name, 'r') as f:
        numar_linii = len(f.readlines())
    if numar_linii < 10000:
        zona = random.choice([zona1, zona2, zona3])
        x = alege_valoarea_pt_coord()
        verifPragx(x, zona)

def verifPragy(y, zona):
    yConvert = convertire(y, zona, "y")
    prag = round(random.random(), 3)
    if yConvert > prag:
        with open(file_name, 'a') as f:
            f.write(f"{y} {zona['name']}\n")
        verificare_nr_puncte()
    else:
        y = alege_valoarea_pt_coord()
        verifPragy(y, zona)

def verifPragx(x, zona):
    xConvert = convertire(x, zona, "x")
    prag = round(random.random(), 3)
    if xConvert > prag:
        with open(file_name, 'a') as f:
            f.write(f"{x} ")
        coordy = alege_valoarea_pt_coord()
        verifPragy(coordy, zona)
    else:
        x = alege_valoarea_pt_coord()
        verifPragx(x, zona)

def distanta_Euclidiana(centroid, punct):
    return math.sqrt((centroid[0] - punct[0]) ** 2 + (centroid[1] - punct[1]) ** 2)

def dateIntrare():
    with open(file_name, 'r') as f:
        for line in f:
            coordonate = line.split()
            punct = (int(coordonate[0]), int(coordonate[1]))
            X.append(punct)

def pozitionareNeuroni():
    for i in range(-300, 300, 60):
        for j in range(-300, 300, 60):
            pozitie = (i,j)
            poz_neuroni.append(pozitie)
            W.append(pozitie)

def coerficientInvatare(epoca_curenta):
    invatare = 0.7 * pow(math.e, (-(epoca_curenta / N)))
    return invatare

def vecinatate(epoca_curenta):
    vecinatate = 6.1 * pow(math.e, (-(epoca_curenta / N)))
    return vecinatate

def actualizareNeuron(neuron, neuronIndex, coeficient, punct):
    neuronNou = []
    neuronX = neuron[0] + coeficient * (punct[0] - neuron[0])
    neuronY = neuron[1] + coeficient * (punct[1] - neuron[1])
    W[neuronIndex] = (neuronX, neuronY)

def isVecin(neuronIndex, neuronCampionIndex, epoca_curenta):
    return distanta_Euclidiana(poz_neuroni[neuronCampionIndex], poz_neuroni[neuronIndex]) < vecinatate(epoca_curenta)
    #return distanta_Euclidiana(W[neuronCampionIndex], W[neuronIndex]) < vecinatate(epoca_curenta)

def actualizarePonderi(puncte, neuroni, epoca_curenta):
    neuron_campion = 0
    for punct in puncte:
        dist = int_max
        for neuron in neuroni:
            if distanta_Euclidiana(neuron,punct) < dist:
                neuron_campion = neuron
                neuron_campion_index = neuroni.index(neuron)
        actualizareNeuron(poz_neuroni[neuron_campion],neuron_campion,coerficientInvatare(epoca_curenta),punct)
        for neuron in neuroni:
            if isVecin(W.index(neuron), neuron_campion, epoca_curenta):
                actualizareNeuron(poz_neuroni[W.index(neuron)],W.index(neuron),coerficientInvatare(epoca_curenta), punct)
def isDone(epoca_curetna):
    return coerficientInvatare(epoca_curetna) <= 10 ** -27


def draw_grid(W, iteration):
    """
    Draws the grid based on the neuron positions in W for a specific iteration.
    """
    plt.figure(figsize=(8, 8))
    plt.title(f"Self-Organizing Map Grid - Iteration {iteration}")
    plt.xlabel("X")
    plt.ylabel("Y")

    sorted_W = sorted(W, key=lambda pos: (pos[1], pos[0]))  # Sort by Y, then X
    grid_size = int(np.sqrt(len(W)))  # Assuming a square grid

    # Draw horizontal lines
    for i in range(grid_size):
        for j in range(grid_size - 1):
            x1, y1 = sorted_W[i * grid_size + j]
            x2, y2 = sorted_W[i * grid_size + j + 1]
            plt.plot([x1, x2], [y1, y2], color='blue')

    # Draw vertical lines
    for j in range(grid_size):
        for i in range(grid_size - 1):
            x1, y1 = sorted_W[i * grid_size + j]
            x2, y2 = sorted_W[(i + 1) * grid_size + j]
            plt.plot([x1, x2], [y1, y2], color='blue')

    plt.xlim(-350, 350)
    plt.ylim(-350, 350)
    plt.grid(True)
    plt.show()


# Main loop
dateIntrare()
pozitionareNeuroni()
epoca_curenta = 1

while not isDone(epoca_curenta):
    actualizarePonderi(X, poz_neuroni, epoca_curenta)
    draw_grid(W, epoca_curenta)  # Draw the grid at each iteration
    epoca_curenta += 1
plt.ioff()  # Turn off interactive plotting
plt.show()  # Show the final state
