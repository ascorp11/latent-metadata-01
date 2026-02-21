import os
import json
import sys
import time
import random
import glob
import re  # Vector 5: Expresiones regulares
from datetime import datetime
import contextlib # [SRE] Requerido para el apagado elegante (Graceful Shutdown)
from datetime import datetime
from google import genai
from google.genai import types
import yt_dlp
# [CORRECCIÓN PDF]: Importación necesaria para evitar AssertionError en suplantación
from yt_dlp.networking.impersonate import ImpersonateTarget 
from PIL import Image
import asyncio
import logging

try:
    import nodriver as nd
except ImportError:
    print("⚠️ 'nodriver' no está instalado. El Minting autónomo fallará.")

class AutonomousPoTokenProvider:
    """Servicio de Ingeniería Inversa para Acuñación de Tokens de Origen (PDF pág. 6)."""
    def __init__(self):
        self.browser = None
        self.config = {
            'browser_executable_path': '/usr/bin/brave-browser', # [SRE] Subrogación de motor base
            'headless': True, # [SRE] Brave nativo opera seguro en headless
            'sandbox': False, 
            'browser_args': ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
        }

    async def mint_fresh_token(self, video_id):
        try:
            self.browser = await nd.start(**self.config)
            url = f"https://www.youtube.com/embed/{video_id}"
            page = await self.browser.get(url)
            await asyncio.sleep(4.5)
            
            # --- GANZÚA UNIVERSAL (SRE PDF Pág. 10) ---
            # Delegamos la búsqueda del DOM al motor V8, eludiendo la lista plana del protocolo CDP.
            script_extraccion_iframe = """
            (() => {
                try {
                    const elemento = document.querySelector('iframe');
                    if (!elemento) return null;
                    return elemento.getAttribute('src');
                } catch (error) { return null; }
            })();
            """
            url_origen = await page.evaluate(script_extraccion_iframe)
            return None
        finally:
            # PROTOCOLO ESTRICTO DE GRACEFUL SHUTDOWN (SRE PDF Pág. 6)
            if self.browser:
                # Fase 1 y 2: Cierre orgánico de pestañas y WebSocket
                if hasattr(self.browser, 'tabs'):
                    for tab in self.browser.tabs:
                        with contextlib.suppress(Exception):
                            await tab.close()
                if hasattr(self.browser, 'connection') and self.browser.connection is not None:
                    with contextlib.suppress(Exception):
                        await self.browser.connection.aclose()
                
                # Fase 3: Detención nominal
                with contextlib.suppress(Exception):
                    self.browser.stop()
                    
                # Fase 4: Aniquilación determinista con sincronización asíncrona
                if hasattr(self.browser, '_process') and self.browser._process is not None:
                    try:
                        self.browser._process.terminate()
                        # CRÍTICO: Espera bloqueante bajo el Event Loop activo
                        await asyncio.wait_for(self.browser._process.wait(), timeout=5.0)
                    except asyncio.TimeoutError:
                        self.browser._process.kill()
                        await self.browser._process.wait()
                    except Exception: pass

