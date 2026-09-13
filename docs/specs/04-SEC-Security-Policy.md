# 04 – SEC · Política de seguridad

**Versión del documento:** 1.2  
**Baseline de referencia:** v0.2.7 / árbol v0.2.8  
**Estado:** Normativo

Norma férrea: ningún comando importa fuera de stdlib y moslib, salvo mini-moslib explícito de la app validada (`minimoslib` + `app_dir`).

Aplica a comandos de sistema, app y usuario. Core es código de confianza. tests/ pueden usar pytest.

Validación AST en runtime y en arranque (inventario sistema + usuario + apps visibles). Rechazo `[SEGURIDAD]`, texto lineal.

Sin excepción A11Y vigente. Recorte de SEC nunca silencioso.

Secretos IA: `.mos/config/.ia_wrap` e `ia_keys.json` no git, 0600, HMAC. status no lista valores. HTTP solo en moslib.core.

share ≠ publicar. Puente :17337 off por defecto; no sirve `.mos`.

Tests: test_security.py, test_all_commands_security.py, test_system_commands_security.py, test_security_minimoslib.py, test_ia_keys.py, test_ia_router.py.

Sin flags para saltar seguridad en operación normal.
