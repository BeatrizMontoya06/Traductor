import streamlit as st
from gtts import gTTS
from googletrans import Translator
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
from streamlit_bokeh_events import streamlit_bokeh_events
import base64
import io

# Configuración de la página
st.set_page_config(
    page_title="Bee's Translator v3.0 - Retro Y2K",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializar traductor de googletrans
translator = Translator()

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
        *** TRADUCTOR POR VOZ EN TIEMPO REAL Y2K *** HAZ CLIC EN EL MICRÓFONO BOKEH Y HABLA ***
    </marquee>
    <div class="retro-info">
        <h2>ℹ INFORMACIÓN DEL SISTEMA</h2>
        <p style="font-size: 12px; margin: 2px 0;">
            Presiona el botón de abajo, concede los permisos de micrófono y habla. Tu voz se convertirá en texto automáticamente sin bloqueos de iframe.
        </p>
    </div>
</body>
</html>
"""
st.components.v1.html(y2k_header, height=185)

# ---------------------------------------------------------
# CAPTURA DE MICRÓFONO CON STREAMLIT-BOKEH-EVENTS
# ---------------------------------------------------------
st.markdown("### 🎙️ 1. Captura de Voz:")

stt_button = Button(label="🎙️ HABLAR POR EL MICRÓFONO", width=300)
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'es-ES';

    recognition.onresult = function (e) {
        var value = e.results[0][0].transcript;
        document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
    }

    recognition.onerror = function (e) {
        document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: "ERROR_MIC"}));
    }

    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=70,
)

captured_text = ""
if result and "GET_TEXT" in result:
    text_received = result.get("GET_TEXT")
    if text_received == "ERROR_MIC":
        st.error("❌ No se pudo acceder al micrófono o no se detectó audio.")
    else:
        captured_text = text_received
        st.success(f"✅ Voz reconocida: **{captured_text}**")

# ---------------------------------------------------------
# DICCIONARIO DE IDIOMAS (Compatible con googletrans / gTTS)
# ---------------------------------------------------------
LANGUAGES = {
    "🇺🇸 Inglés": ("en", "com"),
    "🇫🇷 Francés": ("fr", "fr"),
    "🇮🇹 Italiano": ("it", "it"),
    "🇩🇪 Alemán": ("de", "de"),
    "🇵🇹 Portugués": ("pt", "pt"),
    "🇷🇺 Ruso": ("ru", "ru"),
    "🇯🇵 Japonés": ("ja", "co.jp"),
    "🇨🇳 Chino (Mandarín)": ("zh-cn", "com"),
    "🇰🇷 Coreano": ("ko", "co.kr"),
    "🇦🇪 Árabe": ("ar", "com"),
    "🇪🇸 Español": ("es", "com.mx")
}

# ---------------------------------------------------------
# FORMULARIO DE TRADUCCIÓN
# ---------------------------------------------------------
with st.form(key="translator_form"):
    st.markdown("### 📝 2. Texto a traducir:")
    user_input = st.text_area(
        label="Texto de entrada",
        value=captured_text,
        height=100,
        placeholder="Habla por el micrófono o escribe directamente aquí...",
        label_visibility="collapsed"
    )

    st.markdown("### 🌍 3. Seleccionar Idioma Destino:")
    selected_lang = st.selectbox(
        "Idioma",
        options=list(LANGUAGES.keys()),
        label_visibility="collapsed"
    )

    translate_btn = st.form_submit_button("⚡ TRADUCIR Y REPRODUCIR AUDIO")

# ---------------------------------------------------------
# PROCESAMIENTO CON GOOGLETRANS Y GTTS
# ---------------------------------------------------------
if translate_btn:
    if not user_input.strip():
        st.warning("⚠️ Primero habla por el micrófono o escribe un texto para traducir.")
    else:
        with st.spinner("Traduciendo texto y generando voz..."):
            try:
                target_code, tld_code = LANGUAGES[selected_lang]
                
                # Traducir usando la librería googletrans===4.0.0rc1
                translation_result = translator.translate(user_input, dest=target_code)
                translated_text = translation_result.text
                
                st.success(f"**Traducción en {selected_lang}:** {translated_text}")

                # Generar el audio de la traducción usando gTTS==2.2.2
                tts = gTTS(text=translated_text, lang=target_code, tld=tld_code, slow=False)
                
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                audio_bytes = fp.read()
                b64 = base64.b64encode(audio_bytes).decode()

                # Reproductor HTML5 sin restricciones de autoplay
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
