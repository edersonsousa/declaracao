from tool_box import validar_nome_entry, validar_rg_entry, validar_cpf_entry, limpar_campos
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import Tk, Label, Entry, Checkbutton, W, Button, messagebox, END
from PIL import Image, ImageDraw

window = Tk()
window.title("Declarações")
window.config(padx=20, pady=25, bg="white")

# Labels
nome_label = Label(text="Nome :")
nome_label["font"] = ("Montserrat","12")
nome_label.grid(row=0, column=1, pady = 4, sticky="W")

rg_label = Label(text="RG :")
rg_label["font"] = ("Montserrat","12")
rg_label.grid(row=1, column=1, pady = 4, sticky="W")

cpf_label = Label(text="CPF :")
cpf_label["font"] = ("Montserrat","12")
cpf_label.grid(row=2, column=1, pady = 4, sticky="W")

estado_civil_label = Label(text="Estado Civil :")
estado_civil_label["font"] = ("Montserrat","12")
estado_civil_label.grid(row=3, column=1, pady = 4, sticky="W")

ato_label = Label(text="Ato :")
ato_label["font"] = ("Montserrat","12")
ato_label.grid(row=4, column=1, pady = 4, sticky="W")

jornada_label = Label(text="Jornada :")
jornada_label["font"] = ("Montserrat","12")
jornada_label.grid(row=5, column=1, pady = 4, sticky="W")

lei_label = Label(text="Lei :")
lei_label["font"] = ("Montserrat","12")
lei_label.grid(row=6, column=1, pady = 4, sticky="W")

cargo_label = Label(text="Cargo :")
cargo_label["font"] = ("Montserrat","12")
cargo_label.grid(row=7, column=1, pady = 4, sticky="W")

destinacao_label = Label(text="Destinação :")
destinacao_label["font"] = ("Montserrat","12")
destinacao_label.grid(row=8, column=1, pady = 4, sticky="W")

ua_label = Label(text="UA :")
ua_label["font"] = ("Montserrat","12")
ua_label.grid(row=9, column=1, pady = 4, sticky="W")

coordenadoria_label = Label(text="Coordenadoria :")
coordenadoria_label["font"] = ("Montserrat","12")
coordenadoria_label.grid(row=10, column=1, pady = 4, sticky="W")

cargo_de_origem_label = Label(text="Cargo de Origem :")
cargo_de_origem_label["font"] = ("Montserrat","12")
cargo_de_origem_label.grid(row=11, column=1, pady = 4, sticky="W")

regime_label = Label(text="Regime :")
regime_label["font"] = ("Montserrat","12")
regime_label.grid(row=12, column=1, pady = 4, sticky="W")

# Entries

nome_entry = Entry(width=45)
nome_entry.grid(row=0, column=2)

validate_cmd = window.register(lambda P, entry=nome_entry: validar_nome_entry(P, entry)) # Registra a função de validação
nome_entry.config(validate="key", validatecommand=(validate_cmd, "%P"))
nome_entry.focus()

rg_entry = Entry(width=45)
rg_entry.grid(row=1, column=2, pady = 4)
validate_rg_cmd = window.register(lambda P, entry=rg_entry: validar_rg_entry(P, entry))
rg_entry.config(validate="key", validatecommand=(validate_rg_cmd, "%P"))

cpf_entry = Entry(width=45)
cpf_entry.grid(row=2, column=2, pady = 4)

cpf_entry.bind("<Return>", lambda event: validar_cpf_entry(event, cpf_entry))
cpf_entry.bind("<Tab>", lambda event: validar_cpf_entry(event, cpf_entry))

#estado_civil_entry = Entry(width=45)
#estado_civil_entry.grid(row=3, column=2, pady = 4)

estado_civil_combo = Combobox(window, 
        values=["Solteira(o)", 
                "Casada(o)", 
                "Divorciada(o)", 
                "Viúva(o)"], width=42)
estado_civil_combo.grid(row=3, column=2, pady = 6)



ato_combo = Combobox(window, 
        values=["Nomeação","Designação",
                "Designação com posterior Nomeação"], width=42)
ato_combo.grid(row=4, column=2, pady = 6)

jornada_combo = Combobox(window, 
        values=["Jornada Básica de Trabalho",
                "Jornada Completa de Trabalho",
                "Jornada Parcial de Trabalho",
                "Jornada de 30(trinta) horas de Trabalho"], width=42)
jornada_combo.grid(row=5, column=2)



lei_combo = Combobox(window, 
        values=["Art.5º da lei complementar nº 1080/2008",
                "Art.8º da lei complementar nº 1157/2011"], width=42)
lei_combo.grid(row=6, column=2)

cargo_entry = Entry(width=45)
cargo_entry.grid(row=7, column=2)

destinacao_entry = Entry(width=45)
destinacao_entry.grid(row=8, column=2)

ua_entry = Entry(width=45)
ua_entry.grid(row=9, column=2)

coordenadoria_entry = Entry(width=45)
coordenadoria_entry.grid(row=10, column=2)

cargo_de_origem_entry = Entry(width=45)
cargo_de_origem_entry.grid(row=11, column=2)

cargo_entry = Entry(width=45)
cargo_entry.grid(row=12, column=2)

a_partir=False
periodo_fechado=True
a_partir_entry = Checkbutton(window, text="A partir", variable=a_partir, font="Montserrat").grid(row=1, sticky=W, column=5, columnspan= 4)
periodo_fechado_entry = Checkbutton(window, text="Período Fechado", variable=periodo_fechado, font="Montserrat").grid(row=3, sticky=W, column=5, columnspan= 4)


add_button = Button(text="Gerar Dados \n Não Servidor", width=15, bg="cyan")
add_button["font"] = ("Montserrat","12")
add_button.grid(row=24, column=0, columnspan=2)

add_button = Button(text="Gerar Dados \n Servidor", width=15, bg="cyan")
add_button["font"] = ("Montserrat","12")
add_button.grid(row=24, column=2, columnspan=2)

add_button_limpar = Button(text="Limpar", width=15, bg="gray", command=lambda: limpar_campos(nome_entry, rg_entry, cpf_entry, estado_civil_combo, ato_combo, jornada_combo, lei_combo, cargo_entry, destinacao_entry, ua_entry, coordenadoria_entry, cargo_de_origem_entry, a_partir_entry, periodo_fechado))
add_button_limpar["font"] = ("Montserrat","12")
add_button_limpar.grid(row=24, column=4, columnspan=2, pady=25, padx=25)

add_button_sair = Button(text="SAIR", width=15, bg="red", command=window.quit)
add_button_sair["font"] = ("Montserrat","12")
add_button_sair.grid(row=24, column=8, columnspan=2)

window.mainloop()