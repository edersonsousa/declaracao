import tkinter as tk
from datetime import datetime
from tkinter import Tk, Label, Entry, Checkbutton, W, Button, messagebox, END ,simpledialog
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






def limpar_campos(nome_entry, rg_entry, cpf_entry, estado_civil_combo, ato_combo, jornada_combo, lei_combo, cargo_entry, 
                  destinacao_entry, ua_entry, coordenadoria_entry, cargo_de_origem_entry, 
                  a_partir_var, a_partir_checkbutton, periodo_fechado_var, periodo_fechado_checkbutton):
    # Limpa o valor de todos os campos de entrada
    nome_entry.delete(0, END)
    rg_entry.delete(0, END)
    cpf_entry.delete(0, END)
    estado_civil_combo.set('')
    ato_combo.set('')
    jornada_combo.set('')
    ato_combo["values"] = "Nomeação","Designação","Designação com posterior Nomeação"
    lei_combo.set('')
    cargo_entry.delete(0, END)
    destinacao_entry.delete(0, END)
    ua_entry.delete(0, END)
    coordenadoria_entry.delete(0, END)
    cargo_de_origem_entry.delete(0, END)
    periodo_fechado_var.set(False)
    a_partir_var.set(False)
    a_partir_checkbutton.config(state="normal")
    periodo_fechado_checkbutton.config(state="normal")
    nome_entry.delete(0, END)
    nome_entry.focus()
    nome_entry.delete(0, END)


def toggle_check_a_partir(a_partir_var, periodo_fechado_var, periodo_fechado_checkbutton, ato_combo):
    if a_partir_var.get():
        periodo_fechado_var.set(False)
        periodo_fechado_checkbutton.config(state="disabled")
        # Exibir caixa de diálogo para solicitar uma data
        user_date = simpledialog.askstring("Data", "Qual a data do a partir? Ex:(dd/mm/aaaa)")
        # Verificar se a data está no formato correto
        if user_date and len(user_date) == 10 and user_date[2] == '/' and user_date[5] == '/':
            print("Data selecionada:", user_date)
            # Use a data fornecida pelo usuário como desejar
            # Atualizar valores do Combobox
            ato_combo["values"] = "Designação", "Designação com posterior Nomeação" 
            ato_combo.config(state="normal")
            
        else:
            tk.messagebox.showerror("Erro", "Formato de data inválido. Por favor, insira uma data no formato dd/mm/aaaa.")
            toggle_check_a_partir(var, periodo_fechado_var, periodo_fechado_checkbutton, ato_combo)
    else:
        periodo_fechado_checkbutton.config(state="normal")
    
    #ato_combo["values"] = "Designação"
    


def toggle_check_periodo_fechado(periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo):
    if periodo_fechado_var.get():
        a_partir_var.set(False)
        a_partir_checkbutton.config(state="disabled")
        ato_combo["values"] = "Designação"
    else:
        a_partir_checkbutton.config(state="normal")


def ato_box_select(event, ato_combo, a_partir_var, periodo_fechado_var, a_partir_checkbutton, periodo_fechado_checkbutton):
    selected_value = ato_combo.get()
    if selected_value == "Nomeação":
        a_partir_var.set(False)
        periodo_fechado_var.set(False)
        a_partir_checkbutton.config(state=tk.DISABLED)
        periodo_fechado_checkbutton.config(state=tk.DISABLED)
    elif selected_value == "Designação com posterior Nomeação":
        periodo_fechado_var.set(False)
        a_partir_checkbutton.config(state=tk.NORMAL)
        periodo_fechado_checkbutton.config(state=tk.DISABLED)
    else:
        a_partir_checkbutton.config(state=tk.NORMAL)
        periodo_fechado_checkbutton.config(state=tk.NORMAL)


def lei_box_select(lei_combo, jornada_combo):
    selected_value = lei_combo.get()
    if selected_value == "Art.5º da lei complementar nº 1080/2008":
        jornada_combo["values"] = "Jornada Completa de Trabalho"
        jornada_combo.set("Jornada Completa de Trabalho")
    elif selected_value == "Art.8º da lei complementar nº 1157/2011":
        jornada_combo["values"] = "Jornada Básica de Trabalho", "Jornada Parcial de Trabalho", "Jornada de 30(trinta) horas de Trabalho"
        jornada_combo.focus()