from Data.repository_avtentikacija import Repo
from Data.models import Uporabnik, UporabnikDto
import bcrypt


class AuthService:
    repo: Repo
    def __init__(self):
        self.repo = Repo()

    def dodaj_uporabnika(self, ime: str, priimek: str, uporabnisko_ime: str, geslo: str,
                         telefon: str, email: str) -> UporabnikDto | None:
        if self.repo.obstaja_uporabnik(uporabnisko_ime):
            print("Uporabnik že obstaja.")
            return None  # ali dvigneš izjemo
            # Hashiranje gesla
        geslo_hash = bcrypt.hashpw(geslo.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        uporabnik = Uporabnik(
            id=None,
            ime=ime,
            priimek=priimek,
            uporabnisko_ime=uporabnisko_ime,
            geslo=geslo_hash,
            telefon=telefon,
            email=email
        )

        self.repo.dodaj_uporabnika(uporabnik)
        return UporabnikDto(uporabnisko_ime=uporabnisko_ime, ime=ime, priimek=priimek)

    def obstaja_uporabnik(self, uporabnisko_ime: str) -> bool:
        return self.repo.obstaja_uporabnik(uporabnisko_ime)

    def prijavi_uporabnika(self, uporabnisko_ime: str, geslo: str) -> UporabnikDto | bool:
        try:
            user = self.repo.pridobi_uporabnika_po_uporabniskem_imenu(uporabnisko_ime)
            
        except Exception:
            
            return False
        if bcrypt.checkpw(geslo.encode('utf-8'), user.geslo.encode('utf-8')):
            
            return UporabnikDto(uporabnisko_ime=user.uporabnisko_ime, ime=user.ime, priimek=user.priimek, role=user.role)
        else:
            
            return False
        
    def dobi_id_uporabnika(self, uporabnisko_ime):
        return self.repo.dobi_id_uporabnika(uporabnisko_ime)
    
    def pridobi_prijave_uporabnika(self, uporabnisko_ime: str):
        return self.repo.pridobi_prijave_uporabnika(uporabnisko_ime)
    
    def odjavi_uporabnika_od_pohoda(self, pohod_id, uporabnik_id):
    # Dodatna logika, preverjanje lastništva itd. po potrebi
        self.repo.izbrisi_prijavo(pohod_id, uporabnik_id)

    def pridobi_vse_prijave(self):
        return self.repo.pridobi_vse_prijave()

