import math
import random
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

W, X, poz_neuroni, matrice =[], [], [], []
omega = 0
N = 10
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
    # return abs(centroid[0] - punct[0]) + abs(centroid[1] - punct[1])

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
    print(f"{round(invatare,2)} \n")
    return round(invatare,2)

def vecinatate(epoca_curenta):
    vecinatate = 6.1 * pow(math.e, (-(epoca_curenta / N)))
    return vecinatate

def actualizareNeuron(neuron, neuronIndex, coeficient, punct):
    neuronX = neuron[0] + coeficient * (punct[0] - neuron[0])
    neuronY = neuron[1] + coeficient * (punct[1] - neuron[1])
    W[neuronIndex] = (neuronX, neuronY)

def actualizarePonderi(puncte, neuroni, epoca_curenta):
    neuron_campion = ()
    neuron_campion_index = 0
    for punct in puncte:
        dist = int_max
        for neuron in neuroni:
            if distanta_Euclidiana(neuron, punct) < dist:
                neuron_campion = neuron
                dist = distanta_Euclidiana(neuron, punct)
                neuron_campion_index = neuroni.index(neuron)
        actualizareNeuron(W[neuron_campion_index], neuron_campion_index, coerficientInvatare(epoca_curenta), punct)

        veci = int(round(vecinatate(epoca_curenta)))
        for i, rand in enumerate(matrice):
            for j, element in enumerate(rand):
                if element == neuron_campion:
                    for k in range(1, veci + 1):
                        # Verifică vecinii pe verticală
                        if 0 <= i - k < len(matrice):
                            actualizareNeuron(W[neuroni.index(matrice[i - k][j])], neuroni.index(matrice[i - k][j]), coerficientInvatare(epoca_curenta), punct)
                        if 0 <= i + k < len(matrice):
                            actualizareNeuron(W[neuroni.index(matrice[i + k][j])], neuroni.index(matrice[i + k][j]), coerficientInvatare(epoca_curenta), punct)
                        # Verifică vecinii pe orizontală
                        if 0 <= j - k < len(matrice[i]):
                            actualizareNeuron(W[neuroni.index(matrice[i][j - k])], neuroni.index(matrice[i][j - k]), coerficientInvatare(epoca_curenta), punct)
                        if 0 <= j + k < len(matrice[i]):
                            actualizareNeuron(W[neuroni.index(matrice[i][j + k])], neuroni.index(matrice[i][j + k]), coerficientInvatare(epoca_curenta), punct)
                        # Verifică vecinii pe diagonale
                        if 0 <= i - k < len(matrice) and 0 <= j - k < len(matrice[i]):
                            actualizareNeuron(W[neuroni.index(matrice[i - k][j - k])], neuroni.index(matrice[i - k][j - k]), coerficientInvatare(epoca_curenta), punct)
                        if 0 <= i - k < len(matrice) and 0 <= j + k < len(matrice[i]):
                            actualizareNeuron(W[neuroni.index(matrice[i - k][j + k])], neuroni.index(matrice[i - k][j + k]), coerficientInvatare(epoca_curenta), punct)
                        if 0 <= i + k < len(matrice) and 0 <= j - k < len(matrice[i]):
                            actualizareNeuron(W[neuroni.index(matrice[i + k][j - k])], neuroni.index(matrice[i + k][j - k]), coerficientInvatare(epoca_curenta), punct)
                        if 0 <= i + k < len(matrice) and 0 <= j + k < len(matrice[i]):
                            actualizareNeuron(W[neuroni.index(matrice[i + k][j + k])], neuroni.index(matrice[i + k][j + k]), coerficientInvatare(epoca_curenta), punct)

                        if 0 <= i + k < len(matrice):
                            actualizareNeuron(W[neuroni.index(matrice[i + k][j])],neuroni.index(matrice[i + k][j]),coerficientInvatare(epoca_curenta),punct)
                        # Verifică vecinii pe orizontală
                        if 0 <= j - k < len(matrice[i]):
                            actualizareNeuron(W[neuroni.index(matrice[i][j - k])],neuroni.index(matrice[i][j - k]),coerficientInvatare(epoca_curenta),punct)
                        if 0 <= j + k < len(matrice[i]):
                            actualizareNeuron(W[neuroni.index(matrice[i][j + k])],neuroni.index(matrice[i][j + k]),coerficientInvatare(epoca_curenta),punct)

def isDone(epoca_curetna):
    return round(coerficientInvatare(epoca_curetna), 2) <= 0.01

# Generare puncte

Zona = random.choice([zona1, zona2, zona3])
x = alege_valoarea_pt_coord()
verifPragx(x, Zona)

# Main loop
dateIntrare()
pozitionareNeuroni()
epoca_curenta = 0
matrice = [poz_neuroni[i:i + 10] for i in range(0, len(poz_neuroni), 10)]
plt.figure(figsize=(6, 6))
plt.scatter(*zip(*X), color='black', s=1, label='Puncte')

for i in range(len(W)):
    x, y = W[i]
    if i % 10 != 9:
        plt.plot([x, W[i + 1][0]], [y, W[i + 1][1]], color='gray', linestyle='--', linewidth=0.5)
    if i + 10 < len(W):
        plt.plot([x, W[i + 10][0]], [y, W[i + 10][1]], color='gray', linestyle='--', linewidth=0.5)

plt.xlim(-350, 350)
plt.ylim(-350, 350)
plt.xlabel("X")
plt.ylabel("Y")
plt.title(f"Epoca {0}")
plt.grid(False)
plt.pause(0.1)

while not isDone(epoca_curenta):
    actualizarePonderi(X, poz_neuroni, epoca_curenta)
    plt.figure(figsize=(6, 6))
    plt.scatter(*zip(*X), color='black', s=1, label='Puncte')

    for i in range(len(W)):
        x, y = W[i]
        if i % 10 != 9:
            plt.plot([x, W[i + 1][0]], [y, W[i + 1][1]], color='gray', linestyle='--', linewidth=0.5)
        if i + 10 < len(W):
            plt.plot([x, W[i + 10][0]], [y, W[i + 10][1]], color='gray', linestyle='--', linewidth=0.5)

    plt.xlim(-300, 300)
    plt.ylim(-300, 300)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Epoca {epoca_curenta}")
    plt.grid(False)

    # Afișăm graficul
    plt.pause(0.1)
    epoca_curenta += 1

# Afișăm toate figurile cumulate
plt.show()

