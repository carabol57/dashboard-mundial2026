"""
Dashboard Ciclo Mundialista 2026
Realizado por sportsamc.com
Desarrollado por Andres Mauricio Carabali

Ejecutar con: streamlit run app.py
"""
import sqlite3
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "mundial2026.db")

# Si la base de datos no existe (por ejemplo, en un despliegue nuevo en la nube
# donde solo se sube el codigo fuente), se construye automaticamente desde build_db.py
if not os.path.exists(DB_PATH):
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "data"))
    import build_db
    build_db.build()

st.set_page_config(page_title="Ciclo Mundialista 2026", layout="wide", page_icon="⚽")

COLOR_PRIMARIO = "#1b3a5c"
COLOR_ACENTO = "#c8a44d"
COLOR_ALERTA = "#b23b3b"


@st.cache_resource
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def q(sql, params=()):
    return pd.read_sql_query(sql, get_conn(), params=params)


def footer():
    st.markdown("---")
    st.caption("Realizado por sportsamc.com · Desarrollado por Andres Mauricio Carabali")


def badge_confiabilidad(nivel):
    colores = {"alta": "🟢", "media-alta": "🟡", "media": "🟠", "pendiente": "🔴"}
    return colores.get(nivel, "⚪") + " " + (nivel or "sin dato")


# ---------------------------------------------------------------------------
# Sidebar: filtros globales
# ---------------------------------------------------------------------------
st.sidebar.title("⚽ Ciclo Mundialista 2026")
pagina = st.sidebar.radio(
    "Navegación",
    [
        "1. Resumen mundialista",
        "2. Confederaciones",
        "3. Selección",
        "4. Jugadores",
        "5. Mundial 2026",
        "6. Comparador",
        "Fuentes y metodología",
    ],
)

selecciones_df = q("""
    SELECT s.*, c.nombre AS confederacion_nombre
    FROM seleccion s JOIN confederacion c ON s.id_confederacion = c.id_confederacion
""")

st.sidebar.markdown("---")
conf_filtro = st.sidebar.multiselect(
    "Filtrar por confederación",
    sorted(selecciones_df["confederacion_nombre"].unique()),
    default=None,
)
sel_filtradas = selecciones_df if not conf_filtro else selecciones_df[
    selecciones_df["confederacion_nombre"].isin(conf_filtro)
]

