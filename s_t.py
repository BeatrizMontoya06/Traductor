import streamlit as st
from gTTS import gTTS
from deep_translator import GoogleTranslator
import base64
import io

# Configuración de la página
st.set_page_config(
    page_title="Bee's Translator v3.0 - Retro Y2K",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializar estados de la sesión
if "recognized_text" not in st.session_state:
    st.session_state.recognized_text = ""
if "audio_b64" not in st.session_state:
    st.session_state.audio_b64 = None

# Estilos Retro Y2K Globales
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

    .stApp {
        background-color: #008080 !important;
        background-image: 
            radial-gradient(#40e0d0 15%, transparent 16%),
            radial-gradient(#004040 15%, transparent 16%) !important;
        background-size: 16px 16px !important;
        font-family: 'MS Sans Serif', Tahoma, sans-serif !important;
    }

    div[data-testid="stVerticalBlock"] > div {
        background: #c0c0c0;
        border: 3px solid;
        border-color: #ffffff #808080 #808080 #ffffff;
        padding: 12px;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.5);
    }

    label, p, h1, h2, h3, span {
        color: #000000 !important;
        font-family: 'MS Sans Serif', Tahoma, sans-serif !important;
    }

    textarea, select, div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 2px inset #808080 !important;
        font-family: monospace !important;
        color: #000000 !important;
    }

    .stButton > button {
        background: #c0c0c0 !important;
        color: #000000 !important;
        border: 2px solid !important;
        border-color: #ffffff #808080 #808080 #ffffff !important;
        font-weight: bold !important;
        font-size: 13px !important;
        border-radius: 0px !important;
        box-shadow: 2px 2px 0px #000000 !important;
    }

    .stButton > button:active {
        border-color: #808080 #ffffff #ffffff #808080 !important;
        box-shadow: inset 1px 1px 0px #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado Ventana Y2K
y2k_header = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
        body { font-family: Tahoma, sans-serif; margin: 0; background: transparent; }
        .title-bar {
            background: linear-gradient(90deg, #800080, #d010d0);
            color: white; padding: 4px 8px; font-weight: bold; font-size: 14px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .win-btn {
            width: 16px; height: 14px; background: #c0c0c0; border: 1px solid;
            border-color: #ffffff #808080 #808080 #ffffff; font-size: 9px;
            text-align: center; font-weight: bold; color: #000; display: inline-block;
        }
        marquee {
            background: #000; color: #00ff00; font-family: 'VT323', monospace;
            font-size: 20px; padding: 4px; border: 2px inset #808080; margin: 8px 0;
        }
        .retro-info {
            border: 2px inset #ffffff; background: #e0e0e0; padding: 8px; margin-bottom: 8px;
        }
        .retro-info h2 {
            margin: 0 0 4px 0; font-size: 13px; background: #800080; color: #fff; padding: 2px 6px;
        }
    </style>
</head>
<body>
    <div class="title-bar">
        <span>🐝 C:\\BEES_TRANSLATOR\\v3.0\\VOICE_TRANSLATOR.EXE</span>
        <div>
            <div class="win-btn">_</div>
            <div class="win-btn">□</div>
            <div class="win-btn">✕</div>
        </div>
    </div>
    <marquee scrollamount="5">
        *** TRADUCTOR POR VOZ EN TIEMPO REAL *** PRESIONA EL BOTÓN DEL MICRÓFONO Y HABLA ***
    </marquee>
    <div class="retro-info">
        <h2>ℹ INFORMACIÓN DEL SISTEMA</h2>
        <p style="font-size: 12px; margin: 2px 0;">
            Presiona el botón de hablar, di tu frase en voz alta y el sistema capturará tu voz, la traducirá al idioma seleccionado y reproducirá el audio automáticamente.
        </p>
    </div>
</body>
</html>
"""
st.components.v1.html(y2k_header, height=185)

# Componente HTML de Micrófono con permiso de iframe (allow="microphone")
mic_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    .mic-container {
        background: #e0e0e0;
        border: 2px inset #ffffff;
        padding: 12px;
        text-align: center;
        font-family: Tahoma, sans-serif;
    }
    .btn-speech {
        background: #c0c0c0;
        border: 2px solid;
        border-color: #ffffff #808080 #808080 #ffffff;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 14px;
        cursor: pointer;
        box-shadow: 2px 2px 0px #000;
    }
    .btn-speech:active {
        border-color: #808080 #ffffff #ffffff #808080;
        box-shadow: inset 1px 1px 0px #000;
    }
    #status {
        margin-top: 8px;
        font-size: 12px;
        font-weight: bold;
        color: #000080;
    }
</style>
</head>
<body>
    <div class="mic-container">
        <button class="btn-speech" onclick="startRecognition()">🎙️ PRESIONA PARA HABLAR (MICRÓFONO)</button>
        <div id="status">Estado: Listo para escuchar...</div>
    </div>

    <script>
    function startRecognition() {
        const statusDiv = document.getElementById('status');
        
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert("Tu navegador no soporta el micrófono WebSpeech API. Prueba usar Google Chrome.");
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();

        recognition.lang = 'es-ES';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        statusDiv.innerText = "🔴 ESCUCHANDO... ¡Habla ahora!";
        statusDiv.style.color = "#ff0000";

        recognition.start();

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            statusDiv.innerText = "✅ Capturado: '" + transcript + "'";
            statusDiv.style.color = "#008000";

            // Copia automáticamente el texto reconocido al portapapeles
            navigator.clipboard.writeText(transcript);
            alert("Voz reconocida: " + transcript + "\\n\\n¡Se ha copiado a tu portapapeles! Pégalo en el recuadro de abajo.");
        };

        recognition.onerror = function(event) {
            statusDiv.innerText = "❌ Error: " + event.error;
            statusDiv.style.color = "#ff0000";
        };

        recognition.onend = function() {
            if (statusDiv.innerText.includes("ESCUCHANDO")) {
                statusDiv.innerText = "Fin del escaneo de voz.";
                statusDiv.style.color = "#000080";
            }
        };
    }
    </script>
</body>
</html>
"""

# Inyección del reproductor con el permiso estricto `allow="microphone"`
st.markdown("### 🎙️ 1. Captura de Voz")
st.components.v1.html(mic_html, height=110)

# Diccionario de idiomas y códigos de traducción / voz
LANGUAGES = {
    "🇺🇸 Inglés": ("en", "com"),
    "🇫🇷 Francés": ("fr", "fr"),
    "🇮🇹 Italiano": ("it", "it"),
    "🇩🇪 Alemán": ("de", "de"),
    "🇵🇹 Portugués": ("pt", "pt"),
    "🇷🇺 Ruso": ("ru", "ru"),
    "🇯🇵 Japonés": ("ja", "co.jp"),
    "🇨🇳 Chino (Mandarín)": ("zh-CN", "com"),
    "🇰🇷 Coreano": ("ko", "co.kr"),
    "🇦🇪 Árabe": ("ar", "com"),
    "🇪🇸 Español": ("es", "com.mx")
}

# Formulario de traducción
with st.form(key="translator_form"):
    st.markdown("### 📝 2. Texto Reconocido / A Traducir:")
    user_input = st.text_area(
        label="Texto de entrada",
        height=100,
        placeholder="Escribe aquí tu frase o pega (Ctrl + V) el texto capturado por el micrófono arriba...",
        label_visibility="collapsed"
    )

    st.markdown("### 🌍 3. Idioma Destino:")
    selected_lang = st.selectbox(
        "Idioma",
        options=list(LANGUAGES.keys()),
        label_visibility="collapsed"
    )

    translate_btn = st.form_submit_button("⚡ TRADUCIR Y REPRODUCIR AUDIO")

# Traducción y generación de audio
if translate_btn:
    if not user_input.strip():
        st.warning("⚠️ Ingresa un texto o captura tu voz con el micrófono antes de continuar.")
    else:
        with st.spinner("Traduciendo texto y sintetizando voz..."):
            try:
                target_code, tld_code = LANGUAGES[selected_lang]
                
                # 1. Traducir el texto al idioma seleccionado
                translated_text = GoogleTranslator(source='auto', target=target_code).translate(user_input)
                
                # Muestra el texto traducido
                st.success(f"**Traducción ({selected_lang}):** {translated_text}")

                # 2. Generar el audio de la traducción con gTTS
                tts = gTTS(text=translated_text, lang=target_code, tld=tld_code, slow=False)
                
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                audio_bytes = fp.read()
                b64 = base64.b64encode(audio_bytes).decode()

                # 3. Reproductor HTML5 con Autoplay
                player_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        .player-card {{
                            background: #e0e0e0;
                            border: 2px inset #ffffff;
                            padding: 12px;
                            text-align: center;
                            font-family: Tahoma, sans-serif;
                            margin-top: 10px;
                        }}
                        audio {{ width: 100%; margin-top: 8px; }}
                        .status {{
                            color: #008000; font-weight: bold; font-size: 13px;
                            background: #000; padding: 4px; border: 1px inset #808080;
                        }}
                    </style>
                </head>
                <body>
                    <div class="player-card">
                        <div class="status">🔊 REPRODUCIENDO TRADUCCIÓN...</div>
                        <audio controls autoplay>
                            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                        </audio>
                    </div>
                </body>
                </html>
                """
                st.components.v1.html(player_html, height=120)

            except Exception as e:
                st.error(f"Error procesando la traducción: {e}")
