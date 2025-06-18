import datetime
from functools import wraps
from Presentation.bottleext import route, get, post, run, request, template, redirect, static_file, url, response, template_user, HTTPResponse

from Services.pohodi_service import PohodiService
from Services.poti_service import PotiService
from Services.auth_service import AuthService
from Services.gore_service import GoraService
import os

import traceback

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
    
    uporabnisko_ime = request.get_cookie("uporabnisko_ime", secret="skrivnost")
    # prijave = auth.pridobi_prijave_uporabnika(uporabnisko_ime)
    # for prijava in prijave:
    #     print(prijava)               # izpiše celoten DictRow
    #     print(prijava.keys())
    flash_msg = request.get_cookie("flash_msg", secret="skrivnost")
    response.delete_cookie("flash_msg")
    pohodi = pohodiService.dobi_pohode_dto() 

    return template_user('pohodi.html', pohodi = pohodi, uporabnisko_ime=uporabnisko_ime, flash_msg=flash_msg)

@get('/poti')
# @cookie_required
def poti():
    """
    Poti
    """   
    uporabnisko_ime = request.get_cookie("uporabnisko_ime", secret="skrivnost")
    poti = potiService.dobi_poti_dto() 

    return template_user('poti.html', poti = poti, uporabnisko_ime=uporabnisko_ime)


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

@route('/registracija')
def registracija_get():
    return template('registracija', napaka=None)

@post('/registracija')
def registracija_post():
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    uporabnisko_ime = request.forms.get('username')
    password = request.forms.get('password')
    telefon = request.forms.get('telefon')
    email = request.forms.get('email')

    # preveri, če uporabnik že obstaja
    if auth.obstaja_uporabnik(uporabnisko_ime):
        return template('registracija', napaka="Uporabniško ime že obstaja. Izberi drugo.")

    # dodaj uporabnika (ustvari hash in shrani v bazo)
    try:
        auth.dodaj_uporabnika(ime, priimek, uporabnisko_ime, password, telefon, email)
        # po uspešni registraciji preusmeri na prijavo
        
    except Exception as e:
    
        print("Napaka pri registraciji:", e)
        traceback.print_exc()
        return template('registracija', napaka=f"Napaka pri registraciji: {e}")
    
    redirect(url('/odjava'))



