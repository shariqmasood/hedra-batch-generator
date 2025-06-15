"""
Configuration settings for the Hedra AI Batch Video Generator.

This module contains all the configuration constants and settings used throughout the application.
It includes API endpoints, file patterns, logging settings, and environment variable names.
"""

import os
from pathlib import Path

# API Configuration
# Base URL for the Hedra Character 3 API
HEDRA_API_BASE_URL = "https://api.hedra.ai/v1"
# Maximum time to wait for video generation (5 minutes)
API_TIMEOUT = 300
# Time interval between status checks (10 seconds)
POLL_INTERVAL = 10

# File patterns for finding input files
# Pattern to match PNG image files
IMAGE_PATTERN = "*.png"
# Pattern to match WAV audio files
AUDIO_PATTERN = "*.wav"

# Logging Configuration
# Name of the log file that will be created in the output folder
LOG_FILE = "hedra_batch.log"
# Format for log messages: timestamp - log level - message
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Environment Variables
# Name of the environment variable that stores the Hedra API key
ENV_API_KEY = "HEDRA_API_KEY"

# Default settings
# Default output folder (None means use input folder)
DEFAULT_OUTPUT_FOLDER = None 