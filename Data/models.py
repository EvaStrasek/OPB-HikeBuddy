from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime, date

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
