import re
from datetime import date
from ipaddress import IPv4Address


def valider_code(texte):
    """
    >>> valider_code("AB123")
    True
    >>> valider_code("AB1234")
    False
    >>> valider_code("ab123")
    False
    """
    return re.fullmatch(r"[A-Z]{2}[0-9]{3}", texte) is not None


def valider_date(texte):
    """
    >>> valider_date("2026-10-02")
    True
    >>> valider_date("2026-02-31")
    False
    >>> valider_date("02/10/2026")
    False
    >>> valider_date("2024-02-29")
    True
    """
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", texte) is None:
        return False
    try:
        date.fromisoformat(texte)
    except ValueError:
        return False
    return True


def valider_ipv4(texte):
    """
    >>> valider_ipv4("192.168.1.1")
    True
    >>> valider_ipv4("256.1.1.1")
    False
    >>> valider_ipv4("192.168.1")
    False
    """
    try:
        IPv4Address(texte)
    except ValueError:
        return False
    return True


def valider_mot_de_passe(texte):
    """
    >>> valider_mot_de_passe("Bonjour1!")
    True
    >>> valider_mot_de_passe("bonjour1!")
    False
    >>> valider_mot_de_passe("Bonjour!")
    False
    >>> valider_mot_de_passe("Ab1!")
    False
    """
    motif = r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9\s])\S{8,}"
    return re.fullmatch(motif, texte) is not None


if __name__ == "__main__":
    exemples = [
        (r".", "a"),
        (r"a?", ""),
        (r"a*", "aaa"),
        (r"a+", "aaa"),
        (r"\d", "5"),
        (r"\D", "a"),
        (r"\w", "_"),
        (r"\W", "!"),
        (r"\s", " "),
        (r"\S", "a"),
        (r"a{3}", "aaa"),
        (r"a{2,4}", "aaa"),
        (r"\.", "."),
        (r"^abc$", "abc"),
        (r"[abc]", "b"),
        (r"[^abc]", "z"),
        (r"chat|chien", "chien"),
        (r"(ab)+", "abab"),
    ]

    for motif, texte in exemples:
        print(motif, repr(texte), re.fullmatch(motif, texte) is not None)

    texte = "<b>Bonjour</b><b>Bonsoir</b>"
    print(re.findall(r"<b>.*</b>", texte))
    print(re.findall(r"<b>.*?</b>", texte))

    resultat = re.fullmatch(r"([A-Z]{2})([0-9]{3})", "AB123")
    print(resultat.group(1))
    print(resultat.group(2))

    print(valider_code("AB123"))
    print(valider_date("2026-02-31"))
    print(valider_ipv4("192.168.1.1"))
    print(valider_mot_de_passe("Bonjour1!"))