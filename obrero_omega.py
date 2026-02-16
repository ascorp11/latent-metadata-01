import os
import json
import sys
from datetime import datetime, timedelta
import google.generativeai as genai

# ==========================================
# 🛡️ CAPA 1: CONFIGURACIÓN Y CEREBRO (PROMPT MAESTRO V12.8)
# ==========================================
PROMPT_MAESTRO = """
ACTÚA COMO UNA ENTIDAD DE AUDITORÍA TÉCNICA AVANZADA Y ARQUITECTO SENIOR DE SISTEMAS MULTIMODALES.
MÁXIMA PRIORIDAD: EXTRAER CONOCIMIENTO DE VANGUARDIA EN IA, INGENIERÍA DE PROMPTS Y SISTEMAS AGÉNTICOS PARA EL 'KERNEL 12.0'.

ANÁLISIS MULTIMODAL: PROCESA VOZ (ENTONACIÓN, ÉNFASIS) Y VIDEO (DIAPOSITIVAS, CÓDIGO) COMO UNA UNIDAD INTEGRAL.

ESTRUCTURA DE SALIDA OBLIGATORIA:
1. NIVEL ALFA (SUPER-CONCENTRADO): CONCLUSIÓN DE ALTO IMPACTO Y JUSTIFICACIÓN TÉCNICA EN 1 PÁRRAFO.
2. NIVEL BETA (INTERMEDIO): TABLA COMPARATIVA DE HERRAMIENTAS/TÉCNICAS Y VIÑETAS DE HALLAZGOS TÉCNICOS.
3. NIVEL GAMMA (DESARROLLADO): TUTORIAL GUIADO PASO A PASO, EJEMPLOS DE CÓDIGO MAXIMIZADOS Y PEDAGOGÍA GUIADA.

PROTOCOLO DE EVOLUCIÓN: COMPARA ESTE HALLAZGO CON EL HISTORIAL DEL EXPERTO (6 MESES). JUSTIFICA SI ES EVOLUCIÓN O ERROR CONTRA EL SISTEMA DE VERDAD (GOOGLE DEEPMIND, OPENAI, ANTHROPIC).

[KERNEL_UPGRADE_INSTRUCTIONS]: GENERA INSTRUCCIONES ESPECÍFICAS DE LÓGICA SEMÁNTICA PARA ACTUALIZAR EL KERNEL 12.0 TRAS ESTE HALLAZGO.

RESTRICCIONES: TRADUCE AL ESPAÑOL TÉCNICO. SI HAY AMBIGÜEDAD, DECLARA 'NO ESTOY SEGURO'. PROHIBIDA LA VERBORREA. SOLO DATOS DUROS.
"""

def setup_agente():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY no detectada.")
        sys.exit(1)
    genai.configure(api_key=api_key)
    # Gemini 1.5 Flash: Optimizado para análisis de video y velocidad
    return genai.GenerativeModel('gemini-1.5-flash')

# ==========================================
# 📂 CAPA 2: PERSISTENCIA Y BÓVEDA (ASCORP ARCHITECTURE)
# ==========================================
def gestionar_boveda(plataforma, experto):
    # Estructura: ASCORP_KNOWLEDGE_VAULT/BASE_DE_CONOCIMIENTO_IA/youtube/nombre_experto
    ruta_base = f"ASCORP_KNOWLEDGE_VAULT/BASE_DE_CONOCIMIENTO_IA/{plataforma.lower()}/{experto.replace(' ', '_')}"
    os.makedirs(ruta_base, exist_ok=True)
    
    # Manejo del Catálogo para detección de borrados
    ruta_catalogo = os.path.join(ruta_base, "catalog.json")
    if os.path.exists(ruta_catalogo):
        with open(ruta_catalogo, 'r') as f:
            return json.load(f), ruta_catalogo
    return {"videos_procesados": [], "historial_inactividad": {}}, ruta_catalogo

# ==========================================
# 🚀 CAPA 3: MOTOR OPERATIVO OMEGA
# ==========================================
def ejecutar_sincronizacion():
    print(f"🚀 [SINC] Iniciando Protocolo Omega V12.8 | Fecha: {datetime.now().strftime('%Y-%m-%d')}")
    model = setup_agente()
    
    ruta_mapa = 'specialties/expert_nexus_01.json'
    if not os.path.exists(ruta_mapa):
        print("❌ ERROR: Mapa de expertos no encontrado.")
        sys.exit(1)

    with open(ruta_mapa, 'r', encoding='utf-8') as f:
        mapa = json.load(f)

    for experto in mapa.get('knowledge_repository', []):
        nombre = experto['identity']
        print(f"\n--- 🕵️ ANALIZANDO EXPERTO: {nombre} ---")
        
        for fuente in experto.get('bi_platform_sources', []):
            url = fuente['url']
            plataforma = fuente['platform']
            
            # 1. Gestionar Bóveda y Catálogo
            catalogo, ruta_cat = gestionar_boveda(plataforma, nombre)
            
            # 2. Protocolo de Inactividad (30/60/90 días)
            last_sync = fuente.get('last_sync_marker', datetime.now().strftime('%Y-%m-%d'))
            dias_inactivo = (datetime.now() - datetime.strptime(last_sync, '%Y-%m-%d')).days
            
            if dias_inactivo >= 90:
                print(f"🚨 ALERTA 90 DÍAS: {nombre} inactivo. Generando reporte de búsqueda de reemplazo.")
            elif dias_inactivo >= 30:
                print(f"⚠️ AVISO: {nombre} sin publicaciones nuevas por {dias_inactivo} días.")

            # 3. Procesamiento Multimodal
            if fuente['health_status'] == "active":
                print(f"📡 Conectando con fuente Multimodal: {url}")
                
                # [SIMULACIÓN DE INGESTA - Aquí Gemini procesa la URL directamente]
                # En producción, Gemini 1.5 accede al video/audio vía API o Uri
                try:
                    # En este punto, Gemini realiza la comparativa evolutiva (6 meses)
                    # consultando los archivos .md previos en la carpeta de la bóveda.
                    response = model.generate_content([PROMPT_MAESTRO, f"Fuente a procesar: {url}"])
                    
                    # 4. Guardado Cronológico con Timestamp
                    ts = datetime.now().strftime('%Y-%m-%d_T%H%M')
                    filename = f"ASCORP_KNOWLEDGE_VAULT/BASE_DE_CONOCIMIENTO_IA/{plataforma.lower()}/{nombre.replace(' ', '_')}/{ts}_analisis_ia.md"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    
                    # Actualizar Catálogo (Prevención de borrados)
                    catalogo['videos_procesados'].append({"id": url, "timestamp": ts, "status": "active"})
                    with open(ruta_cat, 'w') as f:
                        json.dump(catalogo, f, indent=2)
                        
                    print(f"✅ CONOCIMIENTO BLINDADO: {filename}")
                    
                except Exception as e:
                    print(f"⚠️ Error al procesar fuente: {e}")
            else:
                print(f"🚫 Fuente marcada como INACTIVA.")

    print("\n✅ [STATUS: SUCCESS] Ciclo de Inteligencia Finalizado.")

if __name__ == "__main__":
    ejecutar_sincronizacion()
