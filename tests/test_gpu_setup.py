import torch
from TTS.api import TTS
import time
import os

def test_gpu_setup():
    """Test GPU acceleration and model performance."""
    
    # Check GPU
    print(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    
    # Test fast model (for development)
    print("\n=== Testing Fast Model ===")
    fast_tts = TTS("tts_models/en/ljspeech/fast_pitch")
    
    if torch.cuda.is_available():
        fast_tts.to("cuda")  # Move to GPU
    
    test_text = "This is a test of the fast development model for quick prototyping."
    
    start_time = time.time()
    fast_tts.tts_to_file(text=test_text, file_path="test_fast.wav")
    fast_time = time.time() - start_time
    
    print(f"Fast model time: {fast_time:.2f} seconds")
    
    # Test high-quality model
    print("\n=== Testing High-Quality Model ===")
    quality_tts = TTS("tts_models/en/vctk/vits")
    
    if torch.cuda.is_available():
        quality_tts.to("cuda")  # Move to GPU
    
    start_time = time.time()
    quality_tts.tts_to_file(text=test_text, 
                           speaker="p225",
                           file_path="test_quality.wav")
    quality_time = time.time() - start_time
    
    print(f"Quality model time: {quality_time:.2f} seconds")
    print(f"Available speakers: {len(quality_tts.speakers)} voices")
    
    # Performance summary
    print(f"\n=== Performance Summary ===")
    print(f"Fast model: {fast_time:.2f}s")
    print(f"Quality model: {quality_time:.2f}s") 
    print(f"Speed ratio: {quality_time/fast_time:.1f}x slower for quality")

if __name__ == "__main__":
    test_gpu_setup()