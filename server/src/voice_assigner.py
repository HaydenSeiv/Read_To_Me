from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from enum import Enum
import re
from .parser import TextSegment
import json
import os

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"

class Age(Enum):
    CHILD = "child"
    YOUNG = "young"
    ADULT = "adult"
    ELDERLY = "elderly"

class Accent(Enum):
    AMERICAN = "american"
    BRITISH = "british"
    NEUTRAL = "neutral"

@dataclass
class VoiceCharacteristics:
    gender: Gender = Gender.NEUTRAL
    age: Age = Age.ADULT
    accent: Accent = Accent.NEUTRAL
    custom_attributes: Dict[str, str] = field(default_factory=dict)
    

@dataclass
class VoiceProfile:
    """Voice profile for a character."""
    voice_id: str
    name: str
    characteristics: VoiceCharacteristics
    is_available: bool = True
    assigned_to: Optional[str] = None
    
    def __post_init__(self):
    
        if not self.voice_id:
            raise ValueError("voice_id cannot be empty")
        
        if not self.name:
            raise ValueError("name cannot be empty")
        
        if self.assigned_to and self.is_available:  
            self.is_available = False
            
                # Length validation
        if len(self.name) > 50: 
            raise ValueError(f"name too long: {len(self.name)} characters (max 50)")

        # Character validation
        if not re.match(r'^[a-zA-Z0-9\s_-]+$', self.name):
            raise ValueError(f"name '{self.name}' contains invalid characters")
        
        
        if self.assigned_to is not None:
            if not self.assigned_to.strip():  # empty or whitespace-only
                raise ValueError("assigned_to cannot be empty string")
            if len(self.assigned_to) > 50:  
                raise ValueError(f"Character name too long: {len(self.assigned_to)}")        
            
            
@dataclass 
class VoiceSegment:
    """A text segment with assigned voice information."""
    text_segment: TextSegment  # Original parser output
    voice_profile: VoiceProfile  # Assigned voice
    
    def get_synthesizer_params(self) -> Dict[str, str]:
        """Get the minimal parameters needed for synthesis."""
        return {
            "text": self.text_segment.content,
            "voice_type": self.voice_profile.voice_id  # Map voice_id to voice_type
        }
    
    
    def get_Voice_info(self) -> Dict[str, Any]:
        """Get parameters for the synthesizer."""
        return {
            "text": self.text_segment.content,
            "voice_id": self.voice_profile.voice_id,
            "voice_name": self.voice_profile.name,
            "speaker": self.voice_profile.assigned_to,
            "confidence": self.text_segment.confidence,
            "segment_type": self.text_segment.segment_type,
            "voice_characteristics": self.voice_profile.characteristics
        }
    
    def get_voice_id(self) -> str:
        """Get the voice ID for the synthesizer."""
        return self.voice_profile.voice_id
    
    def get_voice_name(self) -> str:
        """Get the voice name for the synthesizer."""
        return self.voice_profile.name
    
    def get_type(self) -> str:
        """Get the type of the segment."""
        return self.text_segment.segment_type
    
    def is_dialogue(self) -> bool:
        """Check if this is a dialogue segment."""
        return self.text_segment.segment_type == "dialogue"

    def is_narrative(self) -> bool:
        """Check if this is a narrative segment."""
        return self.text_segment.segment_type == "narrative"

    def get_speaker(self) -> Optional[str]:
        """Get the speaker name if this is dialogue."""
        return self.text_segment.speaker
    
class VoiceAssigner:
    def __init__(self, config_file: str = "server/voices/voice_config.json", 
                 development_mode: bool = True):
        self.development_mode = development_mode
        self.voice_pool = self._load_voice_pool(config_file)
        self.character_assignments = {}  # character_name -> voice_id
        self.persistence_file = "server/voices/voice_assignments.json"
        self._load_assignments()
    
    def _load_voice_pool(self, config_file: str) -> List[VoiceProfile]:
        with open(config_file, "r") as f:
            return [VoiceProfile(**voice) for voice in json.load(f)["voices"]]
    
    def _load_assignments(self) -> None:
        if os.path.exists(self.persistence_file):
            with open(self.persistence_file, "r") as f:
                self.character_assignments = json.load(f)
    
    def assign_voices(self, text_segments: List[TextSegment]) -> List[VoiceSegment]:
        # Main method: convert TextSegments to VoiceSegments
        voice_segments = []
        for segment in text_segments:
            voice_profile = self._assign_character_voice(segment.speaker)
            voice_segments.append(VoiceSegment(segment, voice_profile))
        return voice_segments
    
    def _assign_character_voice(self, character_name: str) -> VoiceProfile:
        # Assign voice to a character (with consistency)
        if character_name in self.character_assignments:
            return self.voice_pool[self.character_assignments[character_name]]
        else:
            return self._get_narrator_voice()
    
    def _get_narrator_voice(self) -> VoiceProfile:
        # Get voice for narrative segments
        for voice in self.voice_pool:
            if voice.role == "narrator":
                return voice
        return self.voice_pool[0]
    
    def save_assignments(self) -> None:
        # Persist current assignments
        with open(self.persistence_file, "w") as f:
            json.dump(self.character_assignments, f)
    
    def load_assignments(self) -> None:
        # Load previous assignments
        with open(self.persistence_file, "r") as f:
            self.character_assignments = json.load(f)
