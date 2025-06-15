# Hedra AI Batch Video Generator

A Python CLI tool that generates videos using the Hedra Character 3 API by processing a folder containing a character image and multiple audio files.

## Current Features

- Process multiple audio files with a single character image
- Generate videos using the Hedra Character 3 API
- Detailed logging of the process
- Configurable output location
- Environment variable support for API key

## Planned Features (Not Yet Implemented)

### 1. Advanced Video Generation
- **Multiple Character Support**: Process multiple character images in a single batch
- **Custom Animation Styles**: Support for different animation styles and transitions
- **Background Customization**: Allow custom backgrounds for generated videos
- **Resolution Options**: Support for different video resolutions and quality settings

### 2. Audio Processing
- **Audio Normalization**: Automatically normalize audio levels across all files
- **Audio Trimming**: Remove silence and trim audio files
- **Format Conversion**: Support for multiple audio formats (MP3, WAV, OGG)
- **Audio Effects**: Basic audio effects and enhancements

### 3. Performance & Scalability
- **Parallel Processing**: Process multiple videos simultaneously
- **Rate Limiting**: Smart API rate limiting to prevent throttling
- **Retry Queue**: Automatic retry for failed requests
- **Progress Tracking**: Real-time progress tracking and estimation

### 4. User Interface
- **Web Interface**: Modern web-based UI using Streamlit
- **Batch Management**: Queue and manage multiple batch jobs
- **Preview Generation**: Generate low-quality previews before final render
- **Template Management**: Save and reuse common prompts and settings

### 5. Enterprise Features
- **User Authentication**: Multi-user support with role-based access
- **API Integration**: REST API for integration with other systems
- **Usage Analytics**: Track and analyze usage patterns
- **Cost Optimization**: Smart batching to minimize API costs

### 6. Quality Assurance
- **Video Validation**: Automated quality checks for generated videos
- **Error Recovery**: Automatic recovery from common failure scenarios
- **Consistency Checks**: Ensure consistent quality across batch
- **Metadata Management**: Track and manage video metadata

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

## Development Roadmap

The development of these features will be prioritized based on client needs and feedback. Each feature will be implemented with:
- Comprehensive testing
- Documentation
- Performance optimization
- Security considerations

## License

MIT License 