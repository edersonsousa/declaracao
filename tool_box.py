import reportlab.rl_config
import tkinter as tk
from datetime import datetime, date
from tkinter import Tk, Label, Entry, Checkbutton, W, Button, messagebox, END ,simpledialog
from PIL import Image, ImageDraw
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, pdfmetrics
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
import babel.numbers
import subprocess, os, locale
from babel.dates import format_date, Locale
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
import os
global date_periodofechado_inicio_variable
global date_periodofechado_fim_variable
locale = Locale('pt', 'BR')


date_periodofechado_inicio_variable = None

date_periodofechado_fim_variable = None
def validar_nome_entry(new_value, nome_entry, statusbar_text):
    # Verifica se a entrada está vazia
    if not new_value:
        return True
    # Capitaliza a primeira letra de cada palavra na string
    new_value = new_value.title()
    # Verifica se a entrada contém apenas letras e espaços
    if re.match(r'^[a-záÀÁéÉíÍóÓúÚüÜçÇñÑA-Z\s]+$', new_value):
        return True
    else:
        if any(char.isdigit() for char in new_value):
            # messagebox.showerror("Erro", "A entrada não pode conter números.")
            statusbar_text.set("O campo nome não pode conter números")
        else:
            statusbar_text.set("A entrada deve conter apenas letras e espaços.")
            # messagebox.showerror("Erro", "A entrada deve conter apenas letras e espaços.")
        nome_entry.delete(len(nome_entry.get()), "end")
        return False

def on_validate(P, nome_entry):
    return validar_nome_entry(P, nome_entry)

def validate_name(event, entry):
    content = entry.get()
    content = capitalize_long_words(content)
    entry.delete(0, "end")
    entry.insert(0, content)

def capitalize_long_words(content):
    words = content.split()
    for i in range(len(words)):
        if len(words[i]) > 3:
            words[i] = words[i].capitalize()
    return " ".join(words)

def mascara_cpf(event, cpf_entry):
    cpf = cpf_entry.get()
    cpf = ''.join(filter(str.isdigit, cpf))  # Mantém apenas os dígitos do CPF
    #cpf = cpf.replace(".", "").replace("-", "")  # Remove pontos e hífen anteriores (se houver)
    # Verifica se o tamanho do CPF é menor que 11 para continuar formatando
    if len(cpf) < 11:
        cpf_formatado = ""
        for i in range(len(cpf)):
            if i == 3 or i == 6:
                cpf_formatado += "."  # Adiciona o ponto nos locais corretos
            elif i == 9:
                cpf_formatado += "-"  # Adiciona o hífen no local correto
            cpf_formatado += cpf[i]
        
        # Atualiza o valor do campo de entrada com o CPF formatado
        cpf_entry.delete(0, "end")
        cpf_entry.insert(0, cpf_formatado)
    elif len(cpf) == 11:
        cpf_formatado = cpf[:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:]
        # Atualiza o valor do campo de entrada com o CPF formatado
        cpf_entry.delete(0, "end")
        cpf_entry.insert(0, cpf_formatado)
    elif len(cpf) > 11:
        # Impede que caracteres adicionais sejam inseridos
        cpf_entry.delete(14, "end")  # Remove apenas o último caractere
    
    
def validar_cpf(event, cpf_entry, statusbar_text):
    cpf_enviado_usuario = cpf_entry.get()
    cpf_enviado_usuario = cpf_enviado_usuario.replace(".", "").replace("-", "")  # Remove pontos e hífen anteriores (se houver)
    nove_digitos = cpf_enviado_usuario[:9]
    contador_regressivo_1 = 10

    resultado_digito_1 = 0
    for digito in nove_digitos:
        resultado_digito_1 += int(digito) * contador_regressivo_1
        contador_regressivo_1 -= 1
    digito_1 = (resultado_digito_1 * 10) % 11
    digito_1 = digito_1 if digito_1 <= 9 else 0

    dez_digitos = nove_digitos + str(digito_1)
    contador_regressivo_2 = 11

    resultado_digito_2 = 0
    for digito in dez_digitos:
        resultado_digito_2 += int(digito) * contador_regressivo_2
        contador_regressivo_2 -= 1
    digito_2 = (resultado_digito_2 * 10) % 11
    digito_2 = digito_2 if digito_2 <= 9 else 0

    cpf_gerado_pelo_calculo = f'{nove_digitos}{digito_1}{digito_2}'
    if cpf_enviado_usuario == cpf_gerado_pelo_calculo: statusbar_text.set("CPF digitado é válido")
    
    elif cpf_enviado_usuario != cpf_gerado_pelo_calculo:
        statusbar_text.set("CPF digitado inválido favor verificar.")
        cpf_entry.delete(0, "end")
    
def limpar_campos(nome_entry, rg_entry, cpf_entry, estado_civil_combo, ato_combo, jornada_combo, lei_combo, cargo_combo, 
                  destinacao_entry, ua_combo, coordenadoria_combo, cargo_origem_combo, a_partir_checkbutton, periodo_fechado_var, 
                  periodo_fechado_checkbutton, regime_combo, btn_n_servidor, btn_servidor, statusbar_text, user_date_a_partir_variable, a_partir_var, 
                  date_periodofechado_inicio_variable, date_periodofechado_fim_variable  ):
    # Limpa o valor de todos os campos de entrada
    nome_entry.delete(0, END)
    nome_entry.focus()
    rg_entry.delete(0, END)
    cpf_entry.delete(0, END)
    estado_civil_combo.set('')
    ato_combo.set('')
    jornada_combo.set('')
    jornada_combo.config(state="readonly")
    ato_combo["values"] = "Nomeação","Designação","Designação com posterior Nomeação"
    ato_combo.config(state="readonly")
    lei_combo.set('')
    lei_combo.config(state="readonly")
    cargo_combo.set('')
    cargo_combo.config(state="readonly")
    cargo_combo["values"] = ""
    destinacao_entry.delete(0, END)
    destinacao_entry.config(state="readonly")
    ua_combo.set('')
    ua_combo.config(state="readonly")
    coordenadoria_combo.set('')
    coordenadoria_combo.config(state="readonly")
    cargo_origem_combo.set('')
    cargo_origem_combo.config(state="readonly")
    periodo_fechado_var.set(False)
    a_partir_var.set(False)
    a_partir_var = None
    a_partir_checkbutton.config(state="normal")
    user_date_a_partir_variable = None
    date_periodofechado_inicio_variable  = None
    date_periodofechado_fim_variable = None
    periodo_fechado_checkbutton.config(state="normal")
    regime_combo.set('')
    regime_combo.config(state="readonly")
    btn_n_servidor.config(state="disable")
    btn_servidor.config(state="disable")
    statusbar_text.set("GADI")
global user_date_a_partir_variable
#global date_periodofechado_inicio_variable
#global date_periodofechado_fim_variable
# user_date_a_partir_variable = None

