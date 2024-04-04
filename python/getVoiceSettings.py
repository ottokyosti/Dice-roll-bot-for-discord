from elevenlabs import VoiceSettings

def get_voice_settings(voice: str):
    if voice == "Roope" or voice == "Otto":
        voice_settings = VoiceSettings(
                stability = 0.3,
                similarity_boost = 0.9,
                style = 0.75,
                use_speaker_boost = True
            )
    elif voice == "Pappa" or voice == "Nipsu":
        voice_settings = VoiceSettings(
            stability = 0.5,
            similarity_boost = 0.9,
            style = 0.25,
            use_speaker_boost = True
        )
    else:
        voice_settings = None
    return voice_settings