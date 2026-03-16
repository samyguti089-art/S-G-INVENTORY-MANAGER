from supabase import create_client, Client

url = "https://vrarxbsvpogzrirjtrjf.supabase.co"
key = "sb_publishable_At5k0LO2vo3LhJZl7f9AqQ_M59TE54p"
supabase: Client = create_client(url, key)

def cargar_inventario(usuario):
    response = supabase.table("inventario").select("*").eq("usuario", usuario).execute()
    return response.data if response.data else []

def guardar_inventario(usuario, inventario):
    # Borrar inventario previo del usuario
    supabase.table("inventario").delete().eq("usuario", usuario).execute()
    # Insertar inventario nuevo
    for producto in inventario:
        producto["usuario"] = usuario
        supabase.table("inventario").insert(producto).execute()