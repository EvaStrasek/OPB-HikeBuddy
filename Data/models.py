from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime, date
from typing import Optional

@dataclass_json
@dataclass
class pohod:
    id: int = field(default=0),
    datum_zacetka: date=field(default=date.today)
    datum_konca: date=field(default=date.today)
    pot: int = field(default=0)

@dataclass_json
@dataclass
class pohodDto:
    id: int = field(default=0),
    datum_zacetka: date=field(default=date.today)
    datum_konca: date=field(default=date.today)
    pot: int = field(default=0)
    udelezenci: str = field(default="")
    ime : str=field(default="")
    zacetna_lokacija: str=field(default="")
    zahtevnost: str=field(default="")
    trajanje_ur: float=field(default=0)
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
    id : int = field(default=0)  
    ime : str=field(default="")
    #datum: date=field(default=date.today) 
    zacetna_lokacija: str=field(default="")
    zahtevnost: str=field(default="")
    trajanje_ur: float=field(default=0)
    visinska_razlika_m: float=field(default=0)
    opis: str=field(default="")
    lokacija: str=field(default="")

@dataclass_json
@dataclass
class potDto:
    id: int = field(default=0)  
    ime: str=field(default="")
    # datum: date=field(default=date.today)  
    zacetna_lokacija: str=field(default="")
    zahtevnost: str=field(default="")
    trajanje_ur: float=field(default=0)
    visinska_razlika_m: float=field(default=0)
    opis: str=field(default="")
    lokacija: str=field(default="")
    oprema: str=field(default="")

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
    vloga: str=field(default="udeleženec")
    ime: str=field(default="")
    priimek: str=field(default="")
    telefon: str=field(default="")
    e_mail: str=field(default="")

@dataclass_json
@dataclass
class udelezenciDto:
    id: int = field(default=0) 
    vloga: str=field(default="udeleženec")
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
    role: str = field(default="")


# Newly added by Manca

@dataclass
class Pot_Gora:
    id: int
    mountain_id: int
    route_name: str
    route_time: str
    route_difficulty: str
    start_point: str
    height_diff: int
    gear_summer: Optional[str]
    gear_winter: Optional[str]

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
    def __init__(self, id, ime, priimek, uporabnisko_ime, geslo, telefon, email, role="uporabnik"):
        self.id = id
        self.ime = ime
        self.priimek = priimek
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo
        self.telefon = telefon
        self.email = email
        self.role = role

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
            role=row.get("role", "uporabnik")
        )
        
        
@dataclass
class UporabnikDto:
    uporabnisko_ime: str = field(default="")
    ime: str = field(default="")
    priimek: str = field(default="")
    role:  str = field(default="user")  # Default role can be 'user', 'admin', etc.