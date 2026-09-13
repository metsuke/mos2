# 08 – Apps

**Versión del documento:** 1.1  
**Estado:** Normativo (implementado en producto 0.2.7)  
**Baseline:** v0.2.7  

Una app es un paquete con identidad, repo o árbol propio y comandos que corren en MOSh. No vive en moslib/commands. Imports: stdlib + moslib + mini-moslib de esa app (SEC minimoslib solo con app_dir).

Ciclo 0.2.7: install path o git, ámbito usuario o sistema, list, show, remove. Sin tienda remota.

Directorios: usuario en `.mos/apps/`; fuente en repo `apps/<id>/` (ejemplo `apps/dev`).

Prioridad ICD: sistema > app sistema > app usuario > user_. Invocación corta, id_cmd y app_id_cmd.

Tests: test_apps.py, test_cmd_loader_apps.py, test_security_minimoslib.py.
