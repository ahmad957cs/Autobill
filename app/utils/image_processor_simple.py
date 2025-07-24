from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import os

class SimpleImageProcessor:
    """Simplified image processor using PIL instead of OpenCV"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    
    def preprocess(self, image_path):
        """
        Preprocess image for better OCR accuracy using PIL
        
        Args:
            image_path (str): Path to the input image
            
        Returns:
            PIL.Image: Preprocessed image
        """
        try:
            # Open image with PIL
            image = Image.open(image_path)
            
            # Convert to grayscale
            gray = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(gray)
            enhanced = enhancer.enhance(2.0)
            
            # Apply slight blur to reduce noise
            denoised = enhanced.filter(ImageFilter.MedianFilter(size=3))
            
            # Convert to binary (black and white)
            threshold = 128
            binary = denoised.point(lambda x: 0 if x < threshold else 255, '1')
            
            return binary
            
        except Exception as e:
            raise Exception(f"Error preprocessing image: {str(e)}")
    
    def resize_image(self, image, max_width=1920, max_height=1080):
        """
        Resize image while maintaining aspect ratio
        
        Args:
            image (PIL.Image): Input image
            max_width (int): Maximum width
            max_height (int): Maximum height
            
        Returns:
            PIL.Image: Resized image
        """
        width, height = image.size
        
        # Calculate scaling factor
        scale = min(max_width/width, max_height/height)
        
        if scale < 1:
            new_width = int(width * scale)
            new_height = int(height * scale)
            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            return resized
        
        return image
    
    def enhance_for_handwriting(self, image):
        """
        Apply additional preprocessing for handwritten text
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            PIL.Image: Enhanced image
        """
        # Apply Gaussian blur to reduce noise
        blurred = image.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(blurred)
        enhanced = enhancer.enhance(1.5)
        
        # Apply threshold
        threshold = 128
        binary = enhanced.point(lambda x: 0 if x < threshold else 255, '1')
        
        return binary 