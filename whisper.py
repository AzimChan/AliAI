#!/usr/bin/env python3
"""
Simple Whisper Speech-to-Text
Input: audio file, Output: text
"""
import requests
import os
import sys

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If dotenv is not available, try to load .env manually
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass

def filter_false_positives(text):
    """
    Filter out common false positive transcriptions when there's no real speech
    """
    if not text:
        return ""
    
    # Common false positive phrases in various languages
    false_positives = [
        # English
        "thanks for watching",
        "don't forget to like and subscribe",
        "thanks for watching and don't forget to like and subscribe",
        "please like and subscribe",
        "hit the like button",
        "subscribe to my channel",
        "thanks for watching this video",
        "make sure to subscribe",
        "don't forget to subscribe",
        "thanks for watching and subscribing",
        "like and subscribe if you enjoyed",
        "thanks for watching and thanks for subscribing",
        "thanks for watching and don't forget to hit the like button",
        "thanks for watching and don't forget to subscribe",
        "thanks for watching and don't forget to like and subscribe to my channel",
        
        # Japanese false positives
        "私のビデオをご覧いただきありがとうございます",
        "良い一日を",
        "ご視聴ありがとうございました",
        "いいねとチャンネル登録をお忘れなく",
        "チャンネル登録をお願いします",
        "いいねボタンを押してください",
        "ご視聴ありがとうございました",
        "いいねとチャンネル登録をお忘れなく",
        "チャンネル登録をお願いします",
        "いいねボタンを押してください",
        "チャンネル登録をお忘れなく",
        "ご視聴ありがとうございました",
        "いいねとチャンネル登録をお忘れなく",
        "チャンネル登録をお願いします",
        "いいねボタンを押してください",
        "チャンネル登録をお忘れなく",
        
        # Partial matches
        "thanks for",
        "don't forget",
        "like and subscribe",
        "subscribe to",
        "hit the like",
        "make sure to",
        "ご視聴",
        "チャンネル登録",
        "いいね",
        "ボタン",
        "ビデオ",
        "ありがとう",
        
        # Very short or repetitive phrases
        "thank you thank you",
        "thanks thanks",
        "subscribe subscribe",
        "like like",
        "watch watch",
        "video video",
    ]
    
    # Convert to lowercase for comparison
    text_lower = text.lower().strip()
    
    # Check for exact matches
    for phrase in false_positives:
        if phrase.lower() in text_lower:
            print(f"🚫 Filtered out false positive: '{phrase}'")
            return ""
    
    # Check for very short text (likely false positive)
    if len(text.strip()) < 10:
        print(f"🚫 Filtered out very short text: '{text}'")
        return ""
    
    # Check for repetitive patterns
    words = text_lower.split()
    if len(words) > 2:
        # Check if more than 50% of words are repeated
        unique_words = set(words)
        if len(unique_words) / len(words) < 0.5:
            print(f"🚫 Filtered out repetitive text: '{text}'")
            return ""
    
    return text

def transcribe_audio(audio_file_path, language=None, filter_false=True):
    """
    Simple function to transcribe audio file to text
    
    Args:
        audio_file_path (str): Path to the audio file
        language (str): Language code (optional, e.g., 'en', 'ru', 'kk')
        filter_false (bool): Whether to filter out false positive transcriptions
    
    Returns:
        str: Transcribed text or None if error
    """
    # Get API key from environment
    api_key = os.getenv("TOKEN")
    if not api_key:
        print("❌ Error: TOKEN not found in environment variables")
        return None
    
    # API configuration
    base_url = "https://openai-hub.neuraldeep.tech"
    transcription_url = f"{base_url}/audio/transcriptions"
    
    try:
        # Check if file exists
        if not os.path.exists(audio_file_path):
            print(f"❌ Error: Audio file not found: {audio_file_path}")
            return None
        
        print(f"🎤 Transcribing: {audio_file_path}")
        
        # Prepare headers and data
        headers = {"Authorization": f"Bearer {api_key}"}
        
        files = {
            "file": (os.path.basename(audio_file_path), open(audio_file_path, "rb"), "audio/mpeg")
        }
        
        data = {
            "model": "whisper-1",
            "response_format": "json"
        }
        
        # Add language if specified
        if language:
            data["language"] = language
            print(f"🌍 Language: {language}")
        
        # Make API request
        response = requests.post(
            transcription_url,
            headers=headers,
            files=files,
            data=data,
            timeout=60
        )
        
        # Close the file
        files["file"][1].close()
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            text = result.get("text", "")
            
            # Filter out common false positives when there's no real speech
            if filter_false:
                text = filter_false_positives(text)
            
            if text:
                print("✅ Transcription successful!")
                return text
            else:
                print("⚠️ No speech detected or filtered out false positives")
                return ""
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Main function - simple usage"""
    if len(sys.argv) < 2:
        print("Usage: python whisper.py <audio_file> [language] [--no-filter]")
        print("Example: python whisper.py audio.ogg en")
        print("Example: python whisper.py audio.ogg en --no-filter")
        print("\nOptions:")
        print("  --no-filter    Disable false positive filtering")
        return
    
    audio_file = sys.argv[1]
    language = None
    filter_false = True
    
    # Parse arguments
    for arg in sys.argv[2:]:
        if arg == "--no-filter":
            filter_false = False
        elif not arg.startswith("--"):
            language = arg
    
    # Transcribe audio
    text = transcribe_audio(audio_file, language, filter_false)
    
    if text:
        print(f"\n📝 Transcription:\n{text}")
        
        # Save to file
        output_file = f"{os.path.splitext(audio_file)[0]}_transcription.txt"
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"\n💾 Saved to: {output_file}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    else:
        print("❌ No speech detected or transcription failed")
        print("💡 Try using --no-filter to see raw transcription results")

if __name__ == "__main__":
    main()
