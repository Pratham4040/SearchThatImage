"""AI Vision service – isolates all AI API interactions.

Replace the placeholder implementation below with a real AI Vision API call
(e.g. Google Cloud Vision, OpenAI GPT-4o Vision, AWS Rekognition, etc.).
The rest of the application should never import an AI SDK directly.
"""

from __future__ import annotations

import os
from pathlib import Path

import requests


def get_image_tags(image_path: Path) -> list[str]:
    """Send an image to the configured AI Vision API and return descriptive tags.

    Args:
        image_path: Absolute or relative path to the image file on disk.

    Returns:
        A list of lowercase string tags describing the image content.

    Raises:
        RuntimeError: If the API call fails or returns an unexpected response.
    """
    api_key: str = os.getenv("AI_VISION_API_KEY", "")
    api_url: str = os.getenv("AI_VISION_API_URL", "")

    if not api_key or not api_url:
        # Fallback when no API is configured (development / testing).
        return _mock_tags(image_path)

    try:
        with open(image_path, "rb") as image_file:
            response = requests.post(
                api_url,
                headers={"Authorization": f"Bearer {api_key}"},
                files={"image": image_file},
                timeout=30,
            )
        response.raise_for_status()
        data: dict[str, object] = response.json()
        # Adapt this key to match your chosen AI API's response schema.
        raw_tags: list[str] = data.get("tags", [])  # type: ignore[assignment]
        return [tag.lower().strip() for tag in raw_tags if tag]
    except requests.RequestException as exc:
        raise RuntimeError(f"AI Vision API request failed: {exc}") from exc


def _mock_tags(image_path: Path) -> list[str]:
    """Return placeholder tags when no AI API is configured.

    Args:
        image_path: Path to the image (used only for logging).

    Returns:
        A static list of placeholder tags.
    """
    return ["placeholder", "no-api-configured", Path(image_path).suffix.lstrip(".")]
