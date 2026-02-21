"""AI Vision service – isolates all AI API interactions.

Uses Google's Gemini 2.0 Flash model to generate descriptive tags for images.
The rest of the application should never import an AI SDK directly.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import google.genai

logger = logging.getLogger(__name__)


def generate_image_tags(image_path: str) -> list[str]:
    """Send an image to Google Gemini and return 5 descriptive tags.

    Uses the gemini-2.0-flash model with JSON mode to ensure a clean,
    structured response. If the API fails or times out, returns an empty list
    and logs the error (does not crash the application).

    Args:
        image_path: Absolute or relative path to the image file on disk.

    Returns:
        A list of up to 5 lowercase string tags describing the image content.
        Returns an empty list if the API call fails or the image cannot be read.
    """
    api_key: str = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        logger.warning("GEMINI_API_KEY not configured; returning empty tags.")
        return []

    try:
        # Validate that the file exists
        image_file = Path(image_path)
        if not image_file.exists():
            logger.error(f"Image file not found: {image_path}")
            return []

        # Initialise the Gemini client
        client = google.genai.Client(api_key=api_key)

        # Read the image file as bytes
        with open(image_file, "rb") as f:
            image_data = f.read()

        # Call the Gemini API with JSON response format
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": _get_mime_type(image_file.suffix),
                                "data": image_data,
                            }
                        },
                        {
                            "text": (
                                "Analyze this image and generate exactly 5 short, "
                                "descriptive tags that capture the main objects, "
                                "scenes, colors, or themes. Return only a JSON array "
                                "of strings: [\"tag1\", \"tag2\", \"tag3\", \"tag4\", \"tag5\"]. "
                                "Use lowercase, simple words."
                            )
                        },
                    ],
                }
            ],
            config={
                "response_mime_type": "application/json",
                "temperature": 0.2,
            },
        )

        # Parse the JSON response
        try:
            response_text = (getattr(response, "text", "") or "").strip()
            if not response_text:
                logger.warning("Gemini returned an empty response body.")
                return []
            tags = json.loads(response_text)

            # Ensure we have a list of strings
            if isinstance(tags, list):
                tags = [str(tag).lower().strip() for tag in tags if tag]
                return tags[:5]  # Return up to 5 tags
            else:
                logger.warning(
                    f"Unexpected response format from Gemini: {type(tags)}"
                )
                return []
        except json.JSONDecodeError as json_err:
            logger.error(f"Failed to parse Gemini JSON response: {json_err}")
            logger.debug(f"Response text was: {response.text}")
            return []

    except FileNotFoundError:
        logger.error(f"Image file not found: {image_path}")
        return []
    except (OSError, IOError) as io_err:
        logger.error(f"Failed to read image file: {io_err}")
        return []
    except TimeoutError as timeout_err:
        logger.error(f"Gemini API request timed out: {timeout_err}")
        return []
    except Exception as exc:
        logger.error(f"Unexpected error while calling Gemini API: {exc}")
        return []


def _get_mime_type(file_extension: str) -> str:
    """Map file extension to MIME type for image upload.

    Args:
        file_extension: File extension (e.g., ".jpg", ".png").

    Returns:
        MIME type string suitable for Google Gemini API.
    """
    mime_map: dict[str, str] = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mime_map.get(file_extension.lower(), "image/jpeg")


def _mock_tags(image_path: Path) -> list[str]:
    """Return placeholder tags when no AI API is configured.

    Args:
        image_path: Path to the image (used only for logging).

    Returns:
        A static list of placeholder tags.
    """
    return ["placeholder", "no-api-configured", Path(image_path).suffix.lstrip(".")]
