import json
import requests
from bs4 import BeautifulSoup

WIKI_URL = 'https://iceandfire.fandom.com/wiki/'  # adresse du wiki


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


def chg_dico(file):
    with open(file, "r") as f:
        return json.load(f)


# Algorithme de parcours en largeur d'un graphe :
# https://fr.wikipedia.org/wiki/Algorithme_de_parcours_en_largeur
def svg_wiki(src, file):
    wiki = {}
    queue = [src]
    explored = [src]
    while queue:
        webpage = queue.pop(0)
        wiki[webpage] = liste_liens(webpage)
        for link in wiki[webpage]:
            if link not in explored:
                queue.append(link)
                explored.append(link)
    svg_dico(wiki, file)


if __name__ == '__main__':  # svg_wiki("Petyr_Baelish", "sauv.json")
    s = "https://iceandfire.fandom.com/wiki/Special:Search?query=liste&scope=internal&navigationSearch=true"
    print(s)