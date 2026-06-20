from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav) # Fixed typo: embed_utteranace -> embed_utterance
        return embedding.tolist()
    except Exception as e:
        st.error(f'Voice recog error: {e}')
        return None 
    
def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    if new_embedding is None or not candidates_dict:
        return None, 0.0
    
    best_sid = None
    best_score = -1.0
    
    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            similiarity = np.dot(new_embedding, stored_embedding)
            if similiarity > best_score:
                best_score = similiarity
                best_sid = sid
                
    if best_score >= threshold:
        return best_sid, best_score
    return None, 0.0

# 1. FIXED: Changed from 'if' to 'def' and out-dented to make it importable
def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    try:
        encoder = load_voice_encoder()
        
        # 2. FIXED: Changed librosa(...) to librosa.load(...)
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)
        
        # 3. FIXED: Initialized the dictionary properly
        identified_results = {}
        
        for start, end in segments:
            if (end - start) < sr * 0.5:
                continue
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)    
            
            sid, score = identify_speaker(embedding, candidates_dict, threshold)
            
            # 4. FIXED: Corrected dictionary lookup logic and typo names
            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score
                    
        return identified_results
    except Exception as e:
        st.error(f'bulk process error: {e}')
        return {}