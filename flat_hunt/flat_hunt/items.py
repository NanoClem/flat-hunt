from dataclasses import dataclass, field, asdict


@dataclass
class FlatItem:
    source_id: str = None
    title: str = None
    rent: int = None
    expenses: int = None
    url: str = None
    lat: float = None
    lon: float = None
    address: str = None
    nb_rooms: int = None
    nb_bathrooms: int = None
    nb_bedrooms: int = None
    surface: int = None
    nb_pics: int = None
    pics: list[str] = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)
