# Authentication & User Management Endpoints

---

# (From API_BACKEND_DOCUMENTATION.md)

# SmartBillCalc Backend API Documentation

## Base URL
```
http://localhost:5000
```

---

## 1. Register User
- **Endpoint:** `POST /api/auth/register`
- **Body:**
```json
{
  "name": "User Name",
  "email": "user@example.com",
  "password": "password"
}
```
- **Response:**
```json
{
  "message": "User registered successfully. Please check your email for the verification code."
}
```

---

## 2. Verify Email
- **Endpoint:** `POST /api/auth/verify`
- **Body:**
```json
{
  "email": "user@example.com",
  "code": "CODE_FROM_EMAIL"
}
```
- **Response (Success):**
```json
{
  "message": "Email verified successfully"
}
```
- **Response (Error):**
```json
{
  "error": "Invalid verification code"
}
```

---

## 3. Login
- **Endpoint:** `POST /api/auth/login`
- **Body:**
```json
{
  "email": "user@example.com",
  "password": "password"
}
```
- **Response (Success):**
```json
{
  "access_token": "..."
}
```
- **Response (Error):**
```json
{
  "error": "Invalid credentials"
}
```

---

## 4. Forgot Password
- **Endpoint:** `POST /api/auth/forgot-password`
- **Body:**
```json
{
  "email": "user@example.com"
}
```
- **Response:**
```json
{
  "message": "Password reset code sent to your email."
}
```

---

## 5. Reset Password
- **Endpoint:** `POST /api/auth/reset-password`
- **Body:**
```json
{
  "email": "user@example.com",
  "code": "RESET_CODE",
  "new_password": "newpassword"
}
```
- **Response:**
```json
{
  "message": "Password reset successful. You can now log in with your new password."
}
```

---

## 6. Protected Route Example
- **Endpoint:** `GET /api/auth/protected`
- **Headers:**
  - `Authorization: Bearer <access_token>`
- **Response:**
```json
{
  "message": "Hello user@example.com, you are authorized!"
}
```

---

## 7. Test Users (For Debugging Only)
- **Endpoint:** `GET /api/auth/test-users`
- **Response:**
```json
[
  {
    "id": 1,
    "name": "User Name",
    "email": "user@example.com",
    "is_verified": true
  }
]
```

---

## General Notes
- **Content-Type:** All POST requests must have `Content-Type: application/json` header.
- **JWT Token:** After login, use the `access_token` in the `Authorization` header for protected endpoints.
- **Error Handling:** Always check for `error` field in the response for error messages.
- **Base URL:** Change `localhost` to your server IP/domain if deploying.

---

# Bill Processing & Main API Endpoints

---

# (From previous API_DOCUMENTATION.md)

# SmartBillCalc Backend API Documentation

## Overview
The SmartBillCalc backend provides OCR-powered bill calculation services. It can process both uploaded image files and base64-encoded images from mobile camera captures.

## Base URL
```
http://localhost:5000 (Development)
https://your-domain.com (Production)
```

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the backend is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "SmartBillCalc backend is running"
}
```

### 2. Process Bill Image (Multi-format)
**POST** `/process_bill_image`

Process bill images from either file upload or base64 data.

#### Option A: File Upload
**Content-Type:** `multipart/form-data`

**Parameters:**
- `image` (file): Image file (PNG, JPG, JPEG, GIF, BMP)

**Example (cURL):**
```bash
curl -X POST http://localhost:5000/process_bill_image \
  -F "image=@bill_photo.jpg"
```

#### Option B: Base64 Image Data
**Content-Type:** `application/json`

**Request Body:**
```json
{
  "image_data": "base64_encoded_image_string"
}
```

**Example (cURL):**
```bash
curl -X POST http://localhost:5000/process_bill_image \
  -H "Content-Type: application/json" \
  -d '{"image_data": "iVBORw0KGgoAAAANSUhEUgAA..."}'
```

### 3. Capture and Process (Mobile Camera)
**POST** `/capture_and_process`

Dedicated endpoint for mobile camera captures.

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "image_data": "base64_encoded_image_string"
}
```

