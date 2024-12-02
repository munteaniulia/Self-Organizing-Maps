import math
import random
from copy import deepcopy
from random import randint
import sys
import numpy as np

sys.setrecursionlimit(10000000)

file_name = 'coord_X_coord_Y_index_Zona.txt'
centroizi_file_name = "Centroizi.txt"

nrOfCentroizi = randint(2, 10)
zona1 = {"name": "zona1", "mx": 180, "my": 220, "sigmax": 10, "sigmay": 10}
zona2 = {"name": "zona2", "mx": -100, "my": 110, "sigmax": 15, "sigmay": 10}
zona3 = {"name": "zona3", "mx": 210, "my": -150, "sigmax": 5, "sigmay": 20}

culori, centroizi, cluster_dict, W, X, poz_neuroni= [], [], {}, [], [], []
omega = 0
N = 20


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


def generareCentroizi():
    k = nrOfCentroizi
    while k > 0:
        with open(centroizi_file_name, 'a') as f:
            x, y = randint(-300, 300), randint(-300, 300)
            centroizi.append((x, y))
            cluster_dict[(x, y)] = []
            f.write(f"{x} {y}\n")
        k -= 1

def distanta_Euclidiana(centroid, punct):
    return math.sqrt((centroid[0] - punct[0]) ** 2 + (centroid[1] - punct[1]) ** 2)


def grupareDupaCentroid():
    with open(file_name, 'r') as f:
        for linie in f:
            coordonate = linie.split()
            punct = (int(coordonate[0]), int(coordonate[1]))
            distanta_minima, centroid_apropiat = float('inf'), None
            for centroid in centroizi:
                distanta = distanta_Euclidiana(centroid, punct)
                if distanta < distanta_minima:
                    distanta_minima, centroid_apropiat = distanta, centroid
            cluster_dict[centroid_apropiat].append(punct)


def calculCentruDeGreutate():
    temp = deepcopy(cluster_dict)
    centroizi.clear()
    for centroid, puncte in temp.items():
        if puncte:
            media_x, media_y = np.mean([p[0] for p in puncte]), np.mean([p[1] for p in puncte])
            cluster_dict[(media_x, media_y)] = cluster_dict.pop(centroid)
            centroizi.append((media_x, media_y))
        else:
            centroizi.append(centroid)


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


def actualizarePonderi():

# Generare puncte
Zona = random.choice([zona1, zona2, zona3])
x = alege_valoarea_pt_coord()
verifPragx(x, Zona)