def toggle_check_a_partir(a_partir_var, periodo_fechado_var, periodo_fechado_checkbutton, ato_combo, window, btn_servidor, btn_n_servidor):
    global user_date_a_partir_variable
    
    if user_date_a_partir_variable is not True: user_date_a_partir_variable = None
    if a_partir_var.get():
        periodo_fechado_var.set(False)
        periodo_fechado_checkbutton.config(state="disabled")
        # Exibir caixa de diálogo para solicitar uma data
        window.withdraw() 
        user_date = simpledialog.askstring("Declarações", "Qual a data do a partir? \nEx:(dd/mm/aaaa)", initialvalue=datetime.now().strftime('%d/%m/%Y'))
        # Verificar se a data está no formato correto
        if user_date and len(user_date) == 10 and user_date[2] == '/' and user_date[5] == '/':
            dia = int(user_date[:2])
            mes = int(user_date[3:5])
            ano = int(user_date[6:])
            # Verificar se o dia, mês e ano são válidos
            if (1 <= mes <= 12) and (ano >= 2024):
                if (mes in [1, 3, 5, 7, 8, 10, 12] and 1 <= dia <= 31) or \
                   (mes in [4, 6, 9, 11] and 1 <= dia <= 30) or \
                   (mes == 2 and ((ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0) and 1 <= dia <= 29) or \
                   (mes == 2 and 1 <= dia <= 28):
                    # Use a data fornecida pelo usuário como desejar
                    user_date_a_partir_variable = user_date
                    # Atualizar valores do Combobox
                    ato_combo["values"] = "Designação", "Designação com posterior Nomeação" 
                    ato_combo.config(state="normal")
                else:
                    messagebox.showerror("Erro", "Dia inválido para o mês fornecido.")
                    toggle_check_a_partir(a_partir_var, periodo_fechado_var, periodo_fechado_checkbutton, ato_combo, window, btn_servidor, btn_n_servidor)
            else:
                messagebox.showerror("Erro", "Mês inválido")# ou ano diferente de 2024.")
                toggle_check_a_partir(a_partir_var, periodo_fechado_var, periodo_fechado_checkbutton, ato_combo, window, btn_servidor, btn_n_servidor)

        elif user_date == None or user_date_a_partir_variable == None:
            window.deiconify()
        else:
            messagebox.showerror("Erro", "Formato de data inválido. Por favor, insira uma data no formato dd/mm/aaaa.")
            toggle_check_a_partir(a_partir_var, periodo_fechado_var, periodo_fechado_checkbutton, ato_combo, window, btn_servidor, btn_n_servidor)
    else:
        periodo_fechado_checkbutton.config(state="normal")
    window.deiconify()
    if btn_servidor.cget("state") == "disable":
        btn_n_servidor.focus()
    elif btn_n_servidor.cget("state") == "disable":
        btn_servidor.focus()
    date_periodofechado_inicio_variable = None
user_date_a_partir_variable = None

def toggle_check_periodo_fechado(periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo, window, btn_servidor, btn_n_servidor):
    global date_periodofechado_inicio_variable
    global date_periodofechado_fim_variable
    date_periodofechado_inicio_variable = None
    date_periodofechado_fim_variable = None
    current_year = datetime.now().year

    if periodo_fechado_var.get():
        a_partir_var.set(False)
        a_partir_checkbutton.config(state="disabled")
        user_date_a_partir_variable = None
        ato_combo["values"] = "Designação"
        window.withdraw()

        date_periodofechado_inicio_variable = simpledialog.askstring("Período Fechado", "Qual a data do início para o período fechado?\nEx:(dd/mm/aaaa)")
        if date_periodofechado_inicio_variable and len(date_periodofechado_inicio_variable) == 10 and date_periodofechado_inicio_variable[2] == '/' and date_periodofechado_inicio_variable[5] == '/':
            dia_inicio = int(date_periodofechado_inicio_variable[:2])
            mes_inicio = int(date_periodofechado_inicio_variable[3:5])
            ano_inicio = int(date_periodofechado_inicio_variable[6:])
            try:
                data_inicio = datetime(ano_inicio, mes_inicio, dia_inicio)
                if data_inicio >= datetime.now():
                    #date_periodofechado_inicio_variable = date_periodofechado_inicio
                #else:
                    messagebox.showerror("Erro", "Data inicial inválida. A data deve ser anterior ao dia atual.")
                    toggle_check_periodo_fechado(periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo, window, btn_servidor, btn_n_servidor)
                    return
            except ValueError:
                messagebox.showerror("Erro", "Data inicial inválida. Por favor, insira uma data válida no formato dd/mm/aaaa.")
                toggle_check_periodo_fechado(periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo, window, btn_servidor, btn_n_servidor)
                return
        elif date_periodofechado_inicio_variable is None:
            window.deiconify()
            return
        else:
            messagebox.showerror("Erro", "Formato de data inválido. Por favor, insira uma data no formato dd/mm/aaaa.")
            toggle_check_periodo_fechado(periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo, window, btn_servidor, btn_n_servidor)
            return

        date_periodofechado_fim = simpledialog.askstring("Data fim...", "Qual a data fim para o período fechado? Ex:(dd/mm/aaaa)")
        if date_periodofechado_fim and len(date_periodofechado_fim) == 10 and date_periodofechado_fim[2] == '/' and date_periodofechado_fim[5] == '/':
            dia_fim = int(date_periodofechado_fim[:2])
            mes_fim = int(date_periodofechado_fim[3:5])
            ano_fim = int(date_periodofechado_fim[6:])
            try:
                data_fim = datetime(ano_fim, mes_fim, dia_fim)
                if data_fim < datetime.now() and data_fim > data_inicio:
                    date_periodofechado_fim_variable = date_periodofechado_fim
                else:
                    messagebox.showerror("Erro", "Data final inválida. A data deve ser anterior ao dia atual e posterior à data inicial.")
                    toggle_check_periodo_fechado(periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo, window, btn_servidor, btn_n_servidor)
                    return
            except ValueError:
                messagebox.showerror("Erro", "Data final inválida. Por favor, insira uma data válida no formato dd/mm/aaaa.")
                toggle_check_periodo_fechado(periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo, window, btn_servidor, btn_n_servidor)
                return
        elif date_periodofechado_fim is None:
            window.deiconify()
            return
        else:
            messagebox.showerror("Erro", "Formato de data inválido. Por favor, insira uma data no formato dd/mm/aaaa.")
            toggle_check_periodo_fechado(periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo, window, btn_servidor, btn_n_servidor)
            return

    else:
        a_partir_checkbutton.config(state="normal")
        window.deiconify()
        if btn_servidor.cget("state") == "disable":
            btn_n_servidor.focus()
        elif btn_n_servidor.cget("state") == "disable":
            btn_servidor.focus()
    #print(date_periodofechado_inicio_variable)
    #print(date_periodofechado_fim_variable)
    window.deiconify()
    
def ato_box_select(event, ato_combo, a_partir_var, periodo_fechado_var, a_partir_checkbutton, periodo_fechado_checkbutton, lei_combo):
    selected_value = ato_combo.get()
    if selected_value == "Nomeação":
        a_partir_var.set(False)
        periodo_fechado_var.set(False)
        a_partir_checkbutton.config(state=tk.DISABLED)
        periodo_fechado_checkbutton.config(state=tk.DISABLED)
        lei_combo.config(state="readonly")
        
    elif selected_value == "Designação com posterior Nomeação":
        periodo_fechado_var.set(False)
        a_partir_checkbutton.config(state=tk.NORMAL)
        periodo_fechado_checkbutton.config(state=tk.DISABLED)
        lei_combo.config(state="readonly")

    else:
        a_partir_checkbutton.config(state=tk.NORMAL)
        periodo_fechado_checkbutton.config(state=tk.NORMAL)
        lei_combo.config(state="readonly")

def lei_box_select(event, lei_combo, jornada_combo):
    selected_value = event.widget.get()
    if selected_value == "Art. 5º da Lei Complementar nº 1.080/2008":
        #jornada_combo.config(state=tk.NORMAL)
        jornada_combo.set("")
        jornada_combo["values"] = ["Jornada Completa de Trabalho"]
        jornada_combo.focus()
        
    elif selected_value == "Art. 8º da Lei Complementar nº 1.157/2011":
        #jornada_combo.config(state=tk.NORMAL)
        jornada_combo.set("")
        jornada_combo["values"] = "Jornada Básica de Trabalho", "Jornada Parcial de Trabalho", "Jornada de 30(trinta) horas de Trabalho"
        jornada_combo.focus()
        
def jornada_box_select(cargo_combo, lei_combo):
    selected_value = lei_combo.get()
    if selected_value == "Art. 5º da Lei Complementar nº 1.080/2008":
        cargo_combo.set("")
        cargo_combo["completevalues"] = [
                                                "Assessor de Gabinete I"                , 
                                                "Assessor de Gabinete II"               , 
                                                "Assessor I"                            ,
                                                "Assessor Técnico de Coordenador"       ,
                                                #"Assessor Técnico de Gabinete I"        ,
                                                #"Assessor Técnico de Gabinete II"       ,
                                                #"Assessor Técnico de Gabinete III"      ,
                                                "Assessor Técnico de Gabinete IV"       ,
                                                "Assessor Técnico I"                ,
                                                "Assessor Técnico II"   	            ,
                                                "Assessor Técnico III"                ,
                                                "Assessor Técnico IV"   	            ,
                                                "Assessor Técnico V"    	            ,
                                                "Chefe de Gabinete"     	            ,
                                                "Chefe I"   	                        ,
                                                "Chefe II"      	                    ,
                                                "Diretor I"                            ,
                                                "Diretor II"    	                    ,
                                                "Diretor III"                           ,
                                                "Diretor Técnico I"                    ,
                                                "Diretor Técnico II"    	            ,
                                                "Diretor Técnico III"   	            ,
                                                "Encarregado I"     	                ,
                                                "Encarregado II"    	                ,
                                                "Supervisor Técnico I"           
                                        ]
        cargo_combo.config(state=tk.NORMAL)
        cargo_combo.set("")
    elif selected_value == "Art. 8º da Lei Complementar nº 1.157/2011":
        cargo_combo.set("")
        cargo_combo["completevalues"] = [
                                            "Assessor Técnico de Coordenador de Saúde"  ,
                                            "Assessor Técnico em Saúde Pública I"       ,
                                            "Assessor Técnico em Saúde Pública II"      ,
                                            "Assessor Técnico em Saúde Pública III"     ,
                                            "Chefe de Saúde I"                          ,
                                            "Chefe de Saúde II"                         ,
                                            #"Cirurgião Dentista Sanitarista Inspetor"   ,
                                            "Coordenador de Saúde"                      ,
                                            "Diretor Técnico de Saúde I"                ,
                                            "Diretor Técnico de Saúde II"               ,
                                            "Diretor Técnico de Saúde III"              ,
                                            "Encarregado de Saúde I"                    ,
                                            "Encarregado de Saúde II"                   ,
                                            #"Enfermeiro Inspetor de Saúde Pública"      ,
                                            #"Engenheiro Sanitarista Assessor"           ,
                                            #"Médico Inspetor"                           ,
                                            "Supervisor de Equipe Técnica de Saúde"     ,
                                            "Supervisor de Saúde"         
                                        ]
        #cargo_combo.config(state=tk.NORMAL)
        cargo_combo.set("")

def cargo_box_select(coordenadoria_combo):
    #coordenadoria_combo.config(state=tk.NORMAL)
    coordenadoria_combo.focus()
    
def coordenadoria_box_select(ua_combo, coordenadoria_combo):
    selected_value = coordenadoria_combo.get()
    ua_combo.set('')
    if selected_value == 'Administração Superior da Secretaria e da Sede':
        ua_combo["completevalues"] = [
                                        #"Gabinete do Coordenador",
                                        "Gabinete do Secretário e Assessorias",
                                        "Coordenadoria de Planejamento de Saúde",
                                        "Coordenadoria de Recursos Humanos",
                                        "Coordenadoria Geral de Administração",
                                        #"Coordenadoria de Gestão de Contratos de Serviços de Saúde",
                                        "Coordenadoria de Gestão Orçamentaria e Financeira"
                                    ]
    elif selected_value =="Coordenadoria de Serviços de Saúde":
        ua_combo["completevalues"] = [
                                            'Ambulatório Médico de Especialidades Digital do Estado de São Paulo - AME Digital SP',
                                            'Centro de Atenção Integrada em Saúde Mental "Philippe Pinel" - CAISM Philippe Pinel',
                                            'Centro de Atenção Integral à Saúde "Clemente Ferreira" de Lins',
                                            'Centro de Atenção Integral à Saúde "Professor Cantídio de Moura Campos"',
                                            "Centro de Atenção Integral à Saúde de Santa Rita - C.A.I.S./SR",
                                            "Centro de Desenvolvimento do Portador de Deficiência Mental, em Itu",
                                            "Centro de Reabilitação de Casa Branca",
                                            "Centro de Referência da Saúde da Mulher",
                                            'Centro Especializado em Reabilitação "Doutor Arnaldo Pezzuti Cavalcanti", em Mogi das Cruzes',
                                            'Centro Pioneiro em Atenção Psicossocial "Arquiteto Januário José Ezemplari"- CPAP',
                                            'Complexo Hospitalar "Padre Bento" de Guarulhos',
                                            "Complexo Hospitalar do Juquery, em Franco da Rocha",
                                            "Conjunto Hospitalar de Sorocaba",
                                            "Conjunto Hospitalar do Mandaqui",
                                            "Departamento de Gerenciamento Ambulatorial da Capital - DGAC",
                                            "Grupo de Resgate - GRAU",
                                            'Hospital "Adhemar de Barros" em Divinolândia',
                                            'Hospital "Dr. Francisco Ribeiro Arantes", em Itu',
                                            'Hospital "Guilherme Álvaro" em Santos',
                                            'Hospital "Manoel de Abreu" de Bauru',
                                            'Hospital "Nestor Goulart Reis" em Américo Brasiliense',
                                            'Hospital das Clínicas "Luzia de Pinho Melo" em Mogi das Cruzes	',
                                            'Hospital Estadual "Dr. Odilo Antunes de Siqueira" em Presidente Prudente',
                                            'Hospital Estadual "Dr. Oswaldo Brandi Faria" em Mirandópolis	',
                                            'Hospital Estadual Especializado em Reabilitação "Dr. Francisco Ribeiro Arantes", em Itu',
                                            'Hospital Geral "Dr. Álvaro Simões de Souza" em Vila Nova Cachoeirinha	',
                                            'Hospital Geral "Dr. José Pangella" de Vila Penteado',
                                            'Hospital Geral "Dr. Manoel Bifulco" em São Mateus',
                                            'Hospital Geral "Jesus Teixeira da Costa" em Guaianazes',
                                            'Hospital Geral "Prefeito Miguel Martin Gualda", de Promissão',
                                            "Hospital Geral de Taipas",
                                            'Hospital Infantil "Cândido Fontoura"',
                                            'Hospital Maternidade Interlagos "Waldemar Seyssel - Arrelia"',
                                            "Hospital Psiquiátrico Pinel, em Pirituba",
                                            'Hospital Regional "Doutor Leopoldo Bevilacqua" do Vale do Ribeira, em Pariquera-Açu',
                                            'Hospital Regional "Dr. Osíris Florindo Coelho" em Ferraz de Vasconcelos	',
                                            'Hospital Regional "Dr. Vivaldo Martins Simões" em Osasco	',
                                            "Hospital Regional de Assis",
                                            "Hospital Regional Sul",
                                            "Hospital Santa Tereza em Ribeirão Preto",
                                            "Instituto Clemente Ferreira - ICF",
                                            'Instituto de Infectologia "Emílio Ribas"',
                                            'Instituto "Dante Pazzanese" de Cardiologia',
                                            'Instituto "Lauro de Souza Lima" em Bauru',
                                            'Instituto Paulista de Geriatria e Gerontologia - IPGG "José Ermírio de Moraes"',
                                            "Núcleo de Gestão Assistencial 14 - Campos Elíseos",
                                            "Unidade de Gestão Assistencial I",
                                            "Unidade de Gestão Assistencial II",
                                            "Unidade de Gestão Assistencial III",
                                            "Unidade de Gestão Assistencial IV",
                                            "Unidade de Gestão Assistencial V",
                                            "Sede"
                                    ]
    elif selected_value == "Coordenadoria de Assistência Farmacêutica":
        ua_combo["completevalues"] = [
                                            "Sede"
                                     ]
    elif selected_value == "Coordenadoria de Ciência, Tecnologia e Insumos Estratégicos de Saúde":
        ua_combo["completevalues"] = [
                                        "Sede",
                                        "Instituto Butantan",
                                        "Instituto de Saúde"
                                    ]
    elif selected_value == "Coordenadoria de Controle de Doenças":
        ua_combo["completevalues"] = [
                                        
                                        'Centro de Referência e Treinamento - "DST/AIDS"',
                                        'Centro de Vigilância Epidemiológica "Professor Alexandre Vranjac"',
                                        "Centro de Vigilância Sanitária",
                                        'Instituto "Adolfo Lutz" - IAL',
                                        "Instituto Pasteur",
                                        "Sede"
                                    ]
    elif selected_value == "Coordenadoria de Gestão de Contratos de Serviços de Saúde":
        ua_combo["completevalues"] = [
                                        "Sede"
                                     ]
    elif selected_value == "Coordenadoria de Regiões de Saúde":
        ua_combo["completevalues"] = [
                                        "DRS I - Grande São Paulo",
                                        "DRS II - Araçatuba",
                                        "DRS III - Araraquara",
                                        'DRS IV "Dr. Maurício Fang" - Baixada Santista	',
                                        "DRS IX - Marília",
                                        "DRS V - Barretos",
                                        "DRS VI - Bauru",
                                        'DRS VII "Dr. Leôncio de Souza Queiroz" - Campinas',
                                        "DRS VIII - Franca",
                                        "DRS X  - Piracicaba",
                                        "DRS XI - Presidente Prudente",
                                        "DRS XII - Registro",
                                        "DRS XIII - Ribeirão Preto",
                                        "DRS XIV - São João da Boa Vista",
                                        "DRS XV - São José do Rio Preto",
                                        "DRS XVI - Sorocaba",
                                        "DRS XVII - Taubaté",
                                        "DRS XVIII - Botucatu",
                                        "Sede"
                                    ]
    ua_combo.focus()

def ua_box_select(destinacao_entry):
    destinacao_entry.config(state="normal")

def btn_on(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
           estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
           coordenadoria_combo, regime_combo):
    if validar_dados_servidor(ato_combo, cargo_origem_combo, btn_n_servidor, btn_servidor, nome_entry, rg_entry, 
                             cpf_entry, estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, 
                             ua_combo, coordenadoria_combo, regime_combo):
        #if (len(destinacao_entry.get())==0 or (destinacao_entry.get())):
            #btn_n_servidor.config(state="disable")
            #btn_servidor.config(state="disable")
            #print('foiiiiiii')
        if ((len(regime_combo.get()) == 0 and len(cargo_origem_combo.get()) > 0) 
                        or (len(regime_combo.get()) > 0 and len(cargo_origem_combo.get()) == 0)):
            #print(destinacao_entry.get())
            #print(len(destinacao_entry.get()))
            btn_n_servidor.config(state="disable")
            btn_servidor.config(state="disable")
        elif(ato_combo.get() == "Nomeação" and len(regime_combo.get()) == 0 and len(cargo_origem_combo.get()) == 0):
            btn_n_servidor.config(state="normal")
            btn_servidor.config(state="disable")
        elif (ato_combo.get() == "Nomeação" and (len(cargo_origem_combo.get()) > 0 and len(regime_combo.get()) > 0)):    
            btn_n_servidor.config(state="disable") 
            btn_servidor.config(state="normal")
        elif ((ato_combo.get() == "Designação" or ato_combo.get() == "Designação com posterior Nomeação") 
                                    and (len(cargo_origem_combo.get()) > 0 and len(regime_combo.get()) > 0)):
            btn_n_servidor.config(state="disable")
            btn_servidor.config(state="normal")
        elif ((ato_combo.get() == "Designação" or ato_combo.get() == "Designação com posterior Nomeação") 
                                    and (len(cargo_origem_combo.get()) == 0 and len(regime_combo.get()) == 0)):
            btn_n_servidor.config(state="normal")
            btn_servidor.config(state="disable")
        #elif (len(destinacao_entry.get())==0 or (len(destinacao_entry.get()) ))
    #print(destinacao_entry.get())
    #print(len(destinacao_entry.get()))
    
def validar_dados_servidor(ato_combo, cargo_origem_combo, btn_n_servidor, btn_servidor, nome_entry, rg_entry, 
                             cpf_entry, estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, 
                             ua_combo, coordenadoria_combo, regime_combo):
    
    if  nome_entry.get() and rg_entry.get() and cpf_entry.get() and estado_civil_combo.get() and ato_combo.get() and \
        jornada_combo.get() and lei_combo.get() and cargo_combo.get() and destinacao_entry.get() and \
        ua_combo.get() and coordenadoria_combo.get():
        return True
    
def path_check(declara, statusbar_text):
    if not (os.path.exists(f"{declara['Ato']}/{declara['Nome']}/")): 
        statusbar_text.set("...Criando a pasta...")
        try:
            os.makedirs(f"./{declara['Ato']}/{declara['Nome']}/")  # Tenta criar a pasta
            statusbar_text.set(f"[GADI] - Pasta {declara['Nome']} criada dentro da pasta {declara['Ato']}...")
        except OSError as e:
            statusbar_text.set("Falha ao tentar criar a pasta. Verifique as permissões...")
    else:
        status_atual = statusbar_text.get()
        novo_status = f"[GADI] - A pasta '{declara['Nome']}' dentro de '{declara['Ato']} já existe."
        statusbar_text.set(novo_status)
        
def rodape(c):
    meses_portugues = {
    1: "JAN", 2: "FEV", 3: "MAR", 4: "ABR", 5: "MAI", 6: "JUN",
    7: "JUL", 8: "AGO", 9: "SET", 10: "OUT", 11: "NOV", 12: "DEZ"
    }
    # Obtém a data atual
    hoje = datetime.now()
    # Extrai o mês e o ano
    mes_abreviado = meses_portugues[hoje.month]
    ano = hoje.year
    # Formata como "NOV/2024"
    data_formatada = f"{mes_abreviado}/{ano}"

    versao="1.342"
        
    # Definir o texto e suas coordenadas
    texto = f"NMP/CCRH/GADI/CRH/SES - versão {versao} | {mes_abreviado}/{ano}"
    x, y = 420, 15  # Posição do texto

    # Adicionar o texto como marca d'água
    c.setFillColorRGB(0.4, 0.4, 0.4)  # Define a cor do texto como cinza (RGB)
    c.setFont("Verdana", 5)  # Define a fonte e o tamanho do texto
    c.drawString(x, y, texto)  # Desenha o texto na posição especificada
    
def declaracao_experiencia(c, declara):
    # Define título
    c.setFont("Verdana-Bold", 14)
    c.drawCentredString(300, 750, "Declaração de Experiência")
    #c.drawCentredString(300, 800, "Declaração de Experiência")

    # Adiciona informações do dicionário do PDF em um parágrafo justificado
    y_position = 650
    nome_em_negrito = f"<b>{declara['Nome']}</b>"
    text = f"Tendo em vista, a indicação por esta Unidade de {nome_em_negrito}, RG. {declara['RG']}, para {declara['Ato']}"
    
    # Para o caso de 'A Partir'
    if declara['A partir'] != False:
        text += f" a partir de {user_date_a_partir_variable}"
    elif declara['Periodo Fechado']:
        #text += f" no período {declara['Periodo Fechado']['Inicio']} a {declara['Periodo Fechado']['Fim']}"
        text += f" no período {date_periodofechado_inicio_variable} a {date_periodofechado_fim_variable}"
        #print(date_periodofechado_inicio_variable)
        #print(date_periodofechado_fim_variable)

    # text += f" e após análise curricular declaro que para fins do disposto do {declara['Lei']}, \
    #         que o(a) indicado(a) atende ao estabelecido no anexo IV da referida Lei Complementar, \
    #         no tocante a experiência profissional exigida nos assuntos relacionados com as atividades a serem desempenhadas \
    #         no cargo de {declara['Cargo']}, classificado no(a) {declara['Destinação']}, do(a) {declara['UA']}, da {declara['Coordenadoria']}."
    
    text += f" com vistas ao disposto no {declara['Lei']}, e após devida análise curricular, DECLARO \
            que o(a) indicado(a) atende ao estabelecido no anexo IV da referida Lei Complementar, \
            no tocante a experiência profissional exigida nos assuntos relacionados com as atividades a serem desempenhadas \
            no cargo de {declara['Cargo']}, classificado no(a) {declara['Destinação']}, do(a) {declara['UA']}, da {declara['Coordenadoria']}."
    
    style = ParagraphStyle(name='Justify', alignment=4, firstLineIndent=125, leading=(12*1.5), fontSize=11, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 300)
    p.drawOn(c, 100, y_position - p.height)
    # Adiciona a data atual formatada
    c.setFont("Verdana", 11)
    data_atual = format_date(datetime.now(), format='full', locale='pt_BR').split(',')[1].strip()
    #c.drawCentredString(300, 500, f"São Paulo, {data_atual}")
    c.setFont("Verdana", 11)
    c.drawCentredString(300, 400, f"São Paulo, {data_atual}")
    # Assinatura
    c.setFont("Verdana", 11)
    c.drawCentredString(300, 215, "_________________________________________")
    c.setFont("Verdana", 11)
    c.drawCentredString(300, 200, "(Assinatura e Carimbo)")
    rodape(c)
    
def termo_de_anuencia(c , declara):
    #Define título
    c.setFont("Verdana-Bold", 14)
    c.drawCentredString(300, 750, "TERMO DE ANUÊNCIA")
    # Adiciona informações do dicionário do PDF em um parágrafo justificado
    c.setFont("Verdana", 11)
    y_position = 700
    nome_em_negrito = f"<b>{declara['Nome']}</b>"
    text = f"Eu, {nome_em_negrito}, RG. {declara['RG']}, "
    # Para o caso de Servidor ou Não Servidor [RAI](da rua)
    if (len(declara['Cargo de Origem']) > 4):
        text += f"{declara['Cargo de Origem']}, "
    if (len(declara['Regime']) > 2):
        text += f"{declara['Regime']}, "
    
    text += f"concordo com\
                a {declara['Ato']}, em {declara['Jornada']}, para o cargo de {declara['Cargo']}"
    # Para o caso do "A partir" CAIeIII AP
    if  user_date_a_partir_variable is not None:
        text += f", a partir de {user_date_a_partir_variable}"
    # Para o caso de "Período Fechado" CAIII PF
    if (declara['Periodo Fechado'] is not None and date_periodofechado_inicio_variable is not None and date_periodofechado_fim_variable is not None) :#True:
        text += f", no período de {date_periodofechado_inicio_variable} a {date_periodofechado_fim_variable}"
    text += f", no(a) {declara['Destinação']}, do(a) {declara['UA']}, da {declara['Coordenadoria']}. "
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), fontSize=11, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 600 - p.height)
    c.setFont("Verdana", 11)
    c.drawRightString(500, 400, f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}.")
    #c.drawRightString(500, 215, f"______________________________________")
    c.drawRightString(500, 200, f"{declara['Nome']}")
    rodape(c)
    
