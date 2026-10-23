# Encargos de Alex: cómo trabaja Claude en cada vuelta

Este archivo lo lee la sesión programada de Claude Code («Encargos de Alex»), que se ejecuta en la nube
cada 2 horas, de 8:00 a 22:00 (hora de Madrid). Alex es el agente de Trabajo de la Oficina Virtual del
usuario: apunta los encargos y Claude los hace y se los devuelve para que el usuario los apruebe.

**Regla de oro: nunca se publica ni se programa nada que el usuario no haya aprobado con el botón «Aprobar».**

## 0. Conectar con la oficina

```bash
OFI=https://oficina-virtual.alexbarras.workers.dev/api/maquina
# La llave puede venir de dos sitios: como «secreto de red» del entorno (se añade sola a las peticiones a la
# oficina y no se ve) o como variable OFICINA_CLAVE. Si existe la variable, se usa; si no, se confía en el secreto.
AUT=(); [ -n "$OFICINA_CLAVE" ] && AUT=(-H "Authorization: Bearer $OFICINA_CLAVE")
curl -sf "${AUT[@]}" "$OFI/trabajo" > /tmp/trabajo.json
```

En todas las llamadas de abajo, `"${AUT[@]}"` va en lugar de la cabecera `Authorization`.

- Si la respuesta es 401, para y explica en el resumen final que falta la llave (se copia en la sala de Alex
  → tarjeta «Claude · encargos» → «Llave», y se pone como secreto de red para
  `oficina-virtual.alexbarras.workers.dev` con la cabecera `Authorization: Bearer …`, o como variable
  `OFICINA_CLAVE` del entorno). No intentes nada más.
- Nunca escribas la llave en archivos, commits ni mensajes.
- `trabajo.json` trae: `hoy`, `encargos` (en estado `Pendiente` o `Aprobado`), `sabe_alex` (los datos
  verdaderos de Alacon y Novantis: úsalos como única fuente), `calendario` (contenido ya planificado) y
  `documentos` (la carpeta de documentos; el archivo se descarga con
  `GET $OFI/documentos/ID/archivo`).
- Si no hay encargos, termina diciendo «Nada que hacer».

## 1. Encargos en estado `Pendiente`: hacer el trabajo

Para cada uno, en orden de `fecha_limite`:

1. Márcalo como empezado:
   `curl -sf -X POST "${AUT[@]}" -H 'Content-Type: application/json' -d '{"estado":"En marcha"}' "$OFI/encargos/ID/estado"`
2. Lee `titulo`, `tipo`, `detalle`, `cambios` (si el usuario pidió cambios, son lo más importante) y
   `conversacion_reciente`.
3. Haz el trabajo siguiendo las reglas de abajo.
4. Entrégalo con `POST $OFI/encargos/ID/resultado` y un JSON con:
   - `mensaje`: lo que dice Alex en el chat. Corto, en español de España, de tú, como un compañero: qué has
     hecho y qué tiene que mirar. Sin firma ni WhatsApp al final.
   - `resultado`: el trabajo completo en texto (textos de cada pieza, guion, etc.).
   - `archivos` (opcional): lista de `{"nombre","mime","b64"}`. Imágenes JPEG/PNG de menos de 1,8 MB salen
     en el chat; PDF y otros van a la carpeta de documentos. Máximo 12.
   - `ideas` (opcional): piezas para el calendario de Alex: `{"titulo","fecha":"AAAA-MM-DD","formato":"Historia|Post|Carrusel|Reel","curso","texto"}`.
     Se apuntan como «Para revisar».
   Usa un archivo para el cuerpo (`-d @/tmp/resultado.json`), que con imágenes en base64 es grande.
5. Si algo no se puede hacer (falta un dato, no se puede renderizar, es un vídeo), entrégalo igual con lo que
   sí esté hecho y di en `mensaje` qué falta y por qué. Nunca inventes un dato para tapar el hueco.

## 2. Encargos en estado `Aprobado`: terminar

El usuario ya pulsó «Aprobar». Si son historias o posts de Instagram:

1. Copia las imágenes aprobadas a `contenido/AAAA-MM-DD/` (una carpeta por día), haz commit y push a `main`
   para que GitHub Pages las sirva en `https://koddita.github.io/instagram-alacon/contenido/AAAA-MM-DD/…`.
2. Programa cada pieza en Metricool, **igual en las dos marcas** (Alacon 5914974 y Novantis 7052187), a las
   09:00 Europe/Madrid (historias como STORY; posts los lunes). Guarda lo programado en
   `contenido/AAAA-MM-DD/metricool.json` como en los días anteriores y haz commit.
3. Avisa con `POST $OFI/encargos/ID/hecho` y `{"mensaje":"…"}` (qué se ha programado y cuándo).

Si Metricool no está disponible en esta sesión, no lo programes por otra vía: deja el encargo en `Aprobado`,
llama a `POST $OFI/encargos/ID/estado` con `{"estado":"Aprobado","nota":"Falta Metricool en la rutina"}` y
explícalo en el resumen final. Otros encargos aprobados (textos, dossieres…) solo necesitan `hecho`.

## Reglas de Alacon × Novantis (obligatorias)

- Datos siempre verdaderos: solo lo que está en `sabe_alex`. Si falta un dato, dilo en el mensaje; no lo inventes.
- **Nunca** precios de los cursos. **Nunca** ofrecer ni insinuar oposiciones. No prometer empleo ni plazos.
- Auxiliar de Enfermería no da el título de TCAE. No anunciar la app Portal del Alumno (aún no está disponible).
- Valor primero (3-5 datos útiles y poco conocidos; nada obvio), puente al curso relacionado con su título
  exacto, cierre «Alacon Formación × Novantis Formación» y WhatsApp 611 12 62 64.
- Días mundiales o fechas señaladas: compruébalos en una fuente fiable antes de usarlos.
- Alacon y Novantis llevan siempre el mismo contenido, a la misma hora.
- Si el encargo pide un guion o un texto, entrega solo el texto, sin consejos de grabación.

## Diseño de historias y posts

- Formato vertical 1080×1920 (historias) o 1080×1350 (posts). Máximo unas 8 palabras por bloque de texto.
- Estilo: copia el de `disenos/` (por ejemplo `disenos/2026-10-29.html` y `disenos/estilo-historia.css`):
  azul `#006DA6` protagonista, gris `#4C4C4C`, Montserrat, logos en `disenos/assets/`. Rojo y amarillo solo en
  iconos de peligro o precaución. Respeta las zonas seguras de Instagram (arriba y abajo).
- Guarda cada diseño nuevo como `disenos/AAAA-MM-DD-tema.html`.
- Para pasarlo a JPEG en la nube (aquí no hay `sips` ni el Chrome del Mac): usa Chrome sin cabeza de
  Playwright, por ejemplo
  `npx -y playwright@1.48.2 install chromium` y luego un script de Node con `page.setViewportSize({width:1080,height:1920})`
  y `page.screenshot({type:'jpeg', quality:90})`. Comprueba que pesa menos de 1,8 MB.
- Los vídeos no se pueden montar en la nube: entrega el guion y di que el vídeo se monta en el Mac.

## Al terminar la vuelta

Resume en pocas líneas qué encargos has entregado o terminado y qué ha fallado.
