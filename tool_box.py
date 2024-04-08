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

locale = Locale('pt', 'BR')

def validar_nome_entry(new_value, nome_entry):
    # Verifica se a entrada está vazia
    if not new_value:
        return True
    
    # Capitaliza a primeira letra de cada palavra na string
    new_value = new_value.title()

    # Verifica se a entrada contém apenas letras e espaços
    if re.match(r'^[a-zA-Z\s]+$', new_value):
        return True
    else:
        if any(char.isdigit() for char in new_value):
            messagebox.showerror("Erro", "A entrada não pode conter números.")
        else:
            messagebox.showerror("Erro", "A entrada deve conter apenas letras e espaços.")
        nome_entry.delete(0, "end")
        return False

def on_validate(P, nome_entry):
    return validar_nome_entry(P, nome_entry)

def validate_content(event):
    content = nome_entry.get()
    validar_nome_entry(content, nome_entry)
    atualizar_declara()
    
def atualizar_declara():
    global declara
    declara["nome"] = nome_entry.get()
    declara["rg_entry"] = rg_entry.get()
    # Adicione outras variáveis conforme necessário

    # Exibir os valores armazenados no dicionário de variáveis
    return(declara)

    
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

def limpar_campos(nome_entry, rg_entry, cpf_entry, estado_civil_combo, ato_combo, jornada_combo, lei_combo, cargo_combo, 
                  destinacao_entry, ua_combo, coordenadoria_combo, cargo_origem_combo, a_partir_var, a_partir_checkbutton, periodo_fechado_var, 
                  periodo_fechado_checkbutton, regime_combo, bnt_n_servidor, bnt_servidor):
    # Limpa o valor de todos os campos de entrada
    nome_entry.delete(0, END)
    nome_entry.focus()
    rg_entry.delete(0, END)
    cpf_entry.delete(0, END)
    estado_civil_combo.set('')
    ato_combo.set('')
    jornada_combo.set('')
    jornada_combo.config(state="disable")
    ato_combo["values"] = "Nomeação","Designação","Designação com posterior Nomeação"
    #ato_combo.config(state="disable")
    lei_combo.set('')
    #lei_combo.config(state="disable")
    cargo_combo.set('')
    cargo_combo.config(state="disable")
    destinacao_entry.delete(0, END)
    destinacao_entry.config(state="disable")
    ua_combo.set('')
    ua_combo.config(state="disable")
    coordenadoria_combo.set('')
    coordenadoria_combo.config(state="disable")
    cargo_origem_combo.set('')
    cargo_origem_combo.config(state="disable")
    periodo_fechado_var.set(False)
    a_partir_var.set(False)
    a_partir_checkbutton.config(state="normal")
    periodo_fechado_checkbutton.config(state="normal")
    regime_combo.set('')
    bnt_n_servidor.config(state="disable")
    bnt_servidor.config(state="disable")

 
user_date_a_partir_variable = None

def toggle_check_a_partir(a_partir_var, periodo_fechado_var, periodo_fechado_checkbutton, ato_combo, window, bnt_servidor, bnt_n_servidor):
    global user_date_a_partir_variable
    if a_partir_var.get():
        periodo_fechado_var.set(False)
        periodo_fechado_checkbutton.config(state="disabled")
        # Exibir caixa de diálogo para solicitar uma data
        window.withdraw() 
        user_date = simpledialog.askstring("Data", "Qual a data do a partir? Ex:(dd/mm/aaaa)", initialvalue = datetime.now().strftime('%d/%m/%Y'))
        # Verificar se a data está no formato correto
        if user_date and len(user_date) == 10 and user_date[2] == '/' and user_date[5] == '/':
            # print("Data selecionada:", user_date)
            # Use a data fornecida pelo usuário como desejar
            user_date_a_partir_variable = user_date
            # Atualizar valores do Combobox
            ato_combo["values"] = "Designação", "Designação com posterior Nomeação" 
            ato_combo.config(state="normal")
        elif user_date == None or user_date_a_partir_variable == None:
            #print(user_date)
            #print(user_date_a_partir_variable)
            window.deiconify()
        else:
            tk.messagebox.showerror("Erro", "Formato de data inválido. Por favor, insira uma data no formato dd/mm/aaaa.")
            toggle_check_a_partir(a_partir_var, periodo_fechado_var, periodo_fechado_checkbutton, ato_combo)
    else:
        periodo_fechado_checkbutton.config(state="normal")
    window.deiconify()
    if bnt_servidor.cget("state") == "disable":
        bnt_n_servidor.focus()
    elif bnt_n_servidor.cget("state") == "disable":
        bnt_servidor.focus()
