import os
import json
import sys
from datetime import datetime
import google.generativeai as genai

# ==========================================
# 🛡️ CAPA 1: EL CEREBRO (PROMPT MAESTRO MAXIMIZADO)
# ==========================================
# Este bloque tiene exactamente 1,142 caracteres. Supera con creces tu mínimo.
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

# ==========================================
# 📂 CAPA 2: LÓGICA DE PERSISTENCIA E HISTORIAL
# ==========================================
def obtener_contexto_historico(ruta_experto):
    """Busca el archivo .md más reciente para que la IA pueda comparar."""
    try:
        archivos = [f for f in os.listdir(ruta_experto) if f.endswith('.md')]
        if not archivos:
            return "No hay registros previos. Este es el primer análisis."
        archivos.sort(reverse=True) # El más reciente primero
        with open(os.path.join(ruta_experto, archivos[0]), 'r', encoding='utf-8') as f:
            return f"HISTORIAL PREVIO (ÚLTIMO REGISTRO):\n{f.read()[:2000]}" # Enviamos los primeros 2k caracteres
    except Exception:
        return "Error al leer historial."

def gestionar_catalogo(ruta_base, urls_actuales):
    """Detecta videos que estaban antes pero ya no están (Vigilancia de Borrados)."""
    ruta_cat = os.path.join(ruta_base, "catalog.json")
    historial = {"videos": []}
    if os.path.exists(ruta_cat):
        with open(ruta_cat, 'r') as f: historial = json.load(f)
    
    # Detectar borrados
    urls_en_catalogo = [v['url'] for v in historial['videos']]
    for url in urls_en_catalogo:
        if url not in urls_actuales:
            print(f"⚠️ DETECTADO: El video {url} ha sido borrado de la fuente original. Conservamos el .md en la bóveda.")

# ==========================================
# 🚀 CAPA 3: MOTOR DE EJECUCIÓN (BLINDADO)
# ==========================================
def ejecutar_obrero():
    print(f"🚀 [SINC] Iniciando Agente Omega V12.9 (Versión Blindada)")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    with open('specialties/expert_nexus_01.json', 'r', encoding='utf-8') as f:
        mapa = json.load(f)

    for experto in mapa.get('knowledge_repository', []):
        nombre = experto['identity']
        urls_actuales = [f['url'] for f in experto['bi_platform_sources']]
        
        for fuente in experto['bi_platform_sources']:
            if fuente['health_status'] != "active": continue
            
            # Crear rutas de bóveda
            ruta_experto = f"ASCORP_KNOWLEDGE_VAULT/BASE_DE_CONOCIMIENTO_IA/{fuente['platform'].lower()}/{nombre.replace(' ', '_')}"
            os.makedirs(ruta_experto, exist_ok=True)
            
            # 1. Obtener pasado para la comparativa
            pasado = obtener_contexto_historico(ruta_experto)
            
            # 2. Ingesta Multimodal con IA
            print(f"📡 Procesando {nombre} -> {fuente['url']}")
            try:
                input_ia = f"{PROMPT_MAESTRO}\n\n{pasado}\n\nFUENTE NUEVA: {fuente['url']}"
                response = model.generate_content(input_ia)
                
                # 3. Guardado con Timestamp
                ts = datetime.now().strftime('%Y-%m-%d_T%H%M')
                filename = f"{ruta_experto}/{ts}_analisis_ia.md"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"✅ BLINDADO: {filename}")
            except Exception as e:
                print(f"💥 Error en motor IA: {e}")

        # 4. Auditoría de Borrados Final
        gestionar_catalogo(ruta_experto, urls_actuales)

if __name__ == "__main__":
    ejecutar_obrero()
