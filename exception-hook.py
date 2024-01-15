from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import sys
import traceback
import sqlite3 as sql
from datetime import datetime
import csv

#deixe a definição desta função antes de todos os elementos do código principal
def exception(type, value, tb):
    filename, line_number, _, _ = traceback.extract_tb(tb)[-1]
    time = datetime.now().strftime('%d/%m/%Y - %H:%M')
    timename = datetime.now().strftime('%d-%m-%Y (%Hh%Mmin)')
    exc = str(f"tipo de erro: {type.__name__},\n erro: {value},\n arquivo: {sys.argv[0]},\n linha: {line_number}\n\n {time}\n fim do relatório")

    class MyFlowable(Paragraph):
        def __init__(self, text, style):
            super().__init__(text, style)
    
    def save_reg(filename,value):
        cn = sql.connect('regerror.db')
        cs = cn.cursor()
        data = f"{time},{type.__name__}, {value}, {line_number},{sys.argv[0]} "
        cs.execute('CREATE TABLE IF NOT EXISTS regerror(datahora TEXT, tipodeerro TEXT, erro TEXT, linha TEXT, arquivo TEXT)')
        cs.execute(f"INSERT INTO regerror (datahora, tipodeerro, erro, linha, arquivo) VALUES ('{time}','{type.__name__}', '{value}', '{line_number}','{sys.argv[0]}')")
        cn.commit()
        cs.execute('SELECT * FROM regerror')
        res = cs.fetchall()
        cn.close()
        create_report(f'Relatório {timename}.pdf',res)
    
    def create_report(filename, res):
        styles = getSampleStyleSheet()
        with open(f'Relatório {timename}.csv', 'w') as file:
            writer = csv.writer(file, delimiter='\t',lineterminator='\n', escapechar=',')
            for register in res:
                for element in register:
                    elements = element.split('\n')
                    writer.writerow(elements)

    def create_pdf(filename, text):
        styles = getSampleStyleSheet()
        excF = str(text.replace("\n\n", "<br/>-----------------------<br/>"))
        SimpleDocTemplate(filename, pagesize=letter).build([MyFlowable(excF.replace("\n", "<br/>"), styles["Code"])])

    create_pdf(f"Erro {datetime.now().strftime('%d.%m.%Y (%Hh%Mmin)')}.pdf", exc)
    save_reg(filename,value)

#segue a definição da customização da função excepthook da lib sys
sys.excepthook = exception

#abaixo segue restante do script. no caso um erro inesperado ocorrer, um pdf será emitido
def io(i):
    i/0
io(1)