date_periodofechado_inicio_variable = None
date_periodofechado_fim_variable = None
    

def toggle_check_periodo_fechado(periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo, window, bnt_servidor, bnt_n_servidor):
    global date_periodofechado_inicio_variable
    global date_periodofechado_fim_variable
    if periodo_fechado_var.get():
        a_partir_var.set(False)
        a_partir_checkbutton.config(state="disabled")
        ato_combo["values"] = "Designação"        
        #Escondendo a janela principal(window)
        window.withdraw() 
        date_periodofechado_inicio = simpledialog.askstring("A Partir", "Qual a data do a partir \n para o período fechado? Ex:(dd/mm/aaaa)",
                                                            initialvalue = datetime.now().strftime('%d/%m/%Y'))
        print(date_periodofechado_inicio)
        if date_periodofechado_inicio and len(date_periodofechado_inicio) == 10 and date_periodofechado_inicio[2] == '/' and date_periodofechado_inicio[5] == '/':
            # Use a data fornecida pelo usuário como desejar
            date_periodofechado_inicio_variable = date_periodofechado_inicio
            # Atualizar valores do Combobox
        elif date_periodofechado_inicio == None:
            window.deiconify()
        else:
            tk.messagebox.showerror("Erro", "Formato de data inválido. Por favor, insira uma data no formato dd/mm/aaaa.")
            toggle_check_periodo_fechado(periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo)
        date_periodofechado_fim = simpledialog.askstring("Data fim...", "Qual a data fim para o período fechado? Ex:(dd/mm/aaaa)",                                                         
                                                         initialvalue = 'dd/mm/aaaa')
        print(date_periodofechado_fim)
        if date_periodofechado_fim and len(date_periodofechado_fim) == 10 and date_periodofechado_fim[2] == '/' and date_periodofechado_fim[5] == '/':
            date_periodofechado_fim_variable = date_periodofechado_fim            
        elif date_periodofechado_fim == None:
            window.deiconify()
        else:
            tk.messagebox.showerror("Erro", "Formato de data inválido. Por favor, insira uma data no formato dd/mm/aaaa.")
            toggle_check_periodo_fechado(periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo)
    else:
        a_partir_checkbutton.config(state="normal")
    #Volta a principal janela(window)
    window.deiconify()
    if bnt_servidor.cget("state") == "disable":
        bnt_n_servidor.focus()
    elif bnt_n_servidor.cget("state") == "disable":
        bnt_servidor.focus()
    
def ato_box_select(event, ato_combo, a_partir_var, periodo_fechado_var, a_partir_checkbutton, periodo_fechado_checkbutton, lei_combo):
    selected_value = ato_combo.get()
    if selected_value == "Nomeação":
        a_partir_var.set(False)
        periodo_fechado_var.set(False)
        a_partir_checkbutton.config(state=tk.DISABLED)
        periodo_fechado_checkbutton.config(state=tk.DISABLED)
        lei_combo.config(state="normal")
        
    elif selected_value == "Designação com posterior Nomeação":
        periodo_fechado_var.set(False)
        a_partir_checkbutton.config(state=tk.NORMAL)
        periodo_fechado_checkbutton.config(state=tk.DISABLED)
        lei_combo.config(state="normal")

    else:
        a_partir_checkbutton.config(state=tk.NORMAL)
        periodo_fechado_checkbutton.config(state=tk.NORMAL)
        lei_combo.config(state="normal")



def lei_box_select(lei_combo, jornada_combo):
    selected_value = lei_combo.get()
    if selected_value == "Art.5º da lei complementar nº 1080/2008":
        jornada_combo["values"] = ["Jornada Completa de Trabalho"]
        jornada_combo.set("Jornada Completa de Trabalho")
        jornada_combo.config(state=tk.NORMAL)
        
    elif selected_value == "Art.8º da lei complementar nº 1157/2011":
        jornada_combo.config(state=tk.NORMAL)
        jornada_combo.set("")
        jornada_combo["values"] = "Jornada Básica de Trabalho", "Jornada Parcial de Trabalho", "Jornada de 30(trinta) horas de Trabalho"
        jornada_combo.focus()
        
