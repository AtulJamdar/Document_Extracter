"""
Test preprocessing effectiveness
Compares OCR quality with and without preprocessing

Run: python test_preprocessing.py
"""

import pytesseract
from PIL import Image
from app.services.preprocessing.image_preprocessor import ImagePreprocessor
from app.core.logger import logger


def test_preprocessing(image_path: str):
    """
    Compare OCR results with and without preprocessing
    
    Args:
        image_path: Path to test image
    """
    print("=" * 60)
    print(f"Testing: {image_path}")
    print("=" * 60)
    print()
    
    # Test 1: OCR without preprocessing
    print("TEST 1: OCR WITHOUT Preprocessing")
    print("-" * 60)
    try:
        raw_image = Image.open(image_path)
        raw_text = pytesseract.image_to_string(raw_image)
        print(f"Extracted Text:\n{raw_text}")
        print(f"Text Length: {len(raw_text)} characters")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print()
    print()
    
    # Test 2: OCR with preprocessing
    print("TEST 2: OCR WITH Preprocessing")
    print("-" * 60)
    try:
        preprocessor = ImagePreprocessor()
        preprocessed_image_array = preprocessor.preprocess(image_path)
        preprocessed_image = Image.fromarray(preprocessed_image_array)
        preprocessed_text = pytesseract.image_to_string(preprocessed_image)
        print(f"Extracted Text:\n{preprocessed_text}")
        print(f"Text Length: {len(preprocessed_text)} characters")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print()
    print()
    
    # Test 3: Comparison
    print("COMPARISON")
    print("-" * 60)
    try:
        improvement = len(preprocessed_text) - len(raw_text)
        if improvement > 0:
            print(f"✅ Preprocessing improved text extraction by {improvement} characters")
        elif improvement < 0:
            print(f"⚠️  Preprocessing reduced text by {abs(improvement)} characters")
        else:
            print(f"ℹ️  Same text length")
        
        print()
        print("Preprocessing Pipeline Steps:")
        print("  1. Grayscale conversion")
        print("  2. 2x Image upscaling (improves small text)")
        print("  3. Denoising (removes artifacts)")
        print("  4. Rotation correction (handles tilted documents)")
        print("  5. Adaptive thresholding (handles uneven lighting)")
        print("  6. Morphological cleanup (removes noise)")
        
    except Exception as e:
        print(f"Error in comparison: {str(e)}")
    
    print()
    print("=" * 60)
    print()


if __name__ == "__main__":
    print("\n")
    print("=" * 60)
    print("IMAGE PREPROCESSING EFFECTIVENESS TEST")
    print("=" * 60)
    print()
    
    # Test with sample image paths
    # You can modify these to test with your actual documents
    test_images = [
        # "app/uploads/test_blurry.jpg",
        # "app/uploads/test_dark.jpg",
        # "app/uploads/test_tilted.jpg",
    ]
    
    if not test_images:
        print("ℹ️  No test images configured.")
        print()
        print("To use this test:")
        print("1. Place test images in app/uploads/")
        print("2. Update test_images list with image paths")
        print("3. Run: python test_preprocessing.py")
        print()
        print("Test image suggestions:")
        print("  - Blurry document photo")
        print("  - Dark/low-light image")
        print("  - Tilted/rotated document")
        print("  - Noisy scanned document")
        print()
    else:
        for image_path in test_images:
            try:
                test_preprocessing(image_path)
            except Exception as e:
                print(f"Error testing {image_path}: {str(e)}")
                print()