# ---------------------------------------------------------------------------
# Página 1: Resumen mundialista
# ---------------------------------------------------------------------------
if pagina.startswith("1"):
    st.title("Resumen mundialista")
    st.caption("Ciclo 2023-2026 · Datos verificados en Fase C, con bloques pendientes señalados explícitamente")

    partidos = q("SELECT * FROM partido")
    partidos_verificados = partidos[partidos["nivel_confiabilidad"] != "pendiente"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Selecciones clasificadas Mundial 2026", len(selecciones_df))
    c2.metric("Confederaciones", selecciones_df["id_confederacion"].nunique())
    c3.metric("Partidos cargados y verificados", len(partidos_verificados))
    c4.metric("Campeón del ciclo", "España 🏆")

    st.info(
        "Este resumen refleja únicamente lo verificado en Fase C. Estadísticas colectivas "
        "(goles totales, promedio de goles, xG) y rankings de jugadores no están cargados aún: "
        "requieren la fuente de datos estructurada descrita en 'Fuentes y metodología'.",
        icon="⚠️",
    )

    st.subheader("Selecciones por confederación")
    fig = px.bar(
        selecciones_df.groupby("confederacion_nombre").size().reset_index(name="selecciones"),
        x="confederacion_nombre", y="selecciones", color="confederacion_nombre",
        color_discrete_sequence=px.colors.qualitative.Prism,
        labels={"confederacion_nombre": "Confederación", "selecciones": "Selecciones clasificadas"},
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Caso destacado verificado: recorrido de Colombia")
    col_partidos = partidos[
        (partidos["id_seleccion_local"] == "COL") | (partidos["id_seleccion_visitante"] == "COL")
    ]
    st.dataframe(col_partidos[[
        "fecha", "fase", "id_seleccion_local", "goles_local", "goles_visitante",
        "id_seleccion_visitante", "fue_penales", "nivel_confiabilidad"
    ]], use_container_width=True, hide_index=True)

    footer()

# ---------------------------------------------------------------------------
# Página 2: Confederaciones
# ---------------------------------------------------------------------------
elif pagina.startswith("2"):
    st.title("Confederaciones")
    conf_sel = st.selectbox("Selecciona una confederación", sorted(selecciones_df["confederacion_nombre"].unique()))

    conf_info = q("SELECT * FROM confederacion WHERE id_confederacion = ?", (conf_sel,))
    if not conf_info.empty:
        st.markdown(f"**Cupos Mundial 2026:** {conf_info.iloc[0]['cupos_mundial_2026']}")
        st.markdown(f"**Formato clasificatorio:** {conf_info.iloc[0]['formato_clasificatorio']}")

    tabla = selecciones_df[selecciones_df["id_confederacion"] == conf_sel][
        ["nombre", "modo_clasificacion", "grupo_mundial_2026"]
    ].rename(columns={"nombre": "Selección", "modo_clasificacion": "Modo de clasificación", "grupo_mundial_2026": "Grupo Mundial 2026"})
    st.dataframe(tabla, use_container_width=True, hide_index=True)

    st.info(
        "Ranking comparativo de selecciones dentro de la confederación pendiente de carga "
        "de estadísticas colectivas (ver Fuentes y metodología).", icon="⚠️"
    )
    footer()

# ---------------------------------------------------------------------------
# Página 3: Selección
# ---------------------------------------------------------------------------
elif pagina.startswith("3"):
    st.title("Perfil de selección")
    sel_id = st.selectbox(
        "Selecciona una selección",
        selecciones_df.sort_values("nombre")["id_seleccion"],
        format_func=lambda x: selecciones_df.set_index("id_seleccion").loc[x, "nombre"],
    )
    row = selecciones_df.set_index("id_seleccion").loc[sel_id]
    st.subheader(row["nombre"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Confederación", row["confederacion_nombre"])
    c2.metric("Modo de clasificación", row["modo_clasificacion"])
    c3.metric("Grupo Mundial 2026", row["grupo_mundial_2026"])

    c4, c5 = st.columns(2)
    entrenador = row.get("entrenador_actual")
    c4.metric("Entrenador actual", entrenador if pd.notna(entrenador) else "Pendiente de confirmar")
    ranking = row.get("ranking_fifa_fin_ciclo")
    c5.metric("Ranking FIFA (fin de ciclo)", int(ranking) if pd.notna(ranking) else "Pendiente")

    partidos = q(
        "SELECT * FROM partido WHERE id_seleccion_local = ? OR id_seleccion_visitante = ? ORDER BY fecha",
        (sel_id, sel_id),
    )
    st.subheader("Calendario y resultados cargados")
    if partidos.empty:
        st.warning("No hay partidos cargados todavía para esta selección (dato pendiente de Fase C).")
    else:
        st.dataframe(partidos[[
            "fecha", "fase", "id_seleccion_local", "goles_local", "goles_visitante",
            "id_seleccion_visitante", "nivel_confiabilidad"
        ]], use_container_width=True, hide_index=True)

    st.subheader("Análisis técnico")
    if sel_id == "COL":
        st.markdown(
            "**Fortaleza observada:** solidez defensiva en el Mundial 2026, un solo gol recibido en cinco "
            "partidos. **Dato observado, no causal:** la eliminación se dio en definición por penales tras "
            "0-0 en tiempo reglamentario y prórroga ante Suiza, no por inferioridad futbolística en el "
            "desarrollo del partido. **Debilidad no verificable aún:** eficiencia ofensiva y dependencia de "
            "jugadores puntuales requieren las estadísticas individuales, todavía no cargadas."
        )
    else:
        st.info("Análisis técnico disponible solo para selecciones con datos de partido cargados (Colombia, por ahora).")

    footer()

# ---------------------------------------------------------------------------
# Página 4: Jugadores
# ---------------------------------------------------------------------------
elif pagina.startswith("4"):
    st.title("Jugadores")
    st.warning(
        "Módulo de jugadores sin datos cargados todavía. El modelo de datos (Fase B) contempla la tabla "
        "completa de estadísticas individuales para las 48 selecciones clasificadas, pero su carga requiere "
        "una fuente estructurada (API o exportación oficial), pendiente de aprobación por costo. "
        "Esta página queda lista a nivel de estructura para recibir esos datos sin rediseñar el dashboard.",
        icon="⚠️",
    )
    st.dataframe(pd.DataFrame(columns=[
        "Jugador", "Selección", "Posición", "Partidos", "Goles", "Asistencias", "xG", "xA"
    ]), use_container_width=True, hide_index=True)
    footer()

# ---------------------------------------------------------------------------
# Página 5: Mundial 2026
# ---------------------------------------------------------------------------
elif pagina.startswith("5"):
    st.title("Copa Mundial de la FIFA 2026")
    partidos = q("SELECT * FROM partido WHERE id_competicion = 'WC2026' ORDER BY fecha")

    fases_orden = ["grupos", "dieciseisavos", "octavos", "cuartos", "semifinal", "tercer_puesto", "final"]
    fase_sel = st.selectbox("Fase", fases_orden)
    st.dataframe(
        partidos[partidos["fase"] == fase_sel][[
            "fecha", "id_seleccion_local", "goles_local", "goles_visitante",
            "id_seleccion_visitante", "fue_penales", "nivel_confiabilidad"
        ]],
        use_container_width=True, hide_index=True,
    )

    st.subheader("Resultado final del torneo")
    st.success("Campeón: España · Subcampeón: Argentina · Tercer puesto: Inglaterra (venció a Francia 6-4)")

    st.subheader("Evolución partido a partido de Colombia")
    col = partidos[(partidos["id_seleccion_local"] == "COL") | (partidos["id_seleccion_visitante"] == "COL")].copy()
    col["goles_colombia"] = col.apply(
        lambda r: r["goles_local"] if r["id_seleccion_local"] == "COL" else r["goles_visitante"], axis=1
    )
    col["goles_rival"] = col.apply(
        lambda r: r["goles_visitante"] if r["id_seleccion_local"] == "COL" else r["goles_local"], axis=1
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=col["fase"], y=col["goles_colombia"], mode="lines+markers", name="Goles Colombia"))
    fig.add_trace(go.Scatter(x=col["fase"], y=col["goles_rival"], mode="lines+markers", name="Goles rival"))
    fig.update_layout(xaxis_title="Fase", yaxis_title="Goles")
    st.plotly_chart(fig, use_container_width=True)

    footer()

# ---------------------------------------------------------------------------
# Página 6: Comparador
# ---------------------------------------------------------------------------
elif pagina.startswith("6"):
    st.title("Comparador")
    modo = st.radio("Tipo de comparación", ["Selección vs. selección", "Confederación vs. confederación"], horizontal=True)

    if modo == "Selección vs. selección":
        c1, c2 = st.columns(2)
        s1 = c1.selectbox("Selección A", selecciones_df["id_seleccion"], format_func=lambda x: selecciones_df.set_index("id_seleccion").loc[x, "nombre"])
        s2 = c2.selectbox("Selección B", selecciones_df["id_seleccion"], index=1, format_func=lambda x: selecciones_df.set_index("id_seleccion").loc[x, "nombre"])
        tabla_comp = selecciones_df.set_index("id_seleccion").loc[[s1, s2], ["nombre", "confederacion_nombre", "modo_clasificacion", "grupo_mundial_2026"]]
        st.dataframe(tabla_comp, use_container_width=True)
        st.info("Comparación estadística (goles, posesión, xG) pendiente de carga de estadísticas colectivas.", icon="⚠️")
    else:
        confs = sorted(selecciones_df["confederacion_nombre"].unique())
        c1, c2 = st.columns(2)
        cf1 = c1.selectbox("Confederación A", confs)
        cf2 = c2.selectbox("Confederación B", confs, index=1)
        resumen = selecciones_df[selecciones_df["confederacion_nombre"].isin([cf1, cf2])].groupby("confederacion_nombre").size()
        st.bar_chart(resumen)

    footer()

# ---------------------------------------------------------------------------
# Página: Fuentes y metodología
# ---------------------------------------------------------------------------
else:
    st.title("Fuentes y metodología")

    st.subheader("Fuentes registradas")
    fuentes = q("SELECT * FROM fuente")
    st.dataframe(fuentes, use_container_width=True, hide_index=True)

    st.subheader("Datos pendientes de verificación (no cargados como definitivos)")
    pendientes = q("SELECT * FROM dato_pendiente")
    for _, r in pendientes.iterrows():
        st.markdown(f"- **{r['bloque']}**: {r['descripcion']} — _{r['razon']}_")

    st.subheader("Criterios de normalización aplicados")
    st.markdown(
        "- Total acumulado, promedio por partido, promedio por 90 minutos, porcentaje, ratio y estadística "
        "por posesión se tratan como magnitudes distintas y no se comparan entre sí.\n"
        "- Ninguna estadística sin fuente verificable se presenta como dato real; los bloques sin dato dicen "
        "explícitamente 'pendiente'.\n"
        "- Las selecciones anfitrionas (México, Estados Unidos, Canadá) no tienen partidos de eliminatoria, "
        "por diseño del modelo de datos."
    )
    footer()
