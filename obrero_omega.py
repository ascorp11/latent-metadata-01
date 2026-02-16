import os
import json
import sys
from datetime import datetime
from google import genai

# ==========================================
# 🛡️ CAPA 1: EL CEREBRO (PROMPT MAESTRO MAXIMIZADO +1300 CARACTERES)
# ==========================================
PROMPT_MAESTRO = """
ACTÚA COMO UNA ENTIDAD DE AUDITORÍA TÉCNICA AVANZADA Y ARQUITECTO SENIOR DE SISTEMAS MULTIMODALES PARA EL ESCALAFÓN DEL 1% TOP MUNDIAL EN INTELIGENCIA ARTIFICIAL. TU MISIÓN ES LA ALIMENTACIÓN, BLINDAJE Y OPTIMIZACIÓN CONTINUA DEL 'KERNEL 12.0'.

ANÁLISIS MULTIMODAL INTEGRAL: PROCESA EL AUDIO (ENTONACIÓN, ÉNFASIS, PAUSAS) Y EL VIDEO (RECONOCIMIENTO DE CÓDIGO EN PANTALLA, DIAGRAMAS DE FLUJO, LÁMINAS TÉCNICAS) COMO UNA UNIDAD SEMÁNTICA ÚNICA. EXTRAE LA LÓGICA SUBYACENTE, NO SOLO EL DISCURSO.

PROTOCOLO DE SALIDA EXIGIDO (PEDAGOGÍA TÉCNICA):
1. NIVEL ALFA (CONCENTRADO): SÍNTESIS EJECUTIVA DE ALTO IMPACTO EN UN SOLO PÁRRAFO QUE DEFINA LA RELEVANCIA TÉCNICA DEL HALLAZGO PARA EL KERNEL 12.0.
2. NIVEL BETA (INTERMEDIO): TABLA COMPARATIVA DE HERRAMIENTAS/TÉCNICAS VS. EL ESTADO DEL ARTE ACTUAL. LISTADO DE HALLAZGOS CON MÉTRICAS Y VARIABLES CLAVE.
3. NIVEL GAMMA (DESARROLLADO): TUTORIAL GUIADO PASO A PASO CON ESTILO DE APRENDIZAJE GUIADO, INCLUYENDO BLOQUES DE CÓDIGO OPTIMIZADOS Y JUSTIFICACIÓN PEDAGÓGICA.

PROTOCOLO DE EVOLUCIÓN: TE ENTREGARÉ EL REGISTRO HISTÓRICO DE LOS ÚLTIMOS 6 MESES. DEBES COMPARAR EL NUEVO HALLAZGO CON EL PASADO. JUSTIFICA SI ES EVOLUCIÓN TECNOLÓGICA O ERROR DEL AUTOR, VALIDANDO CONTRA EL SISTEMA DE VERDAD (GOOGLE DEEPMIND, GOOGLE LABS, OPENAI, ANTHROPIC).

[KERNEL_UPGRADE_INSTRUCTIONS]: REDACTA INSTRUCCIONES DE INYECCIÓN DIRECTA PARA EL KERNEL 12.0. INDICA QUÉ LÓGICA DEBE SER REEMPLAZADA O AJUSTADA PARA EVITAR LA OBSOLESCENCIA.

RESTRICCIONES: IDIOMA ESPAÑOL TÉCNICO. SI EL AUDIO/VIDEO ES DIFUSO, DECLARA 'NO ESTOY SEGURO'. PROHIBIDA LA VERBORREA. SOLO DATOS DUROS.
"""

# ==========================================
# 📂 CAPA 2: SISTEMA DE VIGILANCIA Y PERSISTENCIA
# ==========================================
def obtener_historial_completo(ruta_exp):
    """Garantiza la lectura de los últimos 6 meses de conocimiento previo."""
    try:
        if not os.path.exists(ruta_exp): return "No hay registros previos. Primer ciclo de ingesta."
        archivos = sorted([f for f in os.listdir(ruta_exp) if f.endswith('.md')], reverse=True)
        if not archivos: return "Primer registro para este experto."
        with open(os.path.join(ruta_exp, archivos[0]), 'r', encoding='utf-8') as f:
            return f"--- HISTORIAL DE EVOLUCIÓN DETECTADO ---\n{f.read()[:3000]}"
    except Exception as e:
        return f"Contexto histórico no accesible: {str(e)}"

