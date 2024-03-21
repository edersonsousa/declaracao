import tkinter as tk
from tkinter import Tk, Label, Entry, Checkbutton, W, Button, messagebox, END
from PIL import Image, ImageDraw
import re

def validar_nome_entry(new_value, nome_entry):
    # Verifica se a primeira letra é maiúscula, se não for, converte para maiúscula
    if new_value and not new_value[0].isupper():
        new_value = new_value.capitalize()
        nome_entry.delete(0, "end")
        nome_entry.insert(0, new_value)
    
    # Verifica se a entrada contém apenas letras e espaços
    if re.match(r'^[a-zA-Z\s]+$', new_value):
        return True
    else:
        return False

    
def validar_rg_entry(new_value, rg_entry):
    # Remover caracteres não numéricos do valor inserido
    new_value = ''.join(filter(str.isdigit, new_value))

    # Aplicar máscara de RG (XX.XXX.XXX-X)
    formatted_value = ""
    for i, char in enumerate(new_value):
        if i == 2 or i == 5:
            formatted_value += char + "."
        else:
            formatted_value += char
    formatted_value = formatted_value[:11]  # Limitar o comprimento máximo

    # Verificar se o RG é válido
    if len(new_value) <= 9:
        rg_entry.delete(0, END)
        rg_entry.insert(0, formatted_value)
        return True
    else:
        return False



def validar_cpf_entry(event):
    new_value = cpf_entry.get()

    # Remover caracteres não numéricos do valor inserido
    new_value = ''.join(filter(str.isdigit, new_value))

    # Aplicar máscara de CPF (XXX.XXX.XXX-XX)
    formatted_value = ""
    for i, char in enumerate(new_value):
        if i == 3 or i == 6:
            formatted_value += char + "."
        elif i == 9:
            formatted_value += char + "-"
        else:
            formatted_value += char
    formatted_value = formatted_value[:14]  # Limitar o comprimento máximo

    # Verificar se o CPF é válido
    if len(new_value) == 11:
        cpf_entry.delete(0, "end")
        cpf_entry.insert(0, formatted_value)
        return True
    else:
        return False






def limpar_campos(nome_entry, rg_entry, cpf_entry, estado_civil_combo, ato_combo, jornada_combo, lei_combo, cargo_entry, destinacao_entry, ua_entry, coordenadoria_entry, cargo_de_origem_entry, a_partir, periodo_fechado):
# Limpa o valor de todos os campos de entrada
    nome_entry.delete(0, END)
    rg_entry.delete(0, END)
    cpf_entry.delete(0, END)
    estado_civil_combo.set('')
    ato_combo.set('')
    jornada_combo.set('')
    lei_combo.set('')
    cargo_entry.delete(0, END)
    destinacao_entry.delete(0, END)
    ua_entry.delete(0, END)
    coordenadoria_entry.delete(0, END)
    cargo_de_origem_entry.delete(0, END)
    a_partir_entry.deselect()
    periodo_fechado.deselect()
    nome_entry.focus()



