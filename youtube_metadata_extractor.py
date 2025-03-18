import re
import json
import sys
import argparse
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    """
    Extract the Video ID from a YouTube URL.
    Args:
        url (str): YouTube video URL
    Returns:
        str: YouTube video ID or None if not found
    """
    # Regular expression to match YouTube video IDs from various URL formats
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',      # Matches YouTube standard URLs
        r'(?:embed\/)([0-9A-Za-z_-]{11})',      # Matches embedded video URLs
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'   # Matches short URLs
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)               # Returns the extracted video ID
    return None                                 # Returns None if no valid ID is found

def get_video_transcript(video_id, languages=None):
    """
    Get the transcript/captions for a YouTube video in preferred languages.
    
    Args:
        video_id (str): YouTube video ID
        languages (list): List of language codes to try in order of preference.
                         Default is ['en', 'hi']
    
    Returns:
        tuple: (transcript list, language code) or (None, None) if not available
    """
    if languages is None:
        languages = ['en', 'hi']  # Try English first, then Hindi
    
    try:
        # First, get available transcript languages
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to get transcript in preferred languages
        for lang in languages:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                return transcript, lang
            except Exception as e:
                # If specific language not found, continue to next language
                continue

        # If preferred languages aren't available, try to get any manual transcript
        try:
            # Get the first available manual transcript
            for transcript in transcript_list:
                if not transcript.is_generated:
                    data = transcript.fetch()
                    return data, transcript.language_code
        except:
            pass

        # Try to get any generated transcript
        try:
            # Get the first available auto-generated transcript
            for transcript in transcript_list:
                if transcript.is_generated:
                    data = transcript.fetch()
                    return data, transcript.language_code
        except:
            pass

        print("Available transcript languages:")
        for transcript in transcript_list:
            lang_info = f"{transcript.language_code} "
            lang_info += "(GENERATED)" if transcript.is_generated else "(MANUALLY CREATED)"
            lang_info += "[TRANSLATABLE]" if transcript.is_translatable else ""
            print(f" - {lang_info}")
            
        return None, None
            
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return None, None

def extract_youtube_metadata(url, transcript_languages=None):
    """
    Extract all available metadata from a YouTube video using yt-dlp.
    
    Args:
        url (str): YouTube video URL
        transcript_languages (list): List of preferred language codes for transcript
        
    Returns:
        dict: Dictionary containing all extracted metadata
    """
    # Extract video ID from URL
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL or could not extract video ID")
    
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'ignoreerrors': True,
        }
        
        # Extract info with yt-dlp
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        # Create metadata dictionary
        metadata = {
            "video_id": video_id,
            "title": info.get('title'),
            "description": info.get('description'),
            "views": info.get('view_count'),
            "publish_date": info.get('upload_date'),
            "length": info.get('duration'),
            "author": info.get('uploader'),
            "channel_id": info.get('channel_id'),
            "channel_url": info.get('channel_url'),
            "thumbnail_url": info.get('thumbnail'),
            "categories": info.get('categories'),
            "tags": info.get('tags'),
            "likes": info.get('like_count'),
        }
        
        # Get transcript
        transcript, lang = get_video_transcript(video_id, transcript_languages)
        if transcript:
            metadata["transcript"] = transcript
            metadata["transcript_language"] = lang
            # Create a full transcript text for convenience
            metadata["transcript_text"] = " ".join([item["text"] for item in transcript])
        
        return metadata
    
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return None

def display_metadata(metadata):
    """
    Display the extracted metadata in a readable format.
    
    Args:
        metadata (dict): The extracted metadata
    """
    if metadata:
        print("\n--- Video Metadata ---")
        print(f"Title: {metadata['title']}")
        print(f"Author: {metadata['author']}")
        print(f"Views: {metadata['views']}")
        print(f"Publish Date: {metadata['publish_date']}")
        print(f"Length: {metadata['length']} seconds")
        
        print("\n--- Description ---")
        print(metadata['description'])
        
        if metadata.get('tags'):
            print("\n--- Tags ---")
            print(", ".join(metadata['tags']))
        
        if metadata.get('transcript'):
            lang = metadata.get('transcript_language', 'unknown')
            print(f"\n--- Transcript (language: {lang}, first 3 segments) ---")
            for segment in metadata['transcript'][:3]:
                print(f"[{segment['start']:.1f}s]: {segment['text']}")
            print("...[truncated]...")

def save_to_json(metadata, output_file):
    """
    Save metadata to a JSON file.
    
    Args:
        metadata (dict): The metadata to save
        output_file (str): Path to the output file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Metadata saved to {output_file}")

def main():
    """
    Main function to handle command-line arguments and execute the metadata extraction.
    """
    parser = argparse.ArgumentParser(description='Extract metadata from YouTube videos')
    parser.add_argument('url', nargs='?', help='YouTube video URL')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--languages', '-l', nargs='+', default=['en', 'hi'], 
                        help='Preferred transcript languages (space-separated language codes, e.g., "en hi")')
    
    args = parser.parse_args()
    
    # If URL is not provided as argument, prompt for it
    if args.url:
        url = args.url
    else:
        url = input("Enter YouTube video URL: ")
    
    metadata = extract_youtube_metadata(url, args.languages)
    
    if metadata:
        # Save to JSON if output path is provided
        if args.output:
            save_to_json(metadata, args.output)
        else:
            # Display metadata if not saving to file
            display_metadata(metadata)
    else:
        print("Failed to extract metadata.")
        sys.exit(1)

if __name__ == "__main__":
    main()