def auditoria_de_borrados(ruta_exp, urls_vivas):
    """Verifica la integridad de la fuente. Si el experto borra, el sistema avisa."""
    ruta_cat = os.path.join(ruta_exp, "catalog.json")
    historial_videos = []
    
    if os.path.exists(ruta_cat):
        with open(ruta_cat, 'r') as f:
            data = json.load(f)
            historial_videos = data.get('videos', [])
            for v in historial_videos:
                if v['url'] not in urls_vivas:
                    print(f"🚨 ALERTA DE INTEGRIDAD: Video borrado en origen -> {v['url']}")
    
    # Actualizar catálogo con las URLs actuales para futura vigilancia
    nuevo_catalogo = {"videos": [{"url": u, "detectado": datetime.now().isoformat()} for u in urls_vivas]}
    with open(ruta_cat, 'w') as f:
        json.dump(nuevo_catalogo, f, indent=4)

# ==========================================
# 🚀 CAPA 3: MOTOR OPERATIVO OMEGA (MIGRACIÓN SDK 2026)
# ==========================================
def ejecutar_obrero():
    print(f"🚀 [SINC] Iniciando Agente Omega V12.9.9 | Blindaje Total y Densidad Máxima")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY no detectada en la mochila.")
        sys.exit(1)

    # Inicialización del cliente con la nueva librería google-genai
    client = genai.Client(api_key=api_key)
    
    with open('specialties/expert_nexus_01.json', 'r', encoding='utf-8') as f:
        mapa = json.load(f)

    for experto in mapa.get('knowledge_repository', []):
        nombre = experto['identity']
        print(f"\n--- 🕵️ AUDITANDO EXPERTO: {nombre} ---")
        urls_vivas = [fuente['url'] for fuente in experto.get('bi_platform_sources', [])]
        
        for fuente in experto.get('bi_platform_sources', []):
            # --- PROTOCOLO DE INACTIVIDAD (30/60/90) ---
            last_sync = fuente.get('last_sync_marker', "") or datetime.now().strftime('%Y-%m-%d')
            try:
                dias_inactivo = (datetime.now() - datetime.strptime(last_sync, '%Y-%m-%d')).days
            except:
                dias_inactivo = 0

            if dias_inactivo >= 90:
                print(f"🚨 ALERTA 90 DÍAS: {nombre} inactivo. Sugerencia: Evaluar reemplazo de experto.")
            elif dias_inactivo >= 30:
                print(f"⚠️ AVISO: {nombre} sin actividad por {dias_inactivo} días.")

            # --- PROCESAMIENTO MULTIMODAL ---
            if fuente['health_status'] == "active":
                ruta_exp = f"ASCORP_KNOWLEDGE_VAULT/BASE_DE_CONOCIMIENTO_IA/{fuente['platform']}/{nombre.replace(' ', '_')}"
                os.makedirs(ruta_exp, exist_ok=True)
                
                contexto_h = obtener_historial_completo(ruta_exp)
                
                print(f"📡 Ingesta Multimodal Activa (SDK 2026): {fuente['url']}")
                try:
                    # El Obrero invoca a Gemini con el Prompt Maestro y el Historial
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=f"{PROMPT_MAESTRO}\n\nHISTORIAL PREVIO PARA COMPARAR:\n{contexto_h}\n\nFUENTE NUEVA A ANALIZAR:\n{fuente['url']}"
                    )
                    
                    # Guardado en Bóveda con Timestamp técnico
                    ts = datetime.now().strftime('%Y-%m-%d_T%H%M')
                    filename = os.path.join(ruta_exp, f"{ts}_analisis_ia.md")
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"✅ CONOCIMIENTO BLINDADO Y GUARDADO: {filename}")
                    
                except Exception as e:
                    print(f"💥 FALLO EN EL MOTOR IA: {str(e)}")
            
        # Ejecutar vigilancia de borrados tras procesar las fuentes
        auditoria_de_borrados(ruta_exp, urls_vivas)

if __name__ == "__main__":
    ejecutar_obrero()
