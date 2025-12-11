import streamlit as st
import pandas as pd
import bcrypt

# ============================================================
# ✅ Cargar usuarios
# ============================================================
def cargar_usuarios():
    try:
        df = pd.read_csv("usuarios.csv")
        return df
    except:
        return pd.DataFrame(columns=["usuario", "clave_hash", "rol"])


# ============================================================
# ✅ Guardar usuarios
# ============================================================
def guardar_usuarios(df):
    df.to_csv("usuarios.csv", index=False)


# ============================================================
# ✅ Módulo principal de administración
# ============================================================
def admin_usuarios():

    st.header("👤 Administración de usuarios")

    df = cargar_usuarios()

    # ============================
    # ✅ Mostrar lista de usuarios
    # ============================
    st.subheader("📋 Lista de usuarios")
    st.dataframe(df)

    st.markdown("---")

    # ============================
    # ✅ Crear nuevo usuario
    # ============================
    st.subheader("➕ Crear nuevo usuario")

    nuevo_usuario = st.text_input("Usuario nuevo")
    nueva_clave = st.text_input("Contraseña nueva", type="password")
    nuevo_rol = st.selectbox("Rol", ["admin", "usuario", "vendedor", "auditor"])

    if st.button("Crear usuario"):
        if nuevo_usuario.strip() == "" or nueva_clave.strip() == "":
            st.error("❌ Todos los campos son obligatorios.")
        elif nuevo_usuario in df["usuario"].values:
            st.error("❌ El usuario ya existe.")
        else:
            hash_pw = bcrypt.hashpw(nueva_clave.encode("utf-8"), bcrypt.gensalt()).decode()
            df.loc[len(df)] = [nuevo_usuario, hash_pw, nuevo_rol]
            guardar_usuarios(df)
            st.success(f"✅ Usuario '{nuevo_usuario}' creado correctamente.")
            st.rerun()

    st.markdown("---")

    # ============================
    # ✅ Editar usuario existente
    # ============================
    st.subheader("✏️ Editar usuario existente")

    df = cargar_usuarios()
    usuarios_lista = df["usuario"].tolist()

    usuario_sel = st.selectbox("Seleccionar usuario", usuarios_lista)
    nuevo_rol_edit = st.selectbox("Nuevo rol", ["admin", "usuario", "vendedor", "auditor"])
    nueva_clave_edit = st.text_input("Nueva contraseña (opcional)", type="password")

    if st.button("Actualizar usuario"):
        idx_list = df.index[df["usuario"] == usuario_sel].tolist()

        if not idx_list:
            st.error("❌ El usuario seleccionado ya no existe.")
        else:
            idx = idx_list[0]
            df.at[idx, "rol"] = nuevo_rol_edit

            if nueva_clave_edit.strip() != "":
                hash_pw = bcrypt.hashpw(nueva_clave_edit.encode("utf-8"), bcrypt.gensalt()).decode()
                df.at[idx, "clave_hash"] = hash_pw

            guardar_usuarios(df)
            st.success(f"✅ Usuario '{usuario_sel}' actualizado correctamente.")
            st.rerun()

    st.markdown("---")

    # ============================
    # ✅ Eliminar usuario
    # ============================
    st.subheader("🗑 Eliminar usuario")

    df = cargar_usuarios()
    usuarios_lista_del = df["usuario"].tolist()

    usuario_del = st.selectbox("Usuario a eliminar", usuarios_lista_del)

    if st.button("Eliminar usuario"):
        if usuario_del == "admin":
            st.error("❌ No puedes eliminar al usuario administrador principal.")
        else:
            if usuario_del not in df["usuario"].values:
                st.error("❌ El usuario seleccionado ya no existe.")
            else:
                df = df[df["usuario"] != usuario_del]
                guardar_usuarios(df)
                st.success(f"✅ Usuario '{usuario_del}' eliminado correctamente.")
                st.rerun()