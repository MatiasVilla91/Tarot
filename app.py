import os
from pathlib import Path
import random
import re

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, url_for
from openai import OpenAI


load_dotenv()


app = Flask(__name__)

IMAGES_DIR = Path(app.static_folder) / "images"
AVAILABLE_IMAGES = {path.name for path in IMAGES_DIR.glob("*")} if IMAGES_DIR.exists() else set()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")


CARTAS_TAROT_COMPLETAS = [
    {"nombre": "El Loco", "descripcion": "Nuevo comienzo, libertad y aventura.", "invertida": "Impulsividad y falta de direccion.", "imagen": "the-fool.jpg"},
    {"nombre": "El Mago", "descripcion": "Habilidad, creatividad y poder personal.", "invertida": "Manipulacion y mala planificacion.", "imagen": "the-magician.jpg"},
    {"nombre": "La Sacerdotisa", "descripcion": "Intuicion, misterio y conocimiento oculto.", "invertida": "Secretos revelados y desconexion intuitiva.", "imagen": "sacerdotisa.jpg"},
    {"nombre": "La Emperatriz", "descripcion": "Abundancia, creatividad y fertilidad.", "invertida": "Bloqueo creativo y dependencia.", "imagen": "the-empress.jpg"},
    {"nombre": "El Emperador", "descripcion": "Estabilidad, autoridad y control.", "invertida": "Rigidez, inseguridad y tirania.", "imagen": "the-emperor.jpg"},
    {"nombre": "El Sumo Sacerdote", "descripcion": "Tradicion, guia espiritual y estructura.", "invertida": "Dogmatismo y rebeldia sin direccion.", "imagen": "sacerdote.jpg"},
    {"nombre": "Los Enamorados", "descripcion": "Amor, decisiones y armonia.", "invertida": "Desequilibrio, conflicto e indecision.", "imagen": "the-lovers.jpg"},
    {"nombre": "El Carro", "descripcion": "Determinacion, avance y victoria.", "invertida": "Falta de control y frustracion.", "imagen": "the-chariot.jpg"},
    {"nombre": "La Justicia", "descripcion": "Equilibrio, verdad y consecuencias.", "invertida": "Injusticia y falta de claridad.", "imagen": "justice.jpg"},
    {"nombre": "El Ermitano", "descripcion": "Introspeccion, sabiduria y pausa.", "invertida": "Aislamiento y desconexion.", "imagen": "the-hermit.jpg"},
    {"nombre": "La Rueda de la Fortuna", "descripcion": "Cambio, ciclos y destino.", "invertida": "Resistencia al cambio y mala racha.", "imagen": "wheel-fo-fortune.jpg"},
    {"nombre": "La Fuerza", "descripcion": "Valor, autocontrol y confianza.", "invertida": "Miedo y perdida de control.", "imagen": "strength.jpg"},
    {"nombre": "El Colgado", "descripcion": "Nueva perspectiva, pausa y sacrificio.", "invertida": "Estancamiento e indecision.", "imagen": "the-hanged-man.jpg"},
    {"nombre": "La Muerte", "descripcion": "Transformacion profunda y cierre de etapa.", "invertida": "Resistencia a soltar y estancamiento.", "imagen": "death.jpg"},
    {"nombre": "La Templanza", "descripcion": "Equilibrio, moderacion y claridad.", "invertida": "Exceso y desorden emocional.", "imagen": "temperance.jpg"},
    {"nombre": "El Diablo", "descripcion": "Apego, tentacion y materialismo.", "invertida": "Liberacion y recuperacion del control.", "imagen": "the-devil.jpg"},
    {"nombre": "La Torre", "descripcion": "Cambio brusco, revelacion y ruptura.", "invertida": "Negacion y miedo al cambio.", "imagen": "the-tower.jpg"},
    {"nombre": "La Estrella", "descripcion": "Esperanza, inspiracion y calma.", "invertida": "Desilusion y perdida de fe.", "imagen": "the-start.jpg"},
    {"nombre": "La Luna", "descripcion": "Intuicion, suenos y misterio.", "invertida": "Confusion y autoengano.", "imagen": "the-moon.jpg"},
    {"nombre": "El Sol", "descripcion": "Exito, alegria y vitalidad.", "invertida": "Dudas y alegria bloqueada.", "imagen": "the-sun.jpg"},
    {"nombre": "El Juicio", "descripcion": "Renacimiento, evaluacion y despertar.", "invertida": "Autocritica y dificultad para avanzar.", "imagen": "judgement.jpg"},
    {"nombre": "El Mundo", "descripcion": "Cierre, logro e integracion.", "invertida": "Proceso incompleto y demoras.", "imagen": "the-world.jpg"},
    {"nombre": "As de Copas", "descripcion": "Apertura emocional y nuevos vinculos.", "invertida": "Bloqueo afectivo y sensibilidad cerrada.", "imagen": "ace-of-cups.jpg"},
    {"nombre": "Dos de Copas", "descripcion": "Union, acuerdo y reciprocidad.", "invertida": "Conflicto relacional y desequilibrio.", "imagen": "two-of-cups.jpg"},
    {"nombre": "Tres de Copas", "descripcion": "Celebracion, amistad y comunidad.", "invertida": "Exceso o desgaste social.", "imagen": "three-of-cups.jpg"},
    {"nombre": "Cuatro de Copas", "descripcion": "Repliegue, reflexion y reevaluacion.", "invertida": "Apertura a una nueva oportunidad.", "imagen": "four-of-cups.jpg"},
    {"nombre": "Cinco de Copas", "descripcion": "Perdida, duelo y arrepentimiento.", "invertida": "Aceptacion y reparacion emocional.", "imagen": "five-of-cups.jpg"},
    {"nombre": "Seis de Copas", "descripcion": "Nostalgia, memoria y ternura.", "invertida": "Exceso de apego al pasado.", "imagen": "six-of-cups.jpg"},
    {"nombre": "Siete de Copas", "descripcion": "Opciones, fantasia e imaginacion.", "invertida": "Claridad y decision practica.", "imagen": "seven-of-cups.jpg"},
    {"nombre": "Ocho de Copas", "descripcion": "Soltar, partir y buscar sentido.", "invertida": "Dificultad para dejar atras.", "imagen": "eight-of-cups.jpg"},
    {"nombre": "Nueve de Copas", "descripcion": "Satisfaccion y deseo cumplido.", "invertida": "Insatisfaccion o exceso.", "imagen": "nine-of-cups.jpg"},
    {"nombre": "Diez de Copas", "descripcion": "Armonia emocional y plenitud.", "invertida": "Tension familiar o expectativas rotas.", "imagen": "ten-of-cups.jpg"},
    {"nombre": "Sota de Copas", "descripcion": "Mensaje emocional y apertura creativa.", "invertida": "Inmadurez emocional o bloqueo.", "imagen": "page-of-cups.jpg"},
    {"nombre": "Caballo de Copas", "descripcion": "Romance, propuesta y sensibilidad.", "invertida": "Idealizacion y decepcion.", "imagen": "knight-of-cups.jpg"},
    {"nombre": "Reina de Copas", "descripcion": "Empatia, cuidado y intuicion.", "invertida": "Desborde emocional o manipulacion.", "imagen": "queen-of-cups.jpg"},
    {"nombre": "Rey de Copas", "descripcion": "Madurez emocional y diplomacia.", "invertida": "Distancia afectiva o inestabilidad.", "imagen": "king-of-cups.jpg"},
    {"nombre": "As de Bastos", "descripcion": "Impulso, iniciativa y chispa creativa.", "invertida": "Falta de energia o bloqueo para empezar.", "imagen": "ace-of-wands.jpg"},
    {"nombre": "Dos de Bastos", "descripcion": "Vision, decision y expansion.", "invertida": "Miedo a salir de lo conocido.", "imagen": "two-of-wands.jpg"},
    {"nombre": "Tres de Bastos", "descripcion": "Proyeccion, crecimiento y horizonte abierto.", "invertida": "Demoras o falta de perspectiva.", "imagen": "three-of-wands.jpg"},
    {"nombre": "Cuatro de Bastos", "descripcion": "Celebracion, estabilidad y logro compartido.", "invertida": "Tension en el hogar o alegria incompleta.", "imagen": "four-of-wands.jpg"},
    {"nombre": "Cinco de Bastos", "descripcion": "Competencia, friccion y energia dispersa.", "invertida": "Conflicto evitado o tension interna.", "imagen": "five-of-wands.jpg"},
    {"nombre": "Seis de Bastos", "descripcion": "Reconocimiento, avance y confianza.", "invertida": "Dudas, orgullo herido o validacion externa.", "imagen": "six-of-wands.jpg"},
    {"nombre": "Siete de Bastos", "descripcion": "Defensa, firmeza y posicion ganada.", "invertida": "Agotamiento o dificultad para sostener limites.", "imagen": "seven-of-wands.jpg"},
    {"nombre": "Ocho de Bastos", "descripcion": "Movimiento, noticias y rapidez.", "invertida": "Demoras, trabas o mensajes confusos.", "imagen": "eight-of-wands.jpg"},
    {"nombre": "Nueve de Bastos", "descripcion": "Resistencia, cautela y perseverancia.", "invertida": "Desgaste, desconfianza o guardia excesiva.", "imagen": "nine-of-wands.jpg"},
    {"nombre": "Diez de Bastos", "descripcion": "Carga, responsabilidad y esfuerzo sostenido.", "invertida": "Sobrecarga, agotamiento o dificultad para soltar peso.", "imagen": "ten-of-wands.jpg"},
    {"nombre": "Sota de Bastos", "descripcion": "Curiosidad, entusiasmo y exploracion.", "invertida": "Impaciencia o energia inmadura.", "imagen": "page-of-wands.jpg"},
    {"nombre": "Caballo de Bastos", "descripcion": "Pasion, impulso y accion audaz.", "invertida": "Apuro, inconstancia o choques.", "imagen": "knight-of-wands.jpg"},
    {"nombre": "Reina de Bastos", "descripcion": "Magnetismo, seguridad y creatividad viva.", "invertida": "Celos, desgaste o inseguridad encubierta.", "imagen": "queen-of-wands.jpg"},
    {"nombre": "Rey de Bastos", "descripcion": "Liderazgo, vision y poder de accion.", "invertida": "Autoritarismo, impulsividad o ego desmedido.", "imagen": "king-of-wands.jpg"},
    {"nombre": "As de Espadas", "descripcion": "Claridad mental y verdad.", "invertida": "Confusion y bloqueo.", "imagen": "ace-of-swords.jpg"},
    {"nombre": "Dos de Espadas", "descripcion": "Pausa y decision dificil.", "invertida": "Indecision sostenida.", "imagen": "two-of-swords.jpg"},
    {"nombre": "Tres de Espadas", "descripcion": "Dolor, ruptura y verdad dura.", "invertida": "Sanacion y salida del duelo.", "imagen": "three-of-swords.jpg"},
    {"nombre": "Cuatro de Espadas", "descripcion": "Descanso y recuperacion.", "invertida": "Agotamiento y urgencia.", "imagen": "four-of-swords.jpg"},
    {"nombre": "Cinco de Espadas", "descripcion": "Conflicto y tension.", "invertida": "Reconciliacion o retiro inteligente.", "imagen": "five-of-swords.jpg"},
    {"nombre": "Seis de Espadas", "descripcion": "Transicion y alejamiento de lo dificil.", "invertida": "Resistencia al cambio.", "imagen": "six-of-swords.jpg"},
    {"nombre": "Siete de Espadas", "descripcion": "Estrategia, reserva y cautela.", "invertida": "Sinceramiento o exposicion.", "imagen": "seven-of-swords.jpg"},
    {"nombre": "Ocho de Espadas", "descripcion": "Limitacion y miedo.", "invertida": "Liberacion y nueva perspectiva.", "imagen": "eight-of-swords.jpg"},
    {"nombre": "Nueve de Espadas", "descripcion": "Ansiedad y preocupacion intensa.", "invertida": "Alivio gradual.", "imagen": "nine-of-swords.jpg"},
    {"nombre": "Diez de Espadas", "descripcion": "Final doloroso y cierre.", "invertida": "Renacimiento tras tocar fondo.", "imagen": "ten-of-swords.png"},
    {"nombre": "Sota de Espadas", "descripcion": "Observacion, curiosidad mental y alerta.", "invertida": "Chismes, ansiedad o inmadurez en la comunicacion.", "imagen": "page-of-swords.jpg"},
    {"nombre": "Caballo de Espadas", "descripcion": "Accion rapida y determinacion.", "invertida": "Impulsividad y choque.", "imagen": "knight-of-swords.jpg"},
    {"nombre": "Reina de Espadas", "descripcion": "Lucidez, criterio y limites claros.", "invertida": "Dureza, distancia o juicio severo.", "imagen": "queen-of-swords.jpg"},
    {"nombre": "Rey de Espadas", "descripcion": "Logica, autoridad y criterio.", "invertida": "Frialdad y dureza.", "imagen": "king-of-swords.jpg"},
    {"nombre": "As de Oros", "descripcion": "Oportunidad concreta y prosperidad.", "invertida": "Oportunidad perdida o atraso.", "imagen": "ace-of-pentacles.jpg"},
    {"nombre": "Dos de Oros", "descripcion": "Equilibrio y adaptacion.", "invertida": "Desorden y sobrecarga.", "imagen": "two-of-pentacles.jpg"},
    {"nombre": "Tres de Oros", "descripcion": "Colaboracion y aprendizaje.", "invertida": "Falta de coordinacion.", "imagen": "three-of-pentacles.jpg"},
    {"nombre": "Cuatro de Oros", "descripcion": "Seguridad y control.", "invertida": "Rigidez o apego excesivo.", "imagen": "four-of-pentacles.jpg"},
    {"nombre": "Cinco de Oros", "descripcion": "Carencia y dificultad material.", "invertida": "Recuperacion y ayuda.", "imagen": "five-of-pentacles.jpg"},
    {"nombre": "Seis de Oros", "descripcion": "Intercambio, apoyo y generosidad.", "invertida": "Desequilibrio en el dar y recibir.", "imagen": "six-of-pentacles.jpg"},
    {"nombre": "Siete de Oros", "descripcion": "Espera, evaluacion y paciencia.", "invertida": "Impaciencia o resultados flojos.", "imagen": "seven-of-pentacles.jpg"},
    {"nombre": "Ocho de Oros", "descripcion": "Trabajo, practica y mejora.", "invertida": "Rutina sin foco.", "imagen": "eight-of-pentacles.jpg"},
    {"nombre": "Nueve de Oros", "descripcion": "Autonomia y disfrute de lo logrado.", "invertida": "Dependencia o exceso de confianza.", "imagen": "nine-of-pentacles.jpg"},
    {"nombre": "Diez de Oros", "descripcion": "Legado, estabilidad y abundancia sostenida.", "invertida": "Tension material o inseguridad en la base.", "imagen": "ten-of-pentacles.jpg"},
    {"nombre": "Sota de Oros", "descripcion": "Aprendizaje y oportunidad practica.", "invertida": "Distraccion o falta de constancia.", "imagen": "page-of-pentacles.jpg"},
    {"nombre": "Caballo de Oros", "descripcion": "Constancia, trabajo y responsabilidad.", "invertida": "Lentitud o terquedad.", "imagen": "knight-of-pentacles.jpg"},
    {"nombre": "Reina de Oros", "descripcion": "Cuidado, estabilidad y abundancia.", "invertida": "Desequilibrio material o desgaste.", "imagen": "queen-of-pentacles.jpg"},
    {"nombre": "Rey de Oros", "descripcion": "Solidez, dominio material y liderazgo estable.", "invertida": "Control excesivo o apego a lo material.", "imagen": "king-of-pentacles.jpg"},
]


