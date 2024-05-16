import ast


def bytes_to_dict(string: bytes) -> dict:
    return ast.literal_eval(string.decode("UTF-8"))
