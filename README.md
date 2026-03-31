# Tarot Interactivo

Aplicacion web simple de tarot construida con Flask.

## Configuracion de OpenAI

La app puede usar OpenAI para responder consultas y enriquecer interpretaciones.

La forma recomendada es crear un archivo `.env` en la raiz del proyecto:

```env
OPENAI_API_KEY=tu_api_key
OPENAI_MODEL=gpt-5-mini
```

Alternativamente, en PowerShell:

```powershell
$env:OPENAI_API_KEY="tu_api_key"
$env:OPENAI_MODEL="gpt-5-mini"
```

Si no definis `OPENAI_API_KEY`, la app sigue funcionando con el fallback local basado en reglas.

## Ejecutar

1. Crear un entorno virtual.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Iniciar con `python app.py`.
4. Abrir `http://127.0.0.1:5000`.

## Endpoints

- `GET /`: interfaz principal.
- `POST /chat`: devuelve una carta o una respuesta sobre una carta especifica.
- `POST /tirada`: genera una tirada de `1 carta`, `3 cartas` o `cruz celta`.

## Notas

- La app usa solo las imagenes que realmente existen en `static/images`.
- La integracion usa el SDK oficial de OpenAI para Python.
- El modelo por defecto es `gpt-5-mini`, pero podes cambiarlo con `OPENAI_MODEL`.
