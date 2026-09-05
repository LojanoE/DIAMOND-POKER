# AGENTS.md — DIAMOND CLUB Poker Tracker

## Descripción del proyecto

**DIAMOND CLUB — Poker Tracker** es una aplicación web de un solo archivo (`index.html`) para llevar el control de partidas de poker caseras (cash games). Permite:

- **Jugadores**: registrar y eliminar jugadores, y ver su balance global acumulado.
- **Sesiones**: registrar una sesión de juego con las recargas (préstamos del banco) y las fichas finales de cada jugador; calcula el neto por jugador (`fichas finales − total prestado`).
- **Liquidación**: genera automáticamente las transferencias mínimas entre jugadores para saldar deudas (algoritmo greedy deudor→acreedor).
- **Verificación del banco**: compara el total prestado contra las fichas en mesa y alerta si hay diferencia.
- **Historial**: lista de sesiones guardadas, con **edición** de sesiones (corrige recargas/fichas y recalcula la liquidación conservando la sesión original), exportación/importación de datos en JSON y opción de borrar todo.

La interfaz y los comentarios del código están **en español**; mantén ese idioma para cualquier texto visible al usuario o comentario nuevo.

## Arquitectura y stack tecnológico

- **Un solo archivo HTML autocontenido**: `index.html` (~870 líneas) contiene HTML, CSS (dentro de `<style>`) y JavaScript (dentro de `<script>`). No hay carpetas ni módulos.
- **Sin dependencias de build, sin frameworks, sin npm/pip/cargo**: no existe `package.json`, `pyproject.toml` ni ningún archivo de configuración de build. El único archivo de configuración del repo es `.gitattributes` (normalización LF).
- **Dependencia externa única**: fuentes de Google Fonts (`Orbitron` y `Rajdhani`) cargadas por CDN. Requiere internet solo para las fuentes; la app funciona sin ellas (degrada tipografía).
- **Persistencia**: `localStorage` del navegador, bajo la clave `poker_homegame`. Estructura de datos:
  ```js
  {
    players: ["Nombre1", ...],
    sessions: [{
      id, date, name,
      results: [{ player, reloads: [montos], totalLoaned, final, net }],
      totalLoaned, totalFinal, bankDiff
    }]
  }
  ```
- **Runtime**: se abre directamente en cualquier navegador moderno (doble clic o `file://`). No hay servidor ni backend.
- **Desplegada en GitHub Pages**: `https://lojanoe.github.io/DIAMOND-POKER/`. El archivo DEBE llamarse `index.html` para que la URL raíz funcione.

## Estructura del código (dentro del archivo HTML)

- **CSS** (`<style>`): variables de tema en `:root` (paleta oscura con acentos rojo/naranja/dorado), clases por componente (`.card`, `.btn`, `.tab`, `.player-block`, `.balance-item`, `.version-badge`, etc.).
- **HTML** (`<body>`): header (con badge de versión `#versionBadge`), barra de pestañas (`.tabs`) y tres secciones `tab-content`: `players`, `sessions`, `history`.
- **JavaScript** (`<script>`), organizado en secciones con comentarios `// ========== NOMBRE ==========`:
  - `VERSIÓN`: constante `APP_VERSION` (única fuente de verdad de la versión, ver sección de versionado).
  - Estado global: `data` (cargado de localStorage) y `sessionDraft` (borrador de la sesión en curso, en memoria).
  - `save()` centraliza la persistencia.
  - `JUGADORES`: `addPlayer`, `removePlayer`, `renderPlayers` (incluye cálculo de balance global).
  - `SESIONES`: `getDraft`, `addReload`, `addCustomReload`, `removeReload`, `updateFinal`, `renderSessionForm`, `saveSession`, `showSettle`, `showBankCheck`.
  - `HISTORIAL`: `renderHistory`, `editSession` (carga una sesión en el formulario, activa `editingSessionId`), `cancelEdit`, `exportData`, `importData`, `clearAll`.
  - Edición de sesiones: la variable global `editingSessionId` (null = nueva sesión) indica qué sesión se está editando; `saveSession` actualiza en lugar de crear cuando está definido.

## Comandos de build y prueba

No hay build, tests ni linter configurados. Flujo de trabajo:

- **Ejecutar**: abrir `index.html` en un navegador o visitar `https://lojanoe.github.io/DIAMOND-POKER/`.
- **Probar**: prueba manual en el navegador — agregar jugadores, registrar una sesión, verificar liquidación, exportar/importar JSON y recargar la página para confirmar persistencia en `localStorage`.

## Convenciones de estilo

- **JavaScript estilo ES5**: usar `var` (no `let`/`const`), funciones declaradas con `function`, callbacks con `function(...) {...}` (no arrow functions), concatenación de strings con `+` (no template literals).
- **Renderizado**: el DOM se actualiza construyendo strings HTML con concatenación y asignándolos a `innerHTML`; los handlers se invocan con `onclick` en el markup generado. Mantén este patrón.
- **CSS**: usar las variables de `:root` para colores; tipografía `Orbitron` para títulos/números destacados y `Rajdhani` para texto general.
- **Idioma**: textos de UI, alertas y comentarios en español.
- **Indentación**: 2 espacios.

## Consideraciones de seguridad y datos

- Los datos viven exclusivamente en el `localStorage` del navegador del usuario; no se envían a ningún servidor.
- Los nombres de jugador se interpolan directamente en `innerHTML` (sin sanitización) — al modificar el renderizado, sé consciente del riesgo de XSS por nombres maliciosos.
- `exportData`/`importData` son el único mecanismo de respaldo y migración de datos; el formato importado valida solo la presencia de `players` y `sessions`.

## Control de versiones de la app y caché

La app tiene un **versionado manual** para forzar la actualización de caché en los navegadores de los usuarios. La versión actual es **1.2.0** y se define en **tres lugares que deben mantenerse sincronizados** dentro de `index.html`:

1. `var APP_VERSION = '1.2.0';` al inicio del `<script>` — **única fuente de verdad**; se muestra en el badge del header (`#versionBadge`).
2. `<meta name="version" content="1.2.0">` en el `<head>`.
3. El parámetro `?v=1.2.0` del `<link>` de Google Fonts (rompe la caché del recurso externo).

**Regla obligatoria**: ante CUALQUIER cambio en la app (HTML, CSS o JS), incrementar la versión (semver: patch para fixes, minor para features, major para cambios incompatibles) en los tres lugares anteriores. Esto garantiza que los usuarios siempre reciban la versión más reciente.

Además, el `<head>` incluye meta tags anti-caché (`Cache-Control: no-cache, no-store, must-revalidate`, `Pragma: no-cache`, `Expires: 0`) para que el navegador revalide el archivo en cada visita.

## Despliegue

La app se despliega en **GitHub Pages** desde la rama `main` del repo `LojanoE/DIAMOND-POKER`. Flujo:

1. Hacer los cambios en `index.html` e incrementar la versión (ver sección anterior).
2. Commit y push a `main`.
3. GitHub Pages publica automáticamente en `https://lojanoe.github.io/DIAMOND-POKER/` (el archivo debe llamarse `index.html` para que la URL raíz funcione).

## Control de versiones (git)

Repositorio git. `.gitattributes` fuerza normalización de fin de línea LF (`* text=auto`).
