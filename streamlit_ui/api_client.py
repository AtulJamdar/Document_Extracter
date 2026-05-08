"""
Centralized API client for document extraction backend.

All API communication goes through this module.
Business logic stays in backend.
"""

import requests
from typing import Dict, Any


API_URL = "http://127.0.0.1:8000/extract-text"


class APIClient:
    """Handle all communication with extraction backend"""

    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url

    def upload_document(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Upload document and extract information

        Args:
            file_bytes: File content as bytes
            filename: Original filename

        Returns:
            Response dict with extracted data or error

        Response format:
        {
            "document_id": 123,
            "document_type": "aadhaar",
            "confidence": 0.95,
            "raw_text": "...",
            "extracted_data": {...}
        }

        Or on error:
        {
            "error": {
                "message": "...",
                "code": "..."
            }
        }
        """
        try:
            files = {
                "file": (filename, file_bytes)
            }

            response = requests.post(
                self.base_url,
                files=files,
                timeout=30
            )

            # Handle errors gracefully
            if response.status_code != 200:
                return {
                    "error": {
                        "message": response.json().get(
                            "detail",
                            "Unknown backend error"
                        ),
                        "code": response.status_code
                    }
                }

            return response.json()

        except requests.exceptions.Timeout:
            return {
                "error": {
                    "message": "Request timeout. Backend is not responding.",
                    "code": "TIMEOUT"
                }
            }

        except requests.exceptions.ConnectionError:
            return {
                "error": {
                    "message": "Cannot connect to backend. Is the server running?",
                    "code": "CONNECTION_ERROR"
                }
            }

        except Exception as e:
            return {
                "error": {
                    "message": f"Client error: {str(e)}",
                    "code": "CLIENT_ERROR"
                }
            }


# Global client instance
api_client = APIClient()
