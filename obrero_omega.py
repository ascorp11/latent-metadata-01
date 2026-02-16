import os
import json
import sys
from datetime import datetime
import google.generativeai as genai

# ==========================================
# 🛡️ CAPA 1: EL CEREBRO (PROMPT MAESTRO MAXIMIZADO V12.9)
# ==========================================
PROMPT_MAESTRO = """
ACTÚA COMO UNA ENTIDAD DE AUDITORÍA TÉCNICA AVANZADA Y ARQUITECTO SENIOR DE SISTEMAS MULTIMODALES. 
MÁXIMA PRIORIDAD: EXTRAER CONOCIMIENTO DE VANGUARDIA EN IA, INGENIERÍA DE PROMPTS Y SISTEMAS AGÉNTICOS PARA EL 'KERNEL 12.0'.

ANÁLISIS MULTIMODAL: PROCESA VOZ (ENTONACIÓN, ÉNFASIS) Y VIDEO (CÓDIGO, DIAPOSITIVAS) COMO UNIDAD INTEGRAL.

ESTRUCTURA DE SALIDA OBLIGATORIA (PEDAGOGÍA TÉCNICA):
1. NIVEL ALFA (SUPER-CONCENTRADO): CONCLUSIÓN DE ALTO IMPACTO Y JUSTIFICACIÓN TÉCNICA EN 1 PÁRRAFO.
2. NIVEL BETA (INTERMEDIO): TABLA COMPARATIVA DE HERRAMIENTAS Y VIÑETAS DE HALLAZGOS TÉCNICOS.
3. NIVEL GAMMA (DESARROLLADO): TUTORIAL GUIADO PASO A PASO Y EJEMPLOS DE CÓDIGO MAXIMIZADOS.

PROTOCOLO DE EVOLUCIÓN: TE ENTREGARÉ EL REGISTRO HISTÓRICO DEL EXPERTO (SI EXISTE). DEBES COMPARAR EL NUEVO HALLAZGO CON EL PASADO. JUSTIFICA SI ES EVOLUCIÓN TECNOLÓGICA O ERROR DEL AUTOR, VALIDANDO CONTRA EL SISTEMA DE VERDAD (GOOGLE DEEPMIND, OPENAI, ANTHROPIC).

[KERNEL_UPGRADE_INSTRUCTIONS]: GENERA INSTRUCCIONES ESPECÍFICAS DE LÓGICA SEMÁNTICA PARA ACTUALIZAR EL KERNEL 12.0 TRAS ESTE HALLAZGO.

RESTRICCIONES: TRADUCE AL ESPAÑOL TÉCNICO. SI HAY AMBIGÜEDAD, DECLARA 'NO ESTOY SEGURO'. SOLO DATOS DUROS.
"""

def setup_agente():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR CRÍTICO: GEMINI_API_KEY no detectada.")
        sys.exit(1)
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# ==========================================
# 📂 CAPA 2: LÓGICA DE PERSISTENCIA E HISTORIAL
# ==========================================
def obtener_contexto_historico(ruta_experto):
    """Busca el archivo .md más reciente para que la IA pueda comparar evolución."""
    try:
        if not os.path.exists(ruta_experto): return "Sin registros previos."
        archivos = [f for f in os.listdir(ruta_experto) if f.endswith('.md')]
        if not archivos: return "Primer análisis para este experto."
        archivos.sort(reverse=True)
        with open(os.path.join(ruta_experto, archivos[0]), 'r', encoding='utf-8') as f:
            return f"HISTORIAL PREVIO (ÚLTIMO REGISTRO):\n{f.read()[:2500]}"
    except Exception:
        return "Error al intentar leer historial previo."

def gestionar_catalogo(ruta_base, urls_actuales):
    """Detecta inconsistencias y videos borrados de la fuente original."""
    ruta_cat = os.path.join(ruta_base, "catalog.json")
    historial = {"videos": []}
    if os.path.exists(ruta_cat):
        with open(ruta_cat, 'r') as f: historial = json.load(f)
    
    urls_en_catalogo = [v['url'] for v in historial.get('videos', [])]
    for url in urls_en_catalogo:
        if url not in urls_actuales:
            print(f"⚠️ ALERTA: Video {url} ya no está disponible en la fuente. Conocimiento preservado en la bóveda.")

# ==========================================
# 🚀 CAPA 3: MOTOR OPERATIVO OMEGA (LANZAMIENTO)
# ==========================================
def ejecutar_obrero():
    print(f"🚀 [SINC] Iniciando Agente Omega V12.9 | Modo: Auditoría Multimodal")
    model = setup_agente()
    
    with open('specialties/expert_nexus_01.json', 'r', encoding='utf-8') as f:
        mapa = json.load(f)

    for experto in mapa.get('knowledge_repository', []):
        nombre = experto['identity']
        print(f"\n--- 🕵️ PROCESANDO EXPERTO: {nombre} ---")
        
        urls_actuales = [f['url'] for f in experto['bi_platform_sources']]
        
        for fuente in experto['bi_platform_sources']:
            # Lógica de fechas blindada
            last_sync_str = fuente.get('last_sync_marker', "") or datetime.now().strftime('%Y-%m-%d')
            dias_inactivo = (datetime.now() - datetime.strptime(last_sync_str, '%Y-%m-%d')).days
            
            if dias_inactivo >= 90: print(f"🚨 ALERTA 90 DÍAS: {nombre} inactivo.")

            if fuente['health_status'] == "active":
                ruta_experto = f"ASCORP_KNOWLEDGE_VAULT/BASE_DE_CONOCIMIENTO_IA/{fuente['platform'].lower()}/{nombre.replace(' ', '_')}"
                os.makedirs(ruta_experto, exist_ok=True)
                
                contexto_previo = obtener_contexto_historico(ruta_experto)
                
                print(f"📡 Ingesta Multimodal (Audio/Video): {fuente['url']}")
                try:
                    # Enlace del Prompt Maestro con el Contexto y la Fuente
                    full_prompt = f"{PROMPT_MAESTRO}\n\nCONTEXTO HISTÓRICO:\n{contexto_previo}\n\nFUENTE ACTUAL: {fuente['url']}"
                    response = model.generate_content(full_prompt)
                    
                    ts = datetime.now().strftime('%Y-%m-%d_T%H%M')
                    filename = f"{ruta_experto}/{ts}_analisis_ia.md"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"✅ CONOCIMIENTO BLINDADO: {filename}")
                except Exception as e:
                    print(f"💥 Error en procesamiento IA: {e}")
        
        # Auditoría de Borrados
        gestionar_catalogo(ruta_experto, urls_actuales)

if __name__ == "__main__":
    ejecutar_obrero()
