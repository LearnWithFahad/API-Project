import PyPDF2
import io
import os

class PDFService:
    """Service for handling PDF operations"""
    
    def __init__(self):
        pass
    
    def extract_text(self, file_path):
        """Extract text content from PDF file"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            text_content = ""
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract text from all pages
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text() + "\n"
            
            return text_content.strip()
            
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def extract_text_from_upload(self, file_obj):
        """Extract text content from uploaded file object"""
        try:
            text_content = ""
            
            # Read file content into bytes
            file_content = file_obj.read()
            file_obj.seek(0)  # Reset file pointer
            
            # Create PDF reader from bytes
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            
            # Extract text from all pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"
            
            return text_content.strip()
            
        except Exception as e:
            print(f"Error extracting text from uploaded PDF: {str(e)}")
            return ""
    
    def get_pdf_info(self, file_path):
        """Get PDF metadata information"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                info = {
                    'num_pages': len(pdf_reader.pages),
                    'title': '',
                    'author': '',
                    'subject': '',
                    'creator': '',
                    'producer': '',
                    'creation_date': None,
                    'modification_date': None
                }
                
                # Get metadata if available
                if pdf_reader.metadata:
                    metadata = pdf_reader.metadata
                    info.update({
                        'title': metadata.get('/Title', ''),
                        'author': metadata.get('/Author', ''),
                        'subject': metadata.get('/Subject', ''),
                        'creator': metadata.get('/Creator', ''),
                        'producer': metadata.get('/Producer', ''),
                        'creation_date': metadata.get('/CreationDate'),
                        'modification_date': metadata.get('/ModDate')
                    })
                
                return info
                
        except Exception as e:
            print(f"Error getting PDF info: {str(e)}")
            return {
                'num_pages': 0,
                'title': '',
                'author': '',
                'subject': '',
                'creator': '',
                'producer': '',
                'creation_date': None,
                'modification_date': None
            }
    
    def validate_pdf(self, file_path):
        """Validate if file is a proper PDF"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                # Try to access first page to validate
                if len(pdf_reader.pages) > 0:
                    pdf_reader.pages[0]
                return True
                
        except Exception as e:
            print(f"PDF validation failed: {str(e)}")
            return False