def termo_de_compromisso_clt(c , declara):
    #Define título
    c.setFont("Verdana-Bold", 14)
    c.drawCentredString(300, 750, "TERMO DE COMPROMISSO")
    c.setFont("Verdana", 10)
    c.drawCentredString(300, 735, "(para servidores celetistas)")
    # Adiciona informações do dicionário do PDF em um parágrafo justificado
    c.setFont("Verdana", 11)
    y_position = 700
    nome_em_negrito = f"<b>{declara['Nome']}</b>"
    text = f"Eu, {nome_em_negrito}, RG. {declara['RG']}, {declara['Cargo de Origem']}, CLT, concordo com a \
            {declara['Ato']} para exercer o cargo de {declara['Cargo']}, do SQC-I, no(a) {declara['Destinação']},\
             do(a) {declara['UA']}, da {declara['Coordenadoria']}, comprometo-me a exercer o referido cargo em \
            {declara['Jornada']}."
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), fontSize=11, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700 - p.height)
    c.setFont("Verdana", 11)
    c.drawRightString(500, 400, f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}.")
    c.setFont("Verdana", 11)
    #c.drawRightString(500, 215, f"__________________________________________________")
    c.setFont("Verdana", 11)
    c.drawRightString(500, 200, f"{declara['Nome']}")
    rodape(c)
    
    
