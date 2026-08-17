"""
Fase F: Validacion final / control de calidad sobre mundial2026.db
Ejecutar: python validar_calidad.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "mundial2026.db")


def run():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    hallazgos = []

    # 1. Selecciones duplicadas por nombre
    cur.execute("SELECT nombre, COUNT(*) c FROM seleccion GROUP BY nombre HAVING c > 1")
    dup_sel = cur.fetchall()
    hallazgos.append(("Selecciones duplicadas por nombre", len(dup_sel), dup_sel))

    # 2. Total de selecciones cargadas vs 48 esperadas
    cur.execute("SELECT COUNT(*) FROM seleccion WHERE clasifico_mundial_2026 = 1")
    total_sel = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM seleccion WHERE clasifico_mundial_2026 = 0")
    total_no_clasif = cur.fetchone()[0]
    hallazgos.append(("Selecciones clasificadas cargadas (esperado 48)", total_sel, "OK" if total_sel == 48 else "REVISAR"))
    hallazgos.append(("Selecciones no clasificadas cargadas (contexto, ej. Jamaica)", total_no_clasif, "informativo"))

    # 3. Selecciones por confederacion vs cupos declarados
    cur.execute("""
        SELECT c.id_confederacion, c.cupos_mundial_2026, COUNT(s.id_seleccion) as cargadas
        FROM confederacion c LEFT JOIN seleccion s
          ON c.id_confederacion = s.id_confederacion AND s.clasifico_mundial_2026 = 1
        GROUP BY c.id_confederacion
    """)
    conf_check = cur.fetchall()
    inconsistentes = [r for r in conf_check if r[1] != r[2]]
    hallazgos.append(("Confederaciones con cupos declarados != selecciones cargadas", len(inconsistentes), inconsistentes))

    # 4. Partidos con marcador nulo pero marcados como no pendientes (inconsistencia)
    cur.execute("""
        SELECT id_partido, fecha, id_seleccion_local, id_seleccion_visitante, nivel_confiabilidad
        FROM partido
        WHERE (goles_local IS NULL OR goles_visitante IS NULL) AND nivel_confiabilidad != 'pendiente'
    """)
    marcador_faltante = cur.fetchall()
    hallazgos.append(("Partidos sin marcador pero NO marcados como pendientes (inconsistencia)", len(marcador_faltante), marcador_faltante))

    # 5. Partidos duplicados exactos (misma fecha, mismos equipos)
    cur.execute("""
        SELECT fecha, id_seleccion_local, id_seleccion_visitante, COUNT(*) c
        FROM partido GROUP BY fecha, id_seleccion_local, id_seleccion_visitante HAVING c > 1
    """)
    dup_partidos = cur.fetchall()
    hallazgos.append(("Partidos duplicados (misma fecha y mismos equipos)", len(dup_partidos), dup_partidos))

    # 6. Partidos con selecciones inexistentes en el maestro (integridad referencial)
    cur.execute("""
        SELECT p.id_partido FROM partido p
        WHERE p.id_seleccion_local NOT IN (SELECT id_seleccion FROM seleccion)
           OR p.id_seleccion_visitante NOT IN (SELECT id_seleccion FROM seleccion)
    """)
    huerfanos = cur.fetchall()
    hallazgos.append(("Partidos con selecciones no registradas en el maestro", len(huerfanos), huerfanos))

    # 7. Coherencia de goles en penales: fue_penales=1 exige empate en marcador reglamentario
    cur.execute("""
        SELECT id_partido, goles_local, goles_visitante, fue_penales FROM partido
        WHERE fue_penales = 1 AND goles_local != goles_visitante
    """)
    penales_inconsistentes = cur.fetchall()
    hallazgos.append(("Partidos marcados con penales pero sin empate en el resultado", len(penales_inconsistentes), penales_inconsistentes))

    # 8. Suma de goles de Colombia en el Mundial vs balance reportado (3-0 en contra... validar 5 GF / 1 GC)
    cur.execute("""
        SELECT
          SUM(CASE WHEN id_seleccion_local='COL' THEN goles_local ELSE goles_visitante END) as gf,
          SUM(CASE WHEN id_seleccion_local='COL' THEN goles_visitante ELSE goles_local END) as gc
        FROM partido WHERE (id_seleccion_local='COL' OR id_seleccion_visitante='COL') AND id_competicion='WC2026'
    """)
    gf, gc = cur.fetchone()
    hallazgos.append(("Goles de Colombia en Mundial 2026 (esperado GF=5, GC=1)", f"GF={gf}, GC={gc}", "OK" if (gf == 5 and gc == 1) else "REVISAR"))

    # 9. Registros de fuente sin URL
    cur.execute("SELECT nombre_fuente FROM fuente WHERE url IS NULL OR url = ''")
    fuentes_sin_url = cur.fetchall()
    hallazgos.append(("Fuentes registradas sin URL", len(fuentes_sin_url), fuentes_sin_url))

    conn.close()

    print("=" * 70)
    print("INFORME DE VALIDACION - FASE F")
    print("=" * 70)
    for nombre, resultado, detalle in hallazgos:
        print(f"\n- {nombre}: {resultado}")
        if isinstance(detalle, list) and detalle:
            for d in detalle:
                print(f"    {d}")

    return hallazgos


if __name__ == "__main__":
    run()
