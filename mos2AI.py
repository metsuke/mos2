import os
import sys
import base64
import time
import re
import random
import json
from datetime import datetime
from pathlib import Path

# --- INTEGRACIÓN CON MOSLIB (iarouter / ia_keys) ---
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from moslib.core import ia_keys
    HAS_IA_KEYS = True
except ImportError:
    HAS_IA_KEYS = False

try:
    import google.generativeai as genai
except ImportError:
    print("Por favor, ejecuta: pip install google-generativeai")
    sys.exit(1)

# --- RUTAS Y DIRECTORIOS DE SEGURIDAD ---
RUTA_BASE = os.path.join(os.getcwd(), "rootfs", "home", "Metsuke")
ARCHIVO_CUOTAS = os.path.join(RUTA_BASE, ".quota_state.json")
ARCHIVO_SELECCIONADOS = os.path.join(RUTA_BASE, ".selected_models.json")
ARCHIVO_HISTORIAL = os.path.join(RUTA_BASE, ".chat_history.json")

# --- GESTIÓN SEGURA DE API KEY (INTEGRADA CON IAROUTER / MOSLIB) ---
def gestionar_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key and HAS_IA_KEYS:
        try:
            api_key = ia_keys.resolve_key("google") or ia_keys.resolve_key("gemini")
            if api_key:
                print("[INFO] API Key recuperada del almacén seguro de MetsuOS (iarouter).")
        except Exception as e:
            print(f"[Aviso] No se pudo leer del almacén seguro de MetsuOS: {e}")

    if not api_key:
        api_key = input("Introduce tu GEMINI_API_KEY por primera vez: ").strip()
        if api_key:
            guardar = input("¿Quieres cifrarla y guardarla localmente de forma segura en el almacén de MetsuOS (iarouter)? (s/n): ").strip().lower()
            if guardar == 's':
                if HAS_IA_KEYS:
                    try:
                        ok, msg = ia_keys.save_key("google", api_key)
                        ia_keys.save_key("gemini", api_key)
                        print(f"[INFO] {msg}")
                    except Exception as e:
                        print(f"[Error] No se pudo guardar en el almacén seguro de iarouter: {e}")
                else:
                    print("[Aviso] moslib no disponible; no se pudo guardar en el almacén seguro.")

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

def guardar_historial_chat(chat):
    temp_file = ARCHIVO_HISTORIAL + ".tmp"
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
        with open(temp_file, "w", encoding='utf-8') as f:
            json.dump(historial_serializable, f, indent=4)
        if os.path.exists(ARCHIVO_HISTORIAL):
            os.remove(ARCHIVO_HISTORIAL)
        os.rename(temp_file, ARCHIVO_HISTORIAL)
    except Exception as e:
        print(f"[Aviso] No se pudo guardar el historial en disco: {e}")
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except:
            pass

def cargar_historial_chat():
    if os.path.exists(ARCHIVO_HISTORIAL):
        try:
            with open(ARCHIVO_HISTORIAL, "r", encoding='utf-8') as f:
                data = json.load(f)
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
            print(f"[Aviso] El historial previo estaba corrupto o incompatible. Resguardando y reiniciando limpio: {e}")
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archivo_corrupto = f"{ARCHIVO_HISTORIAL}.corrupt_{timestamp}"
                if os.path.exists(ARCHIVO_HISTORIAL):
                    os.rename(ARCHIVO_HISTORIAL, archivo_corrupto)
                    print(f"[INFO] Historial corrupto movido a: {archivo_corrupto}")
            except Exception as ex_ren:
                print(f"[Aviso] No se pudo mover el historial corrupto: {ex_ren}")
                try:
                    os.remove(ARCHIVO_HISTORIAL)
                except:
                    pass
            return []
    return []

# --- HERRAMIENTAS DE FICHEROS ---
def _resolver_ruta(ruta_relativa: str) -> str:
    """Resuelve una ruta relativa dentro del sandbox (cwd) e impide path traversal."""
    base = os.path.abspath(os.getcwd())
    destino = os.path.abspath(os.path.join(base, ruta_relativa or "."))
    if not (destino == base or destino.startswith(base + os.sep)):
        raise ValueError(f"Ruta fuera del sandbox: {ruta_relativa}")
    return destino

