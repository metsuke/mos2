import os
import sys
import base64
import time
import re
import random
import json
from datetime import datetime

try:
    import google.generativeai as genai
except ImportError:
    print("Por favor, ejecuta: pip install google-generativeai")
    sys.exit(1)

# --- RUTAS Y DIRECTORIOS DE SEGURIDAD ---
RUTA_BASE = os.path.join(os.getcwd(), "rootfs", "home", "Metsuke")
ARCHIVO_KEY = os.path.join(RUTA_BASE, ".gemini_vault.enc")
ARCHIVO_CUOTAS = os.path.join(RUTA_BASE, ".quota_state.json")
ARCHIVO_SELECCIONADOS = os.path.join(RUTA_BASE, ".selected_models.json")
ARCHIVO_HISTORIAL = os.path.join(RUTA_BASE, ".chat_history.json")

# --- BÓVEDA CRIPTOGRÁFICA ROBUSTA A NIVEL DE BYTES (XOR + BASE64) ---
def cifrar_bytes(datos_bytes: bytes, clave: str) -> bytes:
    clave_bytes = clave.encode('utf-8')
    resultado = bytearray()
    for i, byte in enumerate(datos_bytes):
        resultado.append(byte ^ clave_bytes[i % len(clave_bytes)])
    return base64.b64encode(bytes(resultado)).decode('utf-8')

def descifrar_bytes(cifrado_b64: str, clave: str) -> bytes:
    datos_bytes = base64.b64decode(cifrado_b64.encode('utf-8'))
    clave_bytes = clave.encode('utf-8')
    resultado = bytearray()
    for i, byte in enumerate(datos_bytes):
        resultado.append(byte ^ clave_bytes[i % len(clave_bytes)])
    return bytes(resultado)

def gestionar_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key and os.path.exists(ARCHIVO_KEY):
        print(f"[INFO] Bóveda segura encontrada en {ARCHIVO_KEY}")
        pwd = input("Introduce la contraseña para descifrar tu API Key: ").strip()
        try:
            with open(ARCHIVO_KEY, "r", encoding='utf-8') as f:
                cifrado_b64 = f.read().strip()
            api_key_bytes = descifrar_bytes(cifrado_b64, pwd)
            api_key = api_key_bytes.decode('utf-8')
            
            if not api_key.startswith("AIza"):
                print("[Error] Contraseña incorrecta o clave inválida. Borrando bóveda...")
                os.remove(ARCHIVO_KEY)
                api_key = None
        except Exception as e:
            print(f"[Error] Fallo al descifrar. Borrando bóveda...")
            if os.path.exists(ARCHIVO_KEY):
                os.remove(ARCHIVO_KEY)
            api_key = None

    if not api_key:
        api_key = input("Introduce tu GEMINI_API_KEY por primera vez: ").strip()
        guardar = input("¿Quieres cifrarla y guardarla localmente de forma segura? (s/n): ").strip().lower()
        if guardar == 's':
            pwd = input("Inventa una contraseña maestra para la bóveda: ").strip()
            os.makedirs(RUTA_BASE, exist_ok=True)
            cifrado_b64 = cifrar_bytes(api_key.encode('utf-8'), pwd)
            with open(ARCHIVO_KEY, "w", encoding='utf-8') as f:
                f.write(cifrado_b64)
            print(f"[INFO] Key guardada y cifrada de forma segura en {ARCHIVO_KEY}")
            
    return api_key

