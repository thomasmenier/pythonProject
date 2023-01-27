import requests
from bs4 import BeautifulSoup

WIKI_URL = 'https://iceandfire.fandom.com/wiki/'  # adresse du wiki
SEPARATOR = ','  # Séparateur dans le fichier de sauvegarde


# Supprimer les doublons ?!
def liste_liens(source):
    html = requests.get(WIKI_URL + source).text
    body = BeautifulSoup(html, 'html.parser').find('div', id='mw-content-text')
    links = []
    for anchor in body.find_all('a'):
        link = anchor.get('href')
        if link.startswith('/wiki/') and ':' not in link[len('/wiki/'):]:  # Si le nom de la page ne contient pas un ':'
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
    f = open(file, "w")
    f.write(s)
    f.close()


def chg_dico(file):
    dico = {}
    f = open(file)
    for line in f.readlines():
        line.split(SEPARATOR)
        dico[line[0]] = line[1:]
    f.close()
    return dico


def svg_wiki(dico, file):
    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    svg_dico({"Petyr_Baelish": liste_liens("Petyr_Baelish")}, "sauv.txt")
