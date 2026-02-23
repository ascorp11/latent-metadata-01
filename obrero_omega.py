import os
import json
import sys
import traceback

# [SRE] Verificación de Integridad CFFI (PDF Pág. 13)
try:
    import curl_cffi
except ImportError as linker_error:
    print(f"ERROR CRÍTICO DEL SISTEMA ANFITRIÓN: Fallo de enlace dinámico en curl_cffi.\n"
          f"Diagnóstico Interno: {linker_error}\n"
          f"Faltan dependencias libnss3 o libnspr4 en Ubuntu.", file=sys.stderr)
    sys.exit(1)
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

# [SRE] Arquitectura 'nodriver' erradicada por directiva de rendimiento (PDF Pág. 1 y 5).
# La delegación criptográfica ahora pertenece al microservicio local en Rust.

# [SRE] Capa de Aplicación TikTok: Microservicio de Atestación (PDF Pág. 11)
from curl_cffi import requests as curl_requests

class ExtractorEvasivoTikTok:
    def __init__(self):
        self.url_firmas = "http://127.0.0.1:8080/signature"
        # [SRE] Aislamiento de Red: Enrutamiento exclusivo para TikTok
        proxy_url = os.environ.get('SOCKS5_TUNNEL', None)
        proxies_dict = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        self.sesion = curl_requests.Session(impersonate="chrome124", proxies=proxies_dict)
        self.sesion.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Referer": "https://www.tiktok.com/"
        })

    def firmar_peticion(self, url_objetivo):
        try:
            res = curl_requests.post(
                self.url_firmas, 
                json={"url": url_objetivo, "userAgent": self.sesion.headers["User-Agent"]}, 
                impersonate="chrome124"
            )
            return res.json().get("data", {}).get("signed_url") if res.status_code == 200 else None
        except:
            return None

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
        'proxy': os.environ.get('SOCKS5_TUNNEL', None),
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'extract_flat': True,
        'lazy_playlist': True,
    }

# [SRE] Evasión CFFI + Firmas Docker para TikTok (PDF Pág. 11)
    if plataforma == 'tiktok':
        opciones['impersonate'] = ImpersonateTarget(client='chrome110')
        opciones['http_headers'] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Referer': 'https://www.tiktok.com/'
        }
        # Enrutamiento de peticiones a través de la librería CFFI para evadir TLS JA3
        opciones['extractor_args'] = {'tiktok': {'app_info': '7355728856979392518'}}
        opciones['playlist_items'] = '1-15'
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
    
    # [SRE] Extracción Zero-Click activa. El pasaporte PO_TOKEN se solicitará 
    # dinámicamente al Motor BotGuard (Rust) en el puerto 4416 durante la petición.

    # Enrutamiento Residencial Opcional (PDF Evasión pág. 4)
    proxy_url = os.environ.get('PROXY_URL', None)

    # [SRE] Enrutamiento Dinámico de Armaduras (TikTok vs YouTube)
    plataforma_detectada = 'tiktok' if 'tiktok' in video_url.lower() else 'youtube'
    opciones = configurar_yt_dlp(plataforma_detectada)

    # [SRE] Invocación del Motor Docker para Firmar la URL de TikTok (PDF Pág. 13)
    if plataforma_detectada == 'tiktok':
        url_firmada = ExtractorEvasivoTikTok().firmar_peticion(video_url)
        if url_firmada: 
            video_url = url_firmada
            print("✅ [SIGILO] URL de TikTok firmada criptográficamente por Docker.")
    
    # Parámetros universales de descarga visual y sigilo
    opciones.update({
        'skip_download': True,
        'writeautomaticsub': True, 
        'sub_lang': 'en,es',
        'writethumbnail': True,
        'outtmpl': 'temp_vision',
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        'socket_timeout': 10,
        'retries': 2,
        'continuedl': False,
        'no_color': True,
        'js_runtimes': { 'node': {} }
    })

    # Inyección de Armadura YouTube BotGuard (Motor Rust)
    if plataforma_detectada == 'youtube':
        opciones['extractor_args'] = {
            'youtubetab': ['skip=webpage'],
            'youtube': ['player_skip=webpage.configs', 'visitor_data=auto', 'player_client=mweb,default'],
            'youtubepot': ['bgutilhttp:base_url=http://127.0.0.1:4416']
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

    # Cargar el escuadrón de llaves (La Hidra)
    llaves_gemini = []
    for i in range(1, 7):
        k = os.environ.get(f"GEMINI_KEY_{i}")
        if k: llaves_gemini.append(k)
    
    # Fallback por si usan la llave vieja
    if not llaves_gemini:
        k_old = os.environ.get("GEMINI_API_KEY")
        if k_old: llaves_gemini.append(k_old)
        
    if not llaves_gemini: sys.exit("❌ ERROR: No se encontró ninguna API KEY de Gemini")

    llave_actual_idx = 0
    client = genai.Client(api_key=llaves_gemini[llave_actual_idx])
    print(f"🧠 [ESCUADRÓN GEMINI]: {len(llaves_gemini)} cerebros disponibles. Iniciando con Cerebro 1.")
    
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
        # [SRE] Búsqueda heurística del índice para evitar errores [Errno 2] por espacios/versiones
        archivos_indice = glob.glob("INDICE_DE_EXPERTOS*.md")
        if not archivos_indice:
            sys.exit("❌ Error crítico: No se encontró ningún archivo que comience con INDICE_DE_EXPERTOS")
        
        indice_objetivo = archivos_indice[0]
        print(f"📄 [SISTEMA] Leyendo índice atómico desde: {indice_objetivo}")
        
        with open(indice_objetivo, 'r', encoding='utf-8') as f:
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
                    intentos_maximos = len(llaves_gemini) * 3 # 3 intentos por cada cerebro disponible
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
                                    # Lógica de Blindaje Original: Full Jitter
                                    limite_truncado = min(base_retraso * (2 ** intento), 65.0)
                                    retraso = random.uniform(1.0, limite_truncado)
                                    
                                    # NUEVO: Rotación Táctica de Cerebros
                                    llave_actual_idx = (llave_actual_idx + 1) % len(llaves_gemini)
                                    client = genai.Client(api_key=llaves_gemini[llave_actual_idx])
                                    
                                    print(f"⚠️ Cerebro saturado. Rotando al Cerebro {llave_actual_idx + 1}. Esperando sala {retraso:.1f}s (Intento {intento+1}/{intentos_maximos})...")
                                    await asyncio.sleep(retraso)
                                else:
                                    print("❌ Paciencia agotada en todos los cerebros. Omitiendo video temporalmente.")
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
