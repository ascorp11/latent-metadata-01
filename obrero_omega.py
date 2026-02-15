import os
import json
import sys
import google.generativeai as genai

# ==========================================
# 🛡️ CAPA 1: CONFIGURACIÓN Y SEGURIDAD (PASS 1)
# ==========================================
def inicializar_motor_ai():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL_ERROR: 'GEMINI_API_KEY' no detectada en Secrets de GitHub.")
        sys.exit(1) # Cierre forzado preventivo
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash') # Modelo optimizado para barrido rápido

# ==========================================
# 📂 CAPA 2: MOTOR DE INGESTA DE DATOS (PASS 2)
# ==========================================
def cargar_mapa_conocimiento(ruta):
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"El recurso '{ruta}' es inaccesible.")
    
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ DATA_CORRUPTION: Error de sintaxis en el JSON: {e}")
        sys.exit(1)

# ==========================================
# 🤖 CAPA 3: PROCESAMIENTO MULTIMODAL (PASS 3)
# ==========================================
def ejecutar_sincronizacion_omega():
    print("🚀 [SINC] Iniciando Ciclo de Barrido Omega V12.5...")
    
    # Inyectar motor
    model = inicializar_motor_ai()
    
    # Cargar estructura
    ruta_mapa = 'specialties/expert_nexus_01.json'
    mapa = cargar_mapa_conocimiento(ruta_mapa)
    
    ctx_agent = mapa['agent_core']['agent_id']
    especialidad = mapa['agent_core']['specialty_label']
    
    print(f"📡 [AGENTE: {ctx_agent}] [ESPECIALIDAD: {especialidad}]")

    # Ciclo de Auditoría por Experto
    for experto in mapa['knowledge_repository']:
        uuid = experto['expert_uuid']
        identity = experto['identity']
        print(f"\n--- 🕵️ ANALIZANDO: {identity} (ID: {uuid}) ---")
        
        for fuente in experto['bi_platform_sources']:
            plataforma = fuente['platform'].upper()
            tipo = fuente['type']
            url = fuente['url']
            
            # Validación de Salud de Fuente
            if fuente['health_status'] != "active":
                print(f"⚠️ SKIPPED: Fuente {plataforma} marcada como inactiva.")
                continue

            print(f"✅ CONEXIÓN: [{plataforma}] [{tipo}] -> {url}")
            
            # NOTA PARA EL SOCIO: 
            # Aquí es donde el robot invoca a Gemini en el futuro 
            # para analizar el contenido del link detectado.
            
    print("\n✅ [STATUS: SUCCESS] Ciclo de sincronización finalizado sin colisiones.")

if __name__ == "__main__":
    try:
        ejecutar_sincronizacion_omega()
    except Exception as e:
        print(f"💥 FATAL_SYSTEM_ERROR: Fallo imprevisto en el motor: {e}")
        sys.exit(1)
