import tkinter as tk
from datetime import datetime, date
from tkinter import Tk, Label, Entry, Checkbutton, W, Button, messagebox, END ,simpledialog
from PIL import Image, ImageDraw
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
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
                  destinacao_entry, ua_combo, coordenadoria_combo, cargo_de_origem_entry, a_partir_var, a_partir_checkbutton, periodo_fechado_var, 
                  periodo_fechado_checkbutton, regime_combo):
    # Limpa o valor de todos os campos de entrada
    nome_entry.delete(0, END)
    nome_entry.focus()
    rg_entry.delete(0, END)
    cpf_entry.delete(0, END)
    estado_civil_combo.set('')
    ato_combo.set('')
    jornada_combo.set('')
    jornada_combo.config(state="disable")
    #ato_combo["values"] = "Nomeação","Designação","Designação com posterior Nomeação"
    #ato_combo.config(state="disable")
    lei_combo.set('')
    #lei_combo.config(state="disable")
    cargo_combo.set('')
    cargo_combo.config(state="disable")
    destinacao_entry.delete(0, END)
    ua_combo.set('')
    coordenadoria_combo.set('')
    cargo_de_origem_entry.delete(0, END)
    periodo_fechado_var.set(False)
    a_partir_var.set(False)
    a_partir_checkbutton.config(state="normal")
    periodo_fechado_checkbutton.config(state="normal")
    regime_combo.set('')
 
user_date_a_partir_variable = None

def toggle_check_a_partir(a_partir_var, periodo_fechado_var, periodo_fechado_checkbutton, ato_combo, window):
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
date_periodofechado_inicio_variable = None
date_periodofechado_fim_variable = None
    

def toggle_check_periodo_fechado(periodo_fechado_var, a_partir_var, a_partir_checkbutton, ato_combo, window):
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
                                "Assessor Técnico I"	                ,
                                "Assessor Técnico II"   	            ,
                                "Assessor Técnico III"	                ,
                                "Assessor Técnico IV"   	            ,
                                "Assessor Técnico V"    	            ,
                                "Chefe de Gabinete"     	            ,
                                "Chefe I"   	                        ,
                                "Chefe II"      	                    ,
                                "Diretor I"	                            ,
                                "Diretor II"    	                    ,
                                "Diretor III"                           ,
                                "Diretor Técnico I"	                    ,
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


        
def validar_tipo_de_servidor(ato_combo, cargo_de_origem_entry, bnt_n_servidor, bnt_servidor):
    if (ato_combo.get() == "Nomeação" and cargo_de_origem_entry.get() == ""):
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
    text =f"Tendo em vista, a indicação por esta Unidade de {declara['Nome']}, RG. {declara['RG']}, para {declara['Ato']} e após análise curricular declaro que para fins do disposto do {declara['Lei']}, que a indicado(a) atende ao disposto no anexo IV a que se refere Lei Complementar acima mencionada, no tocante a experiência profissional exigida com relação aos assuntos relacionados as atividades a serem desempenhadas no cargo de {declara['Cargo']} classificado no(a) {declara['Destinação']}, do(a) {declara['UA']}, da {declara['Coordenadoria']}."
    
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
    #text = "    "
    #for key, value in declara.items():
    #    text += f"{key}: {value}\n"
    c.setFont("Verdana", 12)
    y_position = 700
    text =f"Termo......"
    
    style = ParagraphStyle(name='Justify', alignment=4, leading=(12*1.5))
    p = Paragraph(text, style)
    p.wrapOn(c, 400, 600)
    p.drawOn(c, 100, 700 - p.height)
   
    c.setFont("Verdana", 12)
    c.drawCentredString(300, 500, f"São Paulo, {format_date(datetime.now(), format='full', locale=locale).split(',')[1].strip()}")
    c.setFont("Verdana", 11)
    c.drawCentredString(300, 470, f"__________________________________________________")
    c.setFont("Verdana", 10)
    c.drawCentredString(300, 450, f"(Assinatura e Carimbo)")

    
def declaracao(declara):
    # Cria PDF
    pdfmetrics.registerFont(TTFont('Verdana', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('Verdana-Bold', 'VeraBd.ttf'))
    nomearquivo = f"{declara['Nome']} - {declara['Cargo']}.pdf"
    
    path_check(declara)
            
    c = canvas.Canvas(f"./{declara['Ato']}/{declara['Nome']}/{nomearquivo}", pagesize=A4) 
    declaracao_experiencia(c , declara)
    c.showPage()
    termo_de_anuencia(c , declara)
    c.showPage()
    
    c.save()
    #print(f"./{declara['Ato']}/{declara['Nome']}/{declara['Nome']}/{nomearquivo}")
    subprocess.Popen([f"./{declara['Ato']}/{declara['Nome']}/{nomearquivo}"], shell=True)
    #subprocess.Popen(["start", f"./{declara['Ato']}/{nomearquivo}"], shell=True)
    #print(f"{declara['Nome']} + Teste + {declara['Cargo']}")
    # def verifica_pasta()
    #     pass
