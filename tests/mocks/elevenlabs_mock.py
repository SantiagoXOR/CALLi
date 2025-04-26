from unittest.mock import MagicMock

class MockVoiceSettings:
    def __init__(self, stability=0.7, similarity_boost=0.75):
        self.stability = stability
        self.similarity_boost = similarity_boost

class MockConversation:
    def __init__(self, voice="Bella", voice_settings=None):
        self.voice = voice
        self.voice_settings = voice_settings or MockVoiceSettings()

    def generate(self, text):
        return b"mock_audio_data"

# Mock para las funciones principales de elevenlabs
generate = MagicMock(return_value=b"mock_audio_data")
set_api_key = MagicMock()
Voice = MagicMock()
VoiceSettings = MockVoiceSettings
Conversation = MockConversation
