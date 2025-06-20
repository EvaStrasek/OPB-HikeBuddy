from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime, date
from typing import Optional

@dataclass_json
@dataclass
class pohod:
    id: int = field(default=0)
    datum_zacetka: date=field(default=date.today)
    datum_konca: date=field(default=date.today)
    pot: int = field(default=0)

@dataclass_json
@dataclass
class pohodDto:
    id: int = field(default=0)
    datum_zacetka: date=field(default=date.today)
    datum_konca: date=field(default=date.today)
    pot: int = field(default=0)
    udelezenci: str = field(default="")
    ime : str=field(default="")
    zacetna_lokacija: str=field(default="")
    zahtevnost: str=field(default="")
    trajanje_ur: str=field(default="")
    visinska_razlika_m: float=field(default=0)
    opis: str=field(default="")
    lokacija: str=field(default="")

# class udelezenec:
#     id,
#     dogodek,
#     ime,
#     priimek,
#     email,
#     telefon

# class vodnik:
#     id,
#     ime,
#     priimek,
#     email,
#     telefon,
#     dogodek : int = field(default=0)  

@dataclass_json
@dataclass
class pot:
    id: int = field(default=0)
    mountain_id: int = field(default=0)
    route_name: str = field(default="")
    route_time: str = field(default="")  # Lahko spremeniš v float ali int, če imaš ure v številki
    route_difficulty: str = field(default="")
    start_point: str = field(default="")
    height_diff: float = field(default=0)
    gear_summer: Optional[str] = field(default="")
    gear_winter: Optional[str] = field(default="")


@dataclass_json
@dataclass
class potDto:
    id: int = field(default=0)
    mountain_id: int = field(default=0)
    route_name: str = field(default="")
    route_time: str = field(default="")
    route_difficulty: str = field(default="")
    start_point: str = field(default="")
    height_diff: float = field(default=0)
    gear_summer: Optional[str] = field(default="")
    gear_winter: Optional[str] = field(default="")
    
@dataclass_json
@dataclass
class oprema:
    id: int = field(default=0) 
    ime_opreme: str=field(default="")
    vrsta_opreme: str=field(default="")
    opis: str=field(default="")

@dataclass_json
@dataclass
class opremaDto:
    id: int = field(default=0) 
    ime_opreme: str=field(default="")
    vrsta_opreme: str=field(default="")
    opis: str=field(default="")

@dataclass_json
@dataclass
class udelezenci:
    id: int = field(default=0) 
    rola: str=field(default="udeleženec")
    ime: str=field(default="")
    priimek: str=field(default="")
    telefon: str=field(default="")
    e_mail: str=field(default="")

@dataclass_json
@dataclass
class udelezenciDto:
    id: int = field(default=0) 
    rola: str=field(default="udeleženec")
    ime: str=field(default="")
    priimek: str=field(default="")
    telefon: str=field(default="")
    e_mail: str=field(default="")

# @dataclass_json
# @dataclass
# class Uporabnik:
#     username: str = field(default="")
#     role: str = field(default="")
#     password_hash: str = field(default="")
#     last_login: str = field(default="")

@dataclass
class UporabnikDto:
    username: str = field(default="")
    rola: str = field(default="udeleženec")


# Newly added by Manca

# @dataclass
# class Pot_Gora:
#     id: int
#     mountain_id: int
#     route_name: str
#     route_time: str
#     route_difficulty: str
#     start_point: str
#     height_diff: int
#     gear_summer: Optional[str]
#     gear_winter: Optional[str]

@dataclass
class Gora:
    mountain_id: int
    name: str
    country: str
    mountain_range: str
    height_m: int
    coordinates: str
    type: str
    popularity: str
    num_paths: int
    num_gps_paths: Optional[int]
    description: Optional[str]
    
@dataclass_json
@dataclass
class goraDto:
    mountain_id: int
    name: str
    
# @dataclass
# class Uporabnik:
#     ime: str
#     priimek: str
#     uporabnisko_ime: str
#     geslo: str
#     telefon: str
#     email: str
#     id: Optional[int] = field(default=None)
    
    
class Uporabnik:
    def __init__(self, id, ime, priimek, uporabnisko_ime, geslo, telefon, email, rola="udeleženec"):
        self.id = id
        self.ime = ime
        self.priimek = priimek
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo
        self.telefon = telefon
        self.email = email
        self.rola = rola

    @staticmethod
    def from_dict(row):
        return Uporabnik(
            id=row.get("id"),
            ime=row.get("ime"),
            priimek=row.get("priimek"),
            uporabnisko_ime=row.get("uporabnisko_ime"),
            geslo=row.get("geslo"),
            telefon=row.get("telefon"),
            email=row.get("email"),
            rola=row.get("rola", "udeleženec")
        )
        
        
@dataclass
class UporabnikDto:
    uporabnisko_ime: str = field(default="")
    ime: str = field(default="")
    priimek: str = field(default="")
    rola:  str = field(default="udeleženec")  # Default role can be 'user', 'admin', etc.
    
class PrijavaNaPohod:
    def __init__(self, uporabnik_id: int, pohod_id: int, cas_prijave: datetime = None):
        self.uporabnik_id = uporabnik_id
        self.pohod_id = pohod_id
        self.cas_prijave = cas_prijave or datetime.now()

    @staticmethod
    def from_dict(row):
        return PrijavaNaPohod(
            uporabnik_id=row["uporabnik_id"],
            pohod_id=row["pohod_id"],
            cas_prijave=row["cas_prijave"]
        )