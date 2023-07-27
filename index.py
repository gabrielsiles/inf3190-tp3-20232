# Copyright 2023 <Votre nom et code permanent>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import render_template
from flask import g
from .database import Database
import random
from flask import request, abort
from flask import redirect
from flask import url_for

app = Flask(__name__, static_url_path="", static_folder="static")

animal_image_urls = {
    'Fluffy': 'https://www.ecomusee-rennes-metropole.fr/app/uploads/2020/10/avranchin_vignette-scaled.jpg',
    'Dragon': 'https://cdn.wamiz.fr/cdn-cgi/image/format=auto,quality=80,width=1200,height=675,fit=cover/article/main-picture/5ec295af75e39460426037.jpg',
    'Perdita': 'https://i.pinimg.com/originals/0e/f2/d4/0ef2d42f8a5d7abac39013c0bf17e5be.jpg',
    'Skippy': 'https://www.parismatch.be/resizer/RTmJ2d5CnT3BC5KX8oaizCDfUq8=/1620x1080/filters:format(jpeg):focal(545x371.5:555x361.5)/cloudfront-eu-central-1.images.arcpublishing.com/ipmgroup/PCIZ2P7TMFBABDDXEKTZLJJ2WM.jpg',
    'Madame Long Cou': 'https://www.rustica.fr/images/058017a-1438867027.jpg',
    'Serpent Haut': 'https://nationalzoo.si.edu/sites/default/files/newsroom/20081126-203mm-green-tree-python.jpg',
    'Mojo': 'https://static.independent.co.uk/s3fs-public/thumbnails/image/2019/10/21/15/pugs-gettyimages-599179108.jpg'
}


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


def get_animal_image_url(animal_name):
    default_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Pas_d%27image_disponible.svg/1200px-Pas_d%27image_disponible.svg.png'
    return animal_image_urls.get(animal_name, default_url)

@app.route('/', endpoint='index')
def index():
    database = get_db()
    animaux = database.get_animaux()
    
    for animal in animaux:
        animal['image_url'] = get_animal_image_url(animal['nom'])

    random_animaux = random.sample(animaux, min(5, len(animaux)))
    return render_template('index.html', animaux=random_animaux)

@app.route('/animal/<int:animal_id>')
def animal(animal_id):
    database = get_db()
    animal = database.get_animal(animal_id)
    if animal is None:
        print("Animal non trouvé")
        return "Animal non trouvé"
    animal['image_url'] = get_animal_image_url(animal['nom'])
    return render_template('animal.html', animal=animal)


@app.route('/form', methods=['GET', 'POST'], endpoint='form')
def form():
    return render_template('form.html')


@app.route('/resultats')
def resultats():
    query = request.args.get('query')
    db = get_db()
    animals = db.search_animals(query)
    return render_template('resultats.html', query=query, animals=animals)


@app.route('/add_animal', methods=['POST'])
def ajouter_animal():
    nom = request.form['nom_animal']
    espece = request.form['espece_animal']
    race = request.form['race_animal']
    age = request.form['age_animal']
    description = request.form['description']
    courriel = request.form['adresse_courriel']
    adresse = request.form['adresse_animal']
    ville = request.form['ville']
    cp = request.form['code_postal']

   
    db = get_db()
    last_id = db.add_animal(nom=nom, espece=espece, race=race, age=age, description=description, courriel=courriel,
                            adresse=adresse, ville=ville, cp=cp)

    return redirect(url_for('animal', animal_id=last_id))


if __name__ == '__main__':
    app.run(debug=True)
