"""
Construccion de la base de datos SQLite del dashboard Ciclo Mundialista 2026.
Carga unicamente datos verificados en Fase C. Todo lo pendiente se deja como NULL
y se marca en la tabla `fuente` con nivel_confiabilidad = 'pendiente'.

Ejecutar: python build_db.py
Genera: mundial2026.db en el mismo directorio.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "mundial2026.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS confederacion (
    id_confederacion TEXT PRIMARY KEY,
    nombre TEXT,
    cupos_mundial_2026 INTEGER,
    formato_clasificatorio TEXT
);

CREATE TABLE IF NOT EXISTS seleccion (
    id_seleccion TEXT PRIMARY KEY,
    nombre TEXT,
    codigo_fifa TEXT,
    id_confederacion TEXT,
    modo_clasificacion TEXT,
    clasifico_mundial_2026 INTEGER,
    grupo_mundial_2026 TEXT,
    ranking_fifa_inicio_ciclo INTEGER,
    ranking_fifa_fin_ciclo INTEGER,
    entrenador_actual TEXT,
    FOREIGN KEY (id_confederacion) REFERENCES confederacion(id_confederacion)
);

CREATE TABLE IF NOT EXISTS competicion (
    id_competicion TEXT PRIMARY KEY,
    nombre TEXT,
    tipo TEXT,
    id_confederacion TEXT,
    fecha_inicio TEXT,
    fecha_fin TEXT,
    campeon TEXT,
    nivel_confiabilidad TEXT
);

CREATE TABLE IF NOT EXISTS partido (
    id_partido INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    id_competicion TEXT,
    fase TEXT,
    id_seleccion_local TEXT,
    id_seleccion_visitante TEXT,
    goles_local INTEGER,
    goles_visitante INTEGER,
    fue_penales INTEGER,
    goles_penales_local INTEGER,
    goles_penales_visitante INTEGER,
    nivel_confiabilidad TEXT,
    FOREIGN KEY (id_competicion) REFERENCES competicion(id_competicion),
    FOREIGN KEY (id_seleccion_local) REFERENCES seleccion(id_seleccion),
    FOREIGN KEY (id_seleccion_visitante) REFERENCES seleccion(id_seleccion)
);

CREATE TABLE IF NOT EXISTS fuente (
    id_fuente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_fuente TEXT,
    url TEXT,
    fecha_consulta TEXT,
    competicion_asociada TEXT,
    variable_obtenida TEXT,
    nivel_confiabilidad TEXT
);

CREATE TABLE IF NOT EXISTS dato_pendiente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bloque TEXT,
    descripcion TEXT,
    razon TEXT
);
"""

CONFEDERACIONES = [
    ("CONMEBOL", "CONMEBOL", 6, "Liguilla unica todos contra todos, 10 selecciones, 18 fechas"),
    ("UEFA", "UEFA", 16, "12 grupos de 4-5 equipos, 2 rondas, mas repechaje"),
    ("CONCACAF", "CONCACAF", 6, "3 rondas: eliminacion directa, 6 grupos de 5, 3 grupos de 4"),
    ("CAF", "CAF", 10, "9 grupos de 6 equipos, mas repechaje de 4 equipos"),
    ("AFC", "AFC", 9, "5 rondas: eliminacion directa, 9 grupos de 4, 3 grupos de 6, 2 grupos de 3, repechaje"),
    ("OFC", "OFC", 1, "3 rondas: llave a partido unico, 2 grupos de 4, llave final"),
]

