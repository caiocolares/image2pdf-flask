from flask import Flask, request, send_file
from PIL import Image
from pdf2image import convert_from_bytes
import io
import zipfile


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.post("/img2pdf")
def image_to_pdf():
    # Verifica se há um arquivo na requisição
    if 'image' not in request.files:
        return {"error": "No image file provided"}, 400
    
    file = request.files['image']
    
    # Verifica se o arquivo tem um nome
    if file.filename == '':
        return {"error": "No file selected"}, 400
    
    try:
        # Abre a imagem
        image = Image.open(file.stream)
        
        # Converte para RGB se necessário (PDF não suporta RGBA)
        if image.mode in ('RGBA', 'LA', 'P'):
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            rgb_image.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = rgb_image
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Cria um buffer para o PDF
        pdf_buffer = io.BytesIO()
        
        # Salva a imagem como PDF no buffer
        image.save(pdf_buffer, format='PDF', resolution=100.0)
        pdf_buffer.seek(0)
        
        # Retorna o PDF
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='converted.pdf'
        )
    
    except Exception as e:
        return {"error": f"Failed to convert image: {str(e)}"}, 500

@app.post("/pdf2img")
def pdf_to_image():
    # Verifica se há um arquivo na requisição
    if 'pdf' not in request.files:
        return {"error": "No PDF file provided"}, 400
    
    file = request.files['pdf']
    
    # Verifica se o arquivo tem um nome
    if file.filename == '':
        return {"error": "No file selected"}, 400
    
    try:
        # Lê o conteúdo do PDF
        pdf_bytes = file.read()
        
        # Converte o PDF em imagens (uma por página)
        images = convert_from_bytes(pdf_bytes, dpi=200)
        
        # Se for apenas uma página, retorna uma imagem
        if len(images) == 1:
            img_buffer = io.BytesIO()
            images[0].save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            return send_file(
                img_buffer,
                mimetype='image/png',
                as_attachment=True,
                download_name='page_1.png'
            )
        
        # Se houver múltiplas páginas, cria um ZIP com todas as imagens
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, image in enumerate(images, start=1):
                img_buffer = io.BytesIO()
                image.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                
                zip_file.writestr(f'page_{i}.png', img_buffer.getvalue())
        
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='converted_pages.zip'
        )
    
    except Exception as e:
        return {"error": f"Failed to convert PDF: {str(e)}"}, 500

if __name__ == "__main__":
    app.run(debug=True)

