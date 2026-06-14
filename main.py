from fastapi import FastAPI
from pydantic import BaseModel

# Creamos la aplicación de la API
app = FastAPI(title="SpamShield API", description="Detector de Spam y Sentimiento")

# Definimos el 'molde' de los datos que van a entrar (un JSON con el texto)
class TextInput(BaseModel):
    text: str

# 1. Ruta de bienvenida (Para probar si el servidor está vivo)
@app.get("/")
def home():
    return {"status": "online", "message": "SpamShield API is running globally!"}

# 2. Ruta principal: Acá es donde va a ocurrir la magia del análisis
@app.post("/analyze")
def analyze_text(input_data: TextInput):
    texto_a_analizar = input_data.text.lower()
    
    # --- LOGICA DE PRUEBA (Después la hacemos ultra inteligente) ---
    es_spam = "no"
    sentimiento = "neutral"
    
    # Regla super simple para ver que funcione:
    if "viagra" in texto_a_analizar or "free money" in texto_a_analizar or "compre ya" in texto_a_analizar:
        es_spam = "yes"
        
    if "malo" in texto_a_analizar or "basura" in texto_a_analizar or "hate" in texto_a_analizar:
        sentimiento = "negative"
    elif "bueno" in texto_a_analizar or "excelente" in texto_a_analizar or "love" in texto_a_analizar:
        sentimiento = "positive"
    # ---------------------------------------------------------------

    # Lo que la API le responde al usuario (el JSON que vendemos)
    return {
        "text_analyzed": input_data.text,
        "spam": es_spam,
        "sentiment": sentimiento
    }
from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob
import nltk

# Descargamos el paquete de datos necesario para el análisis de texto
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

app = FastAPI(title="SpamShield API", description="Detector Inteligente de Spam y Sentimiento")

class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "online", "message": "SpamShield AI Engine is active!"}

@app.post("/analyze")
def analyze_text(input_data: TextInput):
    texto = input_data.text
    texto_lower = texto.lower()
    
    # 1. 🧠 ANALISIS DE SENTIMIENTO CON IA
    # TextBlob analiza las palabras y nos da un puntaje entre -1.0 (muy negativo) y 1.0 (muy positivo)
    analisis = TextBlob(texto)
    polaridad = analisis.sentiment.polarity
    
    if polaridad < -0.1:
        sentimiento = "negative"
    elif polaridad > 0.1:
        sentimiento = "positive"
    else:
        sentimiento = "neutral"
        
    # 2. 🛡️ FILTRO DE SPAM AVANZADO
    # Lista de palabras y frases sospechosas comunes en ofertas falsas globales
    disparadores_spam = [
        "viagra", "free money", "compre ya", "gane dinero", "income", 
        "click here", "compre ahora", "oferta exclusiva", "bitcoin profit",
        "crypto bonus", "casino free", "trabaja desde casa", "urgent secret"
    ]
    
    # Contamos cuántas frases de spam aparecen
    coincidencias = sum(1 for palabra in disparadores_spam if palabra in texto_lower)
    
    # Si tiene 2 o más palabras sospechosas, o si es un texto corto con un link/oferta, es Spam
    es_spam = "no"
    if coincidencias >= 2 or ("http" in texto_lower and coincidencias  >= 1):
        es_spam = "yes"
    elif "free money" in texto_lower or "bitcoin profit" in texto_lower:
        es_spam = "yes" # Casos graves son spam directo
        
    return {
        "text_analyzed": texto,
        "spam": es_spam,
        "sentiment": sentimiento,
        "ai_score": round(polaridad, 2) # Le mostramos al programador el puntaje exacto
    }
