import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.rtbf.be/en-continu"
save = "./assets/production.txt"
product = "./assets/prod.txt"
titre=[]
contenu=[]
lien=[]

def getcontenu(contenu): # recupere le contenu dans les paragraphes de chaque articles
        paragraph=''
        for tag in contenu.find_all("p",class_=False):
                if tag.find("em",class_=False):# recupere les citation
                       paragraph+=tag.text+'\n'
                elif tag.find("span",class_=False): # recupere les citation dans les citation
                        paragraph+=tag.text+'\n'
                elif tag.find("strong",class_=False): # recupere les termes en gras ( svt nom )
                       paragraph+=tag.text+'\n'
                else:
                       paragraph+=tag.text+'\n'

                
        print("article copié!")   
        return paragraph


r = requests.get(url)
content = r.content
soup = BeautifulSoup(content,"html.parser")

for tag in soup.find_all("article"):
        titre.append(tag.find("header").text)
        lien.append(tag.find("a").get('href'))

lien = ["https://www.rtbf.be"+ elem for elem in lien if "/article" in elem] # format les urls correctement
print("liste des liens preparé")

df = pd.DataFrame({"Title": titre}) # initie les colones avec les valeurs recupere sur la page d'acceuil
df["Links"] = lien

fichier = open(save,"a+",encoding='utf-8') #save en format text pour comparaison avec csv
for e in lien:
    fichier.write(titre[lien.index(e)]+'\n') # ajoute titre et lien dans fichier txt
    fichier.write(e+'\n')
    r = requests.get(e) #requete sur les different article recupere a l'acceuil
    if r.status_code == 200:
        print('recuperation du contenu suivant...')
    newcontent = BeautifulSoup(r.content,"html.parser")
    contenu.append(getcontenu(newcontent))
    fichier.write(contenu[lien.index(e)]+'\n')
fichier.close()
df["Article"] = contenu
df.to_csv("./assets/prod.csv", index=False)
print("scraping terminé , veuillez verifié le contenu :)")