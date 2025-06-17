import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

import Data.auth as auth
from Data.models import *
from typing import List, Optional
import os

DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

class Repo:
    def __init__(self):
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.conn.set_client_encoding('UTF8')
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        
        
    # ------------------- POT_GORA -------------------

def dobi_poti(self) -> List[Pot_Gora]:
        self.cur.execute("""
            SELECT * FROM poti_gora ORDER BY id
        """)
        return [Pot_Gora(**p) for p in self.cur.fetchall()]

def dobi_pot(self, id: int) -> Optional[Pot_Gora]:
        self.cur.execute("""
            SELECT * FROM poti_gora WHERE id = %s
        """, (id,))
        row = self.cur.fetchone()
        return Pot_Gora(**row) if row else None

def dodaj_pot(self, p: Pot_Gora):
        self.cur.execute("""
            INSERT INTO poti_gora (id, mountain_id, route_name, route_time, route_difficulty,
                start_point, height_diff, gear_summer, gear_winter)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            p.id, p.mountain_id, p.route_name, p.route_time, p.route_difficulty,
            p.start_point, p.height_diff, p.gear_summer, p.gear_winter
        ))
        self.conn.commit()

def posodobi_pot(self, p: Pot_Gora):
        self.cur.execute("""
            UPDATE poti_gora SET
                mountain_id = %s, route_name = %s, route_time = %s, route_difficulty = %s,
                start_point = %s, height_diff = %s, gear_summer = %s, gear_winter = %s
            WHERE id = %s
        """, (
            p.mountain_id, p.route_name, p.route_time, p.route_difficulty,
            p.start_point, p.height_diff, p.gear_summer, p.gear_winter, p.id
        ))
        self.conn.commit()

def izbrisi_pot(self, id: int):
        self.cur.execute("""
            DELETE FROM poti_gora WHERE id = %s
        """, (id,))
        self.conn.commit()
