from server.src.voice_assigner import VoiceAssigner
from server.src.parser import TextSegment, TextParser
from server.src.synthesizer import AdaptiveSynthesizer


text_segments = []


sample_text = "Hello, this is a test of the voice assigner for a dialogue. Hello,This is a test of the voice assigner for a narrative. Hello,This is a test of the voice assigner for an action."

def test_voice_assigner():
    print("Testing voice assigner")
    voice_assigner = VoiceAssigner()
    print("Voice assigner")
    print(voice_assigner)
    parser = TextParser()
    text_segments = parser.parse_text(sample_text)
    print("Text segments")
    print(text_segments)
    
    voice_assigner.assign_voices(text_segments)
    print("Character assignments")
    print(voice_assigner.character_assignments)
    
    voice_segments = voice_assigner.assign_voices(text_segments)
    print("Voice segments")
    print(voice_segments)
    
    print("Synthesizing voice segments")
    synthesizer = AdaptiveSynthesizer()
    print("Synthesizing voice segments")
    for voice_segment in voice_segments:
        print(voice_segment.get_synthesizer_params())
        synthesizer.synthesize(voice_segment.get_synthesizer_params()["text"], voice_segment.get_synthesizer_params()["voice_type"])
        print(f"Synthesized {voice_segment.get_synthesizer_params()['text']} with voice {voice_segment.get_synthesizer_params()['voice_type']}")


if __name__ == "__main__":
    test_voice_assigner()