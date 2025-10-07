import pytest
import io
from PIL import Image
from main import app


@pytest.fixture
def client():
    """Cria um cliente de teste para a aplicação Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def create_test_image(mode='RGB', size=(100, 100), color=(255, 0, 0)):
    """Cria uma imagem de teste"""
    image = Image.new(mode, size, color)
    img_buffer = io.BytesIO()
    image.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer


def create_test_pdf():
    """Cria um PDF de teste a partir de uma imagem"""
    image = Image.new('RGB', (100, 100), (0, 0, 255))
    pdf_buffer = io.BytesIO()
    image.save(pdf_buffer, format='PDF')
    pdf_buffer.seek(0)
    return pdf_buffer


class TestHelloEndpoint:
    def test_hello_world(self, client):
        """Testa o endpoint raiz"""
        response = client.get('/')
        assert response.status_code == 200
        assert response.data == b"Hello World!"


class TestImage2PDFEndpoint:
    def test_img2pdf_success(self, client):
        """Testa conversão bem-sucedida de imagem para PDF"""
        img_buffer = create_test_image()
        
        data = {
            'image': (img_buffer, 'test.png')
        }
        
        response = client.post('/img2pdf', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        assert response.mimetype == 'application/pdf'
        assert response.headers['Content-Disposition'].startswith('attachment')
    
    def test_img2pdf_no_file(self, client):
        """Testa erro quando nenhum arquivo é enviado"""
        response = client.post('/img2pdf', data={}, content_type='multipart/form-data')
        
        assert response.status_code == 400
        assert b"No image file provided" in response.data
    
    def test_img2pdf_empty_filename(self, client):
        """Testa erro quando o arquivo não tem nome"""
        data = {
            'image': (io.BytesIO(), '')
        }
        
        response = client.post('/img2pdf', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 400
        assert b"No file selected" in response.data
    
    def test_img2pdf_rgba_image(self, client):
        """Testa conversão de imagem RGBA"""
        img_buffer = create_test_image(mode='RGBA', color=(255, 0, 0, 128))
        
        data = {
            'image': (img_buffer, 'test.png')
        }
        
        response = client.post('/img2pdf', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        assert response.mimetype == 'application/pdf'
    
    def test_img2pdf_palette_image(self, client):
        """Testa conversão de imagem com paleta de cores"""
        image = Image.new('P', (100, 100))
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        data = {
            'image': (img_buffer, 'test.png')
        }
        
        response = client.post('/img2pdf', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        assert response.mimetype == 'application/pdf'
    
    def test_img2pdf_invalid_file(self, client):
        """Testa erro com arquivo inválido"""
        invalid_buffer = io.BytesIO(b"not an image")
        
        data = {
            'image': (invalid_buffer, 'test.txt')
        }
        
        response = client.post('/img2pdf', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 500
        assert b"Failed to convert image" in response.data


class TestPDF2ImageEndpoint:
    def test_pdf2img_success_single_page(self, client):
        """Testa conversão bem-sucedida de PDF com uma página"""
        pdf_buffer = create_test_pdf()
        
        data = {
            'pdf': (pdf_buffer, 'test.pdf')
        }
        
        response = client.post('/pdf2img', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        assert response.mimetype == 'image/png'
        assert 'page_1.png' in response.headers['Content-Disposition']
    
    def test_pdf2img_no_file(self, client):
        """Testa erro quando nenhum arquivo é enviado"""
        response = client.post('/pdf2img', data={}, content_type='multipart/form-data')
        
        assert response.status_code == 400
        assert b"No PDF file provided" in response.data
    
    def test_pdf2img_empty_filename(self, client):
        """Testa erro quando o arquivo não tem nome"""
        data = {
            'pdf': (io.BytesIO(), '')
        }
        
        response = client.post('/pdf2img', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 400
        assert b"No file selected" in response.data
    
    def test_pdf2img_invalid_file(self, client):
        """Testa erro com arquivo inválido"""
        invalid_buffer = io.BytesIO(b"not a pdf")
        
        data = {
            'pdf': (invalid_buffer, 'test.pdf')
        }
        
        response = client.post('/pdf2img', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 500
        assert b"Failed to convert PDF" in response.data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

