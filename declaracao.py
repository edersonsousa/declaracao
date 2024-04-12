import subprocess, os, locale
import babel.numbers
import reportlab.rl_config
from tool_box import (
    validar_nome_entry,
    validar_rg_entry,
    validar_cpf_entry,
    limpar_campos,
    toggle_check_a_partir,
    toggle_check_periodo_fechado,
    ato_box_select,
    lei_box_select,
    jornada_box_select,
    on_validate,
    validate_content,
    atualizar_declara,
    validar_tipo_de_servidor,
    declaracao,
    user_date_a_partir_variable,
    cargo_box_select,
    coordenadoria_box_select,
    ua_box_select,
    cargo_de_origem,
    filter_combobox, 
    on_select
                    )
import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox

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
from PIL import Image, ImageDraw

window = Tk()
window.title("Declarações")
window.config(padx=20, pady=25, bg="white")
# Labels
nome_label = Label(text="Nome :")
nome_label["font"] = ("Montserrat", "12")
nome_label.grid(row=0, column=1, pady=4, sticky="W")

rg_label = Label(text="RG :")
rg_label["font"] = ("Montserrat", "12")
rg_label.grid(row=1, column=1, pady=4, sticky="W")

cpf_label = Label(text="CPF :")
cpf_label["font"] = ("Montserrat", "12")
cpf_label.grid(row=2, column=1, pady=4, sticky="W")

estado_civil_label = Label(text="Estado Civil :")
estado_civil_label["font"] = ("Montserrat", "12")
estado_civil_label.grid(row=3, column=1, pady=4, sticky="W")

ato_label = Label(text="Ato :")
ato_label["font"] = ("Montserrat", "12")
ato_label.grid(row=4, column=1, pady=4, sticky="W")

lei_label = Label(text="Lei :")
lei_label["font"] = ("Montserrat", "12")
lei_label.grid(row=5, column=1, pady=4, sticky="W")

jornada_label = Label(text="Jornada :")
jornada_label["font"] = ("Montserrat", "12")
jornada_label.grid(row=6, column=1, pady=4, sticky="W")

cargo_label = Label(text="Cargo :")
cargo_label["font"] = ("Montserrat", "12")
cargo_label.grid(row=7, column=1, pady=4, sticky="W")

coordenadoria_label = Label(text="Coordenadoria :")
coordenadoria_label["font"] = ("Montserrat", "12")
coordenadoria_label.grid(row=8, column=1, pady=4, sticky="W")

ua_label = Label(text="UA :")
ua_label["font"] = ("Montserrat", "12")
ua_label.grid(row=9, column=1, pady=4, sticky="W")

destinacao_label = Label(text="Destinação :")
destinacao_label["font"] = ("Montserrat", "12")
destinacao_label.grid(row=10, column=1, pady=4, sticky="W")

regime_label = Label(text="Regime :")
regime_label["font"] = ("Montserrat", "12")
regime_label.grid(row=11, column=1, pady=4, sticky="W")

cargo_de_origem_label = Label(text="Cargo de Origem :")
cargo_de_origem_label["font"] = ("Montserrat", "12")
cargo_de_origem_label.grid(row=12, column=1, pady=4, sticky="W")

# Entries

nome_entry = Entry(width=45)
nome_entry.grid(row=0, column=2)

validate_cmd = window.register(lambda P, entry=nome_entry: validar_nome_entry(P, entry))
nome_entry.config(validate="key", validatecommand=(validate_cmd, "%P"))
nome_entry.bind("<FocusOut>", lambda event: validate_content)
nome_entry.focus()

rg_entry = Entry(width=45)
rg_entry.grid(row=1, column=2, pady=4)
validate_rg_cmd = window.register(lambda P, entry=rg_entry: validar_rg_entry(P, entry))
rg_entry.config(validate="key", validatecommand=(validate_rg_cmd, "%P"))

cpf_entry = Entry(width=45)
cpf_entry.grid(row=2, column=2, pady=4)

