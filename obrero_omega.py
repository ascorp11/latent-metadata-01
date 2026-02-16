import os
import json
import sys
import time
import random
import glob
from datetime import datetime
from google import genai
from google.genai import types
import yt_dlp
from PIL import Image

# ==========================================
# 🧠 CEREBRO: PROMPT MAESTRO V17 (OMNISCIENTE - MÁXIMA DENSIDAD)
# ==========================================
PROMPT_MAESTRO = """
ACTÚA COMO ARQUITECTO DE IA SENIOR PARA EL 'KERNEL 12.7'.
ANALIZA ESTE CONTENIDO MULTIMODAL (Video Metadata + Imagen Visual + Memoria Histórica).

TU MISIÓN: DECONSTRUIR LA LÓGICA, DETECTAR OBSOLESCENCIA Y ESTRUCTURAR CONOCIMIENTO.

INPUTS DISPONIBLES:
1. METADATA: Título, transcripción y tags.
2. VISIÓN: Análisis del Thumbnail/Frame clave (Detecta código, esquemas o texto en pantalla).
3. MEMORIA EVOLUTIVA: Contexto de archivos previos del experto (Detecta contradicciones).

ESTRUCTURA DE SALIDA (MARKDOWN OPTIMIZADO PARA NOTEBOOKLM):

# [TITULO DEL VIDEO]

## 🚦 SEMÁFORO DE VIGENCIA & EVOLUCIÓN
* **Estado:** (✅ VIGENTE / ⚠️ OBSOLETO / 🔄 EN EVOLUCIÓN)
* **Análisis Evolutivo:** Compara lo dicho en este video con la "Memoria Histórica" adjunta. ¿Ha cambiado de opinión el experto? ¿La tecnología evolucionó?

## 1. SÍNTESIS EJECUTIVA (Nivel Alfa)
Resumen denso de 1 párrafo. Foco en el "Problem-Solution Fit".

## 2. ANÁLISIS VISUAL & TÉCNICO (Nivel Beta)
* **Lo que se ve:** Describe diagramas o código mostrados en la imagen adjunta.
* **Herramientas:** Lista técnica de software/librerías.
* **Secretos:** Trucos no obvios mencionados.

## 3. INGENIERÍA INVERSA (Nivel Gamma)
Explicación paso a paso de la lógica o tutorial. Usa bloques de código si aplica.

## 4. 🔗 GRAPHRAG (NODOS JSON)
```json
{
  "nodos_clave": ["Concepto A", "Concepto B"],
  "relaciones": [
{"origen": "Concepto A", "relacion": "mejora_a", "destino": "Concepto B"}
  ]
}
[KERNEL_UPGRADE_INSTRUCTIONS]
Instrucción directa y atómica para actualizar la lógica del Kernel 12.7.
"""

# ==========================================
# 🎲 LÓGICA DE CASINO & SEGURIDAD
# ==========================================
# ==========================================
# 🧩 MÓDULOS DE SOPORTE V17 (MEMORIA & ARQUEOLOGÍA)
# ==========================================

def leer_memoria_evolutiva(ruta_base_experto):
    """
    MEMORIA EVOLUTIVA: Escanea archivos anteriores del experto 
    para que Gemini detecte si ha cambiado de opinión o si la tecnología avanzó.
    """
    archivos = glob.glob(f"{ruta_base_experto}/**/*.md", recursive=True)
    if not archivos: return "Sin memoria histórica previa disponible."
    
    # Tomamos fragmentos de los últimos 3 archivos analizados del pasado
    muestras = sorted(archivos, reverse=True)[:3] 
    texto_memoria = ""
    for a in muestras:
        try:
            with open(a, 'r', encoding='utf-8') as f:
                texto_memoria += f"\n--- MEMORIA ({os.path.basename(a)}) ---\n{f.read()[:500]}..."
        except: continue
    return texto_memoria

