
import firebase_admin
from firebase_admin import credentials, db

# 🔐 Conectar con Firebase
cred = credentials.Certificate("poyecto-32e73-firebase-adminsdk-fbsvc-38d1aa3583.json")  # Asegúrate de tener este archivo
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://poyecto-32e73-default-rtdb.firebaseio.com/"
})

# 🔧 Limpiar correo para usarlo como clave
def limpiar_correo(correo):
    return correo.replace('.', '_').replace('@', '_')

# ✅ Registrar usuario
def registrar_usuario(correo, contraseña, nombre, edad, rol):
    correo_clave = limpiar_correo(correo)
    nodo = db.reference(rol)

    usuarios = nodo.get()
    if usuarios and correo_clave in usuarios:
        print("⚠️ Ya existe un usuario con ese correo en", rol)
        return False

    nodo.child(correo_clave).set({
        "correo": correo,
        "contraseña": contraseña,
        "nombre": nombre,
        "edad": edad,
        "rol": rol
    })

    print(f"✅ Usuario registrado exitosamente en '{rol}'.")
    return True

# ✅ Iniciar sesión
def login_usuario(correo, contraseña):
    correo_clave = limpiar_correo(correo)
    for rol in ["clientes", "cocina", "meseros"]:
        nodo = db.reference(rol)
        usuarios = nodo.get()
        if usuarios and correo_clave in usuarios:
            usuario = usuarios[correo_clave]
            if usuario["contraseña"] == contraseña:
                print(f"✅ Login exitoso. Bienvenido, {usuario['nombre']} ({rol})")
                return usuario["correo"], rol
            else:
                print("❌ Contraseña incorrecta.")
                return None, None
    print("❌ Usuario no encontrado.")
    return None, None

# ✅ Mostrar menú
def ver_menu():
    menu_ref = db.reference("menu")
    menu = menu_ref.get()

    print("\n🍽️ MENÚ DISPONIBLE:")
    for clave, datos in menu.items():
        print(f"- {datos['nombre']} ({clave})")

# ✅ Hacer pedido
def hacer_pedido(correo_usuario):
    ver_menu()
    seleccionados = input("\n🛒 Escribe los códigos de los platos separados por coma (ej: ajiaco,jugo_fresa):\n> ")
    lista_platos = [p.strip() for p in seleccionados.split(",")]

    pedidos_ref = db.reference("pedidos")
    pedidos_ref.push({
        "usuario": correo_usuario,
        "platos": lista_platos,
        "estado": "pendiente"
    })
    print("✅ Pedido enviado correctamente.")

# ✅ Ver pedidos (para cocina)
def ver_pedidos():
    pedidos_ref = db.reference("pedidos")
    pedidos = pedidos_ref.get()

    if not pedidos:
        print("📭 No hay pedidos por el momento.")
        return

    print("\n📦 PEDIDOS RECIBIDOS:")
    for pedido_id, pedido in pedidos.items():
        print(f"🧾 Pedido ID: {pedido_id}")
        print(f"👤 Usuario: {pedido['usuario']}")
        print(f"🍽️ Platos: {', '.join(pedido['platos'])}")
        print(f"📌 Estado: {pedido['estado']}\n")

# ✅ Menú según rol
def menu_por_rol(correo, rol):
    while True:
        print(f"\n🧑 Rol: {rol}")
        if rol in ["clientes", "meseros"]:
            print("1 - Ver menú")
            print("2 - Hacer pedido")
            print("3 - Cerrar sesión")
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                ver_menu()
            elif opcion == "2":
                hacer_pedido(correo)
            elif opcion == "3":
                break
            else:
                print("❌ Opción inválida.")
        elif rol == "cocina":
            print("1 - Ver pedidos recibidos")
            print("2 - Cerrar sesión")
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                ver_pedidos()
            elif opcion == "2":
                break
            else:
                print("❌ Opción inválida.")

# 🧭 Menú principal
def main():
   
    while True:
        print("\n📌 MENÚ PRINCIPAL")
        print("1 - Registrar usuario")
        print("2 - Iniciar sesión")
        print("3 - Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            correo = input("Correo: ")
            contraseña = input("Contraseña: ")
            nombre = input("Nombre: ")
            edad = input("Edad: ")
            while True:
                rol = input("Rol (clientes/cocina/meseros): ").lower()
                if rol in ["clientes", "cocina", "meseros"]:
                    break
                print("❌ Rol no válido.")
            registrar_usuario(correo, contraseña, nombre, edad, rol)

        elif opcion == '2':
            correo = input("Correo: ")
            contraseña = input("Contraseña: ")
            correo_valido, rol = login_usuario(correo, contraseña)
            if correo_valido:
                menu_por_rol(correo_valido, rol)

        elif opcion == '3':
            print("👋 ¡Hasta luego!")
            break

        else:
            print("❌ Opción inválida.")

# 🔁 Ejecutar programa
if __name__ == '__main__':
    main()
