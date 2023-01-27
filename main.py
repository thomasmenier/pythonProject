import requests
from bs4 import BeautifulSoup

WIKI = 'https://iceandfire.fandom.com/wiki/'  # adresse du wiki
SEPARATOR = ','  # Séparateur dans le fichier de sauvegarde


# Supprimer les doublons ?!
def liste_liens(source):
    html = requests.get(WIKI + source).text
    body = BeautifulSoup(html, 'html.parser').find('div', id='mw-content-text')
    i = 0
    links = []
    for link in body.find_all('a'):
        src = link.get('href')
        if '/wiki/' == src[:6]:
            if not (':' in src[6:]):
                links.append(src[6:])
                i += 1
        elif 'https://iceandfire.fandom.com/wiki/' == src[:35]:
            if not (':' in src[35:]):
                links.append(src[35:])
                i += 1
    print("nombre de liens :", i)
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
    s = ""

    #Page qui se renvoie l'une vers l'autre


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    liste_liens("Petyr_Baelish")