def declaracao_hipotese_inelegibilidade(c , declara):
    #Define título
    c.setFont("Verdana-Bold", 14)
    c.drawCentredString(300, 750, "DECLARAÇÃO")
    c.setFont("Verdana", 11)
    c.drawCentredString(300, 735, "(hipóteses de inelegibilidade)")
    c.setFont("Verdana", 11)
    y_position = 700
    nome_em_negrito = f"<b>{declara['Nome']}</b>"
    text =f"Eu, {nome_em_negrito}, RG. {declara['RG']}, CPF. {declara['CPF']}, brasileiro(a), {declara['Estado Civil']}, \
            declaro ter pleno conhecimento das disposições contidas no Decreto nº 57.970, de 12 de abril de 2012."
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), fontSize=11, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700 - p.height)
    text2 =f"Declaro ainda, sob as penas da lei, não incorrer em nenhuma das hipóteses de inelegibilidade previstas em lei federal."
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), fontSize=11, fontName="Verdana")
    p = Paragraph(text2, style)
    p.wrapOn(c, 400, 535)
    p.drawOn(c, 100, 625 - p.height)
    text3 =f"Assumo, por fim, o compromisso de comunicar a meu superior hierárquico, no prazo de 30 (trinta) dias subsequentes \
            à respectiva ciência, a superveniência de:"
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), fontSize=11, fontName="Verdana")
    p = Paragraph(text3, style)
    p.wrapOn(c, 400, 485)
    p.drawOn(c, 100, 585 - p.height)
    text =f"a) enquadramento em qualquer hipótese de inelegibilidade prevista em lei federal;"
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), fontSize=11, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 445)
    p.drawOn(c, 100, 483)
    text =f"b) instauração de processos administrativos ou judiciais cuja decisão possa importar \
            em inelegibilidade, nos termos de lei federal."
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), fontSize=11, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 415)
    p.drawOn(c, 100, 445)
    c.drawRightString(500, 350, f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}.")
    c.setFont("Verdana", 11)
    c.drawRightString(500, 200, f"{declara['Nome']}")
    rodape(c)
    
def declaracao_cargo_funcao(c , declara):
    c.setFont("Verdana-Bold", 14)
    c.drawCentredString(300, 750, "DECLARAÇÃO")
    c.setFont("Verdana", 11)
    y_position = 700
    nome_em_negrito = f"<b>{declara['Nome']}</b>"
    text =f"Eu, {nome_em_negrito}, RG. {declara['RG']}, "
    ####### Se o que consta no formulário também consta no autocompletar do campo este é exibido aqui   ############
    if (len(declara['Cargo de Origem']) > 4) : text +=f"{declara['Cargo de Origem']}, "
    if (len(declara['Regime']) > 2) : text+=f"{declara['Regime']}, "
    text +=f"DECLARO para fins de {declara['Ato']} no cargo de {declara['Cargo']}, no(a) {declara['Destinação']}, do(a) \
            {declara['UA']}, da {declara['Coordenadoria']}, que não exerço cargo ou função de direção, \
            gerência ou administração em entidades que mantenham contratos ou convênios com o Sistema Único \
            de Saúde - SUS/SP ou sejam por este credenciadas."
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700 - p.height)
    c.drawRightString(500, 400, f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}.")
    c.setFont("Verdana", 11)
    c.drawRightString(500, 200, f"{declara['Nome']}")
    rodape(c)
    
def declaracao_acumulo(c , declara):
    c.setFont("Verdana-Bold", 14)
    c.drawCentredString(300, 750, "DECLARAÇÃO DE ACÚMULO")
    y_position = 700
    text_bold =f"DECLARO, "
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), fontName="Verdana-Bold", fontSize=11)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700 - p.height)
    c.setFont("Verdana", 11)
    y_position = 700
    text_bold =f"sob pena de responsabilidade, para fins de acumulação que no âmbito do Serviço Público Federal, Estadual ou Municipal,\
            ou ainda em Autarquias, Fundações, Empresas Públicas, Sociedade de Economia Mista, suas subsidiárias e Sociedades Controladas,\
            direta ou indiretamente pelo Poder Público.:"
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), firstLineIndent = 65, fontSize=11)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700 - p.height)
    c.setFont("Verdana", 11)
    text=f"EU, {declara['Nome']}, RG Nº {declara['RG']},"
    style = ParagraphStyle(name='Justify', alignment=0, leading=(12*1.5), fontName="Verdana-Bold", fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 570)
    p.drawOn(c, 100, 570)
    text=f"não exerço"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    draw_checkbox(c, 100, 560 , checked=False)
    draw_checkbox(c, 180, 560 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 560)
    p.drawOn(c, 120, 560)
    text=f" exerço"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 560)
    p.drawOn(c, 198, 560)
    text=f"SE EXERCE "
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold", fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 530)
    p.drawOn(c, 100, 530)
        
    text=f"outro cargo"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    draw_checkbox(c, 100, 515 , checked=False)
    draw_checkbox(c, 210, 515 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 515)
    p.drawOn(c, 120, 515)

    text=f"emprego"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 515)
    p.drawOn(c, 228, 515)

    text=f"função pública"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 515)
    p.drawOn(c, 336, 515)
    draw_checkbox(c, 318, 515 , checked=False)
    
    text=f"Onde:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold", fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 480)
    p.drawOn(c, 100, 480)
    
    text=f"Cargo/E/FP:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold", fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 450)
    p.drawOn(c, 100, 450)
    
    text=f"APOSENTADO "
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold", fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 400)
    p.drawOn(c, 100, 400)
        
    text=f"Sim"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    draw_checkbox(c, 135, 380 , checked=False)
    draw_checkbox(c, 238, 380 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 380)
    p.drawOn(c, 100, 380)

    text=f"Não"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 380)
    p.drawOn(c, 210, 380)
    
    text=f"SE SIM: "
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold", fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 335)
    p.drawOn(c, 100, 335)
        
    
    text=f"Orgão Público"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    draw_checkbox(c, 190, 315 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 315)
    p.drawOn(c, 100, 315)
    
    text=f"Qual: "
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold", fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 320, 315)
    p.drawOn(c, 210, 315)
    
    text=f"Cargo: "
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold", fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 320, 290)
    p.drawOn(c, 210, 290)

    text=f"D.O.E da Aposentadoria: "
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold", fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 320, 260)
    p.drawOn(c, 210, 260)
    
    text=f"Empresa Privada "
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    draw_checkbox(c, 190, 230 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 230)
    p.drawOn(c, 100, 230)

    text=f"Onde: "
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 320, 230)
    p.drawOn(c, 250, 230)
    
    text=f"Outro"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    p = Paragraph(text, style)
    p.wrapOn(c, 320, 210)
    p.drawOn(c, 250, 210)
    draw_checkbox(c, 280, 210 , checked=False)
    c.drawRightString(500, 210, f"_________________________")
    nome_em_negrito = f"<b>{declara['Nome']}</b>"

    c.setFont("Verdana", 11)
    c.drawCentredString(300, 150, f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}.")
    c.setFont("Verdana-Bold", 11)
    c.drawCentredString(300, 100, f"{declara['Nome']}")
    rodape(c)
    
def anexo_i(c , declara):
       
    y_position = 780
    text =f"ANEXO I"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 730)
    p.drawOn(c, 100, 780 - p.height)
    y_position = 600
    text_bold =f"a que se referem os artigos 1º e 2º do Decreto nº 54.376,\
                    de 26 de maio de 2009 alterado pelo artigo\
                    1º do Decreto nº 67.445, de 12 de janeiro de 2023"
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold", fontSize=11)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700)

    c.setFont("Verdana", 11)
    y_position = 700
    text_bold =f"DECLARAÇÃO DE PARENTESCO"
    
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 550)
    p.drawOn(c, 100, 665 - p.height)

    c.setFont("Verdana", 11)
    y_position = 650
    text_bold =f"( SÚMULA VINCULANTE Nº 13 DO STF )"
    
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 532)
    p.drawOn(c, 100, 647- p.height)
    
    nome_em_negrito = f"<b>{declara['Nome']}</b>"
    text =f"Nome: {nome_em_negrito}"
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 618)
    p.drawOn(c, 100, 600 - p.height)
    #c.rect(80, 300, 50, 50)
    
    text =f"RG : {declara['RG']}"
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 582 - p.height)

    text =f"CPF : {declara['CPF']}"
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 582)
    p.drawOn(c, 100, 564 - p.height)

    c.rect(90, 300, 450, 236)
    y_position = 350
    text_bold =f"É cônjuge, companheiro ou parente em linha reta, colateral ou por afinidade, até o terceiro grau, inclusive,\
                da autoridade nomeante ou de servidor do Poder Executivo investido em cargo de direção, chefia ou assessoramento?"
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 425)
    p.drawOn(c, 100, 475)
    
    text=f"NÃO"
    style = ParagraphStyle(name='Justify', alignment=4, IdentFirstLine = 10)
    draw_checkbox(c, 100, 430 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 200, 430)
    p.drawOn(c, 120, 430)
    
    text=f"SIM"
    style = ParagraphStyle(name='Justify', alignment=4, IdentFirstLine = 10)
    draw_checkbox(c, 100, 450 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 200, 450)
    p.drawOn(c, 120, 450)
    
    y_position = 400
    text_bold =f"Em caso positivo, apontar:  ⤵ ⤵ ⤵ ⤵ ⤵"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 400)
    p.drawOn(c, 100, 380)
    c.setFont("Verdana", 11)
    
    y_position = 420
    text_bold =f"Nome:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 380)
    p.drawOn(c, 100, 360)
    c.drawRightString(500, 360, f"__________________________________________________")
    
    y_position = 240
    text_bold =f"Relação de Parentesco:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 358)
    p.drawOn(c, 100, 340)
    c.drawRightString(500, 340, f"_______________________________________")

    y_position = 240
    text_bold =f"Cargo:"
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 348)
    p.drawOn(c, 100, 320)
    c.drawRightString(500, 320, f"___________________________________________________")
    c.rect(90, 222, 450, 70)
    
    text =f"Informe também a existência de cônjuge, companheiro ou parente em linha reta, colateral ou por afinidade,\
            até o terceiro grau, inclusive, no exercício de cargo de direção, chefia ou assessoramento no âmbito dos \
            Poderes Judiciário ou Legislativo, do Ministério Público, da Defensoria Pública, das Autarquias \
            (inclusive das universidades públicas), das empresas controladas pelo Estado e das fundações \
            instituídas e mantidas pelo Poder Público:"
    
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text, style)
    p.wrapOn(c, 425, 220)
    p.drawOn(c, 100, 145)
    
    c.rect(90, 140, 450, 75)
    text_bold =f"OBSERVAÇÕES:"
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 260)
    p.drawOn(c, 100, 278)
    text_bold =f"   Parentes em linha reta: pais, avós, bisavós, filho[a], neto[a] e bisneto[a].\
                    Parentes em linha colateral: irmão(ã), tio(a) e sobrinho(a).\
                    Parentes por afinidade: genro, nora, sogro(a), enteado(a), \
                    madrasta, padrasto e cunhado(a) e concunhado(a)."
    
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 190)
    p.drawOn(c, 100, 240)
    c.setFont("Verdana", 11)
    c.setFont("Verdana", 11)
    text=f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}."
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 100)
    p.drawOn(c, 100, 110)
    
    text=f"__________________________________________________"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 75)
    p.drawOn(c, 100, 85)
    
    text=f"{declara['Nome']}"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 60)
    p.drawOn(c, 100, 70)
    rodape(c)
    c.showPage()
    informacoes_adicionais(c, declara)

    
