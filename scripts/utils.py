import unicodedata
from datetime import datetime
import holidays


def strip_acents(string: str) -> str:
    """Strip accents from a string using Unicode normalization."""
    # Normalize the string to NDF (Canolical Descomposition)
    nfd_form = unicodedata.normalize("NFD", string)
    # Filter out all combining characters (which have the 'mn' category)
    striped_string = "".join(c for c in nfd_form if not unicodedata.combining(c))
    return striped_string


def is_business_day(date_str: str) -> bool:
    # Returns True if a given DD/MM/YYYY date string is a Colombian business day
    # False otherwise. Raises ValueError if the date string is invalid.
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError as exc:
        raise ValueError(
            f"Error intentando normalizar la fecha de ejecución: {exc}"
        ) from exc

    co_holidays = holidays.Colombia(years=date_obj.year)
    is_holiday = date_obj in co_holidays
    # weekday() -> Monday=0 ... Sunday=6; so 5 and 6 are Saturday and Sunday
    # Allows executions in Saturdays (Only holidays and Sundays won't execute)
    is_weekend = date_obj.weekday() > 5
    return not (is_holiday or is_weekend)


if __name__ == "__main__":
    print(is_business_day("21/03/2026"))
