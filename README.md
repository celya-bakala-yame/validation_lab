# Validation de données en Python

Ce dépôt regroupe les exemples et les exercices du chapitre sur la validation de données.

main.py présente les expressions régulières, les quantificateurs, les groupes capturants et la différence entre recherche greedy et non-greedy. Il contient des fonctions de validation pour un code, une date, une adresse IPv4 et un mot de passe.

noms_variables.py contient les expressions régulières correspondant aux styles de nommage du cours. Il distingue le respect d’un style de la validité d’un identifiant Python.

modeles.py présente la validation avec Pydantic : champs obligatoires et facultatifs, conversion des types, validation stricte, contraintes de plage, catégories autorisées, modèles imbriqués et validateurs personnalisés. Un contrôle vérifie également que la date de fin d’un projet est postérieure à sa date de début.

validation_population.py applique des règles syntaxiques aux 15 colonnes des fichiers de population. Les règles acceptent notamment les codes corses, les noms accentués, les arrondissements numérotés et les champs facultatifs présents dans le fichier original.

Le fichier population.csv ne présente aucune erreur selon ces règles. Le fichier population-corrupted.csv contient 15 champs invalides répartis sur 15 lignes. Le rapport est enregistré dans erreurs_population.csv.

Les lignes concernées sont :
918, 1884, 3949, 8351, 12712, 17216, 29128, 42376, 52447, 61962, 73094, 87216, 110674, 123639 et 137670.

Ces numéros correspondent aux lignes physiques du CSV, avec l’en-tête en ligne 1.

Le validateur de population contrôle les formats. Il ne vérifie pas l’existence réelle des codes géographiques ni la cohérence des populations entre les colonnes.

Pour installer les dépendances :

uv sync

Pour exécuter les exemples :

uv run python main.py
uv run python noms_variables.py
uv run python modeles.py
uv run python validation_population.py

Les fichiers population.csv et population-corrupted.csv doivent se trouver dans le même dossier que validation_population.py.

Pour exécuter tous les doctests :

uv run python -m doctest -v main.py noms_variables.py modeles.py validation_population.py