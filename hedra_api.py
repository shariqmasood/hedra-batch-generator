"""
Hedra API interaction module for video generation.

This module provides a client for interacting with the Hedra Character 3 API.
It handles all API operations including asset uploads, video creation, status checking,
and video downloads. The module includes error handling and retry logic for API operations.
"""

import os
import time
import logging
import requests
from pathlib import Path
from typing import Optional, Tuple

import config

# Configure logging
logger = logging.getLogger(__name__)

class HedraAPIError(Exception):
    """
    Custom exception for Hedra API related errors.
    Used to distinguish API-specific errors from other exceptions.
    """
    pass

class HedraAPI:
    """
    Client for interacting with the Hedra Character 3 API.
    
    This class provides methods for:
    - Uploading assets (images and audio)
    - Creating videos
    - Checking video generation status
    - Downloading generated videos
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Hedra API client.
        
        Args:
            api_key: Optional API key. If not provided, will try to get from environment.
        
        Raises:
            HedraAPIError: If no API key is available.
        """
        self.api_key = api_key or os.getenv(config.ENV_API_KEY)
        if not self.api_key:
            raise HedraAPIError("API key not provided. Set HEDRA_API_KEY in .env or pass via --api_key")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }

    def upload_asset(self, file_path: Path) -> str:
        """
        Upload an asset (image or audio) to Hedra API.
        
        Args:
            file_path: Path to the file to upload.
            
        Returns:
            str: The asset ID returned by the API.
            
        Raises:
            HedraAPIError: If upload fails.
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f)}
                response = requests.post(
                    f"{config.HEDRA_API_BASE_URL}/assets",
                    headers=self.headers,
                    files=files
                )
                response.raise_for_status()
                return response.json()['asset_id']
        except requests.exceptions.RequestException as e:
            raise HedraAPIError(f"Failed to upload asset {file_path}: {str(e)}")

    def create_video(self, image_id: str, audio_id: str, prompt: str) -> str:
        """
        Create a video using the provided assets and prompt.
        
        Args:
            image_id: ID of the uploaded image asset.
            audio_id: ID of the uploaded audio asset.
            prompt: Text prompt for video generation.
            
        Returns:
            str: The video ID returned by the API.
            
        Raises:
            HedraAPIError: If video creation fails.
        """
        try:
            data = {
                "image_id": image_id,
                "audio_id": audio_id,
                "prompt": prompt
            }
            response = requests.post(
                f"{config.HEDRA_API_BASE_URL}/videos",
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()['video_id']
        except requests.exceptions.RequestException as e:
            raise HedraAPIError(f"Failed to create video: {str(e)}")

    def get_video_status(self, video_id: str) -> str:
        """
        Get the current status of a video generation.
        
        Args:
            video_id: ID of the video to check.
            
        Returns:
            str: Current status of the video.
            
        Raises:
            HedraAPIError: If status check fails.
        """
        try:
            response = requests.get(
                f"{config.HEDRA_API_BASE_URL}/videos/{video_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()['status']
        except requests.exceptions.RequestException as e:
            raise HedraAPIError(f"Failed to get video status: {str(e)}")

    def download_video(self, video_id: str, output_path: Path) -> None:
        """
        Download the generated video.
        
        Args:
            video_id: ID of the video to download.
            output_path: Path where the video should be saved.
            
        Raises:
            HedraAPIError: If download fails.
        """
        try:
            response = requests.get(
                f"{config.HEDRA_API_BASE_URL}/videos/{video_id}/download",
                headers=self.headers,
                stream=True
            )
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        except requests.exceptions.RequestException as e:
            raise HedraAPIError(f"Failed to download video: {str(e)}")

    def wait_for_video(self, video_id: str) -> None:
        """
        Wait for video generation to complete.
        
        Args:
            video_id: ID of the video to wait for.
            
        Raises:
            HedraAPIError: If video generation fails or times out.
        """
        start_time = time.time()
        while True:
            if time.time() - start_time > config.API_TIMEOUT:
                raise HedraAPIError("Video generation timed out")

            status = self.get_video_status(video_id)
            if status == "completed":
                return
            elif status == "failed":
                raise HedraAPIError("Video generation failed")
            
            time.sleep(config.POLL_INTERVAL) 