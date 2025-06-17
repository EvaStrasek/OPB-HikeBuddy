from Data.repository_poti_nove import Repo
from Data.models import Gora, Pot_Gora
from typing import List, Optional

class GoraPotService:
    repo: Repo
    def __init__(self):
        self.repo = Repo()

    # ------------------- GORA -------------------

    def dobi_gore(self) -> List[Gora]:
        return self.repo.dobi_gore()

    def dobi_goro(self, id: int) -> Optional[Gora]:
        return self.repo.dobi_goro(id)

    def dodaj_goro(self, mountain_id: int, name: str, country: str, mountain_range: str,
                   height_m: int, coordinates: str, type: str, popularity: str, num_paths: int,
                   num_gps_paths: Optional[int], description: Optional[str]) -> None:
        g = Gora(mountain_id, name, country, mountain_range, height_m, coordinates, type,
                 popularity, num_paths, num_gps_paths, description)
        self.repo.dodaj_goro(g)

    def posodobi_goro(self, mountain_id: int, name: str, country: str, mountain_range: str,
                      height_m: int, coordinates: str, type: str, popularity: str, num_paths: int,
                      num_gps_paths: Optional[int], description: Optional[str]) -> None:
        g = Gora(mountain_id, name, country, mountain_range, height_m, coordinates, type,
                 popularity, num_paths, num_gps_paths, description)
        self.repo.posodobi_goro(g)

    # ------------------- POT_GORA -------------------

    def dobi_poti(self) -> List[Pot_Gora]:
        return self.repo.dobi_poti()

    def dobi_pot(self, id: int) -> Optional[Pot_Gora]:
        return self.repo.dobi_pot(id)

    def dodaj_pot(self, id: int, mountain_id: int, route_name: str, route_time: str,
                  route_difficulty: str, start_point: str, height_diff: int,
                  gear_summer: Optional[str], gear_winter: Optional[str]) -> None:
        p = Pot_Gora(id, mountain_id, route_name, route_time, route_difficulty,
                     start_point, height_diff, gear_summer, gear_winter)
        self.repo.dodaj_pot(p)

    def posodobi_pot(self, id: int, mountain_id: int, route_name: str, route_time: str,
                     route_difficulty: str, start_point: str, height_diff: int,
                     gear_summer: Optional[str], gear_winter: Optional[str]) -> None:
        p = Pot_Gora(id, mountain_id, route_name, route_time, route_difficulty,
                     start_point, height_diff, gear_summer, gear_winter)
        self.repo.posodobi_pot(p)

    def izbrisi_pot(self, id: int) -> None:
        self.repo.izbrisi_pot(id)
