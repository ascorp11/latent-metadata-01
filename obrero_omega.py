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
# [CORRECCIÓN PDF]: Importación necesaria para evitar AssertionError en suplantación
from yt_dlp.networking.impersonate import ImpersonateTarget 
from PIL import Image

# ==========================================
# 🧠 CEREBRO: PROMPT MAESTRO V17.2 (OMNISCIENTE - MÁXIMA DENSIDAD)
# ==========================================
PROMPT_MAESTRO = """
ACTÚA COMO ARQUITECTO DE IA SENIOR PARA EL 'KERNEL 12.7'.
ANALIZA ESTE CONTENIDO MULTIMODAL (Video Metadata + Imagen Visual + Memoria Histórica).

TU MISIÓN: DECONSTRUIR LA LÓGICA, DETECTAR OBSOLESCENCIA Y EVALUAR VALOR TRANSVERSAL.

INPUTS DISPONIBLES:
1. METADATA: Título, transcripción y tags.
2. VISIÓN: Análisis del Thumbnail/Frame clave (Detecta código, esquemas o texto en pantalla).
3. MEMORIA EVOLUTIVA: Contexto de archivos previos del experto (Detecta contradicciones).

ESTRUCTURA DE SALIDA (MARKDOWN OPTIMIZADO PARA NOTEBOOKLM):

# [TITULO DEL VIDEO]

## 🚦 SEMÁFORO DE VIGENCIA & EVOLUCIÓN
* **Estado:** (✅ VIGENTE / ⚠️ OBSOLETO / 🔄 EN EVOLUCIÓN)
* **Análisis Evolutivo:** Compara lo dicho con la Memoria Histórica adjunta. ¿Ha cambiado de opinión el experto? ¿La tecnología evolucionó? Detecta el cambio de paradigma.

## 🧠 NEXO TRANSVERSAL
* **¿Es Transversal?:** (SÍ / NO)
* **Justificación:** ¿Por qué este hallazgo sirve a otras ramas del Kernel (SEO, IA, VENTAS, LINKEDIN)? 
* **ETIQUETA_NEXO:** [TRANSVERSAL: SÍ] (Escribir exactamente esto solo si aplica).

## 1. SÍNTESIS EJECUTIVA (Nivel Alfa)
Resumen denso de 1 párrafo. Foco en el "Problem-Solution Fit".

## 2. ANÁLISIS VISUAL & TÉCNICO (Nivel Beta)
* **Lo que se ve:** Describe diagramas o código mostrados en la imagen adjunta.
* **Herramientas:** Lista técnica de software/librerías mencionadas.
* **Secretos:** Trucos no obvios o 'hacks' mencionados.

## 3. INGENIERÍA INVERSA (Nivel Gamma)
Explicación paso a paso de la lógica o tutorial. Usa bloques de código si aplica.

## 4. 🔗 GRAPHRAG (NODOS JSON)
```json
{
  "nodos_clave": ["Concepto A"],
  "relaciones": [{"origen": "A", "relacion": "mejora", "destino": "B"}
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

def configurar_yt_dlp(plataforma='youtube'):
    # Configuración base (silenciosa y rápida)
    opciones = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'extract_flat': True,
        'lazy_playlist': True,
    }

    # --- PROTOCOLO DE EVASIÓN TIKTOK 2026 (Basado en Deep Research) ---
    if plataforma == 'tiktok':
        # 1. SUPLANTACIÓN AVANZADA: Usamos un OBJETO, no texto simple.
        # Esto corrige el fallo reportado en el PDF sobre "AssertionError".
        # [CORRECCIÓN]: Usamos Chrome 110. Según el PDF, es la versión "Funcional" 
        # cuando el entorno Linux no soporta las últimas firmas criptográficas.
        # 1. SUPLANTACIÓN: Chrome 110 (Estándar de estabilidad para Linux/GitHub Actions)
        # Si usamos una versión más nueva (ej. 120), faltan librerías criptográficas.
        opciones['impersonate'] = ImpersonateTarget(
            client='chrome',
            version='110',
            os='windows'
        )
        
        # 2. INYECCIÓN DE API MÓVIL:
        # Engañamos a TikTok para que crea que somos una App, no un navegador web.
        opciones['extractor_args'] = {
            'tiktok': {
                'api_hostname': 'api22-normal-c-useast2a.tiktokv.com',
                'app_info': '7355728856979392518' # ID genérico de App
            }
        }
        
        # 3. LÍMITE DE SEGURIDAD:
        # Solo pedimos los 15 primeros videos para no activar alarmas.
        opciones['playlist_items'] = '1-15'
        # IMPORTANTE: False para asegurar orden cronológico (Nuevo -> Viejo)
        opciones['playlistreverse'] = False 
    
    else:
        # Configuración estándar para YouTube (sin cambios)
        opciones['user_agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
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
            # --- FILTRO INTELIGENTE V17.5 (Corrige error de SurferSEO) ---
            # Aceptamos 'video', 'url' y 'url_transparent' para que no se escapen videos en listas planas
            todos = [v for v in todos if v.get('_type', 'video') in ['video', 'url', 'url_transparent']]
            # --- VÁLVULA DE SEGURIDAD (INSERCIÓN CRÍTICA) ---
            if not todos:
                print(f"⚠️ [AVISO]: No se encontraron videos válidos para {nombre_experto}. Saltando...")
                return []
            # ------------------------------------------------
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
        'quiet': True, 
        'skip_download': True,
        'writeautomaticsub': True, 
        'sub_lang': 'en,es',
        'writethumbnail': True,
        'outtmpl': 'temp_vision',
        # ACTIVAMOS COOKIES: Son vitales para saltar el muro de YouTube
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        # USAMOS CLIENTE WEB: Es el único que acepta cookies al 100%
        'extractor_args': {
            'youtube': {
                'player_client': ['web'],
                'po_token': 'web+mn' # Intento de bypass automático del n-challenge
            }
        },
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
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

def obtener_modelo_valido(client):
    """[BLINDAJE ANT-404]: Busca el modelo Flash disponible hoy."""
    try:
        modelos = client.models.list()
        validos = [m.name for m in modelos if "flash" in m.name and "generateContent" in m.supported_methods]
        print(f"📡 [IA CATALOG]: Modelos detectados: {validos}")
        if "models/gemini-1.5-flash-002" in validos: return "gemini-1.5-flash-002"
        if "models/gemini-1.5-flash" in validos: return "gemini-1.5-flash"
        # Mantenemos el nombre completo 'models/...' para que la API Beta no de error 404
        return validos[0] if validos else "models/gemini-1.5-flash"
    except: return "gemini-1.5-flash"

# ==========================================
# 🚀 MOTOR PRINCIPAL OMEGA V18.5 (ESTABILIDAD)
# ==========================================
def ejecutar_obrero():
    print(f"🚀 [SINC V17.1] Iniciando Protocolo Omnisciente | Fábrica de Expertos")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: sys.exit("❌ ERROR: API KEY no encontrada")
    
    client = genai.Client(api_key=api_key)
    
    # --- DETECCIÓN DINÁMICA DE MODELO ---
    modelo_inteligente = obtener_modelo_valido(client)
    print(f"🤖 [IA]: Usando modelo auto-detectado: {modelo_inteligente}")
    
    expertos_totales = []
    try:
        with open('INDICE_DE_EXPERTOS.md', 'r', encoding='utf-8') as f:
            for linea in f:
                if '|' in linea and 'http' in linea:
                    columnas = [c.strip() for c in linea.split('|')]
                    nombre = columnas[1].replace('**', '')
                    especialidad = columnas[2]
                    # Ajustamos los índices porque ahora la tabla es de solo 4 columnas
                    yt_link = columnas[3].strip('[]') if 'http' in columnas[3] else None
                    # Si no hay link de TikTok, la última columna podría estar vacía
                    tt_link = columnas[4].strip('[]') if len(columnas) > 4 and 'http' in columnas[4] else None
                    
                    fuentes = []
                    if yt_link: fuentes.append({'type': 'channel_root', 'platform': 'youtube', 'url': yt_link})
                    if tt_link: fuentes.append({'type': 'channel_root', 'platform': 'tiktok', 'url': tt_link})
                    
                    expertos_totales.append({
                        'identity': nombre,
                        'specialty': especialidad,
                        'bi_platform_sources': fuentes
                    })
    except Exception as e:
        sys.exit(f"❌ Error crítico leyendo la Tabla MD: {e}")

    # 1. SELECCIÓN DE OBJETIVOS (RULETA DE CASINO)
    if len(expertos_totales) > 3:
        expertos_del_turno = random.sample(expertos_totales, k=3)
    else:
        expertos_del_turno = expertos_totales
    print(f"🎰 [RULETA] Turno para: {[e['identity'] for e in expertos_del_turno]}")

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

                    # CORRECCIÓN DE MODELO: Usamos la versión estable 'gemini-1.5-flash'
                    # Google eliminó la etiqueta 'latest' para la API gratuita v1beta
                    # Llamada resiliente: usa el modelo que el Obrero detectó al inicio
                    response = client.models.generate_content(
                        model=modelo_inteligente,
                        contents=inputs_gemini
                    )                  
                    
                    # --- 7. MOTOR DE GUARDADO V17.3 (EXPERTO + NEXO + CRONÓMETRO) ---
                    
                    # LÓGICA DEL CRONÓMETRO: Medimos la antigüedad del hallazgo
                    ahora = datetime.now()
                    fecha_video = datetime.strptime(fecha_str, '%Y%m%d')
                    dias_antiguedad = (ahora - fecha_video).days
                    
                    alerta_obsolescencia = ""
                    # Umbral de Alerta: 180 días para IA/Tech, 365 para el resto
                    if (especialidad in ['IA', 'LINKEDIN'] and dias_antiguedad > 180) or dias_antiguedad > 365:
                        alerta_obsolescencia = f"⚠️ [ALERTA DE VIGENCIA]: Contenido con {dias_antiguedad} días. Riesgo de desfase.\n\n"

                    # Preparamos el contenido final una sola vez
                    contenido_final = f"# {vid.get('title')}\n\n{alerta_obsolescencia}{aviso_tempo}\nLink: {video_url}\nEspecialidad: {especialidad}\n\n{response.text}"

                    # COPIA 1: Guardado en la carpeta del experto
                    with open(archivo_md, 'w', encoding='utf-8') as f:
                        f.write(contenido_final)
                    print(f"✅ [BÓVEDA EXPERTO ACTUALIZADA]: {archivo_md}")

                    # COPIA 2 (NEXO): Solo si el Prompt detectó valor transversal
                    if "[TRANSVERSAL: SÍ]" in response.text:
                        ruta_nexo = f"ASCORP_KNOWLEDGE_VAULT/🧠_CONOCIMIENTO_TRANSVERSAL/{especialidad}"
                        os.makedirs(ruta_nexo, exist_ok=True)
                        archivo_nexo = f"{ruta_nexo}/{fecha_str}_{titulo_clean}.md"
                        
                        with open(archivo_nexo, 'w', encoding='utf-8') as f_n:
                            f_n.write(f"--- 🌐 HALLAZGO TRANSVERSAL ---\nORIGEN: {nombre}\n{contenido_final}")
                        print(f"✨ [NEXO CREADO]: {archivo_nexo}")

                    # 8. MANTENIMIENTO DE SIGILO
                    pausa_tactica()
                    
                except Exception as e:
                    print(f"💥 Error procesando video: {e}")

if __name__ == "__main__":
    ejecutar_obrero()
