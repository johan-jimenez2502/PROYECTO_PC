import firebase_admin
from firebase_admin import credentials, db

# Ruta del archivo de claves
cred = credentials.Certificate("serviceAccountKey.json")

# Inicializar la app con la URL de tu base de datos
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://la-migaja-default-rtdb.firebaseio.com'
})

# Ejemplo: guardar un usuario
ref = db.reference('usuarios')
ref.push({
    'nombre': 'María',
    'correo': 'maria@ejemplo.com',
    'rol': 'cliente'
})

print("✅ Usuario guardado con éxito")
