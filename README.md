# Audience Jugaad - AI Agent for YouTube Creators

An AI-powered tool to help YouTube creators manage and optimize their social media presence.

## Features

### YouTube Metadata Extractor

Extract comprehensive metadata from any YouTube video, including:
- Basic information (title, description, views, etc.)
- Channel information
- Tags/keywords
- Transcript/captions (supports multiple languages)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/audience-jugaad.git
cd audience-jugaad

# Install dependencies (for Python 3)
pip3 install -r requirements.txt
```

## Requirements

The following Python libraries are required:

- **yt-dlp**: A feature-rich YouTube downloader and metadata extractor. Used to extract comprehensive metadata from YouTube videos more reliably than alternative libraries.
- **youtube-transcript-api**: Used to fetch video transcripts/captions from YouTube videos.

Install them using Python 3:

```bash
pip3 install yt-dlp youtube-transcript-api
```

## Usage

### YouTube Metadata Extractor

#### Command-line Usage

```bash
# Basic usage
python3 youtube_metadata_extractor.py https://www.youtube.com/watch?v=VIDEO_ID

# Save output to JSON file
python3 youtube_metadata_extractor.py https://www.youtube.com/watch?v=VIDEO_ID --output video_metadata.json

# Specify preferred transcript languages (will try in order)
python3 youtube_metadata_extractor.py https://www.youtube.com/watch?v=VIDEO_ID --languages en hi
```

#### Programmatic Usage

```python
from youtube_metadata_extractor import extract_youtube_metadata

# Extract metadata from a YouTube video (default tries English then Hindi)
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
metadata = extract_youtube_metadata(url)

# Specify preferred languages for transcript
metadata = extract_youtube_metadata(url, transcript_languages=['en', 'hi', 'fr'])

# Access specific metadata
print(metadata['title'])
print(metadata['views'])
print(metadata['transcript_text'])  # Full transcript text
print(metadata['transcript_language'])  # Language of the transcript
```

### Running the Code

Run the script using Python 3:

```bash
# With URL as argument, saving to JSON file
python3 youtube_metadata_extractor.py https://www.youtube.com/watch?v=VIDEO_ID --output video_metadata.json

# Interactive mode (will prompt for URL)
python3 youtube_metadata_extractor.py

# Specify language preference (English, then Hindi, then Spanish)
python3 youtube_metadata_extractor.py https://www.youtube.com/watch?v=VIDEO_ID --languages en hi es
```

### Transcript Language Support

The tool will attempt to find transcripts in the following order:
1. Try each of the specified languages in the order provided
2. If none are found, try to use any available manual transcript
3. As a last resort, try to use any available auto-generated transcript
4. If a transcript can't be found, the available language options will be displayed

### Missing Transcript Handling

When no transcript is found for a video:

1. The JSON output will not contain the following fields:
   - `transcript`: The transcript segments
   - `transcript_language`: The language code of the transcript
   - `transcript_text`: The full text of the transcript

2. The metadata extractor will still return all other available metadata (title, description, views, etc.)

3. The available transcript languages (if any) will be printed to the console to help you identify which languages are supported for that video.

Example JSON output with no transcript:
```json
{
  "video_id": "VIDEO_ID",
  "title": "Video Title",
  "description": "Video description...",
  "views": 12345,
  "publish_date": "20230101",
  "length": 120,
  "author": "Channel Name",
  // other metadata fields...
  // transcript fields will be absent
}
```

### Testing the Code

To test the YouTube metadata extractor:

1. Make sure you have installed the required dependencies.
2. Run a simple test:

```bash
# Test with a known YouTube video
python3 youtube_metadata_extractor.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Test with a Hindi video
python3 youtube_metadata_extractor.py https://www.youtube.com/watch?v=IN9PW8GRgKo --languages hi en
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
