const formulaire = document.querySelector('#forme_adoption');
const nomAnimal = document.querySelector('#nom_animal');
const especeAnimal = document.querySelector('#espece_animal');
const raceAnimal = document.querySelector('#race_animal');
const ageAnimal = document.querySelector('#age_animal');
const description = document.querySelector('#description');
const adresseCourriel = document.querySelector('#adresse_courriel');
const adresseAnimal = document.querySelector('#adresse_animal');
const ville = document.querySelector('#ville');
const codePostal = document.querySelector('#code_postal');


const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const regexCodePostal = /^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$/;
const champVideId = {
    'nom_animal': 'message_nom_vide',
    'espece_animal': 'message_espece_animal_vide',
    'race_animal': 'message_race_animal_vide',
    'age_animal': 'message_age_animal_vide',
    'description': 'message_description_vide',
    'adresse_courriel': 'message_adresse_courriel_vide',
    'adresse_animal': 'message_adresse_animal_vide',
    'ville': 'message_ville_vide',
    'code_postal': 'message_code_postal_vide'
};




formulaire.addEventListener("submit", function(event) {
const age = parseInt(document.querySelector('#age_animal').value);
const longueur = nomAnimal.value.trim().length;
event.preventDefault();
let estFormValide = true;

for (const field in champVideId) {
    const attribut = document.querySelector(`[name="${field}"]`);
    const messageElement = attribut.nextElementSibling;
    const messageId = champVideId[field];

    if (attribut.value.trim() === '') {
    estFormValide = false;
    afficherErreur(attribut, 'Remplissez tous les champs avant de soumettre', messageId);

    } else if (attribut.value.includes(',')) {
    estFormValide = false;
    afficherErreur(attribut, 'Le champ ne peut pas contenir de virgule', messageId);

    } else {
    cacherErreur(attribut, messageId);
    }
}


if (longueur < 3 || longueur > 20) {
    estFormValide = false;
    const messageElement = document.querySelector('#message_nom');
    afficherErreur(nomAnimal, 'Le nom de l\'animal doit avoir entre 3 et 20 caractères', 'message_nom');
    console.log("allo");
} else {
    cacherErreur(nomAnimal, 'message_nom');
}


if (isNaN(age) || age < 0 || age > 30) {
    estFormValide = false;
    const messageElement = document.querySelector('#message_age');
    afficherErreur(ageAnimal, 'L\'âge doit être une valeur numérique entre 0 et 30', 'message_age');

} else {
    cacherErreur(ageAnimal, 'message_age');
}


if (!regexEmail.test(adresseCourriel.value)) {
    estFormValide = false;
    const messageElement = document.querySelector('#message_courriel');
    afficherErreur(adresseCourriel, 'L\'adresse courriel doit avoir un format valide', 'message_courriel');

} else {
    cacherErreur(adresseCourriel, 'message_courriel');
}


if (!regexCodePostal.test(codePostal.value)) {
    estFormValide = false;
    const messageElement = document.querySelector('#message_postal');
    afficherErreur(codePostal, 'Le code postal doit avoir un format canadien', 'message_postal');

} else {
    cacherErreur(codePostal, 'message_postal');
}


if (estFormValide) {
    formulaire.submit();
}
});

function afficherErreur(input, message, messageId) {
    input.classList.add('est-invalide');
    const messageElement = document.getElementById(messageId);
    messageElement.textContent = message;
    messageElement.classList.add('error-message-visible');
}

function cacherErreur(input, messageId) {
    input.classList.remove('est-invalide');
    const messageElement = document.getElementById(messageId);
    messageElement.textContent = '';
    messageElement.classList.remove('error-message-visible');

}