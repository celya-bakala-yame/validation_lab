import csv
import re
from pathlib import Path


MOTIFS = {
    "Code Officiel Région": r"[0-9]{2,3}",
    "Code Officiel Département": r"(?:[0-9]{2,3}|2[AB])",
    "Code Officiel Arrondissement Départemental": r"[0-9]{3}",
    "Code Officiel Commune / Arrondissement Municipal": (
        r"(?:[0-9]{5,6}|2[AB][0-9]{3})"
    ),
    "Population municipale": r"[0-9]+(?:\.0)?",
    "Population comptée à part": r"[0-9]+(?:\.0)?",
    "Population totale": r"[0-9]+(?:\.0)?",
    "Année de recensement": r"[0-9]{4}",
    "Année d’entrée en vigueur": r"[0-9]{4}",
    "Année de référence géographique": r"[0-9]{4}",
    "Code Officiel EPCI": r"(?:[0-9]{9})?",
}

CARACTERES_NOMS = {
    "Nom Officiel Région": " '-",
    "Nom Officiel Département": " '-",
    "Nom Officiel Commune / Arrondissement Municipal": " '()-",
    "Nom Officiel EPCI": " '\"(),-./0123456789[]",
}

CHAMPS_FACULTATIFS = {
    "Nom Officiel Département",
    "Nom Officiel EPCI",
}

MOTIF_ARRONDISSEMENT = (
    r"(?:Paris|Lyon|Marseille) [0-9]{1,2}(?:er|e) Arrondissement"
)


def valider_champ(champ, valeur):
    """
    >>> valider_champ("Code Officiel Région", "84")
    True
    >>> valider_champ("Code Officiel Région", "8A")
    False
    >>> valider_champ("Code Officiel Département", "2A")
    True
    >>> valider_champ("Population totale", "1384.0")
    True
    >>> valider_champ("Population totale", "|696.0")
    False
    >>> valider_champ("Nom Officiel Commune / Arrondissement Municipal", "Paris 1er Arrondissement")
    True
    >>> valider_champ("Nom Officiel Commune / Arrondissement Municipal", "V1lledieu-le-Château")
    False
    >>> valider_champ("Nom Officiel Département", "Indre_et-Loire")
    False
    >>> valider_champ("Nom Officiel EPCI", "")
    True
    """
    if champ in MOTIFS:
        return re.fullmatch(MOTIFS[champ], valeur) is not None

    if champ == "Nom Officiel Commune / Arrondissement Municipal":
        if re.fullmatch(MOTIF_ARRONDISSEMENT, valeur):
            return True

    if not valeur and champ not in CHAMPS_FACULTATIFS:
        return False

    caracteres = CARACTERES_NOMS[champ]
    return all(
        caractere.isalpha() or caractere in caracteres
        for caractere in valeur
    )


def valider_ligne(ligne):
    """
    >>> valider_ligne({"Code Officiel Région": "84", "Population totale": "12.0"})
    []
    >>> valider_ligne({"Code Officiel Région": "8A"})
    [('Code Officiel Région', '8A')]
    """
    return [
        (champ, valeur)
        for champ, valeur in ligne.items()
        if not valider_champ(champ, valeur)
    ]


def valider_fichier(chemin):
    erreurs = []

    with open(chemin, encoding="utf-8-sig", newline="") as fichier:
        lecteur = csv.DictReader(fichier, delimiter=";")
        champs_attendus = set(MOTIFS) | set(CARACTERES_NOMS)

        if set(lecteur.fieldnames or []) != champs_attendus:
            raise ValueError("Les colonnes du fichier ne correspondent pas")

        for ligne in lecteur:
            numero = lecteur.line_num
            for champ, valeur in valider_ligne(ligne):
                erreurs.append({
                    "ligne": numero,
                    "champ": champ,
                    "valeur": valeur,
                })

    return erreurs


if __name__ == "__main__":
    dossier = Path(__file__).resolve().parent

    for nom in ["population.csv", "population-corrupted.csv"]:
        erreurs = valider_fichier(dossier / nom)

        print(nom)
        print("Nombre de champs invalides :", len(erreurs))
        print(
            "Nombre de lignes concernées :",
            len({erreur["ligne"] for erreur in erreurs}),
        )

        for erreur in erreurs:
            print(
                erreur["ligne"],
                erreur["champ"],
                repr(erreur["valeur"]),
                sep=" | ",
            )

        if nom == "population-corrupted.csv":
            with open(
                dossier / "erreurs_population.csv",
                "w",
                encoding="utf-8",
                newline="",
            ) as fichier:
                writer = csv.DictWriter(
                    fichier,
                    fieldnames=["ligne", "champ", "valeur"],
                    delimiter=";",
                )
                writer.writeheader()
                writer.writerows(erreurs)