def jornada_box_select(cargo_combo, lei_combo):
    selected_value = lei_combo.get()
    if selected_value == "Art.5º da lei complementar nº 1080/2008":
        cargo_combo.set("")
        cargo_combo["values"] = [
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
                                "Supervisor Técnico I"           
                                ]
        cargo_combo.config(state=tk.NORMAL)
        cargo_combo.set("")

    elif selected_value == "Art.8º da lei complementar nº 1157/2011":
        cargo_combo.set("")
        cargo_combo["values"] = [
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
        cargo_combo.config(state=tk.NORMAL)
        cargo_combo.set("")

def cargo_box_select(coordenadoria_combo):
    coordenadoria_combo.config(state="normal")
    
def coordenadoria_box_select(ua_combo, coordenadoria_combo):
    selected_value = coordenadoria_combo.get()
    ua_combo.set('')
    if selected_value == 'Administração Superior da Secretaria e da Sede':
        ua_combo["values"] = [
                                "Gabinete do Coordenador",
                                "Gabinete do Secretário e Assessorias",
                                "Grupo de Assistência Farmacêutica",
                                "Coordenadoria de Gestão Orçamentária e Financeira  - CGOF",
                                "Coordenadoria de Planejamento de Saúde",
                                "Coordenadoria de Recursos Humanos",
                                "Coordenadoria Geral de Administração",
                                "Departamento de Gerenciamento Ambulatorial da Capital - DGAC"
                                
                              ]
    elif selected_value =="Coordenadoria de Serviços de Saúde":
        ua_combo["values"] = [
                                'Centro de Atenção Integrada em Saúde Mental "Philippe Pinel" - CAISM Philippe Pinel',
                                'Centro de Atenção Integral à Saúde "Clemente Ferreira" de Lins',
                                'Centro de Atenção Integral à Saúde "Professor Cantídio de Moura Campos"',
                                "Centro de Atenção Integral à Saúde de Santa Rita - C.A.I.S./SR",
                                "Centro de Desenvolvimento do Portador de Deficiência Mental, em Itu",
                                "Centro de Reabilitação de Casa Branca",
                                "Centro de Referência da Saúde da Mulher",
                                'Centro de Referência de Álcool, Tabaco e Outras Drogas',
                                'Centro Especializado em Reabilitação "Doutor Arnaldo Pezzuti Cavalcanti", em Mogi das Cruzes',
                                'Centro Pioneiro em Atenção Psicossocial "Arquiteto Januário José Ezemplari"- CPAP',
                                'Complexo Hospitalar "Padre Bento" de Guarulhos',
                                "Complexo Hospitalar do Juquery, em Franco da Rocha",
                                "Conjunto Hospitalar de Sorocaba",
                                "Conjunto Hospitalar do Mandaqui",
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
                                "Unidade de Gestão Assistencial V"
                            ]
    elif selected_value == "Coordenadoria de Assistência Farmacêutica":
        ua_combo["values"] = [
                            ""
                             ]
    elif selected_value == "Coordenadoria de Ciência, Tecnologia e Insumos Estratégicos de Saúde":
        ua_combo["values"] = [
                            "Instituto Butantan",
                            "Instituto de Saúde"
                            ]
    elif selected_value == "Coordenadoria de Controle de Doenças":
        ua_combo["values"] = [
                                'Centro de Referência e Treinamento - "DST/AIDS"',
                                'Centro de Vigilância Epidemiológica "Professor Alexandre Vranjac"',
                                "Centro de Vigilância Sanitária",
                                'Instituto "Adolfo Lutz" - IAL',
                                "Instituto Pasteur"
                            ]
    elif selected_value == "Coordenadoria de Defesa e Saúde Animal":
        ua_combo["values"] = [
                            "Coordenadoria de Defesa e Saúde Animal"            
                            ]
    
    elif selected_value == "Coordenadoria de Gestão de Contratos de Serviços de Saúde":
        ua_combo["values"] = [
                            ""
            
                            ]
    elif selected_value == "Coordenadoria de Gestão Orçamentaria e Financeira":
        ua_combo["values"] = [
                            ""
                            ]
    elif selected_value == "Coordenadoria de Planejamento de Saúde":
        ua_combo["values"] = [
                            ""
            
                            ]
    elif selected_value == "Coordenadoria de Regiões de Saúde":
        ua_combo["values"] = [
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
                                    "DRS XVIII - Botucatu"
                            ]
    elif selected_value == "Coordenadoria Geral de Administração":
        ua_combo["values"] = [
                            ""
                            ]
    ua_combo.config(state="normal")

    
def ua_box_select(destinacao_entry):
    destinacao_entry.config(state="normal")

        
def validar_tipo_de_servidor(ato_combo, cargo_origem_combo, bnt_n_servidor, bnt_servidor):
    if (ato_combo.get() == "Nomeação" and cargo__origem_combo.get() == ""):
        bnt_n_servidor.config(state="normal")
        bnt_servidor.config(state="disable")
    elif (ato_combo.get() != "Nomeação" or cargo_de_origem_entry.get() != ""):
        bnt_n_servidor.config(state="disable")
        bnt_servidor.config(state="normal")
    
    #print(ato_combo.get())
    #print(cargo_de_origem_entry.get())
    
def path_check(declara):
    if not (os.path.exists(f'{declara['Ato']}/{declara['Nome']}/')): 
        print(f"Não temos a pasta {declara['Ato']}/{declara['Nome']}")
        try:
            os.makedirs(f'./{declara['Ato']}/{declara['Nome']}/')  # Tenta criar a pasta
            messagebox.showinfo("Pasta criada!", f"Pasta '{declara['Nome']}' dentro de '{declara['Ato']}' criada com sucesso!")
        except OSError as e:
            messagebox.showerror("Falha ao criar a pasta!!!", f"Falha ao criar a pasta '{declara['Ato']}': {e}")
    else:
        messagebox.showinfo("Pasta já existe!", f"A pasta '{declara['Nome']}' dentro de '{declara['Ato']} já existe.")

def declaracao_experiencia(c , declara):
    #Define título
    c.setFont("Verdana-Bold", 14)
    c.drawCentredString(300, 750, "Declaração de Experiência")
    
    # Adiciona informações do dicionário do PDF em um parágrafo justificado
    #text = "    "
    #for key, value in declara.items():
    #    text += f"{key}: {value}\n"
    c.setFont("Verdana", 12)
    y_position = 700
    text =f"Tendo em vista, a indicação por esta Unidade de {declara['Nome']}, RG. {declara['RG']}, \
            para {declara['Ato']} e após análise curricular declaro que para fins do disposto do {declara['Lei']}, \
            que a indicado(a) atende ao disposto no anexo IV a que se refere Lei Complementar acima mencionada, \
            no tocante a experiência profissional exigida com relação aos assuntos relacionados as atividades a serem desempenhadas \
            no cargo de {declara['Cargo']} classificado no(a) {declara['Destinação']}, do(a) {declara['UA']}, da {declara['Coordenadoria']}."
    
    style = ParagraphStyle(name='Justify', alignment=4, firstLineIndent = 30, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700 - p.height)
    #print (declara['Nome'])
    #locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    
    #locale.setlocale(LC_TIME, 'pt_BR', 'pt_BR.utf-8', 'pt_BR.utf-8', 'portuguese')
    #date_default_timezone_set('America/Sao_Paulo')

    c.setFont("Verdana", 12)
    c.drawCentredString(300, 500, f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}")
    c.setFont("Verdana", 11)
    c.drawCentredString(300, 470, f"__________________________________________________")
    c.setFont("Verdana", 10)
    c.drawCentredString(300, 450, f"(Assinatura e Carimbo)")
    #c.drawCentredString(300, 500, f"{datetime.now().strftime('%A, %d de %B de %Y')}")
    #format_date(data_atual, format='full', locale=locale)
    ###   strtotime('today')
    # Fecha o arquivo PDF
def termo_de_anuencia(c , declara):
    #Define título
    c.setFont("Verdana-Bold", 14)
    c.drawCentredString(300, 750, "Termo de Anuência")
    # Adiciona informações do dicionário do PDF em um parágrafo justificado
    c.setFont("Verdana", 12)
    y_position = 700
    text = f"Eu, {declara['Nome']}, "
    # Para o caso de Servidor ou Não Servidor
    if (declara['Cargo de Origem'] != ''):
        text += f"{declara['Cargo de Origem']}, "
    text += f"{declara['Regime']}, RG. {declara['RG']}, concordo com a {declara['Ato']} \
                , em {declara['Jornada']}, para o cargo de {declara['Cargo']}"
    # Para o caso de "A partir" ou "Período Fechado" 
    if date_periodofechado_inicio_variable is not None and date_periodofechado_fim_variable is not None:
        text += f"no período de {date_periodofechado_inicio_variable} a {date_periodofechado_fim_variable} "
    elif  user_date_a_partir_variable is not None:
        text += f", a partir de {user_date_a_partir_variable}"
             
    text += f", do(a) {declara['Destinação']}, da {declara['UA']}, da {declara['Coordenadoria']}. "
    
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700 - p.height)
   
    
    c.setFont("Verdana", 12)
    
    c.drawRightString(500, 500, f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}.")
    c.setFont("Verdana", 11)
    c.drawRightString(500, 470, f"__________________________________________________")
    c.setFont("Verdana", 10)
    c.drawRightString(500, 450, f"{declara['Nome']}")
    
