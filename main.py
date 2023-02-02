import json

import requests
from bs4 import BeautifulSoup

WIKI_URL = 'https://iceandfire.fandom.com/wiki/'  # adresse du wiki
SEPARATOR = "', "  # séparateur du fichier


# Supprimer les doublons lors de l'ajout?!
def liste_liens(source):
    links = []
    html = requests.get(WIKI_URL + source).text
    body = BeautifulSoup(html, 'html.parser').find('div', id='mw-content-text')
    for anchor in body.find_all('a'):
        link = anchor.get('href')
        if link.startswith('/wiki/') and ':' not in link[len('/wiki/'):]:
            links.append(link[len('/wiki/'):])
        elif link.startswith(WIKI_URL) and ':' not in link[len(WIKI_URL):]:
            links.append(link[len(WIKI_URL):])
    return links


# def svg_dico2(dico, file):  # Il faut créer une nouvelle classe dico qui l'hérite pour changer le str()
#     with open(file, "w") as f:
#         f.write(str(dico))


def svg_dico(dico, file): # Un peu de la bidouille
    s = ""
    for page in dico:
        s += page + SEPARATOR + str(dico[page])[1:-2] + "\n"
    with open(file, "w") as f:
        f.write(s)


def chg_dico(file):
    dico = {}
    with open(file) as f:
        for line in f.readlines():
            line.split(SEPARATOR)
            dico[line[0]] = line[1:]
    return dico


def svg_dico_json(dico, file):  # si on peut utiliser les json
    with open(file, "w") as f:
        json.dump(dico, f)


def chg_dico_json(file):
    with open(file) as f:
        return json.load(f)


def svg_wiki(dico, file):  # Question 4 à faire
    return 0


if __name__ == '__main__':
    svg_dico({"Petyr_Baelish": liste_liens("Petyr_Baelish"), "Harrenhal": liste_liens("Harrenhal")}, "sauv.txt")
