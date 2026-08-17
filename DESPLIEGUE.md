# Guía de despliegue: Dashboard Ciclo Mundialista 2026

## Recomendación principal

Usar Streamlit Community Cloud (gratuito) para tener el dashboard disponible en un enlace web permanente, sin depender de tu computador encendido. Es la opción recomendada porque no tiene costo, se actualiza automáticamente cada vez que subas una nueva versión de los datos, y no requiere servidor propio.

## Opción 1: uso local (ya disponible, sin pasos adicionales)

1. Descomprime el archivo `dashboard_mundial2026.zip` en tu computador.
2. Instala Python 3.10 o superior si no lo tienes.
3. Abre una terminal en la carpeta del proyecto y ejecuta:
   ```
   pip install streamlit plotly pandas
   streamlit run app.py
   ```
4. Se abre automáticamente en tu navegador. Cada vez que quieras usarlo, repites el paso 3.

Ventaja: no depende de internet ni de terceros. Desventaja: solo lo puedes ver tú, en ese computador, y solo mientras la terminal está abierta.

## Opción 2: Streamlit Community Cloud (recomendada para uso recurrente)

Pasos:
1. Crear una cuenta gratuita en GitHub (si no tienes) y subir la carpeta del proyecto como un repositorio nuevo.
2. Crear una cuenta gratuita en share.streamlit.io (Streamlit Community Cloud), usando el mismo login de GitHub.
3. Conectar el repositorio y señalar `app.py` como archivo principal.
4. Streamlit Community Cloud instala las dependencias automáticamente a partir de un archivo `requirements.txt` (lo incluyo en este mismo paquete).
5. En unos minutos obtienes una URL pública tipo `tuusuario-dashboard-mundial2026.streamlit.app`, accesible desde cualquier dispositivo, para ti y para quien quieras compartirla (por ejemplo tu equipo en el club o en Indervalle).

Para actualizar los datos más adelante: editas `data/build_db.py` con la información nueva, subes el cambio a GitHub, y la app se actualiza sola en la nube.

## Opción 3: Power BI o herramienta interna del club/Indervalle

Si en algún momento tu organización exige que el reporte viva dentro de Power BI u otra herramienta corporativa, los datos de `data/mundial2026.db` (SQLite) se pueden exportar a Excel o CSV y conectar ahí. Te puedo generar esa exportación cuando la necesites; no hace falta rehacer el proyecto.

## Costo

Las opciones 1 y 2 no tienen costo. La opción 2 tiene límites generosos de uso gratuito (suficiente para un dashboard de consulta interna); si en el futuro se necesita más capacidad o un dominio propio, ahí sí hay planes pagos de Streamlit, pero no son necesarios para este caso de uso.

---
Realizado por sportsamc.com
Desarrollado por Andres Mauricio Carabali