DEFAULT_TIRADA = "3 cartas"
DEFAULT_TIRADA_CANTIDAD = 3


TAROT_SYSTEM_PROMPT = """
Sos un tarotista virtual en español rioplatense. Leés el tarot desde una mirada simbólica, intuitiva y humana.
Tu forma de responder combina calidez, claridad, sensibilidad y profundidad. Tenés una presencia serena, perceptiva y envolvente, sin caer en exageraciones ni frases vacías.

Tu tarea es interpretar cartas y tiradas como lenguajes simbólicos.
No presentás tus respuestas como verdades absolutas ni como hechos comprobados.
No hacés promesas, no garantizás resultados y no afirmás eventos concretos como si fueran inevitables.
Cuando una lectura toca temas delicados, hablás de tendencias, energías, emociones, tensiones, bloqueos, aperturas o posibilidades.

Modo de hablar:
- Siempre en español rioplatense.
- Siempre tratás al usuario de "vos".
- Sonás cercano, cálido, claro y consciente.
- Evitás lo robótico, lo moralista y lo excesivamente esotérico.
- Podés sonar profundo y espiritual, pero nunca confuso.
- Mantenés cierta belleza en el lenguaje, sin perder precisión.

Principios de interpretación:
- Leé cada carta según su símbolo, su energía y su lugar en la tirada.
- Uní las cartas entre sí para formar una lectura coherente, no una lista aislada de significados.
- Adaptá la interpretación a la pregunta del usuario.
- Priorizá lo emocional, vincular, psicológico y energético antes que lo literal.
- Si una carta puede leerse de varias formas, elegí la más coherente con la consulta.
- Si hay ambigüedad, hacela explícita con naturalidad.
- Si la lectura marca algo difícil, decilo con honestidad pero con delicadeza.
- Si marca algo favorable, transmitilo sin vender certezas.

Reglas importantes:
- Nunca afirmes infidelidades, embarazos, enfermedades, muertes, accidentes, delitos, maldiciones, trabajos espirituales ni pensamientos exactos de terceros como si fueran hechos.
- Nunca digas que alguien “te ama”, “te engañó”, “va a volver” o “está con otra persona” como certeza absoluta.
- En esos casos, reformulá en términos como: "la tirada sugiere distancia", "aparece confusión emocional", "hay energía de ocultamiento", "se ve una conexión todavía activa", "no se ve apertura clara en este momento".
- No reemplazás ayuda profesional médica, psicológica, legal o financiera.
- No estimules dependencia con nuevas tiradas compulsivas.
- Si el usuario repite muchas veces la misma pregunta, indicá con suavidad que la energía ya fue observada y que insistir demasiado puede confundir más la lectura.

Formato de respuesta:
- Empezá con una lectura general breve.
- Después interpretá cada carta o posición de forma clara.
- Cerrá con una síntesis final y una orientación reflexiva.
- Mantené las respuestas relativamente breves, salvo que el usuario pida profundidad.

Objetivo:
Que cada respuesta se sienta como una lectura de tarot auténtica, sensible y bien interpretada: mística pero honesta, profunda pero comprensible, cercana pero no invasiva.
""".strip()


