from pokemontcgsdk import Card, Set, Type, Supertype, Subtype, Rarity, RestClient
from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

RestClient.configure('5b9f6767-a8c8-4bcd-be90-81fa1c2a0178')

global card_to_download
global CurrentCard
global CurrentCardName

CurrentCard = ''
CurrentCardName = ''

def DownloadFile(card):
    global card_to_download
    cardImg = card.images.large
    Filename = card.id+'.png'
    try:
        r = requests.get(cardImg)
        print(r)
        with open('./static/img/'+Filename, 'wb') as f:
            f.write(r.content)
    except Exception as e:
        print('exception downloading URL: ', e)

def DownloadPhotoOld(card):
    cardImg = card.images.large
    res = requests.get(cardImg)
    global images
    print("Card Not Found, Downloading")
    with open('static/img/' + card.id + '.png', 'wb') as f:
        f.write(res.content)
        images.append(f)
        f.close()

@app.errorhandler(404)
def PageNotFound(e):
    return render_template("404.html")

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def loadPokemon():
    global CurrentCard
    global CurrentCardName
    global images
    if request.form.get('Search') == 'Search':
        text = request.form['Card']
        cards = Card.where(q=f'name:{text}')

        CurrentCard = cards
        CurrentCardName = text
        for card in cards:
            card.id = card.id.replace("-", "$")
            if os.path.isfile('./static/img/'+card.id+'.png'):
                card.isCached = True
            else:
                card.isCached = False
            card.cardPrice = 0.0
            #cardPriceGBP = round(c.convert(card.cardPrice, 'USD', 'GBP'), 2)
            #card.cardPriceGBP = cardPriceGBP
        return render_template("results.html", Cards=cards, search=text, itemsfound=len(cards), css='./static/results.css')
    if request.form.get('Home') == 'Home':
        return render_template('index.html')

@app.route('/ViewCard')
def viewCard():

    keptTraits = ['abilities', 'attacks', 'cardmarket', 'evolvesFrom', 'hp', 'id', 'rarity', 'resistances']

    cardId = request.args.get('data')
    cardId = cardId.replace("$", "-")

    card = Card.find(cardId)
    
    shownAttributes = []

    for attr in dir(card):
        if attr.lower() in keptTraits:
            shownAttributes.append(attr)
    
    if card.abilities != None:
        card.hasAbilities = True
    else:
        card.hasAbilities = False
    
    for attack in card.attacks:
        print(attack.cost)

    return render_template('cardView.html', card=card, shownAttributes=shownAttributes)