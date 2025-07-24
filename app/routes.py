from flask import Blueprint, request, jsonify, current_app
import os
import base64
import io
from werkzeug.utils import secure_filename
try:
    from app.utils.image_processor import ImageProcessor
except ImportError:
    from app.utils.image_processor_simple import SimpleImageProcessor as ImageProcessor
from app.utils.ocr_engine import OCREngine
from app.utils.math_parser import MathParser

main_bp = Blueprint('main', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image_data(image_data, image_processor, ocr_engine, math_parser, debug=False):
    """
    Common function to process image data (file or base64)
    
    Args:
        image_data: Either file object or base64 string
        image_processor: ImageProcessor instance
        ocr_engine: OCREngine instance
        math_parser: MathParser instance
        debug (bool): If True, save debug images/text
        
    Returns:
        dict: Processing results
    """
    try:
        debug_save_path = os.path.join(current_app.config['UPLOAD_FOLDER']) if debug else None
        # Process image
        processed_image = image_processor.preprocess(image_data)
        
        # Extract text using OCR (with debug path)
        extracted_text = ocr_engine.extract_text(processed_image, debug_save_path=debug_save_path)
        
        # Parse mathematical expressions
        result = math_parser.parse_and_calculate(extracted_text)
        
        return {
            'success': True,
            'extracted_text': extracted_text,
            'lines': result['lines'],
            'total': result['total'],
            'processing_time': result.get('processing_time', 0)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@main_bp.route('/', methods=['GET'])
def root():
    """Root endpoint - API information"""
    return jsonify({
        'message': 'SmartBillCalc API',
        'description': 'OCR-powered bill calculation system',
        'version': '1.0.0',
        'endpoints': {
            'health': 'GET /health',
            'process_bill_image': 'POST /process_bill_image',
            'capture_and_process': 'POST /capture_and_process'
        },
        'status': 'running'
    })

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'SmartBillCalc backend is running'
    })

@main_bp.route('/process_bill_image', methods=['POST'])
def process_bill_image():
    """Process uploaded bill image and extract calculations"""
    try:
        # Check if request contains JSON data (base64 image)
        if request.is_json:
            data = request.get_json()
            if 'image_data' in data:
                # Handle base64 encoded image (from mobile camera)
                try:
                    # Remove data URL prefix if present
                    image_data = data['image_data']
                    if image_data.startswith('data:image'):
                        image_data = image_data.split(',')[1]
                    
                    # Decode base64 to bytes
                    image_bytes = base64.b64decode(image_data)
                    
                    # Create a temporary file-like object
                    image_stream = io.BytesIO(image_bytes)
                    
                    # Initialize processors
                    image_processor = ImageProcessor()
                    ocr_engine = OCREngine()
                    math_parser = MathParser()
                    
                    # Process the image
                    result = process_image_data(image_stream, image_processor, ocr_engine, math_parser)
                    
                    return jsonify(result)
                    
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'error': f'Error processing base64 image: {str(e)}'
                    }), 400
        
        # Check if file is present in request (file upload)
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided. Send either a file upload or base64 image_data in JSON'
            }), 400
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload PNG, JPG, JPEG, GIF, or BMP'
            }), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Initialize processors
            image_processor = ImageProcessor()
            ocr_engine = OCREngine()
            math_parser = MathParser()
            
            # Process the image
            result = process_image_data(filepath, image_processor, ocr_engine, math_parser)
            
            return jsonify(result)
            
        finally:
            # Clean up temporary file
            if os.path.exists(filepath):
                os.remove(filepath)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main_bp.route('/capture_and_process', methods=['POST'])
def capture_and_process():
    """
    Endpoint specifically for mobile camera capture
    Accepts base64 encoded image data
    """
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Request must be JSON with image_data field'
            }), 400
        
        data = request.get_json()
        
        if 'image_data' not in data:
            return jsonify({
                'success': False,
                'error': 'image_data field is required'
            }), 400
        
        # Remove data URL prefix if present
        image_data = data['image_data']
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        # Decode base64 to bytes
        image_bytes = base64.b64decode(image_data)
        
        # Create a temporary file-like object
        image_stream = io.BytesIO(image_bytes)
        
        # Initialize processors
        image_processor = ImageProcessor()
        ocr_engine = OCREngine()
        math_parser = MathParser()
        
        # Process the image
        result = process_image_data(image_stream, image_processor, ocr_engine, math_parser)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 