def build_image_url(filename: str | None) -> str | None:
    if not filename or filename not in AVAILABLE_IMAGES:
        return None
    return url_for("static", filename=f"images/{filename}")


def openai_enabled() -> bool:
    return bool(OPENAI_API_KEY)


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY)


def generate_openai_text(user_prompt: str, context: str | None = None) -> str:
    prompt = user_prompt if not context else f"{context}\n\nConsulta del usuario: {user_prompt}"
    response = get_openai_client().responses.create(
        model=OPENAI_MODEL,
        instructions=TAROT_SYSTEM_PROMPT,
        input=prompt,
    )
    return response.output_text.strip()


def classify_user_message(mensaje: str) -> str:
    response = get_openai_client().responses.create(
        model=OPENAI_MODEL,
        instructions=(
            "Clasifica el mensaje del usuario para una app de tarot.\n"
            "Responde solamente con una palabra: CONSULTA o ACLARAR.\n"
            "CONSULTA: el usuario expresa una duda, tema, emocion, situacion, decision, "
            "o pide significado de una carta, aunque no use signos de pregunta.\n"
            "ACLARAR: el mensaje es ruido, texto sin sentido, demasiado ambiguo, saludo simple, "
            "o no alcanza para hacer una tirada con criterio."
        ),
        input=f"Mensaje del usuario: {mensaje}",
    )
    return response.output_text.strip().upper()


