import re
from datetime import date
from typing import Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)


class Utilisateur(BaseModel):
    """
    >>> utilisateur = Utilisateur(nom="Célya", email="celya@example.com", age="21")
    >>> utilisateur.age
    21
    >>> isinstance(utilisateur.age, int)
    True
    >>> copie = Utilisateur.model_validate_json(utilisateur.model_dump_json())
    >>> copie == utilisateur
    True
    >>> try:
    ...     Utilisateur(nom="Célya", email="invalide", age=21)
    ... except ValidationError:
    ...     print("Email invalide")
    Email invalide
    >>> try:
    ...     Utilisateur(nom="Célya", email="celya@example.com", age=150)
    ... except ValidationError:
    ...     print("Âge invalide")
    Âge invalide
    """
    nom: str = Field(min_length=1)
    email: EmailStr
    age: int = Field(ge=0, le=120)
    telephone: str | None = None

    @field_validator("nom")
    @classmethod
    def verifier_nom(cls, valeur):
        valeur = valeur.strip()
        if not valeur:
            raise ValueError("Le nom ne doit pas être vide")
        return valeur


class AgeStrict(BaseModel):
    """
    >>> AgeStrict(age=21).age
    21
    >>> try:
    ...     AgeStrict(age="21")
    ... except ValidationError:
    ...     print("Un entier est attendu")
    Un entier est attendu
    """
    model_config = ConfigDict(strict=True)
    age: int = Field(ge=0, le=120)


class Produit(BaseModel):
    """
    >>> Produit(code="AB123", prix=9.99, categorie="livre").code
    'AB123'
    >>> try:
    ...     Produit(code="ab123", prix=9.99, categorie="livre")
    ... except ValidationError:
    ...     print("Code invalide")
    Code invalide
    >>> try:
    ...     Produit(code="AB123", prix=-1, categorie="livre")
    ... except ValidationError:
    ...     print("Prix invalide")
    Prix invalide
    >>> try:
    ...     Produit(code="AB123", prix=10, categorie="autre")
    ... except ValidationError:
    ...     print("Catégorie invalide")
    Catégorie invalide
    """
    code: str
    prix: float = Field(ge=0, allow_inf_nan=False)
    categorie: Literal["livre", "informatique", "accessoire"]

    @field_validator("code")
    @classmethod
    def verifier_code(cls, valeur):
        if re.fullmatch(r"[A-Z]{2}[0-9]{3}", valeur) is None:
            raise ValueError("Deux lettres majuscules et trois chiffres attendus")
        return valeur


class Projet(BaseModel):
    """
    >>> projet = Projet(debut="2026-10-02", fin="2026-10-03")
    >>> projet.debut
    datetime.date(2026, 10, 2)
    >>> try:
    ...     Projet(debut="2026-10-02", fin="2026-10-01")
    ... except ValidationError:
    ...     print("Dates incohérentes")
    Dates incohérentes
    """
    debut: date
    fin: date

    @model_validator(mode="after")
    def verifier_dates(self) -> Self:
        if self.fin <= self.debut:
            raise ValueError("La fin doit être postérieure au début")
        return self


class Commande(BaseModel):
    """
    >>> donnees = {
    ...     "client": {"nom": "Célya", "email": "celya@example.com", "age": 21},
    ...     "produits": [{"code": "AB123", "prix": 10, "categorie": "livre"}],
    ... }
    >>> commande = Commande.model_validate(donnees)
    >>> commande.client.nom
    'Célya'
    >>> commande.produits[0].prix
    10.0
    """
    client: Utilisateur
    produits: list[Produit] = Field(min_length=1)


if __name__ == "__main__":
    utilisateur = Utilisateur(
        nom=" Célya ",
        email="celya@example.com",
        age="21",
    )

    print(utilisateur)
    print(utilisateur.model_dump())
    print(utilisateur.model_dump_json())

    produit = Produit(code="AB123", prix=9.99, categorie="livre")
    commande = Commande(client=utilisateur, produits=[produit])
    print(commande.model_dump_json())

    print(Projet(debut="2026-10-02", fin="2026-10-03"))

    for donnees in [
        {"nom": "Célya", "email": "invalide", "age": 21},
        {"nom": " ", "email": "celya@example.com", "age": 21},
        {"nom": "Célya", "email": "celya@example.com", "age": 150},
        {"email": "celya@example.com", "age": 21},
    ]:
        try:
            Utilisateur.model_validate(donnees)
        except ValidationError as erreur:
            print(erreur.errors())

    try:
        AgeStrict(age="21")
    except ValidationError as erreur:
        print(erreur.errors())