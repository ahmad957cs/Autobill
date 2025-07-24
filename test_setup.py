#!/usr/bin/env python3
"""
Test script to verify SmartBillCalc backend setup
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'flask',
        'flask_cors',
        'pytesseract',
        'PIL',
        'numpy',
        'dotenv'
    ]
    
    # Optional packages
    optional_packages = [
        'cv2'
    ]
    
    print("Testing required package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    print("\nTesting optional package imports...")
    for package in optional_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} (optional)")
        except ImportError as e:
            print(f"⚠️  {package}: {e} (optional - will use PIL fallback)")
    
    return len(failed_imports) == 0

def test_tesseract():
    """Test if Tesseract OCR is properly installed"""
    try:
        import pytesseract
        # Try to get Tesseract version
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract OCR version: {version}")
        return True
    except Exception as e:
        print(f"❌ Tesseract OCR not found: {e}")
        print("Please install Tesseract OCR:")
        print("Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("macOS: brew install tesseract")
        print("Linux: sudo apt-get install tesseract-ocr")
        return False

def test_flask_app():
    """Test if Flask app can be created"""
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 SmartBillCalc Backend Setup Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    print()
    
    # Test Tesseract
    tesseract_ok = test_tesseract()
    print()
    
    # Test Flask app
    flask_ok = test_flask_app()
    print()
    
    # Summary
    print("=" * 40)
    if imports_ok and tesseract_ok and flask_ok:
        print("🎉 All tests passed! Backend is ready to run.")
        print("\nTo start the server, run:")
        print("python app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main() 