from Data.repository_poti import Repo
from Data.models import *
from typing import List


# V tej datoteki bomo definirali razred za obdelavo in delo s transakcijami

class PotiService:
    def __init__(self) -> None:
        # Potrebovali bomo instanco repozitorija. Po drugi strani bi tako instanco 
        # lahko dobili tudi kot input v konstrukturju.
        self.repo = Repo()

    def dobi_poti(self) -> List[pot]:
        return self.repo.dobi_poti()
    
    def dobi_poti_dto(self) -> List[potDto]:
        return self.repo.dobi_poti_dto()
    
    def dobi_pot(self, id) -> pot:
        return self.repo.dobi_pot(id)
    
    def dobi_pot_dto(self, id) -> potDto:
        return self.repo.dobi_pot_dto(id)

    def naredi_pot(self, ime : str, zacetna_lokacija :str, zahtevnost : str, trajanje_ur : float, visinka_razlika_m : float, opis : str, lokacija : str) -> None:

        t = pot(
            ime = ime,
            zacetna_lokacija = zacetna_lokacija,
            zahtevnost= zahtevnost,
            trajanje_ur=trajanje_ur,
            visinska_razlika_m=visinka_razlika_m,
            opis = opis,
            lokacija=lokacija
            )        
    # uporabimo repozitorij za zapis v bazo
        self.repo.dodaj_pot(t)

    def dodaj_pot(self,ime : str, zacetna_lokacija :str, zahtevnost : str, trajanje_ur : float, visinka_razlika_m : float, opis : str, lokacija : str) -> None:
       
        t = pot(
            ime = ime,
            zacetna_lokacija = zacetna_lokacija,
            zahtevnost= zahtevnost,
            trajanje_ur=trajanje_ur,
            visinska_razlika_m=visinka_razlika_m,
            opis = opis,
            lokacija=lokacija
            )        
        # uporabimo repozitorij za zapis v bazo
        self.repo.dodaj_pot(t)
       
    def posodobi_pot(self, ime : str, zacetna_lokacija :str, zahtevnost : str, trajanje_ur : float, visinka_razlika_m : float, opis : str, lokacija : str) -> None:
       
        t = pot(
            ime = ime,
            zacetna_lokacija = zacetna_lokacija,
            zahtevnost= zahtevnost,
            trajanje_ur=trajanje_ur,
            visinska_razlika_m=visinka_razlika_m,
            opis = opis,
            lokacija=lokacija
            )       
        # uporabimo repozitorij za zapis v bazo
        self.repo.posodobi_pot(t)      
