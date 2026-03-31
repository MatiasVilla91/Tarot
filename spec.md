# Spec

## Nombre

Oraculo de Camara

## Objetivo

Construir una web de tarot que se vea profesional, transmita autoridad y misterio, y permita obtener lecturas simbolicas de forma inmediata desde una interfaz simple.

## Propuesta de valor

- El usuario puede iniciar una lectura sin friccion.
- La experiencia visual debe sentirse premium, ritual y confiable.
- La app combina tiradas estructuradas con interpretaciones generadas por OpenAI.
- La lectura debe ser breve, clara y con tono de tarotista profesional.

## Usuario objetivo

- Personas interesadas en tarot, guia simbolica y lecturas intuitivas.
- Usuarios que buscan claridad en temas de amor, trabajo, decisiones o bloqueos.
- Visitantes que valoran una experiencia visual cuidada y no una interfaz generica.

## Flujo principal

1. El usuario entra a la landing.
2. Ve una propuesta clara y una interfaz de consulta visible.
3. Elige un tipo de tirada.
4. Opcionalmente escribe una pregunta.
5. Hace click en `Iniciar lectura`.
6. La app muestra un indicador visual de espera.
7. La app devuelve primero las cartas y luego la interpretacion.

## Reglas de UX

- Debe existir una sola accion principal para evitar confusion.
- La tirada se selecciona antes de la consulta.
- La pregunta del usuario es opcional.
- Si el campo de texto esta vacio, la app genera la tirada elegida.
- Si el usuario escribe una consulta, la respuesta debe usar ese contexto.
- Las cartas deben verse antes del texto interpretativo.
- La espera debe sentirse intencional mediante un indicador de escritura.

## Reglas de tono

- Espanol rioplatense.
- Voz de tarotista profesional.
- Respuestas breves.
- Interpretacion simbolica, no afirmaciones absolutas.
- Tono sereno, intuitivo, elegante y claro.

## Alcance funcional actual

- Landing principal con identidad visual premium.
- Chat de consulta.
- Tiradas de `1 carta`, `3 cartas` y `cruz celta`.
- Interpretaciones enriquecidas con OpenAI si existe `OPENAI_API_KEY`.
- Fallback local si OpenAI no esta disponible.
- Indicador visual de escritura.

## Alcance tecnico actual

- Backend en Flask.
- Frontend server-rendered con HTML, CSS y JavaScript plano.
- Configuracion por `.env`.
- Imagenes locales de cartas en `static/images`.
- SDK oficial de OpenAI para Python.

## Endpoints

### `GET /`

Renderiza la interfaz principal.

### `POST /chat`

Recibe:

```json
{
  "mensaje": "quiero una tirada sobre trabajo"
}
```

Devuelve una respuesta textual y, cuando aplica, cartas asociadas.

### `POST /tirada`

Recibe:

```json
{
  "tipo_tirada": "3 cartas"
}
```

Devuelve un arreglo de cartas para la tirada seleccionada.

## Variables de entorno

- `OPENAI_API_KEY`
- `OPENAI_MODEL`

## Requisitos de seguridad

- Nunca subir `.env` al repositorio.
- Nunca hardcodear secretos en el codigo.
- Mantener `.gitignore` actualizado para excluir caches, entornos virtuales y archivos sensibles.
- Tratar las respuestas del tarot como simbolicas y no como consejo medico, legal o financiero.

## Criterios de calidad

- La interfaz debe ser comprensible en menos de 5 segundos.
- El usuario no debe dudar cual boton usar.
- La respuesta debe sentirse corta y significativa.
- El sitio debe funcionar en desktop y mobile.
- Si OpenAI falla, la app debe seguir funcionando.

## Proximos pasos sugeridos

- Normalizar completamente textos del backend para evitar problemas de encoding.
- Agrandar visualmente las cartas para aumentar protagonismo.
- Agregar captura de leads o CTA comercial si el objetivo pasa a ser conversion.
- Guardar historial de lecturas para analitica o continuidad de usuario.
- Agregar tests de interfaz y endpoints.
