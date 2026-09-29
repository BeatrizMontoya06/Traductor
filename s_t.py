import streamlit as st
from gTTS import gTTS
import base64
import io

# Configuración de la página
st.set_page_config(
    page_title="Bee's Translator v2.0 - Retro Y2K",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
        <span>🐝 C:\\BEES_TRANSLATOR\\v2.0\\TRANSLATE.EXE</span>
        <div>
            <div class="win-btn">_</div>
            <div class="win-btn">□</div>
            <div class="win-btn">✕</div>
        </div>
    </div>
    <marquee scrollamount="5">
        *** TRADUCTOR MULTILENGUAJE Y2K *** ESCRIBE TU TEXTO, SELECCIONA EL IDIOMA Y ESCÚCHALO AL INSTANTE ***
    </marquee>
    <div class="retro-info">
        <h2>ℹ INFORMACIÓN DEL SISTEMA</h2>
        <p style="font-size: 12px; margin: 2px 0;">
            Sistema de traducción y síntesis de voz en alta definición sin restricciones de hardware del navegador.
        </p>
    </div>
</body>
</html>
"""
st.components.v1.html(y2k_header, height=185)

# Diccionario de idiomas disponibles con sus códigos de configuración de voz
LANGUAGES = {
    "🇺🇸 Inglés (EE.UU.)": ("en", "com"),
    "🇬🇧 Inglés (Reino Unido)": ("en", "co.uk"),
    "🇫🇷 Francés": ("fr", "fr"),
    "🇮🇹 Italiano": ("it", "it"),
    "🇩🇪 Alemán": ("de", "de"),
    "🇵🇹 Portugués": ("pt", "pt"),
    "🇷🇺 Ruso": ("ru", "ru"),
    "🇯🇵 Japonés": ("ja", "co.jp"),
    "🇨🇳 Chino (Mandarín)": ("zh-CN", "com"),
    "🇰🇷 Coreano": ("ko", "co.kr"),
    "🇦🇪 Árabe": ("ar", "com"),
    "🇪🇸 Español (Latinoamérica)": ("es", "com.mx"),
    "🇪🇸 Español (España)": ("es", "es")
}

# Formulario principal de traducción
with st.form(key="translator_form"):
    st.markdown("### 📝 1. Ingresa el texto a traducir:")
    input_text = st.text_area(
        label="Texto de entrada",
        height=120,
        placeholder="Escribe aquí la frase que deseas traducir...",
        label_visibility="collapsed"
    )

    st.markdown("### 🌍 2. Selecciona el Idioma Destino:")
    selected_lang = st.selectbox(
        "Idioma",
        options=list(LANGUAGES.keys()),
        label_visibility="collapsed"
    )

    translate_btn = st.form_submit_button("⚡ TRADUCIR Y REPRODUCIR AUDIO")

# Procesamiento de la traducción y audio
if translate_btn:
    if not input_text.strip():
        st.warning("⚠️ Debes escribir algún texto antes de traducir.")
    else:
        with st.spinner("Traduciendo y generando audio..."):
            try:
                lang_code, tld_code = LANGUAGES[selected_lang]
                
                # Generación del archivo de audio con gTTS
                tts = gTTS(text=input_text, lang=lang_code, tld=tld_code, slow=False)
                
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                audio_bytes = fp.read()
                b64 = base64.b64encode(audio_bytes).decode()

                # Reproductor HTML5 con autoplay incrustado sin bloqueos de iframe
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
                        <div class="status">🔊 REPRODUCIENDO TRADUCCIÓN EN {selected_lang.upper()}...</div>
                        <audio controls autoplay>
                            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                            Tu navegador no soporta la reproducción de audio.
                        </audio>
                    </div>
                </body>
                </html>
                """
                st.components.v1.html(player_html, height=120)

                # Botón opcional de descarga
                st.download_button(
                    label="💾 DESCARGAR TRADUCCIÓN (.MP3)",
                    data=audio_bytes,
                    file_name="traduccion_bees.mp3",
                    mime="audio/mp3"
                )

            except Exception as e:
                st.error(f"Error al procesar la traducción: {e}")
