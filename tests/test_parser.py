#!/usr/bin/env python3
"""Test script for the TextParser with sample data."""

import sys
import os
sys.path.append('server')
from server.src.parser import TextParser
from pathlib import Path

def test_parser():
    """Test the parser with sample text."""
    
    project_root = Path(__file__).parent.parent
    sample_file_path = project_root / 'server' / 'data' / 'sample_text.txt'
    
    # Load sample text
    with open(sample_file_path, 'r', encoding='utf-8') as f:
        sample_text = f.read()
    
    print('=== TESTING PARSER ON SAMPLE TEXT ===')
    print('Sample text preview:')
    print(repr(sample_text[:80]) + '...')
    print()
    
    # Parse the text
    parser = TextParser()
    segments = parser.parse_text(sample_text)
    
    print(f'Found {len(segments)} segments:')
    print()
    
    for i, segment in enumerate(segments, 1):
        speaker_str = segment.speaker or "None"
        print(f'{i}. Type: {segment.segment_type:10} | Speaker: {speaker_str:8} | Confidence: {segment.confidence}')
        print(f'   Content: {segment.content[:70]}...')
        print()
    
    # Summary
    dialogue_count = sum(1 for s in segments if s.segment_type == 'dialogue')
    narrative_count = sum(1 for s in segments if s.segment_type == 'narrative')
    speakers = set(s.speaker for s in segments if s.speaker)
    
    print('=== SUMMARY ===')
    print(f'Dialogue segments: {dialogue_count}')
    print(f'Narrative segments: {narrative_count}')
    print(f'Unique speakers: {speakers if speakers else "None detected"}')

if __name__ == "__main__":
    test_parser()
