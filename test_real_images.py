#!/usr/bin/env python3
"""
Test script for SmartBillCalc Backend with real bill images
"""

import requests
import base64
import os
import json
from PIL import Image
import io

# API base URL
BASE_URL = "http://localhost:5000"

def test_real_image(image_path):
    """Test a real bill image"""
    print(f"\n📸 Testing real image: {image_path}")
    print("=" * 50)
    
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            return
        
        # Convert image to base64
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Send to capture endpoint
        response = requests.post(
            f"{BASE_URL}/capture_and_process",
            json={'image_data': image_data},
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Image processed successfully!")
                print(f"📝 Extracted text:")
                print("-" * 30)
                print(result.get('extracted_text', 'No text extracted'))
                print("-" * 30)
                
                print(f"💰 Calculated total: {result.get('total', 'N/A')}")
                print(f"⏱️ Processing time: {result.get('processing_time', 'N/A')}s")
                
                # Show line-by-line breakdown
                lines = result.get('lines', [])
                if lines:
                    print(f"\n📋 Line-by-line breakdown:")
                    for i, line in enumerate(lines, 1):
                        print(f"  {i}. {line.get('text', 'N/A')} → {line.get('calculated', 'N/A')}")
                
                return result
            else:
                print(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing image: {e}")

def test_multiple_images(image_folder="uploads"):
    """Test multiple images from a folder"""
    print(f"\n📁 Testing images from folder: {image_folder}")
    print("=" * 50)
    
    if not os.path.exists(image_folder):
        print(f"❌ Folder not found: {image_folder}")
        print("📝 Create a folder called 'uploads' and put your bill images there")
        return
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    image_files = []
    
    for file in os.listdir(image_folder):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(os.path.join(image_folder, file))
    
    if not image_files:
        print(f"❌ No image files found in {image_folder}")
        print("📝 Supported formats: JPG, JPEG, PNG, BMP, GIF")
        return
    
    print(f"📸 Found {len(image_files)} image(s) to test")
    
    results = []
    for image_file in image_files:
        result = test_real_image(image_file)
        if result:
            results.append({
                'file': image_file,
                'result': result
            })
    
    # Summary
    if results:
        print(f"\n📊 Summary:")
        print(f"✅ Successfully processed: {len(results)}/{len(image_files)} images")
        total_sum = sum(r['result'].get('total', 0) for r in results)
        print(f"💰 Total sum across all bills: {total_sum}")
    else:
        print(f"\n❌ No images were processed successfully")

def interactive_test():
    """Interactive test - user provides image path"""
    print("\n🎯 Interactive Image Test")
    print("=" * 30)
    
    while True:
        image_path = input("\n📁 Enter image path (or 'quit' to exit): ").strip()
        
        if image_path.lower() in ['quit', 'exit', 'q']:
            break
        
        if not image_path:
            continue
        
        test_real_image(image_path)
        
        # Ask if user wants to continue
        continue_test = input("\n🔄 Test another image? (y/n): ").strip().lower()
        if continue_test not in ['y', 'yes']:
            break

def main():
    """Main function"""
    print("🧪 SmartBillCalc Real Image Testing")
    print("=" * 40)
    
    # Test health first
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend is not responding")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure to run: python app.py")
        return
    
    # Automatically test images from uploads folder
    print("\n🚀 Starting automatic test of images in 'uploads' folder...")
    test_multiple_images("uploads")

if __name__ == "__main__":
    main() 