import datetime
from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.pohodi_service import PohodiService
from Services.poti_service import PotiService
from Services.auth_service import AuthService
from Services.gore_service import GoraService
import os

# Ustvarimo instance servisov, ki jih potrebujemo. 
# Če je število servisov veliko, potem je service bolj smiselno inicializirati v metodi in na
# začetku datoteke (saj ne rabimo vseh servisov v vseh metodah!)

pohodiService = PohodiService()
potiService = PotiService()
auth = AuthService()
goreService = GoraService()

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):
        cookie = request.get_cookie("uporabnik")
        if cookie:
            return f(*args, **kwargs)
        return template("prijava.html",uporabnik=None, rola=None, napaka="Potrebna je prijava!")
        
    return decorated

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')


@get('/')
# @cookie_required
def index():
    """
    Domača stran s pohodi.
    """   
  
    pohodi = pohodiService.dobi_pohode_dto() 

    return template_user('pohodi.html', pohodi = pohodi)

@get('/poti')
# @cookie_required
def poti():
    """
    Poti
    """   
  
    poti = potiService.dobi_poti_dto() 

    return template_user('poti.html', poti = poti)


# @get('/osebe')
# @cookie_required
# def index():
#     """
#     Domača stran z osebami.    """   
  
#     osebe = service.dobi_osebe_dto()
#     return template_user('osebe.html', osebe = osebe)




@get('/poti_dto')
def poti_dto(): 
  
    poti_dto = potiService.dobi_poti_dto()  
        
    return template_user('pohodiDto.html', poti = poti_dto)

@get('/uredi_pot/<id:int>')
def uredi_pot(id):
    """
    Stran za urejanje poti.  """   
    pot = potiService.dobi_pot_dto(id)
    return template_user('uredi_pot.html', pot = pot)

@get('/uredi_pohod/<id:int>')
def uredi_pohod(id):
    """
    Stran za urejanje pohoda.  """   
    pohod = pohodiService.dobi_pohod_dto(id)
    return template_user('uredi_pohod.html', pohod = pohod)

@get('/dodaj_pohod')
def dodaj_pohod():
    """
    Stran za dodajanje pohodov.  """
    poti = potiService.dobi_poti_dto()    
    return template_user('dodaj_pohod.html', poti=poti)

@get('/dodaj_pot')
def dodaj_pot():
    """
    Stran za dodajanje poti.  """
    poti = potiService.dobi_poti_dto()    
    return template_user('dodaj_pot.html', poti=poti)

@post('/dodaj_pohod')
def dodaj_pohod_post():
    datum_zacetka_str = request.forms.get('datum_zacetka')
    datum_konca_str = request.forms.get('datum_konca')
        
    datum_zacetka = datetime.datetime.strptime(datum_zacetka_str, '%Y-%m-%d').date()
    datum_konca = datetime.datetime.strptime(datum_konca_str, '%Y-%m-%d').date()
    # datum_zacetka = datetime.strptime(request.forms.get('datum_zacetka'))
    # datum_konca = datetime.strptime(request.forms.get('datum_konca'))
    pot = int(request.forms.get('pot'))

    pohodiService.dodaj_pohod(datum_zacetka, datum_konca, pot)
    
    redirect(url('/'))

@post('/dodaj_pot')
def dodaj_pot_post():

    ime = request.forms.get('ime')
    zahtevnost = request.forms.get('zahtevnost')
    zacetna_lokacija = request.forms.get('zacetna_lokacija')
    trajanje_ur = float(request.forms.get('trajanje_ur'))
    visinska_razlika_m = float(request.forms.get('visinska_razlika_m'))
    opis = request.forms.get('opis')
    lokacija = request.forms.get('lokacija')
    potiService.dodaj_pot(ime, zacetna_lokacija, zahtevnost, trajanje_ur, visinska_razlika_m, opis, lokacija)
    
    redirect(url('/poti'))


@post('/uredi_pohod')
def uredi_pohod_post():
#     """
#     Stran za urejanje transakcije.  """ 
    id = int(request.forms.get('id'))
    datum_zacetka_str = request.forms.get('datum_zacetka')
    datum_konca_str = request.forms.get('datum_konca')
        
    datum_zacetka = datetime.datetime.strptime(datum_zacetka_str, '%Y-%m-%d').date()
    datum_konca = datetime.datetime.strptime(datum_konca_str, '%Y-%m-%d').date()
    pot = request.forms.get('pot')
    
    pohodiService.posodobi_pohod(id, datum_zacetka, datum_konca, pot)
    redirect(url('/'))

@post('/uredi_pot')
def uredi_pot_post():
    id = int(request.forms.get('id'))
    ime = request.forms.get('ime')
    zahtevnost = request.forms.get('zahtevnost')
    zacetna_lokacija = request.forms.get('zacetna_lokacija')
    trajanje_ur = float(request.forms.get('trajanje_ur'))
    visinska_razlika_m = float(request.forms.get('visinska_razlika_m'))
    opis = request.forms.get('opis')
    lokacija = request.forms.get('lokacija')
    potiService.posodobi_pot(id,ime, zacetna_lokacija, zahtevnost, trajanje_ur, visinska_razlika_m, opis, lokacija)
    
    redirect(url('/poti'))

@post('/prijava')
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in njegovi roli.
    Drugače sporoči, da je prijava neuspešna.
    """
    username = request.forms.get('username')
    password = request.forms.get('password')
    if not auth.obstaja_uporabnik(username):
        return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja")
    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnik", username)
        response.set_cookie("rola", prijava.role)      
        # redirect v večino primerov izgleda ne deluje
        redirect(url('/'))
        # Uporabimo kar template, kot v sami "index" funkciji
        # transakcije = service.dobi_transakcije()        
        # return template('transakcije.html', transakcije = transakcije)      
    else:
        return template("prijava.html", uporabnik=None, rola=None, napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")

@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """
  
    response.delete_cookie("uporabnik")
    response.delete_cookie("rola")
  
    return template('prijava.html', uporabnik=None, rola=None, napaka=None) 




@get('/gore')
def seznam_gora():
    """
    Prikaz gora po straneh – 20 na stran
    """
    vse_gore = goreService.pridobi_vse_gore()
    stran = int(request.query.get('page', '1'))
    velikost_strani = 20
    zacetek = (stran - 1) * velikost_strani
    konec = zacetek + velikost_strani
    trenutne_gore = vse_gore[zacetek:konec]
    st_strani = (len(vse_gore) + velikost_strani - 1) // velikost_strani

    return template_user('gore.html', gore=trenutne_gore, stran=stran, st_strani=st_strani)








#Dokler nimate razvitega vmesnika za dodajanje uporabnikov, jih dodajte kar ročno.
#auth.dodaj_uporabnika('eva', 'admin', 'eva')
if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)
    
    