"""
Hedra AI Batch Video Generator - Main CLI script.

This script provides a command-line interface for batch processing audio files
with a single character image to generate videos using the Hedra Character 3 API.
It handles file validation, API interactions, and logging of the entire process.
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Optional

from hedra_api import HedraAPI, HedraAPIError
import config

def setup_logging(output_folder: Path) -> None:
    """
    Configure logging to both file and console.
    
    Args:
        output_folder: Path where the log file should be created.
    """
    log_file = output_folder / config.LOG_FILE
    logging.basicConfig(
        level=logging.INFO,
        format=config.LOG_FORMAT,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def find_image_file(folder: Path) -> Optional[Path]:
    """
    Find the single PNG image in the input folder.
    
    Args:
        folder: Path to search for the PNG image.
        
    Returns:
        Path: Path to the found PNG image.
        
    Raises:
        ValueError: If no PNG image is found or if multiple PNG images are found.
    """
    png_files = list(folder.glob(config.IMAGE_PATTERN))
    if not png_files:
        raise ValueError(f"No PNG image found in {folder}")
    if len(png_files) > 1:
        raise ValueError(f"Multiple PNG images found in {folder}. Only one is allowed.")
    return png_files[0]

def process_audio_file(api: HedraAPI, audio_file: Path, image_id: str, prompt: str, output_folder: Path) -> None:
    """
    Process a single audio file and generate its video.
    
    Args:
        api: Initialized HedraAPI instance.
        audio_file: Path to the audio file to process.
        image_id: ID of the previously uploaded image.
        prompt: Text prompt for video generation.
        output_folder: Path where the output video should be saved.
        
    Raises:
        HedraAPIError: If any API operation fails.
    """
    try:
        logger.info(f"Processing {audio_file.name}")
        
        # Upload audio file
        audio_id = api.upload_asset(audio_file)
        logger.info(f"Uploaded audio file: {audio_file.name}")
        
        # Create video
        video_id = api.create_video(image_id, audio_id, prompt)
        logger.info(f"Created video with ID: {video_id}")
        
        # Wait for video generation
        api.wait_for_video(video_id)
        logger.info("Video generation completed")
        
        # Download video
        output_file = output_folder / f"{audio_file.stem}.mp4"
        api.download_video(video_id, output_file)
        logger.info(f"Downloaded video to: {output_file}")
        
    except HedraAPIError as e:
        logger.error(f"Error processing {audio_file.name}: {str(e)}")
        raise

def main():
    """
    Main entry point for the CLI.
    
    Parses command line arguments, validates input/output folders,
    and orchestrates the video generation process.
    """
    parser = argparse.ArgumentParser(description="Hedra AI Batch Video Generator")
    parser.add_argument("--input_folder", required=True, help="Folder containing PNG and WAV files")
    parser.add_argument("--prompt", required=True, help="Prompt to use for video generation")
    parser.add_argument("--output_folder", help="Output folder for generated videos")
    parser.add_argument("--api_key", help="Hedra API key (optional if set in .env)")
    
    args = parser.parse_args()
    
    # Convert paths to Path objects
    input_folder = Path(args.input_folder)
    output_folder = Path(args.output_folder) if args.output_folder else input_folder
    
    # Validate folders
    if not input_folder.exists():
        raise ValueError(f"Input folder does not exist: {input_folder}")
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Setup logging
    setup_logging(output_folder)
    logger.info("Starting Hedra AI Batch Video Generator")
    
    try:
        # Initialize API client
        api = HedraAPI(args.api_key)
        
        # Find and upload image
        image_file = find_image_file(input_folder)
        image_id = api.upload_asset(image_file)
        logger.info(f"Uploaded image: {image_file.name}")
        
        # Process each audio file
        audio_files = list(input_folder.glob(config.AUDIO_PATTERN))
        if not audio_files:
            raise ValueError(f"No WAV files found in {input_folder}")
        
        logger.info(f"Found {len(audio_files)} audio files to process")
        for audio_file in audio_files:
            process_audio_file(api, audio_file, image_id, args.prompt, output_folder)
        
        logger.info("Batch processing completed successfully")
        
    except Exception as e:
        logger.error(f"Batch processing failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 