# Maestro de 48 selecciones verificado en Fase C, lote 1 (corregido)
SELECCIONES = [
    # id, nombre, codigo, confederacion, modo, clasifico, grupo
    ("MEX", "Mexico", "MEX", "CONCACAF", "anfitrion", 1, "A"),
    ("USA", "Estados Unidos", "USA", "CONCACAF", "anfitrion", 1, "D"),
    ("CAN", "Canada", "CAN", "CONCACAF", "anfitrion", 1, "B"),
    ("CUW", "Curazao", "CUW", "CONCACAF", "directo", 1, "E"),
    ("HAI", "Haiti", "HAI", "CONCACAF", "directo", 1, "C"),
    ("PAN", "Panama", "PAN", "CONCACAF", "directo", 1, "L"),
    ("ARG", "Argentina", "ARG", "CONMEBOL", "directo", 1, "J"),
    ("BRA", "Brasil", "BRA", "CONMEBOL", "directo", 1, "C"),
    ("COL", "Colombia", "COL", "CONMEBOL", "directo", 1, "K"),
    ("ECU", "Ecuador", "ECU", "CONMEBOL", "directo", 1, "E"),
    ("PAR", "Paraguay", "PAR", "CONMEBOL", "directo", 1, "D"),
    ("URU", "Uruguay", "URU", "CONMEBOL", "directo", 1, "H"),
    ("GER", "Alemania", "GER", "UEFA", "directo", 1, "E"),
    ("AUT", "Austria", "AUT", "UEFA", "directo", 1, "J"),
    ("BEL", "Belgica", "BEL", "UEFA", "directo", 1, "G"),
    ("BIH", "Bosnia y Herzegovina", "BIH", "UEFA", "repechaje", 1, "B"),
    ("CRO", "Croacia", "CRO", "UEFA", "directo", 1, "L"),
    ("CZE", "Chequia", "CZE", "UEFA", "repechaje", 1, "A"),
    ("SCO", "Escocia", "SCO", "UEFA", "directo", 1, "C"),
    ("ESP", "Espana", "ESP", "UEFA", "directo", 1, "H"),
    ("FRA", "Francia", "FRA", "UEFA", "directo", 1, "I"),
    ("ENG", "Inglaterra", "ENG", "UEFA", "directo", 1, "L"),
    ("NOR", "Noruega", "NOR", "UEFA", "directo", 1, "I"),
    ("NED", "Paises Bajos", "NED", "UEFA", "directo", 1, "F"),
    ("POR", "Portugal", "POR", "UEFA", "directo", 1, "K"),
    ("SWE", "Suecia", "SWE", "UEFA", "repechaje", 1, "F"),
    ("SUI", "Suiza", "SUI", "UEFA", "directo", 1, "B"),
    ("TUR", "Turquia", "TUR", "UEFA", "repechaje", 1, "D"),
    ("ALG", "Argelia", "ALG", "CAF", "directo", 1, "J"),
    ("CPV", "Cabo Verde", "CPV", "CAF", "directo", 1, "H"),
    ("CIV", "Costa de Marfil", "CIV", "CAF", "directo", 1, "E"),
    ("EGY", "Egipto", "EGY", "CAF", "directo", 1, "G"),
    ("GHA", "Ghana", "GHA", "CAF", "directo", 1, "L"),
    ("MAR", "Marruecos", "MAR", "CAF", "directo", 1, "C"),
    ("COD", "RD Congo", "COD", "CAF", "repechaje_intercontinental", 1, "K"),
    ("SEN", "Senegal", "SEN", "CAF", "directo", 1, "I"),
    ("RSA", "Sudafrica", "RSA", "CAF", "directo", 1, "A"),
    ("TUN", "Tunez", "TUN", "CAF", "directo", 1, "F"),
    ("KSA", "Arabia Saudita", "KSA", "AFC", "directo", 1, "H"),
    ("AUS", "Australia", "AUS", "AFC", "directo", 1, "D"),
    ("QAT", "Qatar", "QAT", "AFC", "directo", 1, "B"),
    ("KOR", "Corea del Sur", "KOR", "AFC", "directo", 1, "A"),
    ("IRQ", "Irak", "IRQ", "AFC", "repechaje_intercontinental", 1, "I"),
    ("IRN", "Iran", "IRN", "AFC", "directo", 1, "G"),
    ("JPN", "Japon", "JPN", "AFC", "directo", 1, "F"),
    ("JOR", "Jordania", "JOR", "AFC", "directo", 1, "J"),
    ("UZB", "Uzbekistan", "UZB", "AFC", "directo", 1, "K"),
    ("NZL", "Nueva Zelanda", "NZL", "OFC", "directo", 1, "G"),
    # Selecciones no clasificadas, incluidas solo porque disputaron repechajes documentados
    ("JAM", "Jamaica", "JAM", "CONCACAF", "repechaje_no_clasifico", 0, None),
    ("NGA", "Nigeria", "NGA", "CAF", "repechaje_no_clasifico", 0, None),
    ("CMR", "Camerun", "CMR", "CAF", "repechaje_no_clasifico", 0, None),
    ("GAB", "Gabon", "GAB", "CAF", "repechaje_no_clasifico", 0, None),
    ("PER", "Peru", "PER", "CONMEBOL", "no_clasifico", 0, None),
    ("BOL", "Bolivia", "BOL", "CONMEBOL", "repechaje_no_clasifico", 0, None),
    ("VEN", "Venezuela", "VEN", "CONMEBOL", "no_clasifico", 0, None),
    ("CHI", "Chile", "CHI", "CONMEBOL", "no_clasifico", 0, None),
]