def informacoes_adicionais(c , declara):
    c.rect(50, 750, 500, 40)
    c.setFont("Verdana-Bold", 12)
    c.drawCentredString(300, 765, f"INFORMAÇÕES ADICIONAIS")
    c.rect(50, 480, 500, 270)
    text_bold =f"<u>DO SERVIDOR</u>"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 550, 725)
    p.drawOn(c, 60, 735)
    
    do_servidor_1 =f"1) Indicar o cargo em comissão ou a função de confiança/gratificada de que é ocupante:\v\
                     Cargo/função:_______________________________________________________________\v\
                     Órgão/entidade:_____________________________________________________________\v"
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana", leading=(12*1.5))
    p = Paragraph(do_servidor_1, style)
    p.wrapOn(c, 480, 650)
    p.drawOn(c, 60, 670)
    
    do_servidor_2a =f"2) É ocupante de cargo efetivo/função permanente?"
    style = ParagraphStyle(name='Justify', alignment=0, fontName="Verdana", leading=(12*1.5))
    p = Paragraph(do_servidor_2a, style)
    p.wrapOn(c, 490, 625)
    p.drawOn(c, 60, 635)
    
    do_servidor_2b =f"Em caso positivo, indicar:"
    style = ParagraphStyle(name='Justify', alignment=0, fontName="Verdana", leading=(12*1.5))
    p = Paragraph(do_servidor_2b, style)
    p.wrapOn(c, 490, 605)
    p.drawOn(c, 60, 615)
    
    text=f"Sim"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 500, 630)
    p.drawOn(c, 410, 640)
    draw_checkbox(c, 390, 640 , checked=False)
    
    text=f"Não"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 600, 630)
    p.drawOn(c, 460, 640)
    draw_checkbox(c, 440, 640 , checked=False)
    do_servidor_2c =f"Cargo/função:_______________________________________________________________\v\
                     Órgão/entidade:_____________________________________________________________\v"
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana", leading=(12*1.5))
    p = Paragraph(do_servidor_2c, style)
    p.wrapOn(c, 490, 555)
    p.drawOn(c, 60, 575)
    
    do_servidor_3a =f"3) A nomeação/admissão/designação para o cargo em comissão ou função de confiança/gratificada\
                        ocorreu antes ou após a edição da Súmula Vinculante nº 13 do Supremo Tribunal Federal\
                        , de 29 de agosto de 2008?"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana", leading=(12*1.5))
    p = Paragraph(do_servidor_3a, style)
    p.wrapOn(c, 480, 500)
    p.drawOn(c, 60, 510)
    
    do_servidor_3b =f"Indicar a data: ____ / ____ / ________."
    style = ParagraphStyle(name='Justify', alignment=0, fontName="Verdana", leading=(12*1.5))
    p = Paragraph(do_servidor_3b, style)
    p.wrapOn(c, 490, 490)
    p.drawOn(c, 60, 490)
    
    c.rect(50, 150, 500, 330)
    text_bold =f"<u>DO PARENTE</u>"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 480, 460)
    p.drawOn(c, 60, 460)
    
    do_parente_1 =f"1) Indicar o cargo em comissão ou a função de confiança/gratificada de que o parente é ocupante:\v\
                     Cargo/função:______________________________________________________________\v\
                     Órgão/entidade:____________________________________________________________\v"
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana", leading=(12*1.5))
    p = Paragraph(do_parente_1, style)
    p.wrapOn(c, 480, 380)
    p.drawOn(c, 60, 380)
    
    do_parente_2a =f"2) O parente é ocupante de cargo efetivo/função permanente?"
    style = ParagraphStyle(name='Justify', alignment=0, fontName="Verdana", leading=(12*1.5))
    p = Paragraph(do_parente_2a, style)
    p.wrapOn(c, 490, 340)
    p.drawOn(c, 60, 340)
    
    do_parente_2b =f"Em caso positivo, indicar:"
    style = ParagraphStyle(name='Justify', alignment=0, fontName="Verdana", leading=(12*1.5))
    p = Paragraph(do_parente_2b, style)
    p.wrapOn(c, 490, 320)
    p.drawOn(c, 60, 320)
    
    text=f"Sim"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 500, 345)
    p.drawOn(c, 410, 345)
    draw_checkbox(c, 390, 345 , checked=False)
    
    text=f"Não"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 600, 345)
    p.drawOn(c, 460, 345)
    draw_checkbox(c, 440, 345 , checked=False)
    
    
    do_parente_2c =f"Cargo/função:_______________________________________________________________\v\
                     Órgão/entidade:_____________________________________________________________\v"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana", leading=(12*1.5))
    p = Paragraph(do_parente_2c, style)
    p.wrapOn(c, 490, 280)
    p.drawOn(c, 60, 280)
    
    do_parente_3a =f"3) A nomeação/admissão/designação para o cargo em comissão ou função de confiança/gratificada\
                        ocorreu antes ou após a edição da Súmula Vinculante nº 13 do Supremo Tribunal Federal\
                        , de 29 de agosto de 2008?"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana", leading=(12*1.5))
    p = Paragraph(do_parente_3a, style)
    p.wrapOn(c, 480, 200)
    p.drawOn(c, 60, 200)
    
    do_parente_3b =f"Indicar a data: ____ / ____ / ________."
    style = ParagraphStyle(name='Justify', alignment=0, fontName="Verdana", leading=(12*1.5))
    p = Paragraph(do_parente_3b, style)
    p.wrapOn(c, 490, 150)
    p.drawOn(c, 60, 150)
    
    c.setFont("Verdana", 11)
    text=f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}."
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 100)
    p.drawOn(c, 100, 110)
    
    text=f"__________________________________________________"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 75)
    p.drawOn(c, 100, 85)
    
    text=f"{declara['Nome']}"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 60)
    p.drawOn(c, 100, 70)
    rodape(c)
    
    
def anexo_iii(c , declara):
    y_position = 780
    text =f"ANEXO III"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 730)
    p.drawOn(c, 100, 780 - p.height)
    y_position = 600
    text_bold =f"a que se referem o artigo 5º do Decreto nº 54.376,\
                    de 26 de maio de 2009 alterado pelo artigo\
                    1º do Decreto nº 67.445, de 12 de janeiro de 2023"
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700)

    c.setFont("Verdana", 11)
    y_position = 700
    text_bold =f"DECLARAÇÃO DE PARENTESCO"
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 550)
    p.drawOn(c, 100, 665 - p.height)

    c.setFont("Verdana", 11)
    y_position = 650
    text_bold =f"( SÚMULA VINCULANTE Nº 13 DO STF )"
    
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 532)
    p.drawOn(c, 100, 647- p.height)

    nome_em_negrito = f"<b>{declara['Nome']}</b>"
    text =f"Nome: {nome_em_negrito}"
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 618)
    p.drawOn(c, 100, 600 - p.height)
    c.rect(90, 550, 450, 50)
    
    text =f"RG : {declara['RG']}"
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 582 - p.height)

    text =f"CPF : {declara['CPF']}"
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 582)
    p.drawOn(c, 100, 564 - p.height)
    c.rect(90, 300, 450, 236)
    y_position = 350
    text_bold =f"É cônjuge, companheiro ou parente em linha reta, colateral ou por afinidade, até o terceiro grau, inclusive,\
                da autoridade nomeante ou de servidor do Poder Executivo investido em cargo de direção, chefia ou assessoramento?"
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 425)
    p.drawOn(c, 100, 475)
    
    text=f"NÃO"
    style = ParagraphStyle(name='Justify', alignment=4, IdentFirstLine = 10)
    draw_checkbox(c, 100, 430 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 200, 430)
    p.drawOn(c, 120, 430)
    
    text=f"SIM"
    style = ParagraphStyle(name='Justify', alignment=4, IdentFirstLine = 10)
    draw_checkbox(c, 100, 450 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 200, 450)
    p.drawOn(c, 120, 450)
    
    y_position = 400
    text_bold =f"Em caso positivo, apontar:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 400)
    p.drawOn(c, 100, 380)
    c.setFont("Verdana", 11)
    
    y_position = 420
    text_bold =f"Nome:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 380)
    p.drawOn(c, 100, 360)
    c.drawRightString(500, 360, f"_____________________________________________________")
    
    y_position = 240
    text_bold =f"Relação de Parentesco:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 358)
    p.drawOn(c, 100, 340)
    c.drawRightString(500, 340, f"_______________________________________")

    y_position = 240
    text_bold =f"Cargo:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 348)
    p.drawOn(c, 100, 320)
    c.drawRightString(500, 320, f"_____________________________________________")

    c.rect(90, 222, 450, 70)
    
    text =f"Informe também a existência de cônjuge, companheiro ou parente em linha reta, colateral ou por afinidade,\
            até o terceiro grau, inclusive, no exercício de cargo de direção, chefia ou assessoramento no âmbito dos \
            Poderes Judiciário ou Legislativo, do Ministério Público, da Defensoria Pública, das Autarquias \
            (inclusive das universidades públicas), das empresas controladas pelo Estado e das fundações \
            instituídas e mantidas pelo Poder Público:"
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text, style)
    p.wrapOn(c, 425, 220)
    p.drawOn(c, 100, 145)
    c.rect(90, 140, 450, 75)
    text_bold =f"OBSERVAÇÕES:"
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 260)
    p.drawOn(c, 100, 278)
    
    text_bold =f"   Parentes em linha reta: pais, avós, bisavós, filho[a], neto[a] e bisneto[a].\
                    Parentes em linha colateral: irmão(ã), tio(a) e sobrinho(a).\
                    Parentes por afinidade: genro, nora, sogro(a), enteado(a), \
                    madrasta, padrasto e cunhado(a) e concunhado(a)."
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 190)
    p.drawOn(c, 100, 240)
    #c.setFont("Verdana", 12)
    c.setFont("Verdana", 11)
    text=f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}."
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 100)
    p.drawOn(c, 100, 110)
    
    text=f"__________________________________________________"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 75)
    p.drawOn(c, 100, 85)
    
    text=f"{declara['Nome']}"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 60)
    p.drawOn(c, 100, 70)
    rodape(c)
    c.showPage()
    informacoes_adicionais(c, declara)
    
    
