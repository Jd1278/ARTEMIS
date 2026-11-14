# Revisión del material recibido
Se leyó el DOCX completo, tablas incluidas, y se inspeccionaron README, diccionario, informe, fuentes y scripts de generación, limpieza y validación. El paquete se llama artemis-sleep-dataset (singular).

Hallazgos: diccionario declara 14612 filas, informe 20080; el recuento real está en dataset-audit.json. Escalas reales: Samn–Perelli 1–7 y estrés VAS 0–100. clean.py interpola bidireccionalmente y utiliza días 8–21 para referencias de toda la misión, lo que introduce información futura en días tempranos. Sus columnas derivadas quedan excluidas. Su límite de interpolación no prueba por sí solo que todo hueco rellenado tenga longitud total menor o igual a dos.

Los flags son por fila pero incluyen nombres de variables: el adaptador los interpreta por indicador. Los valores imputados se excluyen y conservan para auditoría. La validación heredada prueba semejanza con supuestos y algunos controles, no validación clínica; validate.py imprime fallos sin garantizar código de salida no cero. No se ejecutó el pipeline que sobrescribe originales ni se verificó de nuevo en NASA cada transformación científica. Fuentes públicas P1 quedan pendientes de esa auditoría.

El paquete mezcla radiación histórica repetida por tripulante, observaciones reales y simulaciones; contar filas no equivale a contar muestras independientes. No se adoptan porcentaje de límite de carrera, countermeasures ni risk_score como resultados personales. Originales conservados fuera de la aplicación.
