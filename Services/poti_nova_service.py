from Data.repository_poti_nove import Repo
from Data.models import *
from typing import List

class GoraPotService:
    def __init__(self) -> None:
        self.repo = Repo()

    def dobi_poti(self) -> List[pot]:
        return self.repo.dobi_poti()
    
    def dobi_poti_dto(self) -> List[potDto]:
        return self.repo.dobi_poti_dto()
    
    def dobi_pot(self, id: int) -> pot:
        return self.repo.dobi_pot(id)
    
    def dobi_pot_dto(self, id: int) -> potDto:
        return self.repo.dobi_pot_dto(id)

    def naredi_pot(self,
                   mountain_id: int,
                   route_name: str,
                   route_time: float,
                   route_difficulty: str,
                   start_point: str,
                   height_diff: float,
                   gear_summer: str,
                   gear_winter: str) -> None:

        nova_pot = pot(
            mountain_id=mountain_id,
            route_name=route_name,
            route_time=route_time,
            route_difficulty=route_difficulty,
            start_point=start_point,
            height_diff=height_diff,
            gear_summer=gear_summer,
            gear_winter=gear_winter
        )
        self.repo.dodaj_pot(nova_pot)

    def dodaj_pot(self,
                  mountain_id: int,
                  route_name: str,
                  route_time: float,
                  route_difficulty: str,
                  start_point: str,
                  height_diff: float,
                  gear_summer: str,
                  gear_winter: str) -> None:

        nova_pot = pot(
            mountain_id=mountain_id,
            route_name=route_name,
            route_time=route_time,
            route_difficulty=route_difficulty,
            start_point=start_point,
            height_diff=height_diff,
            gear_summer=gear_summer,
            gear_winter=gear_winter
        )
        self.repo.dodaj_pot(nova_pot)

    def posodobi_pot(self,
                     id: int,
                     mountain_id: int,
                     route_name: str,
                     route_time: float,
                     route_difficulty: str,
                     start_point: str,
                     height_diff: float,
                     gear_summer: str,
                     gear_winter: str) -> None:

        posodobljena_pot = pot(
            id=id,
            mountain_id=mountain_id,
            route_name=route_name,
            route_time=route_time,
            route_difficulty=route_difficulty,
            start_point=start_point,
            height_diff=height_diff,
            gear_summer=gear_summer,
            gear_winter=gear_winter
        )
        self.repo.posodobi_pot(posodobljena_pot)

    def odstrani_pot(self, id: int):
        self.repo.odstrani_pot(id)

    