def declaracao_de_parentesco(c , declara):
    y_position = 780
    c.setFont("Verdana-Bold", 14)
    c.drawCentredString(300, 780, "DECLARAÇÃO DE PARENTESCO")

    # Definir a largura do texto para sublinhar corretamente
    text_width = c.stringWidth("DECLARAÇÃO DE PARENTESCO", "Verdana-Bold", 14)

    # Desenhar a linha abaixo do texto
    underline_y = 778  # Ajustar conforme necessário
    #c.setFont("Verdana", 16)
    c.line(300 - text_width / 2, underline_y, 300 + text_width / 2, underline_y)
    
    c.setFont("Verdana", 10)
    c.drawCentredString(300, 766, "(ANEXO a que se refere o inciso V do artigo 9º do Decreto nº 68.829/2024)")

    nome_em_negrito = f"{declara['Nome']}"
    nome =f"<b>NOME:</b> {nome_em_negrito}"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)#, leading=(12*1.5))
    p = Paragraph(nome, style)
    p.wrapOn(c, 400, 742)#718
    p.drawOn(c, 58, 742 - p.height)#700
    
    c.rect(50, 720, 495, 30)
    c.rect(50, 690, 247.5, 30)
    c.rect(297.5, 690, 247.5, 30)
    
    text =f"<b>RG</b> : {declara['RG']}"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)#, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 712.5)
    p.drawOn(c, 58, 712.5 - p.height)

    text_cpf =f"<b>CPF :</b> {declara['CPF']}"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)#, leading=(12*1.5))
    p = Paragraph(text_cpf, style)
    p.wrapOn(c, 400, 712.5)
    p.drawOn(c, 300, 712.5 - p.height)
    #c.rect(90, 300, 450, 236)
    y_position = 350
    text_descricao =f"É cônjuge, companheiro ou familiar em linha reta<sup><i>(1)</i></sup> ou colateral<sup><i> (2) </i></sup>, por consanguinidade ou afinidade<sup><i>(3)</i></sup>, \
                    até o terceiro grau inclusive, da autoridade nomeante ou de agente público do Poder Executivo do Estado de São Paulo\
                    que ocupe cargo ou função de confiança? <i> (Exemplo: Diretoria, Chefia, Assessoramento ou similares) </i>"
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana", fontSize=11)
    p = Paragraph(text_descricao, style)
    p.wrapOn(c, 480, 670)
    p.drawOn(c, 58, 670 - p.height)
    c.rect(50, 580, 495, 95)
    
    text_nao=f"<b>NÃO</b>."
    style = ParagraphStyle(name='Justify', alignment=4, IdentFirstLine = 10, fontSize=11)
    draw_checkbox(c, 58, 598 , checked=False)
    p = Paragraph(text_nao, style)
    p.wrapOn(c, 200, 598)
    p.drawOn(c, 78, 598)
    
    text_sim=f"<b>SIM</b>. Em caso positivo apontar:"
    #draw_arrow(c, 225, 590, size=9, line_width=2.5)
    
       
    try:
        #image_path = "pbaixo.png"
        image_path = "pbaixo.jpg"
        # Obtém as dimensões originais da imagem
        img = Image.open(image_path)
        aspect_ratio = img.width / img.height
        # Mantém a proporção da imagem enquanto define uma largura
        desired_width = 8
        desired_height = desired_width / aspect_ratio
        # Insere a imagem com o tamanho proporcional
        c.drawImage(image_path, x=235, y=583, width=desired_width, height=desired_height)
    except:
        # Se a imagem falhar, desenha a seta
        draw_arrow(c, 235, 591, size=9, line_width=2.5)

    style = ParagraphStyle(name='Justify', alignment=4, IdentFirstLine = 10, fontSize=11)
    draw_checkbox(c, 58, 583 , checked=False)
    p = Paragraph(text_sim, style)
    p.wrapOn(c, 200, 583)
    p.drawOn(c, 78, 583)
    y_position = 420
    text_autoridade =f"NOME DA AUTORIDADE<sup><i>(4)</i></sup>/OCUPANTE DE CARGO OU FUNÇÃO DE CONFIANÇA:"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    p = Paragraph(text_autoridade, style)
    p.wrapOn(c, 480, 565)
    p.drawOn(c, 58, 565)
    c.rect(50, 545, 495, 35)
    
    y_position = 240
    text_relacao =f"RELAÇÃO DE PARENTESCO:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana", fontSize=11)
    p = Paragraph(text_relacao, style)
    p.wrapOn(c, 480, 530)
    p.drawOn(c, 58, 530)
    c.rect(50, 510, 495, 35)
    text_bold =f"CARGO/FUNÇÃO OCUPADA:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana", fontSize=11)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 495)
    p.drawOn(c, 58, 495)
    c.rect(50, 475, 495, 35)
    
    text_bold =f"ÓRGÃO DA AUTORIDADE OU OCUPANTE DE CARGO OU FUNÇÃO DE CONFIANÇA:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana", fontSize=11)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 490, 460)
    p.drawOn(c, 58, 460)
    c.rect(50, 440, 495, 35)
    c.rect(50, 327.5, 495, 100)
    text_bold =f"<b>DECLARAÇÃO:</b>"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 480, 412.5)
    p.drawOn(c, 58, 412.5)
    
    text_bold =f"Declaro para os devidos fins que desconheço a atuação com valimento do cargo<sup><i>(5)</i></sup> de autoridade que seja meu/minha cônjuge,\
                    companheiro(a) ou parente em linha reta, colateral ou por afinidade, até o terceiro grau, com fins de viabilizar minha nomeação\
                    em cargo em comissão/função de confiança/demais situações previstas no Art. 7º do Decreto 68.829/2024<sup><i>(6)</i></sup>, ou mesmo para a realização\
                    de ajustes de nomeações ou designações recíprocas, envolvendo outros órgãos e entidades do poder judiciário, legislativo ou Ministério Público."
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=11)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 480, 330)
    p.drawOn(c, 58, 330)
    c.rect(50, 80, 495, 240)
    
    text_bold =f"<b>OBSERVAÇÕES:</b>"
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 480, 307)
    p.drawOn(c, 58, 307)
    
    
    text_obs =f"<sup><i>(1)</i></sup><u>Parentes em linha reta</u>: pais, avós, bisavós, filho(a), neto(a) e bisneto(a);<br/>\
                <sup><i>(2)</i></sup><u>Parentes em linha colateral</u>: irmão(ã), tio(a), sobrinho(a);<br/>\
                <sup><i>(3)</i></sup><u>Parentes por afinidade</u>: genro, nora, sogro(a), enteado(a), madrasta, padrasto e cunhado(a);<br/>\
                <sup><i>(4)</i></sup><u>Autoridade</u>: Governador e o Vice-Governador, Secretário-Chefe, Chefe da Casa Militar, Secretário(s), o Procurador Geral, Controlador Geral, Coordenadores\
                , Diretores, Chefes, Encarregados,Supervisores, Assessores, Autoridades máximas de entidades (Estatais, Autarquias, Paraestatais, Empresas Públicas, Fundações, Institutos, por exemplo);<br/>\
                <sup><i>(5)</i></sup><u>Valimento do cargo</u>: utilização/servir-se do cargo para proveito/benefício pessoal ou de outra pessoa.<br/>\
                <sup><i>(6)</i></sup>Decreto nº 68.829/2024:<br/>\
                &nbsp &quot Artigo 7º - As vedações para contratação, designação e nomeação de parente das autoridades de que trata o artigo &nbsp 3º, nas respectivas áreas de influência, abrangem:<br/>\
                &nbsp &nbsp I - cargo em comissão, emprego público ou função de confiança;<br/>\
                &nbsp   II - gratificações cuja concessão ou a cessação possa ser realizada mediante ato discricionário da autoridade &nbsp competente;<br/>\
                &nbsp &nbsp III - prestação de serviço terceirizado mediante contratos com órgãos ou entidades;<br/>\
                &nbsp &nbsp IV - membros de colegiados da Administração Pública estadual;<br/>\
                &nbsp &nbsp V - contratado para atendimento à necessidade temporária de excepcional interesse público;<br/>\
                &nbsp &nbsp VI - estagiários.<br/>\
                &nbsp §1º - As vedações dos incisos V e VI deste artigo não se aplicam caso o ingresso seja precedido de processo seletivo.<br/>\
                &nbsp §2º - As vedações dos incisos III, V e VI deste artigo não se aplicam àqueles que previamente atuam em órgão ou entidade e que tenha seu parente\
                nomeado ou designado para cargo em comissão ou função de confiança nesse mesmo órgão ou entidade.&quot"
    style = ParagraphStyle(name='Justify', alignment=4, fontSize=9, leading=10)
    p = Paragraph(text_obs, style)
    p.wrapOn(c, 480, 82.5)
    p.drawOn(c, 60, 82.5)
           
    c.setFont("Verdana", 11)
    text=f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}."
    style = ParagraphStyle(name='Left', alignment=0, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 480, 62.5)
    p.drawOn(c, 55, 62.5)
    
    text=f"__________________________________________________"
    style = ParagraphStyle(name='Center', alignment=1, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 495, 40)
    p.drawOn(c, 50, 40)
    
    text=f"{declara['Nome']}"
    style = ParagraphStyle(name='Center', alignment=1, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 495, 25)
    p.drawOn(c, 50, 25)
    rodape(c)
    
def declaracao(declara, statusbar_text):
    
    search_font_verdana()
    nome_arquivo = f"{declara['Nome']} - {declara['Cargo']}.pdf"
    path_check(declara, statusbar_text)

    c = canvas.Canvas(f"./{declara['Ato']}/{declara['Nome']}/{nome_arquivo}", pagesize=A4)
    try:
        #print (date_periodofechado_inicio_variable)
        #print (date_periodofechado_fim_variable)
        #print (toggle_check_periodo_fechado)
        #print(has_date_period_closed)
        gerar_declaracoes(c, declara)
    finally:
        c.save()  # Salva o conteúdo do canvas em um arquivo PDF
        del c     # Libera os recursos do canvas
        subprocess.Popen([f"./{declara['Ato']}/{declara['Nome']}/{nome_arquivo}"], shell=True)
    
def gerar_declaracoes(c, declara):
    declaracao_experiencia(c, declara)
    c.showPage()
    termo_de_anuencia(c, declara)
    c.showPage() 
####### Se for CLT entra aqui o Termo de Compromisso CLT################
    if is_clt(declara):
        termo_de_compromisso_clt(c, declara)
        c.showPage()
#########################################################################
    declaracao_hipotese_inelegibilidade(c, declara)
    c.showPage()
    declaracao_cargo_funcao(c, declara)
    c.showPage()
    declaracao_acumulo(c, declara)
    c.showPage()
    declaracao_de_parentesco(c, declara)
    c.showPage()

def is_designacao(declara):
    return declara['Ato'] == 'Designação'

def is_designacao_nomeacao(declara):
    return declara['Ato'] == 'Designação com posterior Nomeação'

def is_nomeacao(declara):
    return declara['Ato'] == 'Nomeação'

def is_clt(declara):
    return declara['Regime'] == 'CLT'

def has_date_period_closed(declara):
    inicio_var = declara.get('date_periodofechado_inicio_variable')
    fim_var = declara.get('date_periodofechado_fim_variable')
    return inicio_var is not None and fim_var is not None

def is_designacao_com_nomeacao(declara):
    return declara['Ato'] == 'Designação com posterior Nomeação'

def draw_checkbox(c, x, y, size=10, checked=False):
################## Desenha o quadrado ################
    c.rect(x, y, size, size)
    if checked:
        #  Desenha a marca de seleção   #
        c.line(x, y, x + size, y + size)
        c.line(x, y + size, x + size, y)
        
        
