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


def test_parse_date() -> None:
    from mechamd.helpers import parse_date

    cases = {
        "2024": ("2024", "year"),
        "mars 2025": ("2025-03", "month"),
        "Sept. 2025": ("2025-09", "month"),
        "1er août 2026": ("2026-08-01", "day"),
        "12/09/2026": ("2026-09-12", "day"),
        "09/2026": ("2026-09", "month"),
        "2026-09-12": ("2026-09-12", "day"),
        "2026-9": ("2026-09", "month"),
    }
    for text, (iso, precision) in cases.items():
        date = parse_date(text)
        assert date is not None, text
        assert (date.iso, date.precision, date.text) == (iso, precision, text)
    for bad in ["", "bientôt", "plop 2025", "13/13/2026", "32/01/2026", "12 mois"]:
        assert parse_date(bad) is None, bad


def test_split_items() -> None:
    from mechamd.helpers import Item, split_items

    text = (
        "Intro\n- 2024 : Création\n- mars 2025 : Prototype\n  Deux lignes\n  de description.\n"
        "\n1. suite\nFin\n```\n- pas un item\n```"
    )
    items, rest = split_items(text)
    assert items == [
        Item("2024 : Création", "", 2),
        Item("mars 2025 : Prototype", "Deux lignes\nde description.", 3),
        Item("suite", "", 7),
    ]
    assert rest == "Intro\nFin\n```\n- pas un item\n```"
    assert split_items("-") == ([Item("", "", 1)], "")


def test_slugify() -> None:
    from mechamd.helpers import slugify

    assert slugify("Salle B204 : bilan d'été") == "salle-b204-bilan-d-été"
    assert slugify("  ") == ""
