from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.transakcije_service import TransakcijeService
from Services.auth_service import AuthService
import os

# Ustvarimo instance servisov, ki jih potrebujemo. 
# Če je število servisov veliko, potem je service bolj smiselno inicializirati v metodi in na
# začetku datoteke (saj ne rabimo vseh servisov v vseh metodah!)

service = TransakcijeService()
auth = AuthService()


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
  
    pohodi_dto = service.dobi_pohode_dto() 

    return template_user('pohodi.html', pohodi = pohodi_dto)

# @get('/osebe')
# @cookie_required
# def index():
#     """
#     Domača stran z osebami.    """   
  
#     osebe = service.dobi_osebe_dto()
#     return template_user('osebe.html', osebe = osebe)




# @get('/transakcije_dto')
# def transakcije_dto():
#     """
#     Stran z dto transakcijami.
#     """   
  
#     transakcije_dto = service.dobi_transakcije_dto()  
        
#     return template_user('transakcije_dto.html', transakcije = transakcije_dto)

@get('/dodaj_pohod')
def dodaj_pohod():
    """
    Stran za dodajanje pohodov.  """
    pohodi = service.dobi_pohode_dto()    
    return template_user('dodaj_pohod.html', pohodi=pohodi)


# @post('/dodaj_transakcijo')
# def dodaj_transakcijo_post():
#     # Preberemo podatke iz forme. Lahko bi uporabili kakšno dodatno metodo iz service objekta

#     racun = int(request.forms.get('racun'))
#     znesek = float(request.forms.get('znesek'))
#     opis = request.forms.get('opis')
#     cas = request.forms.get('cas')   

#     service.naredi_transakcijo(racun, cas, znesek, opis)
    
    
#     redirect(url('/'))

@get('/uredi_pohod/<id:int>')
def uredi_pohod(id):
    """
    Stran za urejanje pohoda.  """   
    pohod = service.dobi_pohod_dto(id)
    return template_user('uredi_pohod.html', pohod = pohod)

# @post('/uredi_transakcijo')
# def uredi_transakcijo_post():
#     """
#     Stran za urejanje transakcije.  """ 
#     id = int(request.forms.get('id'))  
#     racun = int(request.forms.get('racun'))
#     znesek = float(request.forms.get('znesek'))
#     opis = request.forms.get('opis')   
#     cas = request.forms.get('cas') 
    
#     service.posodobi_transakcijo(id, racun, cas, znesek, opis)
#     redirect(url('/'))

# @post('/prijava')
# def prijava():
#     """
#     Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in njegovi roli.
#     Drugače sporoči, da je prijava neuspešna.
#     """
#     username = request.forms.get('username')
#     password = request.forms.get('password')

#     if not auth.obstaja_uporabnik(username):
#         return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja")

#     prijava = auth.prijavi_uporabnika(username, password)
#     if prijava:
#         response.set_cookie("uporabnik", username)
#         response.set_cookie("rola", prijava.role)
        
#         # redirect v večino primerov izgleda ne deluje
#         redirect(url('/'))

#         # Uporabimo kar template, kot v sami "index" funkciji

#         # transakcije = service.dobi_transakcije()        
#         # return template('transakcije.html', transakcije = transakcije)
        
#     else:
#         return template("prijava.html", uporabnik=None, rola=None, napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")

# @get('/odjava')
# def odjava():
#     """
#     Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
#     """
    
#     response.delete_cookie("uporabnik")
#     response.delete_cookie("rola")
    
#     return template('prijava.html', uporabnik=None, rola=None, napaka=None)


 # Dokler nimate razvitega vmesnika za dodajanje uporabnikov, jih dodajte kar ročno.
#auth.dodaj_uporabnika('gasper', 'admin', 'gasper')
if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)