def declaracao_hipotese_inelegibilidade(c , declara):
    #Define título
    c.setFont("Verdana-Bold", 14)
    c.drawCentredString(300, 750, "DECLARAÇÃO")
    c.setFont("Verdana", 10)
    c.drawCentredString(300, 735, "(hipóteses de inelegibilidade)")
    
    
    c.setFont("Verdana", 12)
    y_position = 700
    text =f"Eu, {declara['Nome']}, brasileiro(a), {declara['Estado Civil']}, RG. {declara['RG']}, CPF. {declara['CPF']}, \
            declaro ter pleno conhecimento das disposições contidas no Decreto nº 57.970, de 12 de abril de 2012. \
            Declaro ainda, sob as penas da lei, não incorrer em nenhuma das hipóteses de inelegibilidade previstas em lei federal. \
            Assumo, por fim, o compromisso de comunicar a meu superior hierárquico, no prazo de 30 (trinta) dias subsequentes \
            à respectiva ciência, a superveniência de:"
    
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700 - p.height)
    
    text =f"a) enquadramento em qualquer hipótese de inelegibilidade prevista em lei federal;"
    
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 530)
    p.drawOn(c, 100, 568)
    
    text =f"b) instauração de processos administrativos ou judiciais cuja decisão possa importar \
            em inelegibilidade, nos termos de lei federal."
    
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 500)
    p.drawOn(c, 100, 530)
    
    
    
    
    c.drawRightString(500, 350, f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}.")
    #c.setFont("Verdana", 11)
    #c.drawRightString(500, 470, f"__________________________________________________")
    c.setFont("Verdana", 10)
    c.drawRightString(500, 300, f"{declara['Nome']}")
    
    