def es_texto_sin_sentido(mensaje: str) -> bool:
    limpio = re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]", "", mensaje)
    if len(limpio) < 4:
        return True
    vocales = sum(1 for c in limpio.lower() if c in "aeiouáéíóúü")
    ratio_vocales = vocales / max(len(limpio), 1)
    if len(mensaje.split()) == 1 and len(limpio) >= 8 and ratio_vocales < 0.2:
        return True
    if len(set(limpio.lower())) <= 3 and len(limpio) >= 6:
        return True
    return False


def necesita_aclaracion(mensaje: str) -> bool:
    texto = mensaje.strip()
    if not texto:
        return True

    texto_limpio = texto.lower().strip("¿?¡!.,;:()[]{}\"'")
    saludos = {"hola", "buenas", "buen dia", "buen día", "hey", "holi", "hello"}
    if texto_limpio in saludos:
        return True

    if es_texto_sin_sentido(texto):
        return True

    palabras = [p for p in re.findall(r"\w+", texto_limpio, flags=re.UNICODE) if p]
    if len(palabras) <= 1 and len(texto_limpio) < 12:
        return True

    disparadores_consulta = [
        "amor", "trabajo", "pareja", "dinero", "decision", "decisión", "quiero",
        "necesito", "siento", "significa", "significado", "deberia", "debería",
        "conviene", "volver", "relacion", "relación", "futuro", "bloqueo", "energia",
        "energía", "camino", "cambio", "cambios", "muerte", "carta", "tirada",
        "pregunta", "claridad", "estoy", "me pasa", "que", "qué", "como", "cómo"
    ]
    if "?" in texto or any(trigger in texto_limpio for trigger in disparadores_consulta):
        return False

    return len(palabras) < 3


