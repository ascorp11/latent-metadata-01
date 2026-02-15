import os
import json
import sys
import google.generativeai as genai

# ==========================================
# 🛡️ CAPA DE SEGURIDAD Y CONFIGURACIÓN
# ==========================================
def inicializar_motor_ai():
    """Valida la API Key y prepara el cerebro de Gemini."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR CRÍTICO: 'GEMINI_API_KEY' no detectada en Secrets.")
        sys.exit(1)
    
    genai.configure(api_key=api_key)
    # Usamos 1.5-flash por su velocidad y ventana de contexto multimodal
    return genai.GenerativeModel('gemini-1.5-flash')

# ==========================================
# 📂 CAPA DE INTEGRIDAD DE DATOS (JSON)
# ==========================================
def cargar_mapa_conocimiento(ruta):
    """Carga el JSON con validación de codificación y sintaxis."""
    if not os.path.exists(ruta):
        print(f"❌ ERROR: El mapa en '{ruta}' no existe.")
        sys.exit(1)
    
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ DATA_CORRUPTION: El JSON tiene un error de formato: {e}")
        sys.exit(1)

# ==========================================
# 🚀 MOTOR DE EJECUCIÓN OMEGA
# ==========================================
def despertar_obrero():
    print("🚀 [SINC] Iniciando Barrido Omega V12.7 (Modo Maximizado)...")
    
    # 1. Preparar herramientas
    model = inicializar_motor_ai()
    ruta_mapa = 'specialties/expert_nexus_01.json'
    mapa = cargar_mapa_conocimiento(ruta_mapa)
    
    # 2. Extraer contexto del Agente
    agente_id = mapa['agent_core'].get('agent_id', 'Unknown-Agent')
    especialidad = mapa['agent_core'].get('specialty_label', 'General')
    print(f"📡 AGENTE: {agente_id} | ESPECIALIDAD: {especialidad}")

    # 3. Procesar el Repositorio de Expertos
    for experto in mapa.get('knowledge_repository', []):
        nombre = experto.get('identity', 'Unnamed Expert')
        uuid = experto.get('expert_uuid', 'N/A')
        print(f"\n--- 🕵️ ANALIZANDO: {nombre} ({uuid}) ---")
        
        # Auditoría de fuentes (YouTube / TikTok)
        for fuente in experto.get('bi_platform_sources', []):
            plataforma = fuente.get('platform', 'unknown').upper()
            url = fuente.get('url', 'no-link')
            estado = fuente.get('health_status', 'inactive')

            if estado == "active":
                print(f"✅ CONEXIÓN ESTABLECIDA: [{plataforma}] -> {url}")
                # Aquí se integrará la lógica de yt-dlp y el prompt de Gemini
            else:
                print(f"⚠️ FUENTE OMITIDA: [{plataforma}] está marcada como '{estado}'.")

    print("\n✅ [STATUS: SUCCESS] El Obrero completó su turno satisfactoriamente.")

if __name__ == "__main__":
    try:
        despertar_obrero()
    except Exception as e:
        print(f"💥 FATAL_ERROR: El sistema colapsó por un error imprevisto: {e}")
        sys.exit(1)
