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

def obtener_candidatos_mixtos(canal_url, plataforma, ruta_base_expertos, nombre_experto):
    """
    ESTRATEGIA DE PINZA CRONOLÓGICA (Diagrama V17):
    1. Toma la Vanguardia (Lo más nuevo).
    2. Busca el video más cercano al presente que falte en la Bóveda (Rev. 01, 02...).
    """
    opciones = configurar_yt_dlp(plataforma)
    print(f"📡 Escaneando Matriz Temporal ({plataforma})...")
    
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(canal_url, download=False)
            if not info or 'entries' not in info: return []
            
            todos = list(info['entries'])
            if not todos: return []
            
            objetivos = []
            # --- PASO 1: VANGUARDIA (Prioridad Absoluta) ---
            objetivos.append(todos[0])
            
            # --- PASO 2: ARQUEOLOGÍA SECUENCIAL (Buscar el primer hueco) ---
            print("🏛️ Iniciando Arqueología Secuencial (Búsqueda de Revisiones)...")
            for vid in todos[1:]:
                # Construimos la ruta de donde DEBERÍA estar el archivo
                fecha_str = vid.get('upload_date', '20260101')
                anio = fecha_str[:4]
                titulo_clean = "".join([c if c.isalnum() else "_" for c in vid.get('title', 'video')])[:50]
                
                # Ruta: Bóveda / Plataforma / Experto / Año / Archivo.md
                ruta_check = f"{ruta_base_expertos}/{plataforma}/{nombre_experto.replace(' ', '_')}/{anio}/{fecha_str}_{titulo_clean}.md"
                
                if not os.path.exists(ruta_check):
                    objetivos.append(vid)
                    print(f"🔎 [HUECO DETECTADO]: El video '{vid.get('title')}' será la revisión de este turno.")
                    break # Solo tomamos uno para respetar el tiempo de 22 min.
            
            return objetivos
    except Exception as e:
        print(f"⚠️ Error en Pinza Cronológica: {e}")
        return []

def descargar_inteligencia_multimodal(video_url):
    """
    Extrae Metadata técnica y activa la VISIÓN descargando el Thumbnail.
    """
    opciones = {
        'quiet': True, 'skip_download': True,
        'writeautomaticsub': True, 'sub_lang': 'en,es',
        'writethumbnail': True, # 👁️ ACTIVAR VISIÓN
        'outtmpl': 'temp_vision', # Nombre temporal para la imagen
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None
    }
    
    # Limpiamos rastros visuales previos
    for f in glob.glob("temp_vision*"): 
        try: os.remove(f)
        except: pass

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(video_url, download=True) # download=True para bajar la foto
        
        # Identificamos el archivo de imagen bajado
        imagen_path = None
        for ext in ['jpg', 'webp', 'png', 'jpeg']:
            if os.path.exists(f"temp_vision.{ext}"):
                imagen_path = f"temp_vision.{ext}"
                break
        
        return info, imagen_path

