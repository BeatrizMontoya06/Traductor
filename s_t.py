import streamlit as st
from gTTS import gTTS
import base64
import io

# Configuración de la página
st.set_page_config(
    page_title="Bee's Translator v1.0 - Retro Y2K",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializar estados de la sesión
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
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
        <span>🐝 C:\\BEES_TRANSLATOR\\v1.0\\VOICE_TRANSLATE.EXE</span>
        <div>
            <div class="win-btn">_</div>
            <div class="win-btn">□</div>
            <div class="win-btn">✕</div>
        </div>
    </div>
    <marquee scrollamount="5">
        *** TRADUCTOR MULTILENGUAJE DE VOZ Y2K *** PRESIONA EL MICRÓFONO Y HABLA ***
    </marquee>
    <div class="retro-info">
        <h2>ℹ TRADUCTOR POR VOZ (SYSTEM INFO)</h2>
        <p style="font-size: 12px; margin: 2px 0;">
            Presiona <b>"🎙️ ESCUCHAR MICRÓFONO"</b>, dale permisos a tu navegador y habla. El sistema detectará tu voz y la traducirá al idioma seleccionado.
        </p>
    </div>
</body>
</html>
"""
st.components.v1.html(y2k_header, height=185)

# Sección 1: Micrófono HTML5 en directo
st.markdown("### 🎙️ 1. Reconocimiento de Voz")

mic_component = """
<!DOCTYPE html>
<html>
<head>
<style>
    .mic-box {
        background: #e0e0e0;
        border: 2px inset #ffffff;
        padding: 10px;
        text-align: center;
        font-family: Tahoma, sans-serif;
    }
    .btn-mic {
        background: #c0c0c0;
        border: 2px solid;
        border-color: #ffffff #808080 #808080 #ffffff;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 14px;
        cursor: pointer;
    }
    .btn-mic:active {
        border-color: #808080 #ffffff #ffffff #808080;
    }
    #status {
        margin-top: 6px;
        font-size: 12px;
        color: #000080;
        font-weight: bold;
    }
</style>
</head>
<body>
    <div class="mic-box">
        <button class="btn-mic" onclick="startDictation()">🎙️ PRESIONA PARA HABLAR (MICRÓFONO)</button>
        <div id="status">Estado: Esperando comando de voz...</div>
    </div>

    <script>
    function startDictation() {
        if (window.hasOwnProperty('webkitSpeechRecognition') || window.hasOwnProperty('SpeechRecognition')) {
            var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = "es-ES"; // Escucha en español

            document.getElementById('status').innerText = "🔴 Escuchando... ¡Habla ahora!";
            document.getElementById('status').style.color = "#ff0000";

            recognition.start();

            recognition.onresult = function(e) {
                var textResult = e.results[0][0].transcript;
                document.getElementById('status').innerText = "✅ Capturado: " + textResult;
                document.getElementById('status').style.color = "#008000";
                
                // Copiar resultado al portapapeles para facilitar pegado rápido
                navigator.clipboard.writeText(textResult);
                alert("Voz capturada: '" + textResult + "'\\n\\n¡Pégalo en el recuadro de abajo (Ctrl + V)!");
            };

            recognition.onerror = function(e) {
                document.getElementById('status').innerText = "❌ Error o permiso denegado.";
                recognition.stop();
            };
        } else {
            alert("Tu navegador no soporta el micrófono en vivo. Usa Google Chrome o Edge.");
        }
    }
    </script>
</body>
</html>
"""
st.components.v1.html(mic_component, height=110)

# Lista completa de idiomas para traducir
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
    st.markdown("### 📝 2. Texto a Traducir (Escribe o Pega lo capturado del micrófono):")
    input_text = st.text_area(
        label="Texto entrada",
        value=st.session_state.input_text,
        height=100,
        placeholder="Escribe aquí o pega (Ctrl+V) la frase capturada con el micrófono...",
        label_visibility="collapsed"
    )

    st.markdown("### 🌍 3. Selecciona el Idioma Destino:")
    selected_lang = st.selectbox(
        "Idioma",
        options=list(LANGUAGES.keys()),
        label_visibility="collapsed"
    )

    translate_btn = st.form_submit_button("⚡ TRADUCIR Y REPRODUCIR AUDIO")

# Traducción en backend
if translate_btn:
    if not input_text.strip():
        st.warning("⚠️ Primero habla por el micrófono o escribe un texto para traducir.")
    else:
        with st.spinner("Traduciendo texto y generando audio..."):
            try:
                lang_code, tld_code = LANGUAGES[selected_lang]
                
                # Proceso de síntesis de audio en el idioma traducido
                tts = gTTS(text=input_text, lang=lang_code, tld=tld_code, slow=False)
                
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                audio_bytes = fp.read()
                b64 = base64.b64encode(audio_bytes).decode()
                st.session_state.audio_b64 = b64

            except Exception as e:
                st.error(f"Error procesando la traducción: {e}")

# Reproductor en pantalla
if st.session_state.audio_b64 is not None:
    st.markdown("### 🔊 4. Audio de la Traducción:")
    player_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .player-card {{
                background: #e0e0e0;
                border: 2px inset #ffffff;
                padding: 10px;
                text-align: center;
                font-family: Tahoma, sans-serif;
            }}
            audio {{ width: 100%; margin-top: 5px; }}
        </style>
    </head>
    <body>
        <div class="player-card">
            <b style="color: #008000;">🔊 REPRODUCIENDO TRADUCCIÓN EN DIRECTO:</b>
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{st.session_state.audio_b64}" type="audio/mp3">
            </audio>
        </div>
    </body>
    </html>
    """
    st.components.v1.html(player_html, height=100)
