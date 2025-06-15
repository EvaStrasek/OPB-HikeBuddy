from Data.repository_pohodi import Repo
from Data.models import *
from typing import List


# V tej datoteki bomo definirali razred za obdelavo in delo s transakcijami

class PohodiService:
    def __init__(self) -> None:
        # Potrebovali bomo instanco repozitorija. Po drugi strani bi tako instanco 
        # lahko dobili tudi kot input v konstrukturju.
        self.repo = Repo()

    def dobi_pohode(self) -> List[pohod]:
        return self.repo.dobi_pohode()
    
    def dobi_pohode_dto(self) -> List[pohodDto]:
        return self.repo.dobi_pohode_dto()
    
    def dobi_pohod(self, id) -> pohod:
        return self.repo.dobi_pohod(id)
    
    def dobi_pohod_dto(self, id) -> pohodDto:
        return self.repo.dobi_pohod_dto(id)
    
    def dodaj_pohod(self, datum_zacetka : datetime, datum_konca: datetime, pot: int) -> None:
       
        t = pohod(
            datum_zacetka=datum_zacetka,
            datum_konca=datum_konca,
            pot=pot,
            )        
        # uporabimo repozitorij za zapis v bazo
        self.repo.dodaj_pohod(t)
    
    def posodobi_pohod(self, id : int, datum_zacetka : datetime, datum_konca: datetime, pot: int) -> None:
       
        t = pohod(
            id=id,
            datum_zacetka=datum_zacetka,
            datum_konca=datum_konca,
            pot=pot,
            )        
        # uporabimo repozitorij za zapis v bazo
        self.repo.posodobi_pohod(t)

    # def naredi_transakcijo_oseba(self, o : oseba, znesek: float, opis: str) -> None:
       
    #     # Naredimo objekt za transakcijo.
    #     # Za to potrebujemo številko računa.

    #     r = self.repo.dobi_racun(o.emso)

    #     # Naredimo objekt za transakcijo
    #     t = transakcija(
    #         racun=r.stevilka,
    #         znesek=znesek,
    #         cas=datetime.now(),
    #         opis=opis
    #         )        
    #     # uporabimo repozitorij za zapis v bazo
    #     self.repo.dodaj_transakcijo(t)

    # def naredi_transakcijo(self, racun: int, cas:str, znesek: float, opis: str) -> None:
       
    #     # Naredimo objekt za transakcijo.
    #     # Za to potrebujemo številko računa.
        

    #     # Naredimo objekt za transakcijo
    #     t = transakcija(
    #         racun=racun,
    #         znesek=znesek,
    #         cas=cas,
    #         opis=opis
    #         )        
    #     # uporabimo repozitorij za zapis v bazo
    #     self.repo.dodaj_transakcijo(t)

    # def posodobi_transakcijo(self, id: int, racun: int, cas:str, znesek: float, opis: str) -> None:
    #     # Naredimo objekt za transakcijo
    #     t = transakcija(
    #         id=id,
    #         racun=racun,
    #         cas=cas,
    #         znesek=znesek,            
    #         opis=opis
    #         )        
    #     # uporabimo repozitorij za zapis v bazo
    #     self.repo.posodobi_transakcijo(t)

    # def izplacaj_nagrado(self, znesek: float, opis: str) -> None:

    #     # Vsek osebam bi radi izplačali nagrado.
    #     osebe = self.repo.dobi_osebe()
    #     for o in osebe:
    #         self.naredi_transakcijo_oseba(o, znesek, opis)