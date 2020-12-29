# dni_peru
Obtener el dni de una persona mediante la web de ESSALUD (PERÚ)

INSTALACIÓN
pip install -r requirements.txt

USO:
Es necesario editar las 2 últimas lineas del archivo "get_dni.py" y proporcionar la información requerida:

-Path: una carpeta existente (usada para almacenar la imagen del captcha)
-Apellido Paterno
-Apellido Materno
-Primer Nombre
-Segundo Nombre (opcional)

![alt text](https://github.com/bayusec/imagenes/raw/main/get_dni.png) 


Nota: Es necesario tener el programa tesseract para poder automatizar el envio del captcha.

Testeado en:

Linux 5.3 GNU/Linux
