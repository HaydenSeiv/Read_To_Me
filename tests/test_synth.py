"""Test the AdaptiveSynthesizer implementation."""

import sys
import os

# Add server directory to path first
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))

# Now import from src
from src.synthesizer import AdaptiveSynthesizer



def test_synthesizer():
    """Test basic synthesizer functionality."""
    
    print("=== Testing AdaptiveSynthesizer ===")
    
    # Test development mode
    print("\n1. Testing Development Mode...")
    dev_synth = AdaptiveSynthesizer(development_mode=True)
    
    test_text = "Hello, this is a test of the development synthesizer."
    output_file = dev_synth.synthesize(test_text, voice_type="narrator")
    print(f"   Audio generated: {output_file}")
    
    # Test voice mappings
    print("\n2. Testing Voice Mappings...")
    voices = dev_synth.get_available_voices()
    print(f"   Available voices: {voices}")
    
    # Test mode switching
    print("\n3. Testing Mode Switch...")
    print("   Switching to production mode (this will download a larger model)...")
    dev_synth.switch_mode(development_mode=False)
    
    output_file_2 = dev_synth.synthesize(test_text, voice_type="narrator")
    print(f"   Quality audio generated: {output_file_2}")
    
    print("\n✅ Synthesizer tests completed!")

if __name__ == "__main__":
    test_synthesizer()