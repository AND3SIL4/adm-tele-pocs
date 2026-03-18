from dataclasses import asdict, dataclass
from json import dumps


@dataclass
class IdCardParts:
    plan: str
    contract: str
    family: str
    user: str


def split_id_card(id_card: str) -> IdCardParts:
    if len(id_card) < 4:
        raise ValueError("El id_card debe tener al menos 4 caracteres")

    id_card_parts = IdCardParts(
        plan=id_card[:2], contract=id_card[2:-2], family=id_card[-2], user=id_card[-1]
    )
    return dumps(asdict(id_card_parts))


print(split_id_card("10632707112"))
