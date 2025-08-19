import pyttsx3
import time
import os
from typing import Dict, List

def test_tts_setup():
    """Test TTS setup and voice capabilities for character assignment."""
    
    print("=== ReadToMe TTS Test ===")
    
    # Initialize TTS engine
    engine = pyttsx3.init()
    
    # Get available voices
    voices = engine.getProperty('voices')
    print(f"\nAvailable voices: {len(voices)}")
    
    # Display voice information
    for i, voice in enumerate(voices[:5]):  # Show first 5 voices
        print(f"Voice {i}: {voice.name} (ID: {voice.id})")
        print(f"  Language: {getattr(voice, 'languages', 'Unknown')}")
        print(f"  Gender: {getattr(voice, 'gender', 'Unknown')}")
    
    # Test different voices for character assignment
    test_text = "Hello! I am a character in your story. Each character should have a unique voice."
    
    print(f"\n=== Testing Voice Assignment for Characters ===")
    
    # Simulate different characters with different voices
    characters = [
        {"name": "Narrator", "voice_id": 0},
        {"name": "Alice", "voice_id": 1 if len(voices) > 1 else 0},
        {"name": "Bob", "voice_id": 2 if len(voices) > 2 else 0},
    ]
    
    for char in characters:
        print(f"\nTesting voice for {char['name']}...")
        
        # Set voice for this character
        if char['voice_id'] < len(voices):
            engine.setProperty('voice', voices[char['voice_id']].id)
        
        # Set speech rate and volume
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.8)  # Volume level (0.0 to 1.0)
        
        # Generate audio file for this character
        output_file = f"test_{char['name'].lower()}.wav"
        
        start_time = time.time()
        
        # Save to file
        engine.save_to_file(test_text, output_file)
        engine.runAndWait()
        
        elapsed_time = time.time() - start_time
        
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"  ✓ Generated: {output_file} ({file_size} bytes) in {elapsed_time:.2f}s")
        else:
            print(f"  ✗ Failed to generate: {output_file}")
    
    print(f"\n=== TTS Engine Properties ===")
    print(f"Current rate: {engine.getProperty('rate')}")
    print(f"Current volume: {engine.getProperty('volume')}")
    print(f"Current voice: {engine.getProperty('voice')}")
    
    # Demonstrate voice switching for dialogue
    print(f"\n=== Character Dialogue Test ===")
    dialogue = [
        {"character": "Alice", "text": "Hello Bob, how are you today?", "voice_id": 1 if len(voices) > 1 else 0},
        {"character": "Bob", "text": "I'm doing well, Alice! Thanks for asking.", "voice_id": 2 if len(voices) > 2 else 0},
        {"character": "Narrator", "text": "And so their conversation continued.", "voice_id": 0},
    ]
    
    for line in dialogue:
        print(f"{line['character']}: {line['text']}")
        
        # Switch voice for each character
        if line['voice_id'] < len(voices):
            engine.setProperty('voice', voices[line['voice_id']].id)
        
        # For demo, we'll just show the voice switching
        # In real app, you'd generate audio here
        current_voice = engine.getProperty('voice')
        voice_name = next((v.name for v in voices if v.id == current_voice), "Unknown")
        print(f"  -> Using voice: {voice_name}")
    
    print(f"\n=== Test Complete ===")
    print("This demonstrates the core functionality for your ReadToMe project:")
    print("1. Multiple voice detection")
    print("2. Voice assignment to characters") 
    print("3. Audio file generation")
    print("4. Voice switching for dialogue")
    
    # Clean up test files
    for char in characters:
        test_file = f"test_{char['name'].lower()}.wav"
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"Cleaned up: {test_file}")

if __name__ == "__main__":
    test_tts_setup()