def configurar_yt_dlp(plataforma):
    """Configuración blindada con Cookies y User-Agent específico."""
    opciones = {
        'quiet': True, 'ignoreerrors': True, 'no_warnings': True,
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        'extract_flat': True,
    }
    if plataforma == 'tiktok':
        opciones['user_agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    else:
        opciones['user_agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'
    return opciones
def pausa_tactica():
    """
    Genera una espera variable entre 60 y 120 segundos.
    Esto rompe el patrón de bot y protege la cuenta IP de GitHub.
    """
    segundos = random.randint(60, 120)
    print(f"🛡️ [SIGILO] Pausa táctica de {segundos} segundos para evitar detección...")
    time.sleep(segundos)

def seleccionar_expertos_ruleta(mapa_completo, max_por_turno=3):
    """
    Selecciona aleatoriamente 'max_por_turno' expertos para procesar hoy.
    Esto asegura que en 22 minutos no intentemos procesar todo el internet.
    """
    lista_expertos = mapa_completo.get('knowledge_repository', [])
    if len(lista_expertos) <= max_por_turno:
        return lista_expertos
    
    seleccionados = random.sample(lista_expertos, k=max_por_turno)
    print(f"🎰 [RULETA] Expertos seleccionados para este turno: {[e['identity'] for e in seleccionados]}")
    return seleccionados

def obtener_candidatos_mixtos(canal_url, plataforma):
    """
    Extrae metadata de los últimos videos sin descargar el video pesado.
    Soporta YouTube y (experimentalmente) TikTok.
    """
    # Configuración blindada para yt-dlp
    opciones = {
        'quiet': True,
        'extract_flat': True, # Solo lista, no descarga
        'ignoreerrors': True,
        'playlistend': 5, # Miramos los últimos 5 para encontrar novedades
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"📡 Escaneando frecuencia ({plataforma}): {canal_url}")
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(canal_url, download=False)
            if 'entries' in info:
                # Retornamos la lista de videos encontrados
                return list(info['entries'])
    except Exception as e:
        print(f"⚠️ Error escaneando canal: {e}")
        return []
    return []

def descargar_metadata_full(video_url):
    """Descarga descripción, tags y subtítulos automáticos para el análisis."""
    opciones = {
        'quiet': True,
        'skip_download': True,
        'writeautomaticsub': True,
        'sub_lang': 'en,es',
        'outtmpl': '%(id)s' # Nombre temporal
    }
    with yt_dlp.YoutubeDL(opciones) as ydl:
        return ydl.extract_info(video_url, download=False)

# ==========================================
# 🚀 MOTOR PRINCIPAL OMEGA V16
# ==========================================
def ejecutar_obrero():
    print(f"🚀 [SINC V16] Iniciando Protocolo Titán | Estrategia: Ruleta & Sigilo")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: sys.exit("❌ ERROR: API KEY no encontrada")
    
    client = genai.Client(api_key=api_key)
    
    # Cargar Mapa
    try:
        with open('specialties/expert_nexus_01.json', 'r', encoding='utf-8') as f:
            mapa = json.load(f)
    except Exception as e:
        sys.exit(f"❌ Error leyendo el Mapa JSON: {e}")

    # 1. SELECCIÓN DE OBJETIVOS (RULETA)
    expertos_del_turno = seleccionar_expertos_ruleta(mapa, max_por_turno=3)

    for experto in expertos_del_turno:
        nombre = experto['identity']
        print(f"\n--- 🕵️ PROCESANDO OBJETIVO: {nombre} ---")
        
        for fuente in experto.get('bi_platform_sources', []):
            if fuente.get('type') != 'channel_root': continue
            
            # 2. ESCANEO DE VANGUARDIA
            candidatos = obtener_candidatos_mixtos(fuente['url'], fuente['platform'])
            
            # Procesamos MÁXIMO 2 videos por experto en este turno (1 nuevo + 1 respaldo)
            # para respetar el presupuesto de tiempo.
            contador_videos = 0
            
            for vid in candidatos:
                if not vid or contador_videos >= 2: break
                
                video_id = vid.get('id')
                if not video_id: continue
                
                # Construcción de URL según plataforma
                if fuente['platform'] == 'youtube':
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                else:
                    video_url = vid.get('url', vid.get('webpage_url'))

                # 3. VERIFICACIÓN DE EXISTENCIA (Estructura de Carpetas por Año)
                fecha_str = vid.get('upload_date', datetime.now().strftime('%Y%m%d'))
                año = fecha_str[:4]
                titulo_clean = "".join([c if c.isalnum() else "_" for c in vid.get('title', 'video_sin_nombre')])[:50]
                
                ruta_final = f"ASCORP_KNOWLEDGE_VAULT/BASE_DE_CONOCIMIENTO_IA/{fuente['platform']}/{nombre.replace(' ', '_')}/{año}"
                archivo_md = f"{ruta_final}/{fecha_str}_{titulo_clean}.md"
                
                if os.path.exists(archivo_md):
                    print(f"⏭️  [SALTANDO] Ya existe en Bóveda: {vid.get('title')}")
                    continue
                
                # 4. EXTRACCIÓN Y ANÁLISIS (Si es contenido nuevo)
                os.makedirs(ruta_final, exist_ok=True)
                print(f"🧠 [ANALIZANDO] {vid.get('title')}...")
                
                try:
                    info_rica = descargar_metadata_full(video_url)
                    descripcion = info_rica.get('description', 'Sin descripción')
                    tags = info_rica.get('tags', [])
                    
                    # Semáforo Temporal Previo
                    anio_video = int(fecha_str[:4])
                    anio_actual = datetime.now().year
                    contexto_temporal = ""
                    if anio_video < (anio_actual - 1):
                        contexto_temporal = f"⚠️ ALERTA: Este video es del {anio_video}. Verificar obsolescencia."

                    # Inyección al Modelo
                    full_prompt = f"{PROMPT_MAESTRO}\n\n--- METADATA ---\nTITULO: {vid.get('title')}\nFECHA: {fecha_str}\nTAGS: {tags}\nDESCRIPCIÓN/TRANSCRIPT: {descripcion}\nURL: {video_url}\n{contexto_temporal}"
                    
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=full_prompt
                    )
                    
                    # 5. GUARDADO BLINDADO
                    with open(archivo_md, 'w', encoding='utf-8') as f:
                        f.write(f"# {vid.get('title')}\n\nLink: {video_url}\nFecha: {fecha_str}\n\n{response.text}")
                    
                    print(f"✅ [GUARDADO] {archivo_md}")
                    contador_videos += 1
                    
                    # 6. PAUSA DE SEGURIDAD (Jitter)
                    pausa_tactica()
                    
                except Exception as e:
                    print(f"💥 Error procesando video: {e}")

if __name__ == "__main__":
    ejecutar_obrero()
