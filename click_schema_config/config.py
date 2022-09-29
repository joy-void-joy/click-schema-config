import ast
import re

regexes = {
    "section": re.compile(r"^\[(?P<section>.*)\](#.*)?$"),
    "comment": re.compile(r"^[#;]\s?(?P<comment>.*)$"),
    "variable": re.compile(
        r"^(?P<variable>\w+)\s*(:\s*(?P<type>\w+))?\s*(=\s*(?P<value>.*))?\s*([#;].*)?$"
    ),
}


def read_config_one_file(file, result=None):
    result = dict(**(result or {}))
    result.setdefault("DEFAULT", {})
    current = {
        "section": "DEFAULT",
        "description": [],
    }
    for i in file:
        match i.strip():
            case "":
                current["description"] = []

            case i if m := regexes["section"].match(i):
                current["section"] = m.group("section")
                result[current["section"]] = result.get(current["section"], {})
                current["description"] = []

            case i if m := regexes["comment"].match(i):
                current["description"] += [m.group("comment")]

            case i if m := regexes["variable"].match(i):
                variable = m.group("variable").strip()
                value = ast.literal_eval(m.group("value") or "None")
                to_modify = result[current["section"]].setdefault(
                    variable, {"description": None}
                )
                to_modify.update(
                    {
                        "value": value,
                        "type": m.group("type") or type(value).__name__,
                    }
                    | (
                        {"description": "\n".join(current["description"])}
                        if current["description"]
                        else {}
                    )
                )
                current["description"] = []

            case i:
                raise ValueError(f"Could not parse line: {i}")

    return result


def read_config(filenames, result=None):
    if not isinstance(filenames, list):
        filenames = [filenames]

    result = dict(**(result or {}))

    for filename in filenames:
        with open(filename) as file:
            result = read_config_one_file(file, result)

    return result