**Example (cURL):**
```bash
curl -X POST http://localhost:5000/capture_and_process \
  -H "Content-Type: application/json" \
  -d '{"image_data": "iVBORw0KGgoAAAANSUhEUgAA..."}'
```

## Response Format

### Success Response
```json
{
  "success": true,
  "extracted_text": "Milk 2 x 50 = 100\nBread 1 x 30 = 30\nTotal = 130",
  "lines": [
    {
      "text": "Milk 2 x 50 = 100",
      "numbers": [2, 50],
      "result": 100,
      "calculated": 100,
      "confidence": 0.9
    },
    {
      "text": "Bread 1 x 30 = 30",
      "numbers": [1, 30],
      "calculated": 30,
      "confidence": 0.9
    }
  ],
  "total": 130,
  "processing_time": 0.245
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message description"
}
```

## Mobile App Integration Examples

### React Native Example

```javascript
import { Camera } from 'expo-camera';

const processBillImage = async (imageUri) => {
  try {
    // Convert image to base64
    const base64Image = await convertImageToBase64(imageUri);
    
    // Send to backend
    const response = await fetch('http://localhost:5000/capture_and_process', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image_data: base64Image
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      console.log('Total:', result.total);
      console.log('Extracted text:', result.extracted_text);
      return result;
    } else {
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Error processing image:', error);
    throw error;
  }
};

const convertImageToBase64 = async (uri) => {
  const response = await fetch(uri);
  const blob = await response.blob();
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const base64 = reader.result.split(',')[1];
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
};
```

### Flutter Example

```dart
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>> processBillImage(String imagePath) async {
  try {
    // Read image file and convert to base64
    File imageFile = File(imagePath);
    List<int> imageBytes = await imageFile.readAsBytes();
    String base64Image = base64Encode(imageBytes);
    
    // Send to backend
    final response = await http.post(
      Uri.parse('http://localhost:5000/capture_and_process'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'image_data': base64Image,
      }),
    );
    
    if (response.statusCode == 200) {
      Map<String, dynamic> result = json.decode(response.body);
      if (result['success']) {
        print('Total: ${result['total']}');
        print('Extracted text: ${result['extracted_text']}');
        return result;
      } else {
        throw Exception(result['error']);
      }
    } else {
      throw Exception('Failed to process image');
    }
  } catch (e) {
    print('Error processing image: $e');
    rethrow;
  }
}
```

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (missing image, invalid format) |
| 500 | Internal Server Error |

## Supported Image Formats
- PNG
- JPG/JPEG
- GIF
- BMP

## Image Processing Features
- **OCR Text Extraction**: Uses Tesseract OCR for text recognition
- **Mathematical Expression Parsing**: Automatically detects and calculates totals
- **Image Preprocessing**: Noise reduction, contrast enhancement, thresholding
- **Handwriting Support**: Optimized for handwritten bills
- **Multi-line Processing**: Handles complex bill formats

## Best Practices for Mobile Apps

### Image Quality
- Ensure good lighting when capturing bills
- Keep the camera steady to avoid blur
- Capture the entire bill in frame
- Use high resolution when possible

### Error Handling
- Always check the `success` field in responses
- Implement retry logic for network failures
- Show user-friendly error messages
- Handle cases where OCR fails to extract text

### Performance
- Compress images before sending (recommended max 2MB)
- Show loading indicators during processing
- Cache results for offline viewing
- Implement timeout handling

## Testing

Use the provided `test_api.py` script to test all endpoints:

```bash
python test_api.py
```

This will test:
- Health check endpoint
- File upload functionality
- Base64 image processing
- Capture endpoint

## Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Tesseract OCR:
   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

3. Run the backend:
```bash
python app.py
```

4. Test the setup:
```bash
python test_setup.py
```

## Production Deployment

For production deployment, consider:
- Using HTTPS
- Implementing rate limiting
- Adding authentication
- Using a production WSGI server like Gunicorn
- Setting up proper logging
- Implementing monitoring and health checks 