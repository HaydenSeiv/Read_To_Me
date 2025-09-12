"""
Text-to-Speech synthesizer module for ReadToMe audiobook generator.

This module handles all TTS operations using CoquiTTS with GPU acceleration.
Supports both fast development models and high-quality production models.
"""

import torch
from TTS.api import TTS
import os
from pathlib import Path
from typing import Dict, Optional
from .utils import setup_logging, get_logger, log_tts_operation
import time
import logging



class AdaptiveSynthesizer:
    """
    Adaptive TTS synthesizer that switches between fast and quality models.
    
    Attributes:
        development_mode (bool): If True, uses fast model for rapid iteration
        tts (TTS): The active TTS model instance
        voice_mapping (Dict[str, str]): Maps character types to voice IDs
    """
    
    def __init__(self, development_mode: bool = True):
        self.development_mode = development_mode  
        self.logger = get_logger(__name__)        
        self.logger.info(f"Initializing synthesizer in {'development' if development_mode else 'production'} mode")
        
        if development_mode:
            setup_logging(logging.DEBUG,True)
            # Fast model for development
            self.tts = TTS("tts_models/en/ljspeech/fast_pitch")
            self.voice_mapping = {"default": "default"}
        else:
            setup_logging(logging.INFO,True)
            # High-quality model for production
            self.tts = TTS("tts_models/en/vctk/vits")
            self.voice_mapping = {
                "narrator": "p225",
                "character_1": "p226", 
                "character_2": "p227",
                # ... more character voices
            }
        # Move to GPU if available
        if torch.cuda.is_available():
            self.tts.to("cuda")
    
    
    
    def synthesize(self, text: str, voice_type: str = "narrator") -> str:
        """
        Generate audio from text using appropriate voice.
        
        Args:
            text: The text to synthesize
            voice_type: Type of voice (narrator, character_1, etc.)
            
        Returns:
            str: Path to generated audio file
        """
        start_time = time.time()
        voice_id = voice_type
        
        # Get project root relative to this file
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        self.audio_output_dir = Path(project_root) / "server" / "audio_output"
        output_path = self.audio_output_dir / f"{voice_type}_{hash(text)}.wav"
        
        if self.development_mode:
            self.tts.tts_to_file(text=text, file_path=output_path)
        else:
            self.tts.tts_to_file(text=text, speaker=voice_id, file_path=output_path)
            
        duration = time.time() - start_time
        log_tts_operation("voice_synthesis", duration, voice_type=voice_type, text_length=len(text))
        
        return output_path
    
    
    def switch_mode(self, development_mode: bool) -> None:
        """Switch between development and production models."""
        self.development_mode = development_mode
        if development_mode:
            self.tts = TTS("tts_models/en/ljspeech/fast_pitch")
        else:
            self.tts = TTS("tts_models/en/vctk/vits")
    
    
    def get_available_voices(self) -> Dict[str, str]:
        """Return available voice mappings."""
        return self.voice_mapping
    
    
    
    
    
    
    
    