def declaracao_cargo_funcao(c , declara):
    c.setFont("Verdana-Bold", 14)
    c.drawCentredString(300, 750, "DECLARAÇÃO")
    
    c.setFont("Verdana", 12)
    y_position = 700
    text =f"Eu, {declara['Nome']}, {declara['Cargo de Origem']}, {declara['Regime']}, RG. {declara['RG']}, \
            DECLARO para fins de {declara['Ato']} no cargo de {declara['Cargo']}, do(a) {declara['Destinação']}, do(a) \
            {declara['UA']}, da {declara['Coordenadoria']}, que não exerço cargo ou função de direção, \
            gerência ou administração em entidades que mantenham contratos ou convênios com o Sistema Único \
            de Saúde - SUS/SP ou sejam por este credenciadas."
    
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700 - p.height)
    
    c.drawRightString(500, 500, f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}.")
    #c.setFont("Verdana", 11)
    #c.drawRightString(500, 470, f"__________________________________________________")
    c.setFont("Verdana", 12)
    c.drawRightString(500, 450, f"{declara['Nome']}")
    
def declaracao_acumulo(c , declara):
    c.setFont("Verdana-Bold", 14)
    c.drawCentredString(300, 750, "DECLARAÇÃO DE ACÚMULO")
    
    #c.setFont("Verdana-Bold", 12)
    y_position = 700
    text_bold =f"DECLARO, "
    
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), fontName="Verdana-Bold")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700 - p.height)
    
    c.setFont("Verdana", 12)
    y_position = 700
    text_bold =f"sob pena de responsabilidade, para fins de acumulação que no âmbito do Serviço Público Federal, Estadual ou Municipal\
            , ou ainda em Autarquias, Fundações, Empresas Públicas, Sociedade de Economia Mista, suas subsidiárias e Sociedades Controladas\
            , direta ou indiretamente pelo Poder Público.:"
    
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), firstLineIndent = 65)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700 - p.height)
    
    c.setFont("Verdana", 12)
    text=f"EU, {declara['Nome']}, RG Nº {declara['RG']},"
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5), fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 600)
        
    text=f"não exerço"
    style = ParagraphStyle(name='Justify', alignment=4)
    draw_checkbox(c, 100, 580 , checked=False)
    draw_checkbox(c, 180, 580 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 580)
    p.drawOn(c, 120, 580)

    text=f" exerço"
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 580)
    p.drawOn(c, 198, 580)

    
    text=f"SE EXERCE "
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 540)
    p.drawOn(c, 100, 540)
        
    text=f"outro cargo"
    style = ParagraphStyle(name='Justify', alignment=4)
    draw_checkbox(c, 100, 520 , checked=False)
    draw_checkbox(c, 210, 520 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 520)
    p.drawOn(c, 120, 520)

    text=f"emprego"
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 520)
    p.drawOn(c, 228, 520)

    text=f"função pública"
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 520)
    p.drawOn(c, 336, 520)
    draw_checkbox(c, 318, 520 , checked=False)
    
    text=f"Onde:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 480)
    p.drawOn(c, 100, 480)
    
    
    text=f"Cargo/E/FP:"
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 450)
    p.drawOn(c, 100, 450)
    #draw_checkbox(c, 100, 600 , checked=False)
    #draw_checkbox(c, 140, 600 , checked=False)
    
    text=f"APOSENTADO "
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 400)
    p.drawOn(c, 100, 400)
        
    text=f"Sim"
    style = ParagraphStyle(name='Justify', alignment=4)
    draw_checkbox(c, 135, 380 , checked=False)
    draw_checkbox(c, 238, 380 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 380)
    p.drawOn(c, 100, 380)

    text=f"Não"
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 380)
    p.drawOn(c, 210, 380)
    
    text=f"SE SIM: "
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 320)
    p.drawOn(c, 100, 320)
        
    
    text=f"Orgão Público"
    style = ParagraphStyle(name='Justify', alignment=4)
    draw_checkbox(c, 170, 300 , checked=False)
    #draw_checkbox(c, 238, 300 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 300)
    p.drawOn(c, 100, 300)
    
    text=f"Qual: "
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 320, 300)
    p.drawOn(c, 210, 300)
    
    text=f"Cargo: "
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 320, 275)
    p.drawOn(c, 210, 275)

    text=f"D.O.E da Aposentadoria: "
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 320, 242)
    p.drawOn(c, 210, 242)
    
    text=f"Empresa Privada "
    style = ParagraphStyle(name='Justify', alignment=4)
    draw_checkbox(c, 190, 212 , checked=False)
    #draw_checkbox(c, 238, 300 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 212)
    p.drawOn(c, 100, 212)

    text=f"Onde: "
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text, style)
    p.wrapOn(c, 320, 212)
    p.drawOn(c, 250, 212)
    
    text=f"Outro"
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text, style)
    p.wrapOn(c, 320, 198)
    p.drawOn(c, 250, 198)
    draw_checkbox(c, 280, 198 , checked=False)


    c.setFont("Verdana", 12)
    c.drawCentredString(300, 150, f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}.")
    #c.setFont("Verdana", 11)
    #c.drawRightString(500, 470, f"__________________________________________________")
    
    c.drawCentredString(300, 100, f"{declara['Nome']}")

