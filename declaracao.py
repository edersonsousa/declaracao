import subprocess, os, locale, sys
import babel.numbers
import reportlab.rl_config
from tool_box import (
    validar_nome_entry,
    validar_cpf,
    limpar_campos,
    btn_on,
    validar_dados_servidor,
    toggle_check_a_partir,
    toggle_check_periodo_fechado,
    ato_box_select,
    lei_box_select,
    jornada_box_select,
    on_validate,
    validate_name,
    declaracao,
    on_select_regime_combo,
    user_date_a_partir_variable,
    cargo_box_select,
    coordenadoria_box_select,
    ua_box_select,
    cargo_de_origem,
    filter_combobox, 
    on_select,
    on_select_estado_civil,
    mascara_cpf
                        )

import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.ttk import *
from tkinter import (
    Tk,
    Label,
    Entry,
    Checkbutton,
    W,
    Button,
    messagebox,
    END,
    simpledialog,
)
from PIL import Image, ImageDraw, ImageTk
############### Loading #############
if getattr(sys, 'frozen', False):
    import pyi_splash
#####################################
global statusbar_text
window = ttk.Window("lumen", resizable=(True, True))
try:
    window.iconbitmap("ico.ico")
except:
    pass
window.title("Declarações")
window.config(padx=20, pady=20)
# Labels                                        
nome_label = ttk.Label(text="Nome :", bootstyle="primary")
nome_label.grid(row=0, column=1, pady=4, sticky="W")
rg_label = ttk.Label(text="RG :", bootstyle="primary")
rg_label.grid(row=1, column=1, pady=4, sticky="W")
cpf_label = ttk.Label(text="CPF :", bootstyle="primary")
cpf_label.grid(row=2, column=1, pady=4, sticky="W")
estado_civil_label = ttk.Label(text="Estado Civil :", bootstyle="primary")
estado_civil_label.grid(row=3, column=1, pady=4, sticky="W")
ato_label = ttk.Label(text="Ato :", bootstyle="primary")
ato_label.grid(row=4, column=1, pady=4, sticky="W")
lei_label = ttk.Label(text="Lei :", bootstyle="primary")
lei_label.grid(row=5, column=1, pady=4, sticky="W")
jornada_label = ttk.Label(text="Jornada :", bootstyle="primary")
jornada_label.grid(row=6, column=1, pady=4, sticky="W")
cargo_label = ttk.Label(text="Cargo :", bootstyle="primary")
cargo_label.grid(row=7, column=1, pady=4, sticky="W")
coordenadoria_label = ttk.Label(text="Coordenadoria :", bootstyle="primary")
coordenadoria_label.grid(row=8, column=1, pady=4, sticky="W")
ua_label = ttk.Label(text="UA :", bootstyle="primary")
ua_label.grid(row=9, column=1, pady=4, sticky="W")
destinacao_label = ttk.Label(text="Destinação :", bootstyle="primary")
destinacao_label.grid(row=10, column=1, pady=4, sticky="W")
regime_label = ttk.Label(text="Regime :", bootstyle="primary")
regime_label.grid(row=11, column=1, pady=4, sticky="W")

cargo_de_origem_label = ttk.Label(text="Cargo de Origem :", bootstyle="primary")
cargo_de_origem_label.grid(row=12, column=1, pady=4, sticky="W")

#Entries
nome_entry = ttk.Entry(width=45, bootstyle="default")
nome_entry.grid(row=0, column=2, pady=4)
validate_cmd = window.register(lambda P, entry=nome_entry: validar_nome_entry(P, entry, statusbar_text))
nome_entry.config(validate="key", validatecommand=(validate_cmd, "%P"))
nome_entry.bind("<FocusOut>", lambda event: validate_name(event, nome_entry))
nome_entry.focus()

rg_entry = ttk.Entry(width=45)
rg_entry.grid(row=1, column=2, pady=4)

cpf_entry = ttk.Entry(width=45)
cpf_entry.grid(row=2, column=2, pady=4)
cpf_entry.bind("<KeyRelease>", lambda event: mascara_cpf(event, cpf_entry))
cpf_entry.bind("<Return>", lambda event: validar_cpf(event, cpf_entry, statusbar_text))
cpf_entry.bind("<Tab>", lambda event: validar_cpf(event, cpf_entry, statusbar_text))
cpf_entry.bind("<FocusOut>", lambda event: validar_cpf(event, cpf_entry, statusbar_text))

estado_civil = ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"]
frame_estado_civil = Frame(window)
frame_estado_civil.grid(row=3, column=2, padx=4, pady=4)
estado_civil_combo = AutocompleteCombobox(
    frame_estado_civil, 
    width=43, 
    completevalues=estado_civil
    )
estado_civil_combo.grid(row=3, column=2, pady=4)
estado_civil_combo.bind("<<ComboboxSelected>>", lambda event: on_select_estado_civil(event, nome_entry, rg_entry, cpf_entry, ato_combo, statusbar_text))

ato =["Nomeação", "Designação", "Designação com posterior Nomeação"]
frame_ato = Frame(window)
frame_ato.grid(row=4, column=2, padx=0, pady=4)
ato_combo = AutocompleteCombobox(
    frame_ato, 
    width=43,
    state="disable",
    completevalues=ato
    )
ato_combo.grid(row=4, column=2, pady=0)
ato_combo.bind("<<ComboboxSelected>>", lambda event: on_select(event, ato, ato_combo))
ato_combo.bind("<FocusOut>",lambda event: btn_on(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                                                    estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                                                    coordenadoria_combo, regime_combo))
ato_combo.bind("<<ComboboxSelected>>",lambda event: btn_on(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                                                    estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                                                    coordenadoria_combo, regime_combo))
ato_combo.bind("<<ComboboxSelected>>", lambda event: ato_box_select(event, ato_combo, a_partir_var, periodo_fechado_var, a_partir_checkbutton, periodo_fechado_checkbutton, lei_combo))
ato_combo.bind("<FocusOut>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
ato_combo.bind("<Tab>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
ato_combo.bind("<Return>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
ato_combo.bind("<KeyRelease>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)

frame_lei = Frame(window)
frame_lei.grid(row=5, column=2,pady=4)
lei = ["Art.5º da lei complementar nº 1080/2008","Art.8º da lei complementar nº 1157/2011"]
lei_combo = AutocompleteCombobox(
    frame_lei, 
    width=43,
    state="disable",
    completevalues=lei
    )
lei_combo.grid(row=5, column=2, pady=4)
lei_combo.bind("<<ComboboxSelected>>", lambda event: lei_box_select(event, lei_combo, jornada_combo))
lei_combo.bind("<FocusOut>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
lei_combo.bind("<Tab>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
lei_combo.bind("<Return>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
lei_combo.bind("<KeyRelease>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)

frame_jornada = Frame(window)
frame_jornada.grid(row=6, column=2, pady=4)
jornada = ["Jornada Básica de Trabalho","Jornada Completa de Trabalho","Jornada Parcial de Trabalho","Jornada de 30(trinta) horas de Trabalho"]
jornada_combo = AutocompleteCombobox(
    frame_jornada, 
    width=43,
    completevalues=jornada,
    state="disable"
    )
jornada_combo.grid(row=6, column=2, pady=4)
jornada_combo.bind("<<ComboboxSelected>>", lambda event: on_select(event, jornada, jornada_combo))
jornada_combo.bind("<<ComboboxSelected>>", lambda event: jornada_box_select(cargo_combo, lei_combo))
jornada_combo.bind("<FocusOut>", lambda event: jornada_box_select(cargo_combo, lei_combo))
jornada_combo.bind("<<Return>>", lambda event: jornada_box_select(cargo_combo, lei_combo))
jornada_combo.bind("<<Tab>>", lambda event: jornada_box_select(cargo_combo, lei_combo))

frame_cargo = Frame(window)
frame_cargo.grid(row=7, column=2, padx=0, pady=4)
cargo = [""]
cargo_combo = AutocompleteCombobox(
    frame_cargo, 
    width=43, 
    completevalues=cargo,
    state="disable"
    )
cargo_combo.grid(row=7, column=2, pady=4)
cargo_combo.bind("<<ComboboxSelected>>", lambda event: on_select(event, cargo, cargo_combo))
cargo_combo.bind("<<ComboboxSelected>>", lambda event: cargo_box_select(coordenadoria_combo))
cargo_combo.bind("<FocusOut>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
cargo_combo.bind("<Tab>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
cargo_combo.bind("<Return>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
cargo_combo.bind("<KeyRelease>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)

coordenadoria = [
        'Administração Superior da Secretaria e da Sede',
        "Coordenadoria de Ciência, Tecnologia e Insumos Estratégicos de Saúde",
        "Coordenadoria de Controle de Doenças",
        "Coordenadoria de Regiões de Saúde",
        "Coordenadoria de Serviços de Saúde",
                    ]
frame_coordenadoria = Frame(window)
frame_coordenadoria.grid(row=8, column=2, pady=4)
coordenadoria_combo = AutocompleteCombobox(
    frame_coordenadoria, 
    width=43,
    completevalues=coordenadoria,
    state="disable"
    )
coordenadoria_combo.grid(row=8, column=2, pady=4)

coordenadoria_combo.bind("<<ComboboxSelected>>", lambda event: coordenadoria_box_select(ua_combo, coordenadoria_combo))
coordenadoria_combo.bind("<<Tab>>", lambda event: coordenadoria_box_select(ua_combo, coordenadoria_combo))
coordenadoria_combo.bind("<<FocusOut>>", lambda event: coordenadoria_box_select(ua_combo, coordenadoria_combo))

frame_ua = Frame(window)
frame_ua.grid(row=9, column=2, padx=0, pady=4)
ua = [""]
ua_combo = AutocompleteCombobox(
    frame_ua, 
    width=43, 
    completevalues=ua,
    state="disable"
    )
ua_combo.grid(row=9, column=2, pady=4)

ua_combo.bind("<<ComboboxSelected>>", lambda event: on_select(event, ua, ua_combo))
ua_combo.bind("<<ComboboxSelected>>", lambda event: ua_box_select(destinacao_entry))

destinacao_entry = ttk.Entry(width=45, state="disable")
destinacao_entry.grid(row=10, column=2, pady=4)

destinacao_entry.bind("<KeyRelease>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
destinacao_entry.bind("<FocusOut>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
destinacao_entry.bind("<Tab>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
destinacao_entry.bind("<Return>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
destinacao_entry.bind("<KeyRelease>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)

frame_regime = Frame(window)
frame_regime.grid(row=11, column=2, padx=0, pady=4)
regime_list = ["Efetivo", "Lei 500", "Comissão", "CLT"]
regime_combo = AutocompleteCombobox(
    frame_regime, 
    width=43, 
    completevalues=regime_list,
    state="disable"
    )
regime_combo.grid(row=11, column=2, pady=4)
regime_combo.bind("<<ComboboxSelected>>", lambda event: on_select_regime_combo(cargo_origem_combo, regime_combo))
regime_combo.bind("<Tab>", lambda event: on_select_regime_combo(cargo_origem_combo, regime_combo))
regime_combo.bind("<Return>", lambda event: on_select_regime_combo(cargo_origem_combo, regime_combo))
regime_combo.bind("<KeyRelease>", lambda event: on_select_regime_combo(cargo_origem_combo, regime_combo))
regime_combo.bind("<FocusOut>", lambda event: on_select_regime_combo(cargo_origem_combo, regime_combo))

frame_cargo_origem = Frame(window)
frame_cargo_origem.grid(row=12, column=2, padx=0, pady=4)
global cargo_origem_list
cargo_origem_list = [""]
cargo_origem_combo = AutocompleteCombobox(
                                        frame_cargo_origem, 
                                        width=43, 
                                        completevalues=cargo_origem_list,
                                        state="disable"
                                        )
cargo_origem_combo.grid(row=12, column=2, pady=4)

cargo_origem_combo.bind("<<ComboboxSelected>>", lambda event: on_select_regime_combo(event, cargo_origem_combo, regime_combo))
cargo_origem_combo.bind("<FocusOut>", lambda event: on_select_regime_combo(event, cargo_origem_combo, regime_combo))
cargo_origem_combo.bind("<KeyRelease>", lambda event: on_select_regime_combo(event, cargo_origem_combo, regime_combo))
cargo_origem_combo.bind("<Return>", lambda event: on_select_regime_combo(event, cargo_origem_combo, regime_combo))
cargo_origem_combo.bind("<Tab>", lambda event: on_select_regime_combo(event, cargo_origem_combo, regime_combo))

cargo_origem_combo.bind("<FocusOut>" and "<<ComboboxSelected>>",lambda event: btn_on(btn_n_servidor, btn_servidor, cargo_origem_combo, 
                                                                                     ato_combo, nome_entry, rg_entry, cpf_entry, 
                                                                                     estado_civil_combo, jornada_combo, lei_combo, 
                                                                                     cargo_combo, destinacao_entry, ua_combo, 
                                                                                     coordenadoria_combo, regime_combo))

cargo_origem_combo.bind("<FocusOut>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
cargo_origem_combo.bind("<Tab>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
cargo_origem_combo.bind("<Return>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)
cargo_origem_combo.bind("<KeyRelease>", lambda event: cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo),)

# a_partir_var = ttk.BooleanVar()
# a_partir_checkbutton = ttk.Checkbutton(
#     window,
#     text="A partir",
#     variable=a_partir_var,
#     bootstyle="primary",
#     command=lambda: toggle_check_a_partir(
#         a_partir_var,
#         periodo_fechado_var,
#         periodo_fechado_checkbutton,
#         ato_combo,
#         window, 
#         btn_servidor, 
#         btn_n_servidor
#     ),
# )

# a_partir_checkbutton.grid(row=1, sticky=tk.W, column=6, columnspan=2)

# Criar um estilo
style = ttk.Style()

# Aplicar o estilo ao Checkbutton
# style.configure('Primary.TCheckbutton', background='blue', foreground='white', font=('Arial', 12))

# Definir as propriedades do estilo para se assemelharem ao estilo Lumen
# style.configure(
#     'Primary.TCheckbutton', 
#     # background='#F0F0F0',  # Cor de fundo semelhante ao Lumen
#     foreground='#376cfe',    # Cor do texto semelhante ao Lumen
#     font=('Verdana', 10),   # Fonte semelhante ao Lumen
#     fontcolor='#376cfe',
#     indicatorforeground="white",
#     # background="black",
#     disabledforeground='white',  # Cor do texto quando desabilitado

# )

style.configure('Custom.TCheckbutton', indicatorrelief='flat', indicatordiameter=0, indicatormargin=(0, 0, 0, 0),
                indicatordistance=0, borderwidth=0, padding=10, foreground='#376cfe')

style.layout('CustomCheckbutton',
             [('Checkbutton.padding', {'sticky': 'nswe', 'children':
                                       [('Checkbutton.indicator', {'side': 'left', 'sticky': ''}),
                                        ('Checkbutton.focus', {'side': 'left', 'sticky': '', 'children':
                                                               [('Checkbutton.label', {'sticky': 'nswe'})]})]})])



style.map("CustomCheckbutton", foreground=[("disabled", "lightgray")], highlightcolor=[("disabled", "white")], relief=[("disabled", "flat"), ("!disabled", "flat")])

# Criar a variável do Checkbutton
a_partir_var = tk.BooleanVar()

# Criar o Checkbutton usando o ttk
a_partir_checkbutton = ttk.Checkbutton(
    window,
    text=" A partir           ",
    # text="  Período Fechado  ",

    variable=a_partir_var,
    style='Custom.TCheckbutton',  # Aplicar o estilo
    command=lambda: toggle_check_a_partir(
        a_partir_var,
        periodo_fechado_var,
        periodo_fechado_checkbutton,
        ato_combo,
        window, 
        btn_servidor, 
        btn_n_servidor
    ),
)

# Adicionar o Checkbutton à janela usando grid
a_partir_checkbutton.grid(row=1, column=4, columnspan=2, padx=25, sticky="w")
# bnt_limpar.grid(row=24, column=4, columnspan=2, pady=25, padx=25)

periodo_fechado_var = tk.BooleanVar()
periodo_fechado_checkbutton = ttk.Checkbutton(
    window,
    text="  Período Fechado  ",
    variable=periodo_fechado_var,

    style='Custom.TCheckbutton',  # Aplicar o estilo
    command=lambda: toggle_check_periodo_fechado(
        periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo, window, btn_servidor, btn_n_servidor
    ),
)
periodo_fechado_checkbutton.grid(row=3, column=4, columnspan=2, padx=25)

try:
    # Carregar a imagem usando PIL
    image = Image.open("logo.png")
    # Redimensionar a imagem para o tamanho do grid
    width, height = 300, 200  # Tamanho desejado para a imagem (ajuste conforme necessário)
    # Redimensionar a imagem para o tamanho do grid
    image = image.resize((width, height))
    # Converter a imagem para o formato suportado pelo Tkinter
    photo = ImageTk.PhotoImage(image)

    # Exibir a imagem em um widget Label
    image_label = tk.Label(window, image=photo)
    image_label.grid(row=4, column=5, columnspan=6, rowspan=10)  # Ajuste as opções de grid conforme necessário
except:
    pass






btn_n_servidor = ttk.Button(
    text="Gerar Dados \n Não Servidor",
    width=15,
    state="disable",
    bootstyle="warning",
    command=lambda : declaracao(        
        declara={
            "Nome": nome_entry.get(),
            "RG": rg_entry.get(),
            "CPF": cpf_entry.get(),
            "Estado Civil": estado_civil_combo.get(),
            "Ato": ato_combo.get(),
            "A partir": a_partir_var.get(),
            "Periodo Fechado": periodo_fechado_var.get(),
            "Lei": lei_combo.get(),
            "Jornada": jornada_combo.get(),
            "Cargo": cargo_combo.get(),
            "Destinação": destinacao_entry.get(),
            "UA": ua_combo.get(),
            "Coordenadoria": coordenadoria_combo.get(),
            "Cargo de Origem": cargo_origem_combo.get(),
            "cargo_origem_list": cargo_origem_list,
            "Regime": regime_combo.get(),
            "regime_list": regime_list
        },
        statusbar_text=statusbar_text
    )
)

btn_n_servidor.grid(row=24, column=0, columnspan=2)
btn_servidor = ttk.Button(
    text="Gerar Dados \n Servidor",
    width=15,
    bootstyle="info",
    state="disable",
    command=lambda: declaracao(
        declara={
            "Nome": nome_entry.get(),
            "RG": rg_entry.get(),
            "CPF": cpf_entry.get(),
            "Estado Civil": estado_civil_combo.get(),
            "Ato": ato_combo.get(),
            "A partir": a_partir_var.get(),
            "Periodo Fechado": periodo_fechado_var.get(),
            "Lei": lei_combo.get(),
            "Jornada": jornada_combo.get(),
            "Cargo": cargo_combo.get(),
            "Destinação": destinacao_entry.get(),
            "UA": ua_combo.get(),
            "Coordenadoria": coordenadoria_combo.get(),
            "Cargo de Origem": cargo_origem_combo.get(),
            "cargo_origem_list": cargo_origem_list,
            "Regime": regime_combo.get(),
            "regime_list": regime_list
        },
        statusbar_text=statusbar_text 
    ),
)

btn_servidor.grid(row=24, column=2, columnspan=2)

bnt_limpar = ttk.Button(
    text="Limpar",
    width=15,
    bootstyle="secondary",
    command=lambda: limpar_campos(
    nome_entry,
    rg_entry,
    cpf_entry,
    estado_civil_combo,
    ato_combo,
    jornada_combo,
    lei_combo,
    cargo_combo,
    destinacao_entry,
    ua_combo,
    coordenadoria_combo,
    cargo_origem_combo,
    a_partir_checkbutton,
    periodo_fechado_var,
    periodo_fechado_checkbutton,
    regime_combo,
    btn_n_servidor,
    btn_servidor,
    statusbar_text,
    user_date_a_partir_variable,
    a_partir_var  # Passando como argumento posicional, não como argumento de palavra-chave
)
,
)

bnt_limpar.grid(row=24, column=4, columnspan=2, pady=25, padx=25)

bnt_sair = ttk.Button(text="SAIR", width=15, command=window.quit, bootstyle="danger")
bnt_sair.grid(row=24, column=6, columnspan=2)

# Definindo a barra de status
statusbar_text = tk.StringVar()
statusbar = ttk.Label(window, textvariable=statusbar_text, borderwidth=0, relief="sunken", anchor="w", bootstyle="primary", justify="center")
statusbar_text.set("GADI")
statusbar.grid(row=32, column=0, columnspan=999, sticky="ew")
####################### Loading off ###########################
if getattr(sys, 'frozen', False):
    pyi_splash.close()
###############################################################
window.mainloop()