COMPETICIONES = [
    ("WC2026", "Copa Mundial de la FIFA 2026", "mundial", None, "2026-06-11", "2026-07-19", "ESP", "media-alta"),
    ("COPAAMERICA2024", "Copa America 2024", "torneo_confederacion", "CONMEBOL", "2024-06-20", "2024-07-14", "ARG", "media-alta"),
    ("EURO2024", "Eurocopa 2024", "torneo_confederacion", "UEFA", "2024-06-14", "2024-07-14", "ESP", "media-alta"),
    ("ASIANCUP2023", "Copa Asiatica AFC 2023", "torneo_confederacion", "AFC", "2024-01-12", "2024-02-10", "QAT", "media"),
    ("AFCON2023", "Copa Africana de Naciones 2023-24", "torneo_confederacion", "CAF", "2024-01-13", "2024-02-11", "CIV", "media"),
    ("GOLDCUP2023", "Copa Oro CONCACAF 2023", "torneo_confederacion", "CONCACAF", "2023-06-24", "2023-07-16", "MEX", "media"),
    ("GOLDCUP2025", "Copa Oro CONCACAF 2025", "torneo_confederacion", "CONCACAF", "2025-06-14", "2025-07-06", "MEX", "media-alta"),
    ("AFCON2025", "Copa Africana de Naciones 2025", "torneo_confederacion", "CAF", "2025-12-21", "2026-01-18", "MAR", "media-alta"),
    ("OFCNC2024", "OFC Nations Cup 2024", "torneo_confederacion", "OFC", None, None, "NZL", "alta"),
    ("UNL2425", "Liga de Naciones UEFA 2024-25", "torneo_confederacion", "UEFA", None, None, "POR", "media"),
    ("CNL2024", "Liga de Naciones CONCACAF 2024", "torneo_confederacion", "CONCACAF", None, None, "USA", "media"),
    ("REPECHAJE2026", "Repechaje intercontinental 2026", "repechaje", None, None, "2026-03", "IRQ / COD", "media-alta"),
    ("REPECHAJEAF2025", "Repechaje africano 2025", "repechaje", "CAF", "2025-11-16", "2025-11-17", "COD", "media-alta"),
    ("ELIM_CONMEBOL", "Eliminatoria CONMEBOL 2023-2025", "eliminatoria", "CONMEBOL", "2023-09-07", "2025-09-09", None, "media-alta"),
]

