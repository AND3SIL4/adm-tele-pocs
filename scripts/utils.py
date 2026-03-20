import unicodedata


def strip_acents(string: str) -> str:
    """Strip accents from a string using Unicode normalization."""
    # Normalize the string to NDF (Canolical Descomposition)
    nfd_form = unicodedata.normalize("NFD", string)
    # Filter out all combining characters (which have the 'mn' category)
    striped_string = "".join(c for c in nfd_form if not unicodedata.combining(c))
    return striped_string


if __name__ == "__main__":
    print(strip_acents("Holá que más"))
    print(strip_acents("Hola que mas"))