import json
import requests
from bs4 import BeautifulSoup

WIKI_URL = 'https://iceandfire.fandom.com/wiki/'  # adresse du wiki
SRC = 'Petyr_Baelish'


# Supprimer les doublons lors de l'ajout?!
def liste_liens(source):
    links = []
    html = requests.get(WIKI_URL + source).text
    soup = BeautifulSoup(html, 'html.parser').find('div', id='mw-content-text')
    for anchor in soup.find_all('a'):
        link = anchor.get('href')
        if link.startswith('/wiki/') and ':' not in link[len('/wiki/'):]:
            links.append(link[len('/wiki/'):])
        elif link.startswith(WIKI_URL) and ':' not in link[len(WIKI_URL):]:
            links.append(link[len(WIKI_URL):])
    return links


def svg_dico(dico, file):
    with open(file, "w") as f:
        json.dump(dico, f)


def chg_disco(file):
    with open(file, "r") as f:
        return json.load(f)


# Algorithme de parcours en largeur d'un graphe :
# https://fr.wikipedia.org/wiki/Algorithme_de_parcours_en_largeur
def svg_wiki(src, file):
    wiki = {}
    queue = [src]
    while queue:
        page = queue.pop(0)
        wiki[page] = liste_liens(page)
        for link in wiki[page]:
            if link not in wiki.keys():
                queue.append(link)
    svg_dico(wiki, file)


# Le parcours; chaque élément n'a qu'un seul parent
def parcours_largeur(wiki):
    parents = {}  # Faire avec une liste ou un dico ?
    queue = [SRC]  # Autorisé ?
    explored = []
    while queue:
        page = queue.pop(0)
        explored.append(page)
        for link in wiki[page]:
            if link not in explored:
                parents[link] = page
                queue.append(link)
    return parents


# reconstitution du chemin à partir du tableau des provenances
# def plus_court_chemin(dest, provenance):


def plus_court_chemin_rec(src, dest, parents):
    if src == dest:
        return [src]
    return plus_court_chemin_rec(parents[dest], parents).append(dest)


if __name__ == '__main__':
    # svg_wiki(SRC, "sauv.json")
    # s = "https://iceandfire.fandom.com/wiki/Special:Search?query=liste&scope=internal&navigationSearch=true"
    wiki = chg_disco("sauv.json")
    provenance = parcours_largeur(wiki)
    plus_court_chemin_rec("Dorne", "Rhaego", provenance)