# Partidos del Mundial 2026 verificados (fase eliminatoria + hitos de Colombia)
PARTIDOS = [
    # fecha, competicion, fase, local, visitante, gl, gv, penales, gpl, gpv, confiabilidad
    ("2026-06-15", "WC2026", "grupos", "COL", "UZB", 3, 1, 0, None, None, "media-alta"),
    ("2026-06-19", "WC2026", "grupos", "COL", "COD", 1, 0, 0, None, None, "media-alta"),
    ("2026-06-23", "WC2026", "grupos", "COL", "POR", 0, 0, 0, None, None, "media-alta"),
    ("2026-06-30", "WC2026", "dieciseisavos", "COL", "GHA", 1, 0, 0, None, None, "media-alta"),
    ("2026-07-05", "WC2026", "octavos", "COL", "SUI", 0, 0, 1, 3, 4, "media-alta"),
    ("2026-07-09", "WC2026", "cuartos", "FRA", "MAR", 2, 0, 0, None, None, "media-alta"),
    ("2026-07-09", "WC2026", "cuartos", "ESP", "BEL", 1, 0, 0, None, None, "media-alta"),
    ("2026-07-10", "WC2026", "cuartos", "ENG", "NOR", 2, 1, 0, None, None, "media-alta"),
    ("2026-07-11", "WC2026", "cuartos", "ARG", "SUI", 3, 1, 0, None, None, "media-alta"),
    ("2026-07-14", "WC2026", "semifinal", "ESP", "FRA", None, None, 0, None, None, "pendiente"),
    ("2026-07-15", "WC2026", "semifinal", "ARG", "ENG", None, None, 0, None, None, "pendiente"),
    ("2026-07-18", "WC2026", "tercer_puesto", "FRA", "ENG", 4, 6, 0, None, None, "alta"),
    ("2026-07-19", "WC2026", "final", "ESP", "ARG", 1, 0, 0, None, None, "media-alta"),
    (None, "REPECHAJE2026", "repechaje_intercontinental_final", "JAM", "COD", 0, 1, 0, None, None, "media-alta"),
    ("2025-11-16", "REPECHAJEAF2025", "repechaje_semifinal", "COD", "CMR", 1, 0, 0, None, None, "media-alta"),
    ("2025-11-16", "REPECHAJEAF2025", "repechaje_semifinal", "NGA", "GAB", 4, 1, 0, None, None, "media-alta"),
    ("2025-11-17", "REPECHAJEAF2025", "repechaje_final", "COD", "NGA", 1, 1, 1, 4, 3, "media-alta"),
    # Eliminatoria CONMEBOL de Colombia, verificada partido por partido - 18 de 18 identificados
    ("2023-09-07", "ELIM_CONMEBOL", "fecha_1", "COL", "VEN", 1, 0, 0, None, None, "media-alta"),
    ("2023-09-12", "ELIM_CONMEBOL", "fecha_2", "PER", "COL", 0, 0, 0, None, None, "alta"),
    ("2023-10-12", "ELIM_CONMEBOL", "fecha_3", "COL", "URU", 2, 2, 0, None, None, "alta"),
    ("2023-10-17", "ELIM_CONMEBOL", "fecha_4", "ECU", "COL", 0, 0, 0, None, None, "alta"),
    ("2023-11-16", "ELIM_CONMEBOL", "fecha_5", "COL", "BRA", 2, 1, 0, None, None, "alta"),
    ("2023-11-21", "ELIM_CONMEBOL", "fecha_6", "PAR", "COL", 0, 1, 0, None, None, "alta"),
    ("2024-09-10", "ELIM_CONMEBOL", "fecha_8", "COL", "ARG", 2, 1, 0, None, None, "alta"),
    ("2024-10-09", "ELIM_CONMEBOL", "fecha_9", "BOL", "COL", 1, 0, 0, None, None, "alta"),
    ("2024-10-15", "ELIM_CONMEBOL", "fecha_10", "COL", "CHI", 4, 0, 0, None, None, "alta"),
    (None, "ELIM_CONMEBOL", "fecha_11", "URU", "COL", 3, 2, 0, None, None, "media-alta"),
    ("2025-03-21", "ELIM_CONMEBOL", "fecha_13", "BRA", "COL", 2, 1, 0, None, None, "alta"),
    ("2025-03-26", "ELIM_CONMEBOL", "fecha_14", "COL", "PAR", 2, 2, 0, None, None, "alta"),
    ("2025-06-06", "ELIM_CONMEBOL", "fecha_15", "COL", "PER", 0, 0, 0, None, None, "alta"),
    ("2025-06-10", "ELIM_CONMEBOL", "fecha_16", "ARG", "COL", 1, 1, 0, None, None, "alta"),
    ("2025-09-04", "ELIM_CONMEBOL", "fecha_17", "COL", "BOL", 3, 0, 0, None, None, "alta"),
    ("2025-09-09", "ELIM_CONMEBOL", "fecha_18", "VEN", "COL", 3, 6, 0, None, None, "alta"),
    (None, "ELIM_CONMEBOL", "fecha_vuelta_ecuador", "COL", "ECU", 0, 1, 0, None, None, "media-alta"),
    (None, "ELIM_CONMEBOL", "fecha_vuelta_chile", "CHI", "COL", 0, 0, 0, None, None, "media-alta"),
]