def build_clarification_message() -> str:
    return (
        "Todavia no veo una consulta clara para abrir la tirada.\n"
        "Contame un poco mas: puede ser sobre amor, trabajo, una decision, un bloqueo o el significado de una carta.\n"
        "Cuando me des un tema o una pregunta concreta, hago la lectura."
    )


def seleccionar_carta() -> dict:
    carta = random.choice(CARTAS_TAROT_COMPLETAS)
    posicion = random.choice(["normal", "invertida"])
    descripcion = carta["descripcion"] if posicion == "normal" else carta["invertida"]
    return {
        "nombre": carta["nombre"],
        "descripcion": descripcion,
        "posicion": posicion,
        "imagen": build_image_url(carta.get("imagen")),
    }


def generar_tirada(cantidad: int) -> list[dict]:
    cartas = random.sample(CARTAS_TAROT_COMPLETAS, k=min(cantidad, len(CARTAS_TAROT_COMPLETAS)))
    resultado = []
    for carta in cartas:
        posicion = random.choice(["normal", "invertida"])
        resultado.append(
            {
                "nombre": carta["nombre"],
                "descripcion": carta["descripcion"] if posicion == "normal" else carta["invertida"],
                "posicion": posicion,
                "imagen": build_image_url(carta.get("imagen")),
            }
        )
    return resultado


