import cv2
import numpy as np
from PIL import Image
import os
import io

class ImageProcessor:
    """Handles image preprocessing for better OCR results"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    
    def preprocess(self, image_input, resize=True, max_width=1920, max_height=1080, use_adaptive_threshold=False):
        """
        Preprocess image for better OCR accuracy
        Args:
            image_input: Can be a file path (str) or BytesIO object
            resize (bool): Whether to resize image
            max_width (int): Max width for resizing
            max_height (int): Max height for resizing
            use_adaptive_threshold (bool): Use adaptive thresholding instead of Otsu
        Returns:
            numpy.ndarray: Preprocessed image
        """
        try:
            # Handle different input types
            if isinstance(image_input, str):
                image = cv2.imread(image_input)
                if image is None:
                    raise ValueError(f"Could not read image from {image_input}")
            elif isinstance(image_input, io.BytesIO):
                image_bytes = image_input.getvalue()
                nparr = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if image is None:
                    raise ValueError("Could not decode image from bytes")
            else:
                raise ValueError("Unsupported image input type")

            # Resize if needed
            if resize:
                image = self.resize_image(image, max_width, max_height)

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply noise reduction
            denoised = cv2.medianBlur(gray, 3)

            # Enhance contrast using CLAHE
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)

            # Thresholding
            if use_adaptive_threshold:
                binary = cv2.adaptiveThreshold(
                    enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
                )
            else:
                _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Morphological cleaning
            kernel = np.ones((1,1), np.uint8)
            cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

            return cleaned

        except Exception as e:
            raise Exception(f"Error preprocessing image: {str(e)}")
    
    def resize_image(self, image, max_width=1920, max_height=1080):
        """
        Resize image while maintaining aspect ratio
        
        Args:
            image (numpy.ndarray): Input image
            max_width (int): Maximum width
            max_height (int): Maximum height
            
        Returns:
            numpy.ndarray: Resized image
        """
        height, width = image.shape[:2]
        
        # Calculate scaling factor
        scale = min(max_width/width, max_height/height)
        
        if scale < 1:
            new_width = int(width * scale)
            new_height = int(height * scale)
            resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            return resized
        
        return image
    
    def enhance_for_handwriting(self, image):
        """
        Apply additional preprocessing for handwritten text
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Enhanced image
        """
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(image, (3, 3), 0)
        
        # Apply adaptive threshold
        adaptive_thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        return adaptive_thresh 