FUENTES = [
    ("Wikipedia - 2026 FIFA World Cup qualification", "en.wikipedia.org", "2026-08-16", "General", "Cupos por confederacion, formato, fechas", "media"),
    ("bracketmundial2026.com", "bracketmundial2026.com", "2026-08-16", "WC2026", "Sorteo de grupos, 48 selecciones", "media-alta"),
    ("Britannica", "britannica.com", "2026-08-16", "WC2026", "Confederaciones de origen, cruce de verificacion", "media-alta"),
    ("El Pais Cali", "elpais.com.co", "2026-08-16", "WC2026", "Recorrido completo de Colombia", "media-alta"),
    ("FIFA.com match centre", "fifa.com", "2026-08-17", "WC2026", "Resultado tercer puesto", "alta"),
    ("CNN / Telemundo", "cnnespanol.cnn.com", "2026-08-16", "WC2026", "Resultado de la final", "media-alta"),
    ("ESPN", "espndeportes.espn.com", "2026-08-17", "UEFA repechaje", "Resultados de repechaje UEFA", "media-alta"),
]

# Entrenadores confirmados por confederacion (fuente: si.com, listado de los 48 tecnicos del Mundial 2026,
# consultado el 17 de agosto de 2026, confiabilidad media-alta por ser fuente unica no cruzada)
ENTRENADORES = {
    "JPN": "Hajime Moriyasu", "KOR": "Myung-bo Hong", "IRN": "Amir Ghalenoei",
    "KSA": "Georgios Donis", "JOR": "Jamal Sellami", "QAT": "Julen Lopetegui",
    "AUS": "Tony Popovic", "UZB": "Fabio Cannavaro", "IRQ": "Graham Arnold",
    "ARG": "Lionel Scaloni", "URU": "Marcelo Bielsa", "COL": "Nestor Lorenzo",
    "BRA": "Carlo Ancelotti", "PAR": "Gustavo Alfaro", "ECU": "Sebastian Beccacece",
    "AUT": "Ralf Rangnick", "BEL": "Rudi Garcia", "CRO": "Zlatko Dalic",
    "ENG": "Thomas Tuchel", "FRA": "Didier Deschamps", "GER": "Julian Nagelsmann",
    "NED": "Ronald Koeman", "NOR": "Stale Solbakken", "POR": "Roberto Martinez",
    "ESP": "Luis de la Fuente", "SCO": "Steve Clarke", "SUI": "Murat Yakin",
    "BIH": "Sergej Barbarez", "CZE": "Miroslav Koubek", "TUR": "Vincenzo Montella",
    "SWE": "Graham Potter", "EGY": "Hossam Hassan", "ALG": "Vladimir Petkovic",
    "TUN": "Herve Renard", "CIV": "Emerse Fae", "SEN": "Aliou Cisse",
    "GHA": None, "MAR": "Mohamed Ouahbi", "RSA": "Hugo Broos",
    "CPV": "Pedro Leitao Brito (Bubista)", "COD": "Sebastien Desabre",
    "NZL": "Darren Bazeley", "USA": "Mauricio Pochettino", "MEX": "Javier Aguirre",
    "CAN": "Jesse Marsch", "HAI": "Sebastien Migne", "CUW": "Dick Advocaat",
    "PAN": "Thomas Christiansen Tarin",
}