# ==========================================
# 🚀 MOTOR PRINCIPAL OMEGA V17.1 (OMNISCIENTE)
# ==========================================
def ejecutar_obrero():
    print(f"🚀 [SINC V17.1] Iniciando Protocolo Omnisciente | Fábrica de Expertos")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: sys.exit("❌ ERROR: API KEY no encontrada")
    
    client = genai.Client(api_key=api_key)
    
    # Cargar Mapa de Expertos
    try:
        with open('specialties/expert_nexus_01.json', 'r', encoding='utf-8') as f:
            mapa = json.load(f)
    except Exception as e:
        sys.exit(f"❌ Error leyendo el Mapa JSON: {e}")

    # 1. SELECCIÓN DE OBJETIVOS (RULETA DE CASINO)
    expertos_del_turno = seleccionar_expertos_ruleta(mapa, max_por_turno=3)

    for experto in expertos_del_turno:
        nombre = experto['identity']
        # --- MEJORA SEMÁNTICA: Especialidad Dinámica ---
        # Si no existe el campo 'specialty' en el JSON, usa 'IA' por defecto.
        especialidad = experto.get('specialty', 'IA').replace(' ', '_').upper()
        ruta_base_especialidad = f"ASCORP_KNOWLEDGE_VAULT/{especialidad}"
        
        print(f"\n--- 🕵️ OBJETIVO: {nombre} | RAMA: {especialidad} ---")
        
        for fuente in experto.get('bi_platform_sources', []):
            if fuente.get('type') != 'channel_root': continue
            
            # 2. ESCANEO CON PINZA CRONOLÓGICA (Dibujo V17: Vanguardia + Huecos)
            candidatos = obtener_candidatos_mixtos(fuente['url'], fuente['platform'], ruta_base_especialidad, nombre)
            
            for vid in candidatos:
                video_id = vid.get('id')
                if not video_id: continue
                
                video_url = f"https://www.youtube.com/watch?v={video_id}" if fuente['platform'] == 'youtube' else vid.get('url')

                # 3. RUTA DINÁMICA POR AÑO
                fecha_str = vid.get('upload_date', datetime.now().strftime('%Y%m%d'))
                año = fecha_str[:4]
                titulo_clean = "".join([c if c.isalnum() else "_" for c in vid.get('title', 'video')])[:50]
                
                ruta_final = f"{ruta_base_especialidad}/{fuente['platform']}/{nombre.replace(' ', '_')}/{año}"
                archivo_md = f"{ruta_final}/{fecha_str}_{titulo_clean}.md"
                
                if os.path.exists(archivo_md):
                    continue
                
                # 4. EXTRACCIÓN MULTIMODAL (METADATA + VISIÓN)
                os.makedirs(ruta_final, exist_ok=True)
                print(f"🧠 [ANALIZANDO V17.1] {vid.get('title')}...")
                
                try:
                    # Bajamos metadata e imagen (Ojos activos)
                    info_rica, imagen_path = descargar_inteligencia_multimodal(video_url)
                    
                    # 5. MEMORIA EVOLUTIVA (Leer pasado histórico)
                    ruta_memoria = f"{ruta_base_especialidad}/{fuente['platform']}/{nombre.replace(' ', '_')}"
                    memoria_pasada = leer_memoria_evolutiva(ruta_memoria)
                    
                    # 6. ENSAMBLAJE DEL PROMPT OMNISCIENTE
                    anio_video = int(fecha_str[:4])
                    aviso_tempo = f"⚠️ [CONTENIDO DEL {anio_video}]" if anio_video < 2025 else "✅ [VANGUARDIA]"
                    
                    full_prompt = f"{PROMPT_MAESTRO}\n\n--- INPUTS DE CONTEXTO ---\nESPECIALIDAD: {especialidad}\n{aviso_tempo}\nMEMORIA HISTÓRICA: {memoria_pasada}\n\nMETADATA:\n{info_rica.get('description', '')}\nURL: {video_url}"
                    
                    # Llamada Multimodal a Gemini
                    inputs_gemini = [full_prompt]
                    if imagen_path and os.path.exists(imagen_path):
                        try:
                            img = Image.open(imagen_path)
                            inputs_gemini.append(img)
                        except:
                            print("⚠️ Imagen dañada, procesando solo como audio/texto.")

                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=inputs_gemini
                    )
                    
                    # 7. GUARDADO EN BÓVEDA
                    with open(archivo_md, 'w', encoding='utf-8') as f:
                        f.write(f"# {vid.get('title')}\n\n{aviso_tempo}\nLink: {video_url}\nEspecialidad: {especialidad}\n\n{response.text}")
                    
                    print(f"✅ [BÓVEDA ACTUALIZADA]: {archivo_md}")
                    pausa_tactica()
                    
                except Exception as e:
                    print(f"💥 Error procesando video: {e}")

if __name__ == "__main__":
    ejecutar_obrero()