def buscar_carta_por_nombre(mensaje: str) -> dict | None:
    texto = mensaje.lower()
    for carta in CARTAS_TAROT_COMPLETAS:
        if carta["nombre"].lower() in texto:
            return carta
    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    mensaje_usuario = str(data.get("mensaje", "")).strip()
    if not mensaje_usuario:
        return jsonify({"respuesta": "Escribi un mensaje para continuar."}), 400

    decision = "CONSULTA"
    if openai_enabled():
        try:
            decision = classify_user_message(mensaje_usuario)
        except Exception:
            decision = "ACLARAR" if necesita_aclaracion(mensaje_usuario) else "CONSULTA"
    else:
        decision = "ACLARAR" if necesita_aclaracion(mensaje_usuario) else "CONSULTA"

    if decision != "CONSULTA":
        return jsonify({"respuesta": build_clarification_message(), "accion": "aclarar", "cartas": []})

    tirada = generar_tirada(DEFAULT_TIRADA_CANTIDAD)
    texto = "Tu tirada de 3 cartas es:\n" + "\n".join(
        f"- {carta['nombre']} ({carta['posicion']}): {carta['descripcion']}" for carta in tirada
    )
    if openai_enabled():
        context = (
            "Interpreta esta tirada de tarot usando solamente las cartas provistas.\n"
            "La consulta del usuario debe guiar la lectura, pero la respuesta siempre tiene que basarse en la tirada.\n"
            + "\n".join(
                f"- {carta['nombre']} ({carta['posicion']}): {carta['descripcion']}" for carta in tirada
            )
        )
        try:
            texto = generate_openai_text(mensaje_usuario, context)
        except Exception:
            pass
    return jsonify({"respuesta": texto, "cartas": tirada, "accion": "tirada"})


@app.route("/tirada", methods=["POST"])
def tirada():
    data = request.get_json(silent=True) or {}
    tipo_tirada = str(data.get("tipo_tirada", DEFAULT_TIRADA)).strip().lower()
    if tipo_tirada and tipo_tirada != DEFAULT_TIRADA:
        return jsonify({"error": "Esta version usa una tirada fija de 3 cartas."}), 400

    return jsonify({"tirada": generar_tirada(DEFAULT_TIRADA_CANTIDAD)})


if __name__ == "__main__":
    app.run(debug=True)
