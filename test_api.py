#!/usr/bin/env python3
"""
Test script for SmartBillCalc Backend API
Tests both file upload and base64 image processing endpoints
"""

import requests
import base64
import json
import os
from PIL import Image
import io

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def create_test_image():
    """Create a simple test image with text"""
    # Create a white image with black text
    img = Image.new('RGB', (400, 200), color='white')
    
    # Add some text (this would be replaced with actual bill text in real usage)
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    # Add sample bill text
    text_lines = [
        "Milk 2 x 50 = 100",
        "Bread 1 x 30 = 30", 
        "Eggs 1 x 120 = 120",
        "Total = 250"
    ]
    
    y_position = 20
    for line in text_lines:
        draw.text((20, y_position), line, fill='black', font=font)
        y_position += 30
    
    return img

def test_file_upload():
    """Test file upload endpoint"""
    print("\n📁 Testing file upload endpoint...")
    
    # Create test image
    test_img = create_test_image()
    
    # Save to temporary file
    temp_file = "test_bill.png"
    test_img.save(temp_file)
    
    try:
        # Upload file
        with open(temp_file, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{BASE_URL}/process_bill_image", files=files)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ File upload test passed")
                print(f"   Extracted text: {result.get('extracted_text', 'N/A')}")
                print(f"   Total: {result.get('total', 'N/A')}")
                print(f"   Processing time: {result.get('processing_time', 'N/A')}s")
            else:
                print(f"❌ File upload processing failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ File upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ File upload error: {e}")
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)

def test_base64_upload():
    """Test base64 image upload endpoint"""
    print("\n📱 Testing base64 image upload endpoint...")
    
    # Create test image
    test_img = create_test_image()
    
    # Convert to base64
    buffer = io.BytesIO()
    test_img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    try:
        # Send base64 data
        data = {'image_data': img_str}
        response = requests.post(
            f"{BASE_URL}/process_bill_image", 
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Base64 upload test passed")
                print(f"   Extracted text: {result.get('extracted_text', 'N/A')}")
                print(f"   Total: {result.get('total', 'N/A')}")
                print(f"   Processing time: {result.get('processing_time', 'N/A')}s")
            else:
                print(f"❌ Base64 upload processing failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ Base64 upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Base64 upload error: {e}")

def test_capture_endpoint():
    """Test the dedicated capture endpoint"""
    print("\n📸 Testing capture endpoint...")
    
    # Create test image
    test_img = create_test_image()
    
    # Convert to base64
    buffer = io.BytesIO()
    test_img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    try:
        # Send to capture endpoint
        data = {'image_data': img_str}
        response = requests.post(
            f"{BASE_URL}/capture_and_process", 
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Capture endpoint test passed")
                print(f"   Extracted text: {result.get('extracted_text', 'N/A')}")
                print(f"   Total: {result.get('total', 'N/A')}")
                print(f"   Processing time: {result.get('processing_time', 'N/A')}s")
            else:
                print(f"❌ Capture endpoint processing failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ Capture endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Capture endpoint error: {e}")

def main():
    """Run all tests"""
    print("🧪 SmartBillCalc Backend API Tests")
    print("=" * 40)
    
    # Test health check first
    test_health_check()
    
    # Test file upload
    test_file_upload()
    
    # Test base64 upload
    test_base64_upload()
    
    # Test capture endpoint
    test_capture_endpoint()
    
    print("\n" + "=" * 40)
    print("✅ All tests completed!")

if __name__ == "__main__":
    main() 