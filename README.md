# Hedra AI Batch Video Generator

A Python CLI tool that generates videos using the Hedra Character 3 API by processing a folder containing a character image and multiple audio files.

## Features

- Process multiple audio files with a single character image
- Generate videos using the Hedra Character 3 API
- Detailed logging of the process
- Configurable output location
- Environment variable support for API key

## Requirements

- Python 3.9 or higher
- Required Python packages:
  - requests
  - python-dotenv

## Installation

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.template` to `.env` and add your Hedra API key:
   ```bash
   cp .env.template .env
   ```

## Usage

Basic usage:
```bash
python hedra_batch.py --input_folder ./my_folder --prompt "Welcome to our AI demo video!"
```

Full options:
```bash
python hedra_batch.py \
    --input_folder ./my_folder \
    --prompt "Welcome to our AI demo video!" \
    --output_folder ./output \
    --api_key your_api_key_here
```

### Input Folder Structure

The input folder should contain:
- One `.png` image file (character)
- One or more `.wav` audio files

Example:
```
input_folder/
├── character.png
├── audio1.wav
├── audio2.wav
└── ...
```

### Output

For each `.wav` file, a corresponding `.mp4` video will be generated in the output folder (or input folder if not specified).

A log file `hedra_batch.log` will be created in the output folder with detailed processing information.

## Error Handling

The tool includes comprehensive error handling for:
- Missing or invalid input files
- API communication issues
- Video generation timeouts
- File system errors

## Future Possibilities

This basic implementation can be extended with additional features based on requirements:

- Web interface for easier management
- Support for multiple audio formats
- Audio processing and normalization
- Parallel processing for faster generation
- Custom video settings and styles
- Enterprise features like user management and analytics

## License

MIT License 