@post('/prijava')
def prijava():
    

    username = request.forms.get('username')
    password = request.forms.get('password')

    if not auth.obstaja_uporabnik(username):
        return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja", rola=None, uporabnik=None)

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnisko_ime", username, secret="skrivnost")
        response.set_cookie("rola", getattr(prijava, 'role', 'uporabnik'))  # če nimaš role, privzeto uporabnik
        redirect(url('/'))
    else:
        return template("prijava.html", napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.", uporabnik=None, rola=None)


@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """
  
    response.delete_cookie("uporabnik")
    response.delete_cookie("rola")
  
    return template('prijava.html', uporabnik=None, rola=None, napaka=None) 

# @route('/prijavi_na_pohod/<pohod_id:int>', method='POST')
# def prijava_na_pohod(pohod_id):
#     # Tukaj predpostavljamo, da imaš nek mehanizem za prijavo uporabnika, 
#     # ki shrani uporabnikov id v cookie ali session
#     uporabnik_id = request.get_cookie("uporabnik_id", secret='tvoj_secret_kljuc')
    
#     if not uporabnik_id:
#         response.status = 401
#         return {"napaka": "Uporabnik ni prijavljen"}

#     try:
#         pohodiService.prijavi_uporabnika_na_pohod(int(uporabnik_id), pohod_id)
#         return {"sporocilo": "Uspešno prijavljen na pohod"}
#     except Exception as e:
#         response.status = 400
#         return {"napaka": str(e)}
    
    
# @route('/pohodi')
# def prikazi_pohode():
#     flash_msg = request.get_cookie("flash_msg", secret="skrivnost")
#     if flash_msg:
#         response.set_cookie("flash_msg", "", expires=0)  # počisti cookie

#     pohodi = pohodiService.dobi_pohode_dto()
#     return template('pohodi', pohodi=pohodi, flash_msg=flash_msg)


@route('/pohodi')
def prikazi_pohode():
    pohodi = pohodiService.dobi_pohode_dto()

    # preberi flash sporočilo in ga takoj zbriši
    flash_msg = request.get_cookie("flash_msg", secret="skrivnost")
    if flash_msg:
        response.delete_cookie("flash_msg", path='/')
    else:
        flash_msg = None
    # Pridobi uporabnikove prijave na pohode
    uporabnisko_ime = request.get_cookie("uporabnisko_ime", secret="skrivnost")
    prijave = []
    if uporabnisko_ime:
        uporabnik_id = auth.dobi_id_uporabnika(uporabnisko_ime)
        if uporabnik_id:
            prijave = pohodiService.dobi_prijave_uporabnika(uporabnik_id)  # vrne seznam prijav

    return template('pohodi', pohodi=pohodi, flash_msg=flash_msg, prijave=prijave, uporabnisko_ime=uporabnisko_ime)


@post('/prijava_na_pohod')
def prijava_na_pohod():
    pohod_id = request.forms.get('pohod_id')

    # Pridobi uporabniško ime iz piškotka
    uporabnisko_ime = request.get_cookie("uporabnisko_ime", secret="skrivnost")
    print("Uporabnisko ime:", uporabnisko_ime)
    if not uporabnisko_ime:
        return template('napaka', sporocilo='Najprej se moraš prijaviti.')

    # Poskusi pridobiti ID uporabnika iz baze na podlagi uporabniškega imena
    try:
        uporabnik_id = auth.dobi_id_uporabnika(uporabnisko_ime)
        print("Uporabnik ID:", uporabnik_id)
        if uporabnik_id is None:
            return template('napaka', sporocilo='Uporabnik ne obstaja.')

        # pohodiService.prijavi_uporabnika_na_pohod(int(uporabnik_id), int(pohod_id))
        
        # pohodni_podrobnosti = pohodiService.dobi_pohode_dto(int(pohod_id))  # recimo ime poti
        # ime_poti = pohodni_podrobnosti.ime
        print(f"Uporabnik {uporabnisko_ime} uspešno prijavljen na pohod {pohod_id}")
        print("Pred redirect")
        response.set_cookie("flash_msg", f"Uspešno prijavljeni na pohod.", secret="skrivnost")
        return redirect('/')
    except HTTPResponse:
        # redirect vrže exception, ki ga pustimo mimo
        raise    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return template('napaka', sporocilo='Napaka pri prijavi: ' + str(e))

@get('/moje_prijave')
def moje_prijave():
    uporabnisko_ime = request.get_cookie("uporabnisko_ime", secret="skrivnost")
    if not uporabnisko_ime:
        return template('napaka', sporocilo='Najprej se moraš prijaviti.')

    prijave = auth.pridobi_prijave_uporabnika(uporabnisko_ime)

    return template_user('moje_prijave.html', prijave=prijave, uporabnisko_ime=uporabnisko_ime)

# @post('/odjava_na_pohod')
# def odjava_na_pohod():
#     prijava_id = request.forms.get('prijava_id')

#     uporabnisko_ime = request.get_cookie("uporabnisko_ime", secret="skrivnost")
#     if not uporabnisko_ime:
#         return template('napaka', sporocilo='Najprej se moraš prijaviti.')

#     uporabnik_id = auth.dobi_id_uporabnika(uporabnisko_ime)
#     if not uporabnik_id:
#         return template('napaka', sporocilo='Uporabnik ne obstaja.')

#     try:
#         pohodiService.odjavi_uporabnika_od_pohoda(prijava_id, uporabnik_id)
#         response.set_cookie("flash_msg", "Uspešno ste se odjavili od pohoda.", secret="skrivnost", path='/')
#         return redirect('/pohodi')

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return template('napaka', sporocilo='Napaka pri odjavi: ' + str(e))
    

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


# # registracija novega uporabnika
# auth.dodaj_uporabnika("Test", "Test", "testuser", "testpass", "041234567", "test@example.com")

# # prijava z istim uporabnikom
# rezultat = auth.prijavi_uporabnika("testuser", "testpass")
# print("Rezultat prijave:", rezultat)




#Dokler nimate razvitega vmesnika za dodajanje uporabnikov, jih dodajte kar ročno.
#auth.dodaj_uporabnika('eva', 'admin', 'eva')
if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)
    
    