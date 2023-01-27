import json

import requests
from bs4 import BeautifulSoup

WIKI_URL = 'https://iceandfire.fandom.com/wiki/'  # adresse du wiki
SEPARATOR = ','  # Séparateur dans le fichier de sauvegarde


# Supprimer les doublons ?!
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


def svg_dico(dico, file):
    s = ""
    for page in dico:
        s += page
        for link in dico[page]:
            s += SEPARATOR + link
        s += "\n"
    with open(file, "w") as f:
        f.write(s)


def svg_dico_json(dico, file):
    with open(file, "w") as f:
        json.dump(dico, f)


def chg_dico(file):
    dico = {}
    with open(file) as f:
        for line in f.readlines():
            line.split(SEPARATOR)
            dico[line[0]] = line[1:]
    return dico


def chg_dico_json(file):
    with open(file) as f:
        return json.load(f)


def svg_wiki(dico, file):
    return 0


if __name__ == '__main__':
    svg_dico_json({"Petyr_Baelish": liste_liens("Petyr_Baelish")}, "sauv_json.txt")
