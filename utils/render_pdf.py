import os
import base64
import numpy as np
from docx2pdf import convert
from datetime import datetime
from docxtpl import DocxTemplate

TEMPLATE = "template.docx"

def render(context, output_path):
	doc = DocxTemplate(TEMPLATE)
	doc.render(context)
	doc.save("generated_doc.docx")
	convert("generated_doc.docx", output_path)
	os.remove("generated_doc.docx")

def get_context(df):

    date = datetime.today().strftime("%d, %b, %Y")

    total = (np.array(df['Cantidad'], int) * \
             np.array(df['Valor Unitario'].str.replace('.', ''), int)).sum()
    sub_total = np.ceil(total / 1.19).astype(np.uint64)
    iva = total - sub_total # np.ceil(total * (0.19 / 1.19)).astype(np.uint64)

    context = {'date': date, 'iva': iva, 'total': total, 'sub_total': sub_total}

    for i in range(11):

        try:
            context[f'n_{i+1}'] = df.loc[i]['Cantidad']
            context[f'np_{i+1}'] = df.loc[i]['Nº de Parte']
            context[f'desc_{i+1}'] = df.loc[i]['Descripcion']
            context[f'prc_{i+1}'] = df.loc[i]['Valor Unitario']
        except:
            context[f'n_{i+1}'] = context[f'np_{i+1}'] \
                = context[f'desc_{i+1}'] = context[f'prc_{i+1}'] = ""

    return context

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'''<iframe src="data:application/pdf;base64,{base64_pdf}"
                        width="800" height="800" type="application/pdf">
                      </iframe>'''
    return pdf_display
