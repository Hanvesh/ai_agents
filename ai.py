from flask import Flask, request, send_file, jsonify
from pdf2docx import Converter
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

app = Flask(__name__)

def convert_pdf_to_docx(pdf_path, docx_path):
    # Create a PDF to DOCX converter object
    converter = Converter(pdf_path)
    # Convert PDF to DOCX
    converter.convert(docx_path, start=0, end=None)
    # Close the converter
    converter.close()

def remove_table_formatting(docx_path):
    doc = Document(docx_path)
    
    for table in doc.tables:
        # Remove table borders
        tbl = table._element
        
        tblBorders = tbl.xpath('.//w:tblBorders')
        for border in tblBorders:
            parent = border.getparent()
            if parent is not None:
                parent.remove(border)
        
        # Remove shading
        tblShd = tbl.xpath('.//w:shd')
        for shading in tblShd:
            parent = shading.getparent()
            if parent is not None:
                parent.remove(shading)
        
        # Remove table width
        tblW = tbl.xpath('.//w:tblW')
        if tblW:
            parent = tblW[0].getparent()
            if parent is not None:
                parent.remove(tblW[0])
        
        # Remove table alignment
        tblAlign = tbl.xpath('.//w:tblAlign')
        if tblAlign:
            parent = tblAlign[0].getparent()
            if parent is not None:
                parent.remove(tblAlign[0])
    
    doc.save(docx_path)

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.lower().endswith('.pdf'):
        pdf_path = 'uploaded.pdf'
        docx_path = 'output.docx'
        
        file.save(pdf_path)
        
        # Convert the PDF to DOCX
        convert_pdf_to_docx(pdf_path, docx_path)
        
        # Remove table formatting
        remove_table_formatting(docx_path)
        
        os.remove(pdf_path)  # Clean up the uploaded PDF file
        
        return send_file(docx_path, as_attachment=True, download_name='output.docx')
    
    return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