cpf_entry.bind("<Return>", lambda event: validar_cpf_entry(event, cpf_entry))
cpf_entry.bind("<Tab>", lambda event: validar_cpf_entry(event, cpf_entry))

estado_civil = ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"]
# estado_civil_combo = Combobox(window, values=estado_civil, width=42)
frame = Frame(window)
frame.grid(row=3, column=2, padx=0, pady=0)
# Label(
#     frame, 
#     background='#8DBF5A',
#     font=('Montserrat', 12),
#     text='Countries in North America '
#     ).grid(row=0, column=13, pady=10)

estado_civil_combo = AutocompleteCombobox(
    frame, 
    width=36, 
    font=('Montserrat', 10),
    background='#ffffff',
    completevalues=estado_civil
    )
estado_civil_combo.grid(row=3, column=2, pady=0)
# estado_civil_combo.bind("<KeyRelease>", lambda event: filter_combobox(event, estado_civil, estado_civil_combo))
# estado_civil_combo.bind("<<ComboboxSelected>>", lambda event: on_select(event, estado_civil, estado_civil_combo))


# estado_civil_combo.grid(row=3, column=2, pady=6)
ato_combo = Combobox(
    window,
    values=["Nomeação", "Designação", "Designação com posterior Nomeação"],
    width=42,
)

ato_combo.grid(row=4, column=2, pady=6)
ato_combo.bind(
    "<<ComboboxSelected>>",
    lambda event: ato_box_select(
        event,
        ato_combo,
        a_partir_var,
        periodo_fechado_var,
        a_partir_checkbutton,
        periodo_fechado_checkbutton,
        lei_combo,
    ),
)
ato_combo.bind(
    "<FocusOut>",
    lambda event: validar_tipo_de_servidor(
        ato_combo, cargo_origem_combo, bnt_n_servidor, bnt_servidor
    ),
)
lei = ["Art.5º da lei complementar nº 1080/2008","Art.8º da lei complementar nº 1157/2011"]

lei_combo = Combobox(
    window,
    values=lei
    ,
    width=42,
    state="enable",
)
lei_combo.grid(row=5, column=2)
lei_combo.bind(
    "<<ComboboxSelected>>", lambda event: lei_box_select(lei_combo, jornada_combo)
)
lei_combo.bind("<KeyRelease>", lambda event: filter_combobox(event, lei, lei_combo))
lei_combo.bind("<<ComboboxSelected>>", lambda event: on_select(event, lei, lei_combo))

jornada_combo = Combobox(
    window,
    values=[
        "Jornada Básica de Trabalho",
        "Jornada Completa de Trabalho",
        "Jornada Parcial de Trabalho",
        "Jornada de 30(trinta) horas de Trabalho",
    ],
    width=42,
    state="disable"
)
jornada_combo.grid(row=6, column=2)
jornada_combo.bind(
    "<<ComboboxSelected>>", lambda event: jornada_box_select(cargo_combo, lei_combo)
)

cargo_combo = Combobox(window, width=42, state="disable")
cargo_combo.grid(row=7, column=2)
cargo_combo.bind(
    "<<ComboboxSelected>>", lambda event: cargo_box_select(coordenadoria_combo)
)

coordenadoria_combo = Combobox(
    window,
    values=[
        'Administração Superior da Secretaria e da Sede',
        "Coordenadoria de Assistência Farmacêutica",
        "Coordenadoria de Ciência, Tecnologia e Insumos Estratégicos de Saúde",
        "Coordenadoria de Controle de Doenças",
        "Coordenadoria de Defesa e Saúde Animal",
        "Coordenadoria de Gestão de Contratos de Serviços de Saúde",
        "Coordenadoria de Gestão Orçamentaria e Financeira",
        "Coordenadoria de Planejamento de Saúde",
        "Coordenadoria de Regiões de Saúde",
        "Coordenadoria de Serviços de Saúde",
        "Coordenadoria Geral de Administração",
    ],
    width=72,
    state="disable",
)
coordenadoria_combo.grid(row=8, column=2, columnspan=3, sticky='w')
coordenadoria_combo.bind(
    "<<ComboboxSelected>>", lambda event: coordenadoria_box_select(ua_combo, coordenadoria_combo)
)