# --- GESTIÓN DE ESTADOS Y PERSISTENCIA ---
def cargar_estado_cuotas():
    if os.path.exists(ARCHIVO_CUOTAS):
        try:
            with open(ARCHIVO_CUOTAS, "r", encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def guardar_estado_cuotas(estado):
    os.makedirs(RUTA_BASE, exist_ok=True)
    with open(ARCHIVO_CUOTAS, "w", encoding='utf-8') as f:
        json.dump(estado, f, indent=4)

def modelo_esta_bloqueado_hoy(modelo):
    estado = cargar_estado_cuotas()
    hoy = datetime.now().strftime("%Y-%m-%d")
    if modelo in estado:
        if estado[modelo].get("fecha") == hoy and estado[modelo].get("bloqueado"):
            return True
    return False

def bloquear_modelo_hoy(modelo):
    estado = cargar_estado_cuotas()
    hoy = datetime.now().strftime("%Y-%m-%d")
    estado[modelo] = {"fecha": hoy, "bloqueado": True}
    guardar_estado_cuotas(estado)

def cargar_modelos_seleccionados():
    if os.path.exists(ARCHIVO_SELECCIONADOS):
        try:
            with open(ARCHIVO_SELECCIONADOS, "r", encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_modelos_seleccionados(lista):
    os.makedirs(RUTA_BASE, exist_ok=True)
    with open(ARCHIVO_SELECCIONADOS, "w", encoding='utf-8') as f:
        json.dump(lista, f, indent=4)

# Funciones para persistir el historial de chat en disco
def guardar_historial_chat(chat):
    try:
        historial_serializable = []
        for message in chat.history:
            parts_data = []
            for p in message.parts:
                if hasattr(p, 'text') and p.text:
                    parts_data.append({"text": p.text})
                elif hasattr(p, 'function_call') and p.function_call:
                    fc = p.function_call
                    parts_data.append({"function_call": {"name": fc.name, "args": dict(fc.args)}})
                elif hasattr(p, 'function_response') and p.function_response:
                    fr = p.function_response
                    parts_data.append({"function_response": {"name": fr.name, "response": dict(fr.response)}})
            historial_serializable.append({"role": message.role, "parts": parts_data})
        
        os.makedirs(RUTA_BASE, exist_ok=True)
        with open(ARCHIVO_HISTORIAL, "w", encoding='utf-8') as f:
            json.dump(historial_serializable, f, indent=4)
    except Exception as e:
        print(f"[Aviso] No se pudo guardar el historial en disco: {e}")

def cargar_historial_chat():
    if os.path.exists(ARCHIVO_HISTORIAL):
        try:
            with open(ARCHIVO_HISTORIAL, "r", encoding='utf-8') as f:
                data = json.load(f)
            # Reconstruimos objetos Content compatibles con google.generativeai
            from google.ai.generativelanguage_v1beta.types import Content, Part, FunctionCall, FunctionResponse
            
            contenido_historial = []
            for item in data:
                role = item["role"]
                parts = []
                for p_data in item["parts"]:
                    if "text" in p_data:
                        parts.append(Part.from_text(p_data["text"]))
                    elif "function_call" in p_data:
                        fc_data = p_data["function_call"]
                        fc = FunctionCall(name=fc_data["name"], args=fc_data["args"])
                        parts.append(Part(function_call=fc))
                    elif "function_response" in p_data:
                        fr_data = p_data["function_response"]
                        fr = FunctionResponse(name=fr_data["name"], response=fr_data["response"])
                        parts.append(Part(function_response=fr))
                contenido_historial.append(Content(role=role, parts=parts))
            return contenido_historial
        except Exception as e:
            print(f"[Aviso] El historial previo estaba corrupto o incompatible. Iniciando limpio: {e}")
            return []
    return []

# --- HERRAMIENTAS ---
def listar_directorio(ruta_relativa: str = ".") -> str:
    base_path = os.getcwd()
    full_path = os.path.join(base_path, ruta_relativa)
    try:
        return "\n".join(os.listdir(full_path))
    except Exception as e:
        return f"Error al listar {ruta_relativa}: {str(e)}"

def leer_fichero(ruta_relativa: str) -> str:
    base_path = os.getcwd()
    full_path = os.path.join(base_path, ruta_relativa)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error al leer {ruta_relativa}: {str(e)}"

# --- GESTOR DE RITMO Y BARRAS ---
ULTIMA_PETICION = 0

def regulador_proactivo():
    global ULTIMA_PETICION
    ahora = time.time()
    tiempo_base = 12.0
    margen_aleatorio = random.uniform(1.0, 3.0)
    tiempo_ideal = tiempo_base + margen_aleatorio
    tiempo_transcurrido = ahora - ULTIMA_PETICION
    
    if ULTIMA_PETICION > 0 and tiempo_transcurrido < tiempo_ideal:
        espera = tiempo_ideal - tiempo_transcurrido
        sys.stdout.write(f"   [~] Regulando ritmo proactivamente. Esperando {espera:.1f}s...\r")
        sys.stdout.flush()
        time.sleep(espera)
        sys.stdout.write("                                                              \r")
        sys.stdout.flush()
    ULTIMA_PETICION = time.time()

def barra_progreso_ascii(segundos):
    ancho = 40
    print(f"\n[!] Esperando liberación de cuota ({segundos}s)...")
    for i in range(segundos + 1):
        porcentaje = i / segundos if segundos > 0 else 1
        bloques = int(ancho * porcentaje)
        barra = "█" * bloques + "░" * (ancho - bloques)
        sys.stdout.write(f"\r[{barra}] {i}/{segundos}s ")
        sys.stdout.flush()
        if i < segundos:
            time.sleep(1)
    print("\n[INFO] Reanudando operación...")

# --- BUCLE PRINCIPAL ---
def main():
    print("========================================")
    print("   PUENTE TEMPORAL DE INGESTA METSUAI   ")
    print("========================================")
    
    api_key = gestionar_api_key()
    if not api_key:
        print("Se requiere la clave para funcionar. Saliendo.")
        return

    genai.configure(api_key=api_key)
    
    try:
        todos_modelos = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name.lower():
                nombre = m.name.replace('models/', '')
                if 'tts' not in nombre and 'image' not in nombre:
                    todos_modelos.append(nombre)
    except Exception as e:
        print(f"[Error] No se pudo conectar con la API: {e}")
        return
        
    if not todos_modelos:
        print("[Error] No se encontraron modelos Flash compatibles disponibles.")
        return

    cola_seleccionada = cargar_modelos_seleccionados()
    cola_seleccionada = [m for m in cola_seleccionada if m in todos_modelos]

    if not cola_seleccionada:
        print("\n[INFO] Secuencia vacía. Elige el primer modelo para arrancar:")
        for i, modelo in enumerate(todos_modelos):
            print(f"  {i + 1}. {modelo}")
        while True:
            try:
                sel = int(input("\nSelecciona el número del modelo inicial: ")) - 1
                if 0 <= sel < len(todos_modelos):
                    cola_seleccionada.append(todos_modelos[sel])
                    guardar_modelos_seleccionados(cola_seleccionada)
                    break
            except ValueError:
                pass

    indice_actual = 0
    while modelo_esta_bloqueado_hoy(cola_seleccionada[indice_actual]) and indice_actual < len(cola_seleccionada) - 1:
        indice_actual += 1

    modelo_elegido = cola_seleccionada[indice_actual]
    print(f"\n[INFO] Modelo activo: {modelo_elegido} (Secuencia total: {len(cola_seleccionada)} modelo(s))")
    
    system_instruction = (
        "Eres un asistente de IA corriendo temporalmente en un script independiente. "
        "Usa tus herramientas para leer la documentación de MetsuOS y los ficheros del repositorio "
        "con el fin de descubrir los requisitos estrictos para crear un comando nativo válido. "
        "Analiza el código paso a paso."
    )
    
    model = genai.GenerativeModel(
        model_name=modelo_elegido,
        tools=[listar_directorio, leer_fichero],
        system_instruction=system_instruction
    )
    
    # Cargamos el historial previo guardado en disco si existe
    historial_previo = cargar_historial_chat()
    chat = model.start_chat(history=historial_previo, enable_automatic_function_calling=False)
    
    if historial_previo:
        print(f"[INFO] Historial de sesión anterior recuperado con éxito ({len(historial_previo)} mensajes guardados).")

    permisos_lote = {}
    niveles_lote = {}

    print("\n[INFO] Puente establecido. Escribe 'salir' para terminar.")
    
    forzar_sigue = False

    while True:
        if not forzar_sigue:
            prompt = input(f"\n[Tú - Modelo activo: {modelo_elegido}]: ").strip()
            if prompt.lower() in ['salir', 'exit', 'quit']:
                print("[INFO] Guardando historial y cerrando puente...")
                guardar_historial_chat(chat)
                break
            if not prompt:
                continue
            ultimo_input = prompt
        else:
            prompt = f"El modelo anterior se agotó. Continúa exactamente donde lo dejaste con la tarea o análisis anterior: '{ultimo_input}'"
            forzar_sigue = False
            print(f"\n[INFO] Lanzando auto-continuación en el nuevo modelo: {modelo_elegido}...")
            
        exito = False
        intentos_modelo = 0
        
        while not exito and intentos_modelo < len(cola_seleccionada) * 2:
            if modelo_esta_bloqueado_hoy(modelo_elegido):
                print(f"\n[!] El modelo '{modelo_elegido}' está agotado hoy. Buscando siguiente en la secuencia...")
                indice_actual = (indice_actual + 1) % len(cola_seleccionada)
                modelo_elegido = cola_seleccionada[indice_actual]
                
                h_prev = chat.history
                model = genai.GenerativeModel(
                    model_name=modelo_elegido,
                    tools=[listar_directorio, leer_fichero],
                    system_instruction=system_instruction
                )
                chat = model.start_chat(history=h_prev, enable_automatic_function_calling=False)
                intentos_modelo += 1
                forzar_sigue = True
                continue

            try:
                regulador_proactivo()
                response = chat.send_message(prompt)
                exito = True
                guardar_historial_chat(chat) # Guardamos tras cada éxito
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "Quota exceeded" in error_str or "PerDay" in error_str:
                    print(f"\n[!] Límite diario alcanzado para '{modelo_elegido}'. Bloqueando y rotando...")
                    bloquear_modelo_hoy(modelo_elegido)
                    
                    indice_actual = (indice_actual + 1) % len(cola_seleccionada)
                    modelo_elegido = cola_seleccionada[indice_actual]
                    
                    h_prev = chat.history
                    model = genai.GenerativeModel(
                        model_name=modelo_elegido,
                        tools=[listar_directorio, leer_fichero],
                        system_instruction=system_instruction
                    )
                    chat = model.start_chat(history=h_prev, enable_automatic_function_calling=False)
                    intentos_modelo += 1
                    forzar_sigue = True
                    continue
                else:
                    print(f"\n[Error API/Ejecución]: {e}")
                    break
        
        if not exito:
            print("\n[!] TODOS los modelos de tu secuencia automática están agotados por hoy.")
            disponibles_extra = [m for m in todos_modelos if m not in cola_seleccionada]
            
            print("\nModelos disponibles para añadir a la secuencia:")
            if disponibles_extra:
                for idx_m, m_ext in enumerate(disponibles_extra):
                    print(f"  {idx_m + 1}. {m_ext}")
            else:
                print("  (No quedan más modelos nuevos en la API)")
            print("  N. Entrar en bucle de espera circular")

            opcion = input("\nIntroduce el número del modelo a añadir o 'N': ").strip().lower()
            
            if opcion == 'n' or opcion == '':
                print("[INFO] Entrando en bucle de espera circular sobre tu secuencia...")
                indice_actual = 0
                modelo_elegido = cola_seleccionada[indice_actual]
                barra_progreso_ascii(60)
                continue
            else:
                try:
                    idx_add = int(opcion) - 1
                    if 0 <= idx_add < len(disponibles_extra):
                        m_nuevo = disponibles_extra[idx_add]
                        cola_seleccionada.append(m_nuevo)
                        guardar_modelos_seleccionados(cola_seleccionada)
                        print(f"[+] Modelo '{m_nuevo}' añadido a tu secuencia y activado.")
                        modelo_elegido = m_nuevo
                        indice_actual = len(cola_seleccionada) - 1
                        
                        h_prev = chat.history
                        model = genai.GenerativeModel(
                            model_name=modelo_elegido,
                            tools=[listar_directorio, leer_fichero],
                            system_instruction=system_instruction
                        )
                        chat = model.start_chat(history=h_prev, enable_automatic_function_calling=False)
                        forzar_sigue = True
                except Exception as ex:
                    print(f"Opción no válida ({ex}). Reintentando ciclo...")
                continue
            
        try:
            while True:
                function_calls = [part.function_call for part in response.parts if part.function_call]
                if not function_calls:
                    break
                    
                respuestas_herramientas = []
                for fc in function_calls:
                    args_dict = dict(fc.args)
                    print(f" > [Permiso Requerido] Acción: {fc.name} | Arg: {args_dict}")
                    
                    if permisos_lote.get(fc.name, 0) > 0:
                        permisos_lote[fc.name] -= 1
                        print(f"   [Auto-aprobado] (Quedan {permisos_lote[fc.name]} permisos para '{fc.name}')")
                        conf = 's'
                    else:
                        conf_input = input("   ¿Permitir? (s = una vez / S = lote progresivo / n = denegar): ").strip()
                        if conf_input == 'S':
                            nivel_actual = niveles_lote.get(fc.name, 0) + 1
                            incremento = min(nivel_actual * 50, 500)
                            niveles_lote[fc.name] = nivel_actual
                            permisos_lote[fc.name] = incremento - 1
                            print(f"   [Lote activado Nivel {nivel_actual}] Se conceden {incremento} permisos automáticos para '{fc.name}'.")
                            conf = 's'
                        elif conf_input.lower() == 's':
                            conf = 's'
                        else:
                            conf = 'n'
                    
                    if conf == 's':
                        if fc.name == "leer_fichero":
                            res = leer_fichero(**args_dict)
                        elif fc.name == "listar_directorio":
                            res = listar_directorio(**args_dict)
                        else:
                            res = "Función no reconocida."
                    else:
                        res = "Acceso denegado por el usuario."
                        print("   - Denegado.")
                    
                    respuestas_herramientas.append({
                        "function_response": {
                            "name": fc.name,
                            "response": {"result": res}
                        }
                    })
                
                print(f"[MetsuAI]: Analizando resultados...")
                regulador_proactivo()
                
                enviado_ok = False
                intentos_tool = 0
                while not enviado_ok and intentos_tool < len(cola_seleccionada) * 2:
                    try:
                        response = chat.send_message(respuestas_herramientas)
                        enviado_ok = True
                        guardar_historial_chat(chat)
                    except Exception as err_tool:
                        err_str = str(err_tool)
                        if "429" in err_str or "Quota exceeded" in err_str or "PerDay" in err_str:
                            print(f"\n[!] Límite diario alcanzado durante herramientas en '{modelo_elegido}'. Rotando...")
                            bloquear_modelo_hoy(modelo_elegido)
                            
                            indice_actual = (indice_actual + 1) % len(cola_seleccionada)
                            modelo_elegido = cola_seleccionada[indice_actual]
                            
                            h_prev = chat.history
                            model = genai.GenerativeModel(
                                model_name=modelo_elegido,
                                tools=[listar_directorio, leer_fichero],
                                system_instruction=system_instruction
                            )
                            chat = model.start_chat(history=h_prev, enable_automatic_function_calling=False)
                            intentos_tool += 1
                            regulador_proactivo()
                            continue
                        else:
                            raise err_tool
            
            print("\n[MetsuAI]:")
            print(response.text)
            
            if hasattr(response, 'usage_metadata'):
                print(f"\n[Tokens totales usados: {response.usage_metadata.total_token_count}]")
                
        except Exception as e:
            print(f"\n[Error en bucle de herramientas]: {e}")

if __name__ == "__main__":
    main()