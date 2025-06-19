import datetime
from functools import wraps
from Presentation.bottleext import route, get, post, run, request, template, redirect, static_file, url, response, template_user, HTTPResponse

from Services.pohodi_service import PohodiService
from Services.poti_service import PotiService
from Services.auth_service import AuthService
from Services.gore_service import GoraService
from Services.poti_nova_service import GoraPotService
import os

import traceback

# Ustvarimo instance servisov, ki jih potrebujemo. 
# Če je število servisov veliko, potem je service bolj smiselno inicializirati v metodi in na
# začetku datoteke (saj ne rabimo vseh servisov v vseh metodah!)

pohodiService = PohodiService()
potiService = PotiService()
auth = AuthService()
goreService = GoraService()
nove_potiService = GoraPotService()

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


@get('/nove_poti')
# @cookie_required
def nove_poti():
    """
    Stran z novimi potmi
    """   
    izbrana_gora = request.query.get('gora')  

    vse_nove_poti = nove_potiService.dobi_poti()
    seznam_gor = goreService.pridobi_vse_gore() 
    uporabnisko_ime=request.get_cookie("uporabnisko_ime", secret="skrivnost") 

    # če uporabnik izbere goro po imenu, poišči ustrezen id
    if not izbrana_gora and seznam_gor:
        izbrana_gora = seznam_gor[0].name
    if izbrana_gora:
        gor_ids = [g.mountain_id for g in seznam_gor if g.name == izbrana_gora]
        if gor_ids:
            vse_nove_poti = [p for p in vse_nove_poti if p.mountain_id == gor_ids[0]]

    stran = int(request.query.get('page', '1'))
    velikost_strani = 20
    zacetek = (stran - 1) * velikost_strani
    konec = zacetek + velikost_strani
    trenutne_poti = vse_nove_poti[zacetek:konec]
    st_strani = (len(vse_nove_poti) + velikost_strani - 1) // velikost_strani


    return template_user('nove_poti.html', nove_poti=trenutne_poti, stran=stran, st_strani=st_strani, 
                         uporabnisko_ime=uporabnisko_ime, seznam_gor=seznam_gor,izbrana_gora=izbrana_gora)




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
    
    # Force UTF-8 decoding
    raw_body = request.body.read()
    decoded_body = raw_body.decode('utf-8')
    
    from urllib.parse import parse_qs
    form_data = parse_qs(decoded_body)

    ime = form_data.get('ime', [''])[0]
    zahtevnost = form_data.get('zahtevnost', [''])[0]
    zacetna_lokacija = form_data.get('zacetna_lokacija', [''])[0]
    trajanje_ur = float(form_data.get('trajanje_ur', [0])[0])
    visinska_razlika_m = float(form_data.get('visinska_razlika_m', [0])[0])
    opis = form_data.get('opis', [''])[0]
    lokacija = form_data.get('lokacija', [''])[0]
    
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

@post('/odstrani_pohod')
def odstrani_pohod():
    id = int(request.forms.get('id'))
    pohodiService.odstrani_pohod(id)
    redirect(url('/pohodi'))

@post('/uredi_pot')
def uredi_pot_post():
    from urllib.parse import parse_qs

    # Preberi telo zahteve kot UTF-8
    raw_body = request.body.read()
    decoded_body = raw_body.decode('utf-8')

    # Parsiraj parametre iz obrazca
    form_data = parse_qs(decoded_body)

    id = int(form_data.get('id', [''])[0])
    ime = form_data.get('ime', [''])[0]
    zahtevnost = form_data.get('zahtevnost', [''])[0]
    zacetna_lokacija = form_data.get('zacetna_lokacija', [''])[0]
    trajanje_ur = float(form_data.get('trajanje_ur', [0])[0])
    visinska_razlika_m = float(form_data.get('visinska_razlika_m', [0])[0])
    opis = form_data.get('opis', [''])[0]
    lokacija = form_data.get('lokacija', [''])[0]

    print("IME:", ime)
    print("LOKACIJA:", lokacija)

    potiService.posodobi_pot(id, ime, zacetna_lokacija, zahtevnost, trajanje_ur,
                             visinska_razlika_m, opis, lokacija)
    
    redirect(url('/poti'))

@post('/odstrani_pot')
def odstrani_pot():
    id = int(request.forms.get('id'))
    potiService.odstrani_pot(id)
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
        response.set_cookie("uporabnisko_ime", username, secret="skrivnost", path='/')
        response.set_cookie("rola", getattr(prijava, 'role', 'uporabnik'), path='/')  # če nimaš role, privzeto uporabnik
        redirect(url('/'))
    else:
        return template("prijava.html", napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.", uporabnik=None, rola=None)


@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """
  
    response.delete_cookie("uporabnisko_ime", path='/')
    response.delete_cookie("rola", path='/')
    
    #redirect('/odjava')
    return template('prijava.html', uporabnik=None, rola=None, napaka=None) 



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
    #    uporabnik_id = auth.dobi_id_uporabnika(uporabnisko_ime)
    #    if uporabnik_id:
        prijave = auth.pridobi_prijave_uporabnika(uporabnisko_ime)  # vrne seznam prijav

    return template('pohodi', pohodi=pohodi, flash_msg=flash_msg, prijave=prijave, rola=None, uporabnisko_ime=uporabnisko_ime)


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

        pohodiService.prijavi_uporabnika_na_pohod(int(uporabnik_id), int(pohod_id))
        
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
    flash_msg = request.get_cookie("flash_msg", secret="skrivnost")
    
    # Če obstaja, ga pobriši
    if flash_msg:
        response.delete_cookie("flash_msg", path="/")
    uporabnisko_ime = request.get_cookie("uporabnisko_ime", secret="skrivnost")
    if not uporabnisko_ime:
        return template('napaka', sporocilo='Najprej se moraš prijaviti.')

    prijave = auth.pridobi_prijave_uporabnika(uporabnisko_ime)

    return template_user('moje_prijave.html', prijave=prijave, uporabnisko_ime=uporabnisko_ime, flash_msg=flash_msg)



@post('/odjava_na_pohod')
def odjava_na_pohod():
    pohod_id = request.forms.get('pohod_id')

    uporabnisko_ime = request.get_cookie("uporabnisko_ime", secret="skrivnost")
    if not uporabnisko_ime:
        return template('napaka', sporocilo='Najprej se moraš prijaviti.')

    uporabnik_id = auth.dobi_id_uporabnika(uporabnisko_ime)
    if not uporabnik_id:
        return template('napaka', sporocilo='Uporabnik ne obstaja.')

    try:
        auth.odjavi_uporabnika_od_pohoda(pohod_id, uporabnik_id)
        response.set_cookie("flash_msg", "Uspešno ste se odjavili od pohoda.", secret="skrivnost", path='/')
        return redirect('/moje_prijave')
    except HTTPResponse:
        # redirect vrže exception, ki ga pustimo mimo
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        return template('napaka', sporocilo='Napaka pri odjavi: ' + str(e))
    

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
    
    