# Top 10 del ranking FIFA post-Mundial 2026 (fuente: TUDN, consultado 17 de agosto de 2026,
# confiabilidad media-alta; posiciones 11-48 quedan pendientes)
RANKING_FIN_CICLO_TOP10 = {
    "ESP": 1, "ARG": 2, "FRA": 3, "ENG": 4, "BRA": 5,
    "MAR": 6, "POR": 7, "BEL": 8, "NED": 9, "MEX": 10,
}

DATOS_PENDIENTES = [
    ("CONMEBOL eliminatoria Colombia - detalles menores", "Fecha exacta de 3 de los 18 partidos (Uruguay fecha 11, vuelta Ecuador, vuelta Chile) y localia exacta de la fecha 1 ante Venezuela", "Marcador y rival confirmados con 2+ fuentes; solo falta precisar fecha/localia exacta"),
    ("Mundial 2026 semifinales", "Marcador exacto de Espana-Francia y Argentina-Inglaterra", "Solo se confirmo el resultado cualitativo (quien avanzo)"),
    ("Eliminatorias CAF/AFC/CONCACAF/OFC", "Tablas de posiciones completas de selecciones no clasificadas", "Fuera de alcance manual verificado en esta fase"),
    ("Liga de Naciones UEFA 2024-25", "Marcador exacto de la final Portugal-Espana", "Campeon confirmado, marcador exacto no verificado"),
    ("Entrenador de Ghana", "Nombre del tecnico actual de Ghana", "No confirmado en la fuente consultada (aparece como 'por confirmar')"),
    ("Ranking FIFA posiciones 11-48", "Ranking FIFA fin de ciclo de las selecciones fuera del top 10, y ranking de inicio de ciclo (sept 2023) de las 48", "Solo se obtuvo el top 10 post-Mundial en esta fase"),
    ("Estadisticas colectivas e individuales", "Goles, tiros, posesion, xG, y estadisticas de jugadores", "No recopilado en esta fase; requiere fuente estructurada"),
]


def build():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(SCHEMA)

    cur.executemany(
        "INSERT INTO confederacion VALUES (?,?,?,?)", CONFEDERACIONES
    )
    cur.executemany(
        "INSERT INTO seleccion (id_seleccion,nombre,codigo_fifa,id_confederacion,modo_clasificacion,"
        "clasifico_mundial_2026,grupo_mundial_2026) VALUES (?,?,?,?,?,?,?)",
        SELECCIONES,
    )
    cur.executemany(
        "INSERT INTO competicion VALUES (?,?,?,?,?,?,?,?)", COMPETICIONES
    )
    cur.executemany(
        "INSERT INTO partido (fecha,id_competicion,fase,id_seleccion_local,id_seleccion_visitante,"
        "goles_local,goles_visitante,fue_penales,goles_penales_local,goles_penales_visitante,nivel_confiabilidad) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        PARTIDOS,
    )
    cur.executemany(
        "INSERT INTO fuente (nombre_fuente,url,fecha_consulta,competicion_asociada,variable_obtenida,nivel_confiabilidad) "
        "VALUES (?,?,?,?,?,?)",
        FUENTES,
    )
    cur.executemany(
        "INSERT INTO dato_pendiente (bloque,descripcion,razon) VALUES (?,?,?)", DATOS_PENDIENTES
    )

    for id_sel, entrenador in ENTRENADORES.items():
        cur.execute(
            "UPDATE seleccion SET entrenador_actual = ? WHERE id_seleccion = ?",
            (entrenador, id_sel),
        )
    for id_sel, pos in RANKING_FIN_CICLO_TOP10.items():
        cur.execute(
            "UPDATE seleccion SET ranking_fifa_fin_ciclo = ? WHERE id_seleccion = ?",
            (pos, id_sel),
        )

    conn.commit()
    conn.close()
    print(f"Base de datos creada en {DB_PATH}")
    print(f"{len(SELECCIONES)} selecciones, {len(PARTIDOS)} partidos, {len(COMPETICIONES)} competiciones cargadas.")


if __name__ == "__main__":
    build()
