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
    
    def dobi_pohod_dto(self, id) -> pohodDto:
        return self.repo.dobi_pohod_dto(id)