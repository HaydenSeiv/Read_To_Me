import re
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.utils import get_logger
from typing import List, Dict, Optional, NamedTuple
from dataclasses import dataclass
import time
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    

# Patterns to identify:
# Build patterns with explicit Unicode characters to avoid copy/paste issues
_ASCII_QUOTE = chr(34)      # "
_SMART_OPEN = chr(8220)     # "
_SMART_CLOSE = chr(8221)    # "
_ASCII_SINGLE = chr(39)     # '
_SMART_SINGLE_OPEN = chr(8216)  # '
_SMART_SINGLE_CLOSE = chr(8217) # '

DIALOGUE_PATTERNS = [
    rf'{_ASCII_QUOTE}([^{_ASCII_QUOTE}]*){_ASCII_QUOTE}',           # ASCII quotes "text"
    rf'{_SMART_OPEN}([^{_SMART_CLOSE}]*){_SMART_CLOSE}',           # Smart quotes "text"
    rf'{_ASCII_QUOTE}([^{_SMART_CLOSE}]*){_SMART_CLOSE}',          # Mixed: ASCII open, smart close
    rf'{_SMART_OPEN}([^{_ASCII_QUOTE}]*){_ASCII_QUOTE}',           # Mixed: smart open, ASCII close
    rf'{_ASCII_SINGLE}([^{_ASCII_SINGLE}]*){_ASCII_SINGLE}',       # Single quotes 'text'
    rf'{_SMART_SINGLE_OPEN}([^{_SMART_SINGLE_CLOSE}]*){_SMART_SINGLE_CLOSE}',  # Smart single quotes
]

SPEAKER_PATTERNS = [
    # ASCII quote patterns
    rf'{_ASCII_QUOTE}[^{_ASCII_QUOTE}]*{_ASCII_QUOTE},?\s*(\w+)\s+(?:said|asked|replied|whispered|muttered)',
    rf'(\w+)\s+(?:said|asked|replied|muttered),?\s*{_ASCII_QUOTE}[^{_ASCII_QUOTE}]*{_ASCII_QUOTE}',
    
    # Mixed quote patterns (ASCII open, smart close)
    rf'{_ASCII_QUOTE}[^{_SMART_CLOSE}]*{_SMART_CLOSE},?\s*(\w+)\s+(?:said|asked|replied|whispered|muttered)',
    rf'(\w+)\s+(?:said|asked|replied|muttered),?\s*{_ASCII_QUOTE}[^{_SMART_CLOSE}]*{_SMART_CLOSE}',
    
    # Smart quote patterns
    rf'{_SMART_OPEN}[^{_SMART_CLOSE}]*{_SMART_CLOSE},?\s*(\w+)\s+(?:said|asked|replied|whispered|muttered)',
    rf'(\w+)\s+(?:said|asked|replied|muttered),?\s*{_SMART_OPEN}[^{_SMART_CLOSE}]*{_SMART_CLOSE}',
    
    # More flexible patterns for complex attribution (using mixed quotes for your text)
    rf'{_ASCII_QUOTE}[^{_SMART_CLOSE}]*{_SMART_CLOSE},?\s*(\w+),?\s+[^,]*(?:said|asked|replied|muttered)',
]

@dataclass
class TextSegment:
    """Represents a parsed segment of text."""
    content: str
    segment_type: str  # 'dialogue', 'narrative', 'action'
    speaker: Optional[str] = None
    confidence: float = 1.0  # How sure are we about this classification?

class TextParser:
    """Parses story text into dialogue and narrative segments."""
    def __init__(self):
        self.logger = get_logger(__name__)
        # Initialize any state you need
    
    def parse_text(self, text: str) -> List[TextSegment]:
        """
        Parse text into segments.
        
        Args:
            text: Raw story text to parse
            
        Returns:
            List of TextSegment objects with classification and metadata
        """
        start_time = time.time()
        
        segments = []
        
        # Step 1: Clean and normalize text
        cleaned_text = self._clean_text(text)
        
        # Step 2: Split into sentences
        sentences = self._split_sentences(cleaned_text)
        
        # Step 3: Process each sentence
        for sentence in sentences:
            segment = self._classify_sentence(sentence)
            segments.append(segment)
        
        self.logger.info(f"Parsed {len(segments)} segments from text")
        duration = time.time() - start_time
        self.logger.info(f"Parsed text in {duration:.2f}s")
        return segments
    
    def _clean_text(self, text: str) -> str:
        """Private helper method for text cleaning."""
        # remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        # remove leading and trailing whitespace
        text = text.strip()
        return text
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences, handling dialogue complexities."""
        return nltk.sent_tokenize(text)
    
    def _classify_sentence(self, sentence: str) -> TextSegment:
        """Classify a single sentence as dialogue, narrative, or action."""
        
        # Check for dialogue patterns first
        for pattern in DIALOGUE_PATTERNS:
            if re.search(pattern, sentence):
                # It's dialogue, now find the speaker
                speaker = self._extract_speaker(sentence)
                return TextSegment(
                    content=sentence,
                    segment_type="dialogue",
                    speaker=speaker,
                    confidence=0.8
                )
        
        # If no dialogue found, it's narrative
        return TextSegment(
            content=sentence,
            segment_type="narrative",
            confidence=0.9
        )

    def _extract_speaker(self, sentence: str) -> Optional[str]:
        """Extract speaker name from dialogue."""
        for pattern in SPEAKER_PATTERNS:
            match = re.search(pattern, sentence)
            if match:
                return match.group(1)
        return None 
    