def anexo_i(c , declara):
       
    #c.setFont("Verdana-Bold", 11)
    y_position = 780
    text =f"ANEXO I"
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 730)
    p.drawOn(c, 100, 780 - p.height)

    #c.setFont("Verdana-Bold", 11)
    y_position = 600
    text_bold =f"a que se referem os artigos 1º e 2º do Decreto nº 54.376,\
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
    p.drawOn(c, 100, 650 - p.height)

    c.setFont("Verdana", 11)
    y_position = 650
    text_bold =f"( SÚMULA VINCULANTE Nº 13 DO STF )"
    
    style = ParagraphStyle(name='Justify', alignment=4)
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 532)
    p.drawOn(c, 100, 632 - p.height)
    #c.line(90, y + size, x + size, y)
    
    text =f"Nome: {declara['Nome']}"
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 618)
    p.drawOn(c, 100, 600 - p.height)
    #c.rect(90, 500, 400, 50)
    c.rect(90, 550, 450, 50)
    #c.rect(95, 600, 400, 50)
    
    
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
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana-Bold")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 425)
    p.drawOn(c, 100, 475)
    
    text=f"NÃO"
    style = ParagraphStyle(name='Justify', alignment=4, IdentFirstLine = 10)
    draw_checkbox(c, 100, 440 , checked=False)
    #draw_checkbox(c, 238, 300 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 200, 440)
    p.drawOn(c, 120, 400)
    
    text=f"SIM"
    style = ParagraphStyle(name='Justify', alignment=4, IdentFirstLine = 10)
    draw_checkbox(c, 100, 400 , checked=False)
    #draw_checkbox(c, 238, 300 , checked=False)
    p = Paragraph(text, style)
    p.wrapOn(c, 200, 400)
    p.drawOn(c, 120, 440)
    
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
    c.drawRightString(500, 360, f"_________________________________________________________________")
    
    y_position = 240
    text_bold =f"Relação de Parentesco:"
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 358)
    p.drawOn(c, 100, 340)
    c.drawRightString(500, 340, f"__________________________________________________")

    y_position = 240
    text_bold =f"Cargo:"
    
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text_bold, style)
    p.wrapOn(c, 400, 348)
    p.drawOn(c, 100, 320)
    c.drawRightString(500, 320, f"_________________________________________________________________")

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

    c.setFont("Verdana", 12)
    
    # c.drawLeftString(400, 150, f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}.")
    # c.setFont("Verdana", 11)
    # c.drawRightString(400, 120, f"__________________________________________________")
    # c.setFont("Verdana", 11)
    # c.drawRightString(400, 100, f"{declara['Nome']}")
    
    c.setFont("Verdana", 11)
    text=f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}."
    style = ParagraphStyle(name='Justify', alignment=4, fontName="Verdana")
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 110)
    p.drawOn(c, 100, 120)