def draw_arrow(c, x, y, size=20, line_width=2):
    """
    Desenha uma seta mais compacta que vai para a direita e depois para baixo, com uma ponta simples.
    
    :param c: Canvas do ReportLab
    :param x: Posição X inicial da seta
    :param y: Posição Y inicial da seta
    :param size: Tamanho da seta
    :param line_width: Largura do traçado da seta
    """
    # Salva o estado atual do canvas
    c.saveState()

    # Define a largura do traçado apenas para a seta
    c.setLineWidth(line_width)
    
    # Linha horizontal (vai para a direita)
    c.line(x, y, x + size, y)
    
    # Linha vertical (aponta para baixo)
    c.line(x - 1 + size, y - 1, x + size -1, y - size)
    #c.line(x + size, y - 1, x + size , y - size)
    
    # Desenhar a ponta da seta como um triângulo compacto
    arrow_head_size = size / 2  # Define o tamanho da ponta da seta

    # Ponta da seta sobre a linha vertical
    c.line(x  + size - arrow_head_size , y - size + arrow_head_size, x + size, y - size)  # Diagonal esquerda
    c.line(x - 1.8 + size + arrow_head_size , y - size + arrow_head_size, x + size, y - size)  # Diagonal direita
    
    # Restaura o estado anterior do canvas (volta ao line_width original)
    c.restoreState()

def cargo_de_origem(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                        estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                        coordenadoria_combo, regime_combo):
    global cargo_origem_list
    #regime_combo.config(state="enable")
    ua = ua_combo.get() 
    cargo_origem_list = cargo_origem_combo["completevalues"]
    btn_on(btn_n_servidor, btn_servidor, cargo_origem_combo, ato_combo, nome_entry, rg_entry, cpf_entry,
                estado_civil_combo, jornada_combo, lei_combo, cargo_combo, destinacao_entry, ua_combo,
                coordenadoria_combo, regime_combo)
    
def filter_combobox(event, valores, combo):
    typed = combo.get().lower()
    if typed == "":
        combo['values'] = valores
    else:
        filtered_items = [item for item in valores if typed in item.lower()]
        combo['values'] = filtered_items

def on_select(event, valores, combo):
    selected = event.widget.get()
    if selected not in combo['values']:
        messagebox.showinfo("Atenção", "O valor preenchido não consta na lista atual.")
        combo.focus()

def on_select_estado_civil(event, nome_entry, rg_entry, cpf_entry, ato_combo, statusbar_text, estado_civil_combo):
  
    if len(nome_entry.get()) < 3 :
        statusbar_text.set("Favor preencher o nome do servidor")
        nome_entry.focus()
        ato_combo.config(state="disable")
    elif len(rg_entry.get()) < 4 :
        statusbar_text.set("Favor preencher o RG do servidor")
        rg_entry.focus()
        ato_combo.config(state="disable")
    elif len(cpf_entry.get()) < 1 :
        statusbar_text.set("Favor preencher o cpf do servidor")
        cpf_entry.focus()
        ato_combo.config(state="disable")
    elif len(cpf_entry.get()) > 1 and len(nome_entry.get()) > 3 and len(rg_entry.get()) > 4 and (estado_civil_combo.get() in estado_civil_combo['values']):
        ato_combo.config(state="readonly")
        #ato_combo.focus()
    
def search_font_verdana():
    # Diretório padrão de fontes do Windows
    fonts_directory = "C:\\Windows\\Fonts\\"
    # Nomes dos arquivos de fonte que estamos procurando
    font_files = {
        "Verdana": "verdana.ttf",
        "Verdana-Bold": "verdanab.ttf",
        "Verdana-Italic": "verdanai.ttf"
    }
    # Verifica se os arquivos de fonte existem
    existing_fonts = {}
    for font_name, font_file in font_files.items():
        font_path = os.path.join(fonts_directory, font_file)
        if os.path.exists(font_path):
            existing_fonts[font_name] = font_path
    # Registra as fontes existentes no ReportLab
    for font_name, font_path in existing_fonts.items():
        pdfmetrics.registerFont(TTFont(font_name, font_path))
    
