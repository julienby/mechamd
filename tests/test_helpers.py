from mechamd.helpers import Image, Link, first_heading, first_image, trailing_link


def test_first_heading() -> None:
    assert first_heading("texte\n## Titre ##\nsuite") == ("Titre", "texte\nsuite")
    assert first_heading("pas de titre") == (None, "pas de titre")
    assert first_heading("```\n# pas un titre\n```\n### Vrai")[0] == "Vrai"


def test_first_image() -> None:
    image, rest = first_image('![Sonde](a/b.jpg "légende")\n# T')
    assert image == Image(src="a/b.jpg", alt="Sonde")
    assert rest == "# T"
    assert first_image("avant ![x](y.png) après")[1] == "avant après"
    assert first_image("~~~\n![x](y.png)\n~~~")[0] is None


def test_trailing_link() -> None:
    assert trailing_link("texte\n[Voir](a.md)\n\n") == (Link("a.md", "Voir"), "texte")
    assert trailing_link("un [lien](a.md) dans le texte")[0] is None
    assert trailing_link("")[0] is None
    assert trailing_link("```\n[Voir](a.md)")[0] is None
