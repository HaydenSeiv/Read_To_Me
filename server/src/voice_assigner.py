from dataclasses import dataclass
from typing import Optional, Dict, List
from enum import Enum

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