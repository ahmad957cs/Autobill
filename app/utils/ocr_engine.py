import pytesseract
import re
import os
from PIL import Image
import numpy as np

class OCREngine:
    """Handles OCR text extraction from images"""
    
    def __init__(self):
        # Configure Tesseract path for Windows
        import platform
        if platform.system() == 'Windows':
            # Try common Windows Tesseract paths
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                os.getenv('TESSERACT_CMD_PATH', '')
            ]
            
            tesseract_found = False
            for path in possible_paths:
                if path and os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    print(f"✅ Tesseract found at: {path}")
                    tesseract_found = True
                    break
            
            if not tesseract_found:
                print("⚠️ Warning: Tesseract not found in common paths")
                print("Please install Tesseract or set TESSERACT_CMD_PATH environment variable")
        else:
            # For Linux/Mac, use environment variable or default
            tesseract_path = os.getenv('TESSERACT_CMD_PATH')
            if tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
                print(f"✅ Tesseract configured from environment: {tesseract_path}")
        
        # Configure OCR settings for better mathematical text recognition
        self.config = '--oem 3 --psm 6'  # Whitelist removed for full text extraction
    
    def extract_text(self, image, debug_save_path=None):
        """
        Extract text from preprocessed image
        Args:
            image (numpy.ndarray or PIL.Image): Preprocessed image
            debug_save_path (str, optional): If provided, save debug images/text here
        Returns:
            str: Extracted text
        """
        try:
            from PIL import Image as PILImage
            import numpy as np
            import datetime
            # Convert numpy array to PIL Image if needed
            if hasattr(image, 'shape'):  # numpy array
                pil_image = PILImage.fromarray(image)
            else:  # already PIL Image
                pil_image = image

            # Save preprocessed image for debugging
            if debug_save_path:
                ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                img_path = os.path.join(debug_save_path, f'preprocessed_{ts}.png')
                pil_image.save(img_path)

            # Extract text using Tesseract
            text = pytesseract.image_to_string(
                pil_image, 
                config=self.config,
                lang='eng'
            )

            # Save raw OCR text for debugging
            if debug_save_path:
                txt_path = os.path.join(debug_save_path, f'raw_ocr_{ts}.txt')
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(text)

            # Clean up the extracted text
            cleaned_text = self._clean_text(text)

            return cleaned_text

        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")
    
    def _clean_text(self, text):
        """
        Clean and format extracted text
        
        Args:
            text (str): Raw OCR text
            
        Returns:
            str: Cleaned text
        """
        # Remove extra whitespace and normalize
        lines = text.strip().split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove extra spaces
            line = re.sub(r'\s+', ' ', line.strip())
            
            # Only keep lines that might contain mathematical expressions
            if self._contains_math_expression(line):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _contains_math_expression(self, text):
        """
        Check if text contains mathematical expressions
        
        Args:
            text (str): Text to check
            
        Returns:
            bool: True if contains math expression
        """
        # Look for numbers, operators, and equals signs
        math_pattern = r'[\d+\-*/=xX]'
        return bool(re.search(math_pattern, text))
    
    def extract_lines_with_math(self, image):
        """
        Extract only lines containing mathematical expressions
        
        Args:
            image (numpy.ndarray or PIL.Image): Preprocessed image
            
        Returns:
            list: List of lines containing math expressions
        """
        try:
            # Convert numpy array to PIL Image if needed
            if hasattr(image, 'shape'):  # numpy array
                pil_image = Image.fromarray(image)
            else:  # already PIL Image
                pil_image = image
            
            # Use Tesseract to get data with bounding boxes
            data = pytesseract.image_to_data(
                pil_image, 
                config=self.config,
                output_type=pytesseract.Output.DICT
            )
            
            lines = []
            current_line = ""
            current_top = -1
            
            for i, text in enumerate(data['text']):
                if text.strip():
                    # Check if this is a new line
                    if current_top == -1 or abs(data['top'][i] - current_top) > 10:
                        if current_line and self._contains_math_expression(current_line):
                            lines.append(current_line.strip())
                        current_line = text
                        current_top = data['top'][i]
                    else:
                        current_line += " " + text
            
            # Add the last line if it contains math
            if current_line and self._contains_math_expression(current_line):
                lines.append(current_line.strip())
            
            return lines
            
        except Exception as e:
            raise Exception(f"Error extracting lines: {str(e)}") 

    def extract_raw_text(self, image):
        """
        Extract raw text from image (no cleaning, as-is from OCR)
        Args:
            image (numpy.ndarray or PIL.Image): Preprocessed or original image
        Returns:
            str: Raw extracted text
        """
        from PIL import Image
        import numpy as np
        # Convert numpy array to PIL Image if needed
        if hasattr(image, 'shape'):
            pil_image = Image.fromarray(image)
        else:
            pil_image = image
        # Convert to grayscale
        pil_image = pil_image.convert('L')
        text = pytesseract.image_to_string(pil_image, config=self.config, lang='eng')
        return text 