def on_select_regime_combo(cargo_origem_combo, regime_combo):
    
    if regime_combo.get() == "":
        cargo_origem_combo["completevalues"] = [""]
        #print("Nada no Regime")
    elif regime_combo.get() == "Comissão":
        cargo_origem_combo["completevalues"] = [
                                                "Assessor de Gabinete I"                , 
                                                "Assessor de Gabinete II"               , 
                                                "Assessor I"                            ,
                                                "Assessor Técnico de Coordenador"       ,
                                                "Assessor Técnico de Gabinete I"        ,
                                                "Assessor Técnico de Gabinete II"       ,
                                                "Assessor Técnico de Gabinete III"      ,
                                                "Assessor Técnico de Gabinete IV"       ,
                                                "Assessor Técnico I"                ,
                                                "Assessor Técnico II"   	            ,
                                                "Assessor Técnico III"                ,
                                                "Assessor Técnico IV"   	            ,
                                                "Assessor Técnico V"    	            ,
                                                "Chefe de Gabinete"     	            ,
                                                "Chefe I"   	                        ,
                                                "Chefe II"      	                    ,
                                                "Diretor I"                            ,
                                                "Diretor II"    	                    ,
                                                "Diretor III"                           ,
                                                "Diretor Técnico I"                    ,
                                                "Diretor Técnico II"    	            ,
                                                "Diretor Técnico III"   	            ,
                                                "Encarregado I"     	                ,
                                                "Encarregado II"    	                ,
                                                "Supervisor Técnico I"                  ,
                                                "Assessor Técnico de Coordenador de Saúde"  ,
                                                "Assessor Técnico em Saúde Pública I"       ,
                                                "Assessor Técnico em Saúde Pública II"      ,
                                                "Assessor Técnico em Saúde Pública III"     ,
                                                "Chefe de Saúde I"                          ,
                                                "Chefe de Saúde II"                         ,
                                                "Cirurgião Dentista Sanitarista Inspetor"   ,
                                                "Coordenador de Saúde"                      ,
                                                "Diretor Técnico de Saúde I"                ,
                                                "Diretor Técnico de Saúde II"               ,
                                                "Diretor Técnico de Saúde III"              ,
                                                "Encarregado de Saúde I"                    ,
                                                "Encarregado de Saúde II"                   ,
                                                "Enfermeiro Inspetor de Saúde Pública"      ,
                                                "Engenheiro Sanitarista Assessor"           ,
                                                "Médico Inspetor"                           ,
                                                "Supervisor de Equipe Técnica de Saúde"     ,
                                                "Supervisor de Saúde" 
                                                ]
    elif regime_combo.get() != "Comissão":
        cargo_origem_combo["completevalues"] = [
                            "Agente Administrativo",
                            "Agente Administrativo de Ensino",
                            "Agente de Administração Pública",
                            "Agente de Apoio a Pesquisa Científica e Tecnológica",
                            "Agente de Apoio Agropecuário",
                            "Agente de Áreas de Administração Geral",
                            "Agente de Desenvolvimento Educacional",
                            "Agente de Desenvolvimento Social",
                            "Agente de Escolta e Vigilância Penitenciária",
                            "Agente de Ofícios e Manutenção",
                            "Agente de Organização Escolar",
                            "Agente de Pessoal",
                            "Agente de Praça de Pedágio",
                            "Agente de Praça de Pesagem",
                            "Agente de Saneamento",
                            "Agente de Saúde",
                            "Agente de Segurança Penitenciária de Classe I",
                            "Agente de Segurança Penitenciária de Classe II",
                            "Agente de Segurança Penitenciária de Classe III",
                            "Agente de Segurança Penitenciária de Classe IV",
                            "Agente de Segurança Penitenciária de Classe V",
                            "Agente de Segurança Penitenciária de Classe VI",
                            "Agente de Segurança Penitenciária de Classe VII",
                            "Agente de Segurança Penitenciária de Classe VIII",
                            "Agente de Serviços Escolares",
                            "Agente de Serviços Técnicos",
                            "Agente de Telecomunicações Policial de 1ª Classe",
                            "Agente de Telecomunicações Policial de 2ª Classe",
                            "Agente de Telecomunicações Policial de 3ª Classe",
                            "Agente de Telecomunicações Policial de 4ª Classe",
                            "Agente de Telecomunicações Policial de 5ª Classe",
                            "Agente de Telecomunicações Policial de Classe Especial",
                            "Agente de Tráfego",
                            "Agente Fiscal de Rendas",
                            "Agente Operacional",
                            "Agente Policial de 1ª Classe",
                            "Agente Policial de 2ª Classe",
                            "Agente Policial de 3ª Classe",
                            "Agente Policial de 4ª Classe",
                            "Agente Policial de 5ª Classe",
                            "Agente Policial de Classe Especial",
                            "Agente Regional de Saúde Pública",
                            "Agente Técnico de Assistência à Saúde",
                            "Agente Técnico de Saúde",
                            "Ajudante de Laboratório",
                            "Almoxarife",
                            "Análise Clínica",
                            "Análise Clínica",
                            "Análises Clínicas"
                            "Analista Administrativo",
                            "Analista de Tecnologia",
                            "Analista Sociocultural",
                            "Arquiteto (vide Lei Complementar 540/88)",
                            "Arquiteto I",
                            "Arquiteto II",
                            "Arquiteto III",
                            "Arquiteto IV",
                            "Arquiteto V",
                            "Arquiteto VI",
                            "Arrais",
                            "Ascensorista",
                            "Assistente Agropecuário I",
                            "Assistente Agropecuário II",
                            "Assistente Agropecuário III",
                            "Assistente Agropecuário IV",
                            "Assistente Agropecuário V",
                            "Assistente Agropecuário VI",
                            "Assistente de Administração Escolar",
                            "Assistente de Aeroporto",
                            "Assistente de Diretor de Escola",
                            "Assistente Social",
                            "Assistente Social Encarregado",
                            "Assistente Social Encarregado de Turno",
                            "Assistente Técnico de Pesquisa Científica e Tecnológica I",
                            "Assistente Técnico de Pesquisa Científica e Tecnológica II",
                            "Assistente Técnico de Pesquisa Científica e Tecnológica III",
                            "Assistente Técnico de Pesquisa Científica e Tecnológica IV",
                            "Assistente Técnico de Pesquisa Científica e Tecnológica V",
                            "Assistente Técnico de Pesquisa Científica e Tecnológica VI",
                            "Atendente de Consultório Dentário",
                            "Atendente de Enfermagem",
                            "Atendente de Necrotério Policial de 1ª Classe",
                            "Atendente de Necrotério Policial de 2ª Classe",
                            "Atendente de Necrotério Policial de 3ª Classe",
                            "Atendente de Necrotério Policial de 4ª Classe",
                            "Atendente de Necrotério Policial de 5ª Classe",
                            "Atendente de Necrotério Policial de Classe Especial",
                            "Atendente de Nutrição",
                            "Atuario",
                            "Auxiliar Agropecuário",
                            "Auxiliar de Administração Pública",
                            "Auxiliar de Análises Clínicas",
                            "Auxiliar de Apoio a Pesquisa Científica e Tecnológica",
                            "Auxiliar de Apoio Agropecuário",
                            "Auxiliar de Desapropriação",
                            "Auxiliar de Desenvolvimento Infantil",
                            "Auxiliar de Enfermagem",
                            "Auxiliar de Enfermagem do Trabalho",
                            "Auxiliar de Engenheiro",
                            "Auxiliar de Laboratório",
                            "Auxiliar de Lavanderia e Rouparia Hospitalar",
                            "Auxiliar de Necropsia de 1ª Classe",
                            "Auxiliar de Necropsia de 2ª Classe",
                            "Auxiliar de Necropsia de 3ª Classe",
                            "Auxiliar de Necropsia de 4ª Classe",
                            "Auxiliar de Necropsia de 5ª Classe",
                            "Auxiliar de Necropsia de Classe Especial",
                            "Auxiliar de Papiloscopista Policial de 1ª Classe",
                            "Auxiliar de Papiloscopista Policial de 2ª Classe",
                            "Auxiliar de Papiloscopista Policial de 3ª Classe",
                            "Auxiliar de Papiloscopista Policial de 4ª Classe",
                            "Auxiliar de Papiloscopista Policial de 5ª Classe",
                            "Auxiliar de Papiloscopista Policial de Classe Especial",
                            "Auxiliar de Radiologia",
                            "Auxiliar de Recepções",
                            "Auxiliar de Saúde",
                            "Auxiliar de Serviços",
                            "Auxiliar de Serviços de Saúde",
                            "Auxiliar de Serviços Gerais",
                            "Auxiliar Técnico de Equipamento Rodoviário",
                            "Auxiliar Técnico de Saúde",
                            "Bibliotecário",
                            "Bibliotecário Encarregado",
                            "Bilheteiro",
                            "Biologista",
                            "Biologista Encarregado",
                            "Biologista Encarregado de Turno",
                            "Biólogo",
                            "Biomédico",
                            "Botânico",
                            "Capelão",
                            "Carcereiro de 1ª Classe",
                            "Carcereiro de 2ª Classe",
                            "Carcereiro de 3ª Classe",
                            "Carcereiro de 4ª Classe",
                            "Carcereiro de 5ª Classe",
                            "Carcereiro de Classe Especial",
                            "Cirurgião Dentista",
                            "Citotécnico",
                            "Contador",
                            "Coordenador Pedagogico",
                            "Cozinheiro Hospitalar",
                            "Criminologista",
                            "Delegado de Polícia de 1ª Classe",
                            "Delegado de Polícia de 2ª Classe",
                            "Delegado de Polícia de 3ª Clsse",
                            "Delegado de Polícia de 4ª Classe",
                            "Delegado de Polícia de 5ª Classe",
                            "Delegado de Polícia de Classe Especial",
                            "Desenhista",
                            "Desenhista Técnico Pericial de 1ª Classe",
                            "Desenhista Técnico Pericial de 2ª Classe",
                            "Desenhista Técnico Pericial de 3ª Classe",
                            "Desenhista Técnico Pericial de 4ª Classe",
                            "Desenhista Técnico Pericial de 5ª Classe",
                            "Desenhista Técnico Pericial de Classe Especial",
                            "Desinsetizador",
                            "Diretor de Escola",
                            "Economista",
                            "Economista Doméstico",
                            "Educador de Saúde Pública",
                            "Educador de Saúde Pública Encarregado",
                            "Educador Regional de Saúde Pública",
                            "Encarregado de Setor de Saúde",
                            "Encarregado de Setor Técnico de Saúde",
                            "Encarregado de Turno de Saúde",
                            "Enfermeiro",
                            "Enfermeiro do Trabalho",
                            "Enfermeiro Encarregado",
                            "Enfermeiro Encarregado de Turno",
                            "Enfermeiro Regional de Saúde Pública",
                            "Engenheiro (vide Lei Complementar 540/88)",
                            "Engenheiro Agrônomo",
                            "Engenheiro Agrônomo I",
                            "Engenheiro Agrônomo II",
                            "Engenheiro Agrônomo III",
                            "Engenheiro Agrônomo IV",
                            "Engenheiro Agrônomo V",
                            "Engenheiro Agrônomo VI",
                            "Engenheiro I",
                            "Engenheiro II",
                            "Engenheiro III",
                            "Engenheiro IV",
                            "Engenheiro VI",
                            "Escrivão de Polícia de 1ª Classe",
                            "Escrivão de Polícia de 2ª Classe",
                            "Escrivão de Polícia de 3ª Classe",
                            "Escrivão de Polícia de 4ª Classe",
                            "Escrivão de Polícia de 5ª Classe",
                            "Escrivão de Polícia de Classe Especial",
                            "Especialista Ambiental",
                            "Especialista Ambiental II",
                            "Especialista Ambiental III",
                            "Especialista Ambiental IV",
                            "Especialista Ambiental V",
                            "Especialista Ambiental VI",
                            "Especialista em Desenvolvimento Social",
                            "Especialista Em Recursos Humanos",
                            "Estatístico",
                            "Executivo Público",
                            "Executivo Público I",
                            "Executivo Público II",
                            "Farmacêutico",
                            "Farmacêutico Encarregado",
                            "Feitor",
                            "Fiscal de Junta Comercial",
                            "Fiscal de Obras",
                            "Fiscal de Taxas",
                            "Fiscal de Transportes Coletivos",
                            "Fiscal Sanitário",
                            "Físico",
                            "Físico Encarregado",
                            "Fisioterapeuta",
                            "Fisioterapeuta Encarregado",
                            "Fonoaudiólogo",
                            "Fonoaudiólogo Encarregado",
                            "Fotógrafo Técnico Pericial de 1ª Classe",
                            "Fotógrafo Técnico Pericial de 2ª Classe",
                            "Fotógrafo Técnico Pericial de 3ª Classe",
                            "Fotográfo Técnico Pericial de 4ª Classe",
                            "Fotógrafo Técnico Pericial de 5ª Classe",
                            "Fotógrafo Técnico Pericial de Classe Especial",
                            "Geofísico",
                            "Geógrafo",
                            "Guarda Rodoviário",
                            "Histoquímico",
                            "Historiógrafo",
                            "Inspetor",
                            "Inspetor de Ensino Artístico",
                            "Inspetor de Máquinas e Veículos",
                            "Inspetor de Taxas",
                            "Inspetor de Trabalho",
                            "Investigador de Polícia de 1ª Classe",
                            "Investigador de Polícia de 2ª Classe",
                            "Investigador de Polícia de 3ª Classe",
                            "Investigador de Polícia de 4ª Classe",
                            "Investigador de Polícia de 5ª Classe",
                            "Investigador de Polícia de Classe Especial",
                            "Julgador de taxas",
                            "Julgador Tributário",
                            "Lançador",
                            "Marinheiro",
                            "Matemático",
                            "Mecânico de Aparelhos de Precisão",
                            "Médico",
                            "Médico I",
                            "Médico II",
                            "Médico III",
                            "Médico Legista de 1ª Classe",
                            "Médico Legista de 2ª Classe",
                            "Médico Legista de 3ª Classe",
                            "Médico Legista de 4ª Classe",
                            "Médico Legista de 5ª Classe",
                            "Médico Legista de Classe Especial",
                            "Médico Sanitarista",
                            "Médico Veterinário",
                            "Médico Veterinário Encarregado",
                            "Mestre de Artesanato",
                            "Mestre de Obras",
                            "Mestre de Oficina",
                            "Mestre de Ofício",
                            "Meteorologista",
                            "Monitor de Museus",
                            "Motociclista",
                            "Motorista",
                            "Motorista (EFCJ)",
                            "Motorista de Ambulância",
                            "Motorista de Barco",
                            "Motorista de Lancha",
                            "Motorista Naval",
                            "Museologo",
                            "Nivelador",
                            "Nutricionista",
                            "Nutricionista Encarregado",
                            "Nutricionista Encarrregado de Turno",
                            "Oficial Administrativo",
                            "Oficial de Apoio a Pesquisa Científica e Tecnológica",
                            "Oficial de Apoio Agropecuário",
                            "Oficial de Atendimento de Saúde",
                            "Oficial de Saúde",
                            "Oficial de Serviços e Manutenção",
                            "Oficial de Serviços em Cine e Foto",
                            "Oficial de Serviços Gráficos",
                            "Oficial Operacional",
                            "Oficial Sociocultural",
                            "Operador de Equipamento Hospitalar",
                            "Operador de Máquinas",
                            "Operador de Máquinas Rodoviárias",
                            "Operador de Máquinas Rodoviárias Especiais",
                            "Operador de Praça de Pedágio",
                            "Operador de Praça de Pesagem",
                            "Operador de Telecomunicações",
                            "Operador de Terminal de Computador",
                            "Operador Destilaria",
                            "Orientador  Educacional",
                            "Orientador Artístico",
                            "Orientador Trabalhista",
                            "Papiloscopista Policial de 1ª Classe",
                            "Papiloscopista Policial de 2ª Classe",
                            "Papiloscopista Policial de 3ª Classe",
                            "Papiloscopista Policial de 4ª Classe",
                            "Papiloscopista Policial de 5ª Classe",
                            "Papiloscopista Policial de Classe Especial",
                            "Perito Criminal de 1ª Classe",
                            "Perito Criminal de 2ª Classe",
                            "Perito Criminal de 3ª Classe",
                            "Perito Criminal de 4ª Classe",
                            "Perito Criminal de 5ª Classe",
                            "Perito Criminal de Classe Especial",
                            "Pesquisador Científico I",
                            "Pesquisador Científico II",
                            "Pesquisador Científico III",
                            "Pesquisador Científico IV",
                            "Pesquisador Científico V",
                            "Pesquisador Científico VI",
                            "Procurador de Autarquia Nivel I",
                            "Procurador de Autarquia Nivel II",
                            "Procurador de Autarquia Nivel III",
                            "Procurador de Autarquia Nivel IVIII",
                            "Procurador de Autarquia Nivel V",
                            "Procurador de Autarquia Substituto",
                            "Procurador do Estado Nível I",
                            "Procurador do Estado Nivel II",
                            "Procurador do Estado Nivel III",
                            "Procurador do Estado Nivel IV",
                            "Procurador do Estado Nivel V",
                            "Procurador do Estado Substituto",
                            "Professor de Academia de Polícia I",
                            "Professor de Academia de Polícia II",
                            "Professor de Conservatório Musical",
                            "Professor Educação Básica I",
                            "Professor Educação Básica II",
                            "Professor II",
                            "Psicólogo",
                            "Psicólogo Encarregado",
                            "Químico",
                            "Químico Encarregado",
                            "Recepcionista",
                            "Recepcionista Bilingue",
                            "Recreacionista",
                            "Redator",
                            "Relações Públicas",
                            "Restaurador",
                            "Revisor",
                            "Salva Vidas",
                            "Serviçal de Laboratório",
                            "Sociólogo",
                            "Sondador",
                            "Supervisor de Área Hospitalar",
                            "Supervisor de Ensino",
                            "Supervisor de Saneamento",
                            "Técnico Agricola",
                            "Técnico Agropecuário",
                            "Técnico de Aparelhos de Precisão",
                            "Técnico de Aparelhos Eletrônicos Medico-hospitalares",
                            "Técnico de Apoio a Pesquisa Científica e Tecnológica",
                            "Técnico de Apoio Agropecuário",
                            "Técnico de Apoio Arrecadação Tributária"
                            "Técnico de Apoio de Recursos Humanos"
                            "Técnico de Contabilidade",
                            "Técnico de Eletrônica",
                            "Técnico de Enfermagem",
                            "Técnico de Enfermagem",
                            "Técnico de Higiene Dental",
                            "Técnico de Laboratório",
                            "Técnico de Ortóptica",
                            "Técnico de Radiologia",
                            "Técnico de Reabilitação Física",
                            "Técnico de Saúde Coletiva",
                            "Técnico de Segurança do Trabalho",
                            "Técnico Desportivo",
                            "Técnico em Agrimensura",
                            "Técnico Químico",
                            "Tecnologista",
                            "Técnologo",
                            "Tecnólogo em Radiologia",
                            "Telefonista",
                            "Terapeuta Ocupacional",
                            "Terapeuta Ocupacional Encarregado",
                            "Topógrafo",
                            "Trabalhador Braçal",
                            "Vigia",
                            "Vigilância em Saúde",
                            "Visitador Comunitário",
                            "Visitador Sanitário",
                            "Zootecnista",
                            "",
                        ]