def listar_directorio(ruta_relativa: str = ".") -> str:
    """Lista el contenido de un directorio relativo al directorio de trabajo."""
    try:
        full_path = _resolver_ruta(ruta_relativa)
        entradas = os.listdir(full_path)
        if not entradas:
            return f"(vacío) {ruta_relativa}"
        lineas = []
        for nombre in sorted(entradas):
            ruta = os.path.join(full_path, nombre)
            marca = "/" if os.path.isdir(ruta) else ""
            lineas.append(nombre + marca)
        return "\n".join(lineas)
    except Exception as e:
        return f"Error al listar {ruta_relativa}: {str(e)}"

def leer_fichero(ruta_relativa: str) -> str:
    """Lee el contenido de texto UTF-8 de un fichero relativo al directorio de trabajo."""
    try:
        full_path = _resolver_ruta(ruta_relativa)
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error al leer {ruta_relativa}: {str(e)}"

def escribir_fichero(ruta_relativa: str, contenido: str, append: bool = False) -> str:
    """Crea un fichero si no existe y escribe (o añade) contenido de texto UTF-8."""
    try:
        full_path = _resolver_ruta(ruta_relativa)
        padre = os.path.dirname(full_path)
        if padre:
            os.makedirs(padre, exist_ok=True)
        modo = "a" if append else "w"
        with open(full_path, modo, encoding="utf-8") as f:
            f.write(contenido if contenido is not None else "")
        accion = "añadido" if append else "escrito"
        return f"OK: {accion} en {ruta_relativa} ({len(contenido or '')} chars)"
    except Exception as e:
        return f"Error al escribir {ruta_relativa}: {str(e)}"

def crear_fichero(ruta_relativa: str, contenido: str = "") -> str:
    """Crea un fichero nuevo (o lo sobrescribe) con el contenido indicado."""
    return escribir_fichero(ruta_relativa, contenido, append=False)

def crear_directorio(ruta_relativa: str) -> str:
    """Crea un directorio y sus padres si no existen."""
    try:
        full_path = _resolver_ruta(ruta_relativa)
        os.makedirs(full_path, exist_ok=True)
        return f"OK: directorio listo: {ruta_relativa}"
    except Exception as e:
        return f"Error al crear directorio {ruta_relativa}: {str(e)}"

HERRAMIENTAS = [
    listar_directorio,
    leer_fichero,
    escribir_fichero,
    crear_fichero,
    crear_directorio,
]

DISPATCH_HERRAMIENTAS = {
    "listar_directorio": listar_directorio,
    "leer_fichero": leer_fichero,
    "escribir_fichero": escribir_fichero,
    "crear_fichero": crear_fichero,
    "crear_directorio": crear_directorio,
}

def crear_modelo(nombre_modelo, system_instruction):
    return genai.GenerativeModel(
        model_name=nombre_modelo,
        tools=HERRAMIENTAS,
        system_instruction=system_instruction
    )

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
        "Usa tus herramientas para listar directorios, leer ficheros, crear directorios "
        "y escribir o crear ficheros dentro del workspace. "
        "Para crear un fichero llama a crear_fichero o escribir_fichero con ruta_relativa y contenido. "
        "Usa append=true en escribir_fichero si debes añadir texto al final. "
        "Analiza el código paso a paso y no inventes rutas fuera del directorio de trabajo."
    )

    model = crear_modelo(modelo_elegido, system_instruction)

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
                model = crear_modelo(modelo_elegido, system_instruction)
                chat = model.start_chat(history=h_prev, enable_automatic_function_calling=False)
                intentos_modelo += 1
                forzar_sigue = True
                continue

            try:
                regulador_proactivo()
                response = chat.send_message(prompt)
                exito = True
                guardar_historial_chat(chat)
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "Quota exceeded" in error_str or "PerDay" in error_str:
                    print(f"\n[!] Límite diario alcanzado para '{modelo_elegido}'. Bloqueando y rotando...")
                    bloquear_modelo_hoy(modelo_elegido)

                    indice_actual = (indice_actual + 1) % len(cola_seleccionada)
                    modelo_elegido = cola_seleccionada[indice_actual]

                    h_prev = chat.history
                    model = crear_modelo(modelo_elegido, system_instruction)
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
                        model = crear_modelo(modelo_elegido, system_instruction)
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
                        fn = DISPATCH_HERRAMIENTAS.get(fc.name)
                        if fn:
                            res = fn(**args_dict)
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
                            model = crear_modelo(modelo_elegido, system_instruction)
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
