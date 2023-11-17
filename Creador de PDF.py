#!/usr/bin/env python
# coding: utf-8

# In[6]:


import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Función para verificar si alguna columna tiene 'nan' o 'False'
def row_has_invalid_data(row):
    return any(pd.isna(value) or value == 'False' for value in row)

# Función para crear un PDF
def create_pdf(data):
    output = BytesIO()
    c = canvas.Canvas(output, pagesize=letter)
    width, height = letter
    styles = getSampleStyleSheet()

    for index, row in data.iterrows():
        data_list = [
            [Paragraph(f"<b>{key}</b>", styles['Normal']),
             Paragraph(f"{value}", styles['Normal'])]
             for key, value in row.items()
        ]

        if data_list:
            table = Table(data_list, colWidths=[200, 300])
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ])
            table.setStyle(style)
            y_position = height / 2
            table.wrapOn(c, width, height)
            table.drawOn(c, 30, y_position - table._height / 2)

        c.showPage()

    c.save()
    output.seek(0)
    return output

# Streamlit interface
st.title('Generador de Informes PDF')

uploaded_file = st.file_uploader("Sube tu archivo CSV aquí", type=['csv'])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    # Eliminar filas con 'nan' o 'False'
    data = data[~data.apply(row_has_invalid_data, axis=1)]

    if st.button('Generar PDF'):
        pdf_output = create_pdf(data)
        st.download_button(label="Descargar PDF",
                           data=pdf_output,
                           file_name="informes.pdf",
                           mime="application/pdf")


# In[ ]:




