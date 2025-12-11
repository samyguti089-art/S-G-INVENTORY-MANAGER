import streamlit as st
import pandas as pd
import json
import os

def cargar_inventario(archivo="inventario.json"):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_inventario(inventario, archivo="inventario.json"):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)



