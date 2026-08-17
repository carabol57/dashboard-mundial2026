# Dashboard Ciclo Mundialista 2026

## Cómo ejecutarlo

1. Instalar dependencias: `pip install streamlit plotly pandas`
2. Generar la base de datos (ya viene generada, pero se puede regenerar): `python data/build_db.py`
3. Ejecutar: `streamlit run app.py`
4. Abre la URL local que muestra la terminal (por defecto http://localhost:8501)

## Estructura

- `data/build_db.py`: script que construye `data/mundial2026.db` (SQLite) a partir de los datos verificados en Fase C. Editar este archivo para añadir selecciones, partidos, competiciones o fuentes nuevas.
- `data/mundial2026.db`: base de datos ya generada.
- `app.py`: aplicación Streamlit con las 6 páginas del dashboard más la página de Fuentes y metodología.

## Estado de los datos

Todo lo cargado tiene fuente y nivel de confiabilidad registrados en la tabla `fuente` y visibles en la página "Fuentes y metodología" del propio dashboard. Los bloques sin datos verificados (eliminatorias completas por confederación, estadísticas colectivas e individuales, ranking FIFA, entrenadores) se muestran explícitamente como pendientes en la interfaz, no se ocultan ni se estiman.

## Cómo continuar actualizando

Para cargar un nuevo bloque de datos: añadir las filas correspondientes en las listas `SELECCIONES`, `COMPETICIONES`, `PARTIDOS` o `FUENTES` de `data/build_db.py`, volver a ejecutar el script, y los cambios aparecen automáticamente en el dashboard sin tocar `app.py`. El modelo está preparado para el siguiente ciclo mundialista: basta con añadir una nueva fila en `competicion` con el nuevo Mundial y sus partidos asociados.

---
Realizado por sportsamc.com
Desarrollado por Andres Mauricio Carabali
