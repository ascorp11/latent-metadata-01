import os
import json
import sys
import time
import random
from datetime import datetime
from google import genai
import yt_dlp

# ==========================================
# 🧠 CEREBRO: PROMPT MAESTRO V16 (SIN RECORTES - MÁXIMA DENSIDAD)
# ==========================================
PROMPT_MAESTRO = """
ACTÚA COMO ARQUITECTO DE SISTEMAS DE IA Y AUDITOR TÉCNICO SENIOR PARA EL 'KERNEL 12.0'.
TU MISIÓN ES DECONSTRUIR EL SIGUIENTE CONTENIDO (METADATA + TRANSCRIPCIÓN) Y GENERAR UN ARTEFACTO DE CONOCIMIENTO PERDURABLE.

OBJETIVO: EXTRAER LA LÓGICA PROFUNDA, NO SOLO RESUMIR EL DISCURSO.

ESTRUCTURA DE SALIDA EXIGIDA (MARKDOWN PURO):

1.  **🚦 SEMÁFORO DE VIGENCIA:**
    * Si el contenido tiene > 1 año: "⚠️ [ADVERTENCIA HISTÓRICA]: Conceptos del año [AÑO]. Validar vigencia vs. Estado del Arte 2026."
    * Si es reciente: "✅ [VIGENTE]: Conocimiento alineado con la vanguardia actual."

2.  **NIVEL ALFA (SÍNTESIS EJECUTIVA):**
    * Resumen de alto impacto (Máximo 1 párrafo denso). ¿Qué problema resuelve esto?

3.  **NIVEL BETA (HALLAZGOS TÉCNICOS):**
    * Lista de Herramientas / Librerías / Modelos mencionados.
    * Métricas clave o benchmarks (si existen).
    * "Secretos de Oficio": Trucos o heurísticas que el experto menciona de pasada.

4.  **NIVEL GAMMA (INGENIERÍA INVERSA):**
    * Reconstrucción lógica o pseudo-código de lo explicado.
    * Tutorial paso a paso si el contenido es un "How-to".

5.  **🔗 GRAPHRAG (NODOS DE CONEXIÓN):**
    * Identifica relaciones semánticas para el Grafo de Conocimiento Futuro.
    * Formato: `[Concepto A] --tipo_relación--> [Concepto B]`
    * Ejemplo: `[RAG] --evolucionó_a--> [GraphRAG]`.

[KERNEL_UPGRADE_INSTRUCTIONS]: Redacta una instrucción de inyección directa para la base de conocimiento del usuario (Dify/Kernel). ¿Qué regla lógica debe actualizarse con esto?

RESTRICCIONES:
* Idioma: Español Técnico.
* Tono: Profesional, directo, sin "paja" (fluff).
* Si falta información, declara: "DATOS INSUFICIENTES EN FUENTE".
"""

# ==========================================
# 🎲 LÓGICA DE CASINO & SEGURIDAD
# ==========================================
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
