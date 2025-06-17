from Data.repository_gore import Repo
from Data.models import Gora
from typing import List, Optional

class GoraService:
    repo: Repo
    def __init__(self):
        self.repo = Repo()

    def pridobi_vse_gore(self) -> List[Gora]:
        return self.repo.dobi_gore()

    def pridobi_goro(self, id: int) -> Optional[Gora]:
        return self.repo.dobi_goro(id)

    def ustvari_goro(self, gora: Gora):
        # Tukaj lahko dodaš validacije, npr. preveri če že obstaja id
        self.repo.dodaj_goro(gora)

    def posodobi_goro(self, gora: Gora):
        # Lahko preveriš, ali gora obstaja pred posodobitvijo
        self.repo.posodobi_goro(gora)
