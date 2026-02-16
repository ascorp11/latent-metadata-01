import os
import json
import sys
from datetime import datetime
import google.generativeai as genai

# ==========================================
# 🛡️ CAPA 1: CONFIGURACIÓN Y CEREBRO
# ==========================================
PROMPT_MAESTRO = """
ACTÚA COMO UNA ENTIDAD DE AUDITORÍA TÉCNICA AVANZADA Y ARQUITECTO SENIOR DE SISTEMAS MULTIMODALES.
MÁXIMA PRIORIDAD: EXTRAER CONOCIMIENTO DE VANGUARDIA EN IA, INGENIERÍA DE PROMPTS Y SISTEMAS AGÉNTICOS PARA EL 'KERNEL 12.0'.

ESTRUCTURA DE SALIDA OBLIGATORIA:
1. NIVEL ALFA (SUPER-CONCENTRADO): CONCLUSIÓN EJECUTIVA TÉCNICA EN 1 PÁRRAFO.
2. NIVEL BETA (INTERMEDIO): TABLA COMPARATIVA Y VIÑETAS TÉCNICAS.
3. NIVEL GAMMA (DESARROLLADO): TUTORIAL PASO A PASO Y PEDAGOGÍA GUIADA.

[KERNEL_UPGRADE_INSTRUCTIONS]: GENERA INSTRUCCIONES ESPECÍFICAS PARA ACTUALIZAR EL KERNEL 12.0.
"""

def setup_agente():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY no detectada.")
        sys.exit(1)
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def gestionar_boveda(plataforma, experto):
    ruta_base = f"ASCORP_KNOWLEDGE_VAULT/BASE_DE_CONOCIMIENTO_IA/{plataforma.lower()}/{experto.replace(' ', '_')}"
    os.makedirs(ruta_base, exist_ok=True)
    ruta_catalogo = os.path.join(ruta_base, "catalog.json")
    if os.path.exists(ruta_catalogo):
        with open(ruta_catalogo, 'r') as f:
            return json.load(f), ruta_catalogo
    return {"videos_procesados": [], "historial_inactividad": {}}, ruta_catalogo

# ==========================================
# 🚀 MOTOR OPERATIVO CORREGIDO (FECHAS BLINDADAS)
# ==========================================
def ejecutar_sincronizacion():
    print(f"🚀 [SINC] Iniciando Protocolo Omega V12.8.1 | Modo Auto-Curación")
    model = setup_agente()
    
    ruta_mapa = 'specialties/expert_nexus_01.json'
    if not os.path.exists(ruta_mapa):
        print("❌ ERROR: Mapa no encontrado.")
        sys.exit(1)

    with open(ruta_mapa, 'r', encoding='utf-8') as f:
        mapa = json.load(f)

    for experto in mapa.get('knowledge_repository', []):
        nombre = experto['identity']
        print(f"\n--- 🕵️ ANALIZANDO: {nombre} ---")
        
        for fuente in experto.get('bi_platform_sources', []):
            # --- CAPA DE SEGURIDAD PARA FECHAS ---
            last_sync_str = fuente.get('last_sync_marker', "")
            if not last_sync_str: # Si está vacío, usamos hoy
                last_sync_str = datetime.now().strftime('%Y-%m-%d')
            
            try:
                fecha_dt = datetime.strptime(last_sync_str, '%Y-%m-%d')
                dias_inactivo = (datetime.now() - fecha_dt).days
            except ValueError:
                dias_inactivo = 0 # Si el formato es raro, reseteamos a 0
            # -------------------------------------

            if dias_inactivo >= 90:
                print(f"🚨 ALERTA 90 DÍAS: {nombre} inactivo.")
            
            if fuente['health_status'] == "active":
                print(f"📡 Procesando: {fuente['url']}")
                try:
                    # El Obrero genera el conocimiento
                    response = model.generate_content([PROMPT_MAESTRO, f"Analiza esta fuente: {fuente['url']}"])
                    
                    # Guardado en Bóveda
                    catalogo, ruta_cat = gestionar_boveda(fuente['platform'], nombre)
                    ts = datetime.now().strftime('%Y-%m-%d_T%H%M')
                    filename = f"ASCORP_KNOWLEDGE_VAULT/BASE_DE_CONOCIMIENTO_IA/{fuente['platform'].lower()}/{nombre.replace(' ', '_')}/{ts}_analisis_ia.md"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"✅ BLINDADO: {filename}")
                except Exception as e:
                    print(f"⚠️ Error en IA: {e}")

    print("\n✅ [STATUS: SUCCESS] Ciclo completado.")

if __name__ == "__main__":
    ejecutar_sincronizacion()