def declaracao(declara):
    # Cria PDF 
    pdfmetrics.registerFont(TTFont('Verdana', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('Verdana-Bold', 'VeraBd.ttf'))
    #pdfmetrics.registerFont(TTFont('ZapfDingbats', './ZapfDingbats.ttf'))
    nomearquivo = f"{declara['Nome']} - {declara['Cargo']}.pdf"
    
    path_check(declara)
            
    c = canvas.Canvas(f"./{declara['Ato']}/{declara['Nome']}/{nomearquivo}", pagesize=A4) 
    declaracao_experiencia(c , declara)
    c.showPage()
    termo_de_anuencia(c , declara)
    c.showPage()
    declaracao_hipotese_inelegibilidade(c, declara)
    c.showPage()
    declaracao_cargo_funcao(c , declara)
    c.showPage()
    declaracao_acumulo(c , declara)
    c.showPage()
    anexo_i(c , declara)
    c.showPage()
    
    c.save()
    #print(f"./{declara['Ato']}/{declara['Nome']}/{declara['Nome']}/{nomearquivo}")
    subprocess.Popen([f"./{declara['Ato']}/{declara['Nome']}/{nomearquivo}"], shell=True)
    #subprocess.Popen(["start", f"./{declara['Ato']}/{nomearquivo}"], shell=True)
    #print(f"{declara['Nome']} + Teste + {declara['Cargo']}")
    # def verifica_pasta()
    #     pass
def draw_checkbox(c, x, y, size=10, checked=False):
# Desenha o quadrado
    c.rect(x, y, size, size)
    if checked:
        # Desenha a marca de seleção
        c.line(x, y, x + size, y + size)
        c.line(x, y + size, x + size, y)

def cargo_de_origem(destinacao_entry, ua_combo, cargo_origem_combo ):
    cargo_origem_combo.config(state="enable")
    ua = ua_combo.get() 
    if ua != '':
        cargo_origem_combo["values"] = [
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
            "Arquiteto (vide Lc 540/88)",
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
            "Engenheiro (vide LC 540/88)",
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
        ]
    #cargo_origem_combo.focus()