ua_combo = Combobox(
    window,
    values=[
        ""
    ],
    width=75,
    state="disable",
)
ua_combo.grid(row=9, column=2, pady=6, columnspan=5, sticky='w')
ua_combo.bind(
    "<<ComboboxSelected>>", lambda event: ua_box_select(destinacao_entry)
)

destinacao_entry = Entry(width=75, state="disable")
destinacao_entry.grid(row=10, column=2, pady=6, columnspan=5, sticky='w')
destinacao_entry.bind(
    "<FocusOut>",
    lambda event: cargo_de_origem(
        destinacao_entry, ua_combo, cargo_origem_combo
    ),
)

regime_combo = Combobox(
    window, values=["Efetivo", "Lei 500", "Comissão", "CLT"], width=42
)
regime_combo.grid(row=11, column=2)

cargo_origem_combo = Combobox(
    window,
    values=[""],
    width=75,
    state="disable",
)

cargo_origem_combo.grid(row=12, column=2, columnspan=5)
cargo_origem_combo.bind(
    "<FocusOut>",
    lambda event: validar_tipo_de_servidor(
        ato_combo, cargo_origem_combo, bnt_n_servidor, bnt_servidor
    ),
)

a_partir_var = tk.BooleanVar()
a_partir_checkbutton = Checkbutton(
    window,
    text="A partir",
    variable=a_partir_var,
    font="Montserrat",
    command=lambda: toggle_check_a_partir(
        a_partir_var,
        periodo_fechado_var,
        periodo_fechado_checkbutton,
        ato_combo,
        window, 
        bnt_servidor, 
        bnt_n_servidor
    ),
)

a_partir_checkbutton.grid(row=1, sticky=tk.W, column=7, columnspan=4)

periodo_fechado_var = tk.BooleanVar()
periodo_fechado_checkbutton = Checkbutton(
    window,
    text="Período Fechado",
    variable=periodo_fechado_var,
    font="Montserrat",
    command=lambda: toggle_check_periodo_fechado(
        periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo, window, bnt_servidor, bnt_n_servidor
    ),
)
periodo_fechado_checkbutton.grid(row=3, sticky=tk.W, column=7, columnspan=4)

bnt_n_servidor = Button(
    text="Gerar Dados \n Não Servidor",
    width=15,
    bg="cyan",
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
            "Cargo de Origem": cargo_de_origem_entry.get(),
            "Regime": regime_combo.get(),
        }
    ),
)

bnt_n_servidor["font"] = ("Montserrat", "12")
bnt_n_servidor.grid(row=24, column=0, columnspan=2)

bnt_servidor = Button(
    text="Gerar Dados \n Servidor",
    width=15,
    bg="cyan",
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
            "Regime": regime_combo.get(),
        }
    ),
)
bnt_servidor["font"] = ("Montserrat", "12")
bnt_servidor.grid(row=24, column=2, columnspan=2)

bnt_limpar = Button(
    text="Limpar",
    width=15,
    bg="gray",
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
        a_partir_var,
        a_partir_checkbutton,
        periodo_fechado_var,
        periodo_fechado_checkbutton,
        regime_combo,
        bnt_n_servidor, 
        bnt_servidor 
    ),
)
bnt_limpar["font"] = ("Montserrat", "12")
bnt_limpar.grid(row=24, column=4, columnspan=2, pady=25, padx=25)

bnt_sair = Button(text="SAIR", width=15, bg="red", command=window.quit)
bnt_sair["font"] = ("Montserrat", "12")
bnt_sair.grid(row=24, column=8, columnspan=2)

window.mainloop()