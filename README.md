# Publicador de Instagram · Alacon Formación × Novantis Formación

Publica cada día la historia programada y, los lunes, el post de la semana.

- `contenido/AAAA-MM-DD/plan.json`: qué se publica ese día y en qué cuenta.
- `disenos/`: los diseños en HTML; `herramientas/renderizar.sh` los convierte en JPEG.
- `publicar.py`: publica con la API oficial de Instagram.
- `.github/workflows/publicar.yml`: lo lanza cada mañana (9:00, hora de Madrid).

Solo se sube aquí el contenido ya aprobado. Las claves viven en los Secrets de GitHub y en `.env` (que nunca se sube).
