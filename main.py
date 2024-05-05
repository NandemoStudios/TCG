from pokemontcgsdk import Card, Set, Type, Supertype, Subtype, Rarity, RestClient
from flask import Flask, render_template, request
import requests
import os
from currency_converter import CurrencyConverter

c = CurrencyConverter()

app = Flask(__name__)

RestClient.configure('5b9f6767-a8c8-4bcd-be90-81fa1c2a0178')

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def loadPokemon():
    print(request.method)
    if request.form.get('Search') == 'Search':
        text = request.form['Card']
        cards = Card.where(q=f'name:{text}')
        images = []
        for card in cards:
            cardImg = card.images.small
            res = requests.get(cardImg)
            card.cardmarket.prices.averageSellPriceGBP = round(
                c.convert(card.cardmarket.prices.averageSellPrice, 'USD', 'GBP'), 2)
            if os.path.isfile('static/img/' + card.id + '.png'):
                images.append(open('static/img/' + card.id + '.png', 'r'))
            else:
                print("Card Not Found, Downloading")
                with open('static/img/' + card.id + '.png', 'wb') as f:
                    f.write(res.content)
                    images.append(f)
        return render_template("results.html", Cards=cards, search=text, images=images, itemsfound=len(cards))
    if request.form.get('Home') == 'Home':
        return render_template('index.html')