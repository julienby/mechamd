from mechamd.attrs import is_directive_info, parse_info


def test_name_only() -> None:
    info = parse_info("card")
    assert (info.name, info.variant, info.id, info.attrs, info.warnings) == (
        "card",
        None,
        None,
        {},
        [],
    )


def test_full_attrs() -> None:
    info = parse_info(' Card {.cover #intro cols=3 title="Avec espaces"}')
    assert info.name == "card"
    assert info.variant == "cover"
    assert info.id == "intro"
    assert info.attrs == {"cols": "3", "title": "Avec espaces"}
    assert info.warnings == []


def test_is_directive_info() -> None:
    assert is_directive_info("card{.x}")
    assert not is_directive_info("")
    assert not is_directive_info("{.x}")


def test_tolerant_on_bad_input() -> None:
    info = parse_info('card{.a .b #x #y ?? =v title="oops}')
    assert info.variant == "a"
    assert info.id == "x"
    assert len(info.warnings) >= 3


def test_missing_brace_and_trailing_text() -> None:
    assert parse_info("card{.a").variant == "a"
    assert parse_info("card{.a").warnings
    assert parse_info("card{.a} trop").warnings
    assert parse_info("card du texte").warnings
