import os

# Ruta donde está instalado gettext (comprueba la tuya)
gettext_path = r"C:\Program Files\gettext\bin"  

# Agrega la ruta al PATH del sistema
os.environ["PATH"] = gettext_path + os.pathsep + os.environ["PATH"]

print("✅ PATH actualizado correctamente.")