# ==========================================
# 🧠 CEREBRO: PROMPT MAESTRO (OMNISCIENTE - MÁXIMA DENSIDAD)
# ==========================================
PROMPT_MAESTRO = """
ACTÚA COMO UN 'RECEPTOR COGNITIVO UNIVERSAL'. TU OBJETIVO ES LA CAPTURA TOTAL SIN FILTROS.
NO RESUMAS SI ESO IMPLICA PERDER UN SOLO DATO TÉCNICO, TRUCO O REFERENCIA VISUAL.

# PROTOCOLO DE EXTRACCIÓN TOTAL:
1. DETALLE DE CARRUSELES/VISIÓN: Analiza cada elemento de la imagen adjunta. Si hay texto en pantalla, código, esquemas o productos, descríbelos con precisión milimétrica.
2. METADATA PROFUNDA: Extrae hasta el último 'hack' mencionado en la descripción del video o hashtags.
3. INFERENCIA DE INTENCIÓN: ¿Qué está tratando de vender o enseñar realmente bajo la superficie?

ESTRUCTURA DE SALIDA (DENSIDAD MÁXIMA):

# 💎 [TITULO TÉCNICO COMPLETO]

## 🎯 VALOR ESTRATÉGICO (TRANSVERSALIDAD)
* **HALLAZGO CLAVE:** (Un solo dato que justifica este video).
* **NEXO_TRANSVERSAL:** [TRANSVERSAL: SÍ] (Escribir esto solo si el conocimiento es aplicable a otras áreas).

## 📊 DECONSTRUCCIÓN TÉCNICA (NIVEL GAMA)
* **Captura Visual:** Análisis exhaustivo de la imagen adjunta (Thumbnail/Frames/Texto en carrusel).
* **Stack Tecnológico:** Lista de herramientas, IA o librerías mencionadas.
* **Algoritmos/Procesos:** Ingeniería inversa de lo enseñado.

## 📝 BITÁCORA DE DETALLES "INVISIBLE"
* Lista de consejos, 'hacks' o advertencias que el 90% de los espectadores pasaría por alto.

## 🔗 GRAPHRAG (MAPA DE CONOCIMIENTO)
```json
{
  "entidades": ["Herramienta X", "Concepto Y"],
  "axiomas": "Verdad absoluta extraída del contenido",
  "memoria": "Contradicción o evolución respecto a la memoria histórica"
}
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
        # 1. SUPLANTACIÓN AVANZADA: Perfil chrome-116:windows-10 (Cero AssertionError)
        try:
            opciones['impersonate'] = ImpersonateTarget.from_str('chrome-116:windows-10')
        except:
            pass # Fallback silencioso si la librería no soporta from_str aún
            
        # [SRE] Evasión de Datacenter: Suplantación de iPhone 15 Pro Max (Capa Móvil)
        opciones['http_headers'] = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.tiktok.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        }
        
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
            
            entradas_crudas = info.get('entries', [])
            if not entradas_crudas: return []
            
            objetivos = []
            # --- FILTRO DE CONFIANZA CERO (SRE PDF Pág. 4 y 6) ---
            # Evade el error NoneType y nodos corruptos exigiendo la existencia de la clave primaria 'id'
            todos = [
                v for v in entradas_crudas 
                if v is not None and isinstance(v, dict) and v.get('_type', 'video') in ['video', 'url', 'url_transparent'] and v.get('id') is not None
            ]
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

# Vector 5: Heurística matemática estricta
def validar_topologia_youtube(video_id: str) -> bool:
    return bool(re.match(r'^[\w-]{11}$', video_id))

async def descargar_inteligencia_multimodal(video_url):
    """
    Extrae Metadata técnica y activa la VISIÓN descargando el Thumbnail con Minting Autónomo.
    """
    video_id = video_url.split('v=')[-1] if 'v=' in video_url else video_url.split('/')[-1]
    po_token = None
    
    # Vector 5: Freno de emergencia. Nunca aplicar Minting a TikTok
    if validar_topologia_youtube(video_id):
        print(f"🤖 [MINTING]: Acuñando pasaporte PO_TOKEN in-situ para {video_id}...")
        try:
            provider = AutonomousPoTokenProvider()
            # Vector 6: Temporizador de muerte de 45s para evitar procesos zombies
            po_token = await asyncio.wait_for(provider.mint_fresh_token(video_id), timeout=45.0)
            if po_token: print("✅ [MINTING]: Pasaporte criptográfico generado.")
        except asyncio.TimeoutError:
            print("⚠️ [MINTING]: Tiempo agotado. Procediendo con modo sigilo estándar.")
        except Exception as e:
            print(f"⚠️ [MINTING]: Falla estructural: {e}")

    # Enrutamiento Residencial Opcional (PDF Evasión pág. 4)
    proxy_url = os.environ.get('PROXY_URL', None)

    opciones = {
        'quiet': True, 
        'skip_download': True,
        'writeautomaticsub': True, 
        'sub_lang': 'en,es',
        'writethumbnail': True,
        'outtmpl': 'temp_vision',
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        # --- BLINDAJE DE RED (NUEVO) ---
        'socket_timeout': 10,        # Si en 10s no hay respuesta, aborta conexión
        'retries': 2,                # Máximo 2 reintentos, no más bucles infinitos
        'continuedl': False,         # No intentar retomar descargas fallidas
        'no_color': True,
        # ------------------------------
        'js_runtimes': { 'node': {} },
        'proxy': proxy_url, 
        'extractor_args': {
            'youtube': {
                'player_client': ['mweb', 'tv', 'default'],
                # [SRE] Envoltura en lista para evitar iteración por caracteres y Warning "got w,e,b..."
                'po_token': [f"mweb+{po_token}" if po_token else "web+mn"],
                'formats': 'missing_pot'
            }
        },
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    }

    if proxy_url:
        opciones['proxy'] = proxy_url
    
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

def obtener_modelo_valido(client, target_alias="gemini-1.5-flash"):
    """[PROTOCOLO DE RESILIENCIA]: Usa 'supported_actions' según PDF pág. 7."""
    try:
        modelos = list(client.models.list())
        candidatos = [
            m for m in modelos 
            if target_alias in m.name and "generateContent" in m.supported_actions
        ]
        if candidatos:
            candidatos.sort(key=lambda x: x.name, reverse=True)
            return candidatos[0].name
        return f"models/{target_alias}"
    except Exception as e:
        print(f"⚠️ Error en descubrimiento: {e}")
        return f"models/{target_alias}"

# ==========================================
# 🚀 MOTOR PRINCIPAL OMEGA V21.0 (AUTONOMÍA & FÉNIX)
# ==========================================
async def ejecutar_obrero():
    print(f"🚀 [SINC V21.0] Iniciando Protocolo de Autonomía Total")
    
    # --- AUTO-ACTUALIZACIÓN PROACTIVA (PDF pág. 9) ---
    try:
        import subprocess
        print("📡 [SISTEMA]: Purgando caché de red y descargando antídotos...")
        # Rutina 1: Limpiar caché de red para evitar sesiones corruptas
        subprocess.run(["yt-dlp", "--rm-cache-dir"], check=False)
        # Rutina 2: Actualizar a la última versión nocturna
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "--pre", "yt-dlp[default]"], check=True)
    except Exception as e:
        print(f"⚠️ Aviso: Omitiendo auto-actualización ({e})")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: sys.exit("❌ ERROR: API KEY no encontrada")
    
    client = genai.Client(api_key=api_key)
    
    # --- PROTOCOLO DE BOOTSTRAP BLINDADO (PDF pág. 8) ---
    # Interroga el catálogo para evitar error 404 y asegura prefijo models/
    modelo_inteligente = obtener_modelo_valido(client)
    
    try:
        # Pre-flight Check: Operación nula (ping) para validar estado de cuota
        client.models.generate_content(
            model=modelo_inteligente,
            contents="ping",
            config=types.GenerateContentConfig(max_output_tokens=1)
        )
        print(f"✅ [SISTEMA]: Conexión con Gemini ({modelo_inteligente}) exitosa.")
    except Exception as e:
        # Detección de Cuota 0 (Resource Exhausted) 
        if "429" in str(e):
            sys.exit("❌ ERROR: Cuota de API agotada (Nivel 0). Revisa facturación en Google Cloud.")
        else:
            print(f"⚠️ Advertencia de conexión inicial: {e}")
    
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
                    info_rica, imagen_path = await descargar_inteligencia_multimodal(video_url)
                    
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
                    # Vector 2: Paciencia Programada y Retroceso Exponencial (SRE PDF Pág. 9-10)
                    intentos_maximos = 6
                    base_retraso = 2.0
                    for intento in range(intentos_maximos):
                        try:
                            response = client.models.generate_content(
                                model='gemini-2.5-flash',
                                contents=inputs_gemini
                            )
                            break # Éxito en la respuesta, rompemos el bucle de espera
                        except Exception as e_cuota:
                            if "429" in str(e_cuota) or "RESOURCE_EXHAUSTED" in str(e_cuota):
                                if intento < intentos_maximos - 1:
                                    # Full Jitter: Espera matemática desincronizada
                                    limite_truncado = min(base_retraso * (2 ** intento), 65.0)
                                    retraso = random.uniform(1.0, limite_truncado)
                                    print(f"⚠️ Consultor Gemini ocupado (429). Esperando en sala {retraso:.1f}s (Intento {intento+1}/{intentos_maximos})...")
                                    await asyncio.sleep(retraso)
                                else:
                                    print("❌ Paciencia agotada. El consultor no responde. Omitiendo video temporalmente.")
                                    raise e_cuota
                            else:
                                raise e_cuota # Error semántico, no de cuota                  
                    
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
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(ejecutar_obrero())
    except KeyboardInterrupt:
        print("\nDespliegue finalizado manualmente.")
