def fix_encoding(string: str) -> str:
    """Fixes æøåÆØÅ erros encountered if the file name is latin1 encoding in UTF-8

    :param str string: the string to fix

    :returns str: fixed UTF-8 string
    """
    string.encode(encoding="UTF-8", errors="backslashreplace").decode("utf-8")

    replace_table = {}
    replace_table["\udce6"] = "æ"
    replace_table["\udcf8"] = "ø"
    replace_table["\udce5"] = "å"
    replace_table["\udcc6"] = "Æ"
    replace_table["\udcd8"] = "Ø"
    replace_table["\udcc5"] = "Å"

    for search, replace in replace_table.items():
        string = string.replace(search, replace)

    return string
