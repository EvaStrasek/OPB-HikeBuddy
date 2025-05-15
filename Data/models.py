from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime

@dataclass_json
@dataclass
class pohodi:
    id : int = field(default=0)  
    ime_pohoda : str=field(default="")
    datum: datetime=field(default=datetime.now()) 
    zacetna_lokacija: str=field(default="")
    zahtevnost: str=field(default="")
    trajanje_ur: float=field(default=0)
    visinska_razlika: float=field(default=0)
    opis: str=field(default="")
    lokacija: str=field(default="")

@dataclass_json
@dataclass
class pohodiDto:
    id: int = field(default=0)  
    ime_pohoda: str=field(default="")
    datum: datetime=field(default=datetime.now()) 
    zacetna_lokacija: str=field(default="")
    zahtevnost: str=field(default="")
    trajanje_ur: float=field(default=0)
    visinska_razlika: float=field(default=0)
    opis: str=field(default="")
    lokacija: str=field(default="")

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
