# 사용법
# python TIMIT_prep.py --input_path ./raw_dataset/TIMIT/data/TRAIN/ --output_path ./raw_dataset/TIMIT/output

import os
import random
import argparse
from pydub import AudioSegment
import numpy as np

# 오디오 공백 제거 함수
def remove_silence(audio, silence_threshold=-40.0, chunk_size=10, buffer_ms=200):
    trimmed_audio = audio
    start_trim = detect_leading_silence(trimmed_audio, silence_threshold, chunk_size)
    end_trim = detect_leading_silence(trimmed_audio.reverse(), silence_threshold, chunk_size)
    duration = len(trimmed_audio)
    
    # 공백 길이를 남기기 위해 buffer_ms 추가
    start_trim = max(0, start_trim - buffer_ms)
    end_trim = max(0, end_trim - buffer_ms)
    
    return trimmed_audio[start_trim:duration - end_trim]


def detect_leading_silence(sound, silence_threshold=-40.0, chunk_size=10):
    trim_ms = 0
    while trim_ms < len(sound):
        if sound[trim_ms:trim_ms + chunk_size].dBFS > silence_threshold:
            return trim_ms
        trim_ms += chunk_size
    return trim_ms

# 오디오 파일 정규화 함수
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

# 폴더 내 오디오 처리 함수
def process_speaker_audios(speaker_path, speaker_name, output_folder, inter_file_silence_ms=100):
    audio_files = [f for f in os.listdir(speaker_path) if f.endswith(('.mp3', '.wav', '.flac', '.ogg'))]
    
    if len(audio_files) < 5:
        print(f"{speaker_name}의 오디오 파일이 부족합니다. 파일 개수: {len(audio_files)}")
        return
    
    selected_files = random.sample(audio_files, 5)
    
    combined_audio = AudioSegment.empty()
    for i, file in enumerate(selected_files):
        audio_path = os.path.join(speaker_path, file)
        audio = AudioSegment.from_file(audio_path)
        audio = remove_silence(audio)
        combined_audio += audio

        # 마지막 파일이 아닌 경우 지정한 길이의 공백 추가
        if i < len(selected_files) - 1:
            silence = AudioSegment.silent(duration=inter_file_silence_ms)
            combined_audio += silence

    combined_audio = combined_audio[:5000] if len(combined_audio) > 5000 else combined_audio
    combined_audio = match_target_amplitude(combined_audio, -20.0)

    output_path = os.path.join(output_folder, f"{speaker_name}_normalized.wav")
    combined_audio.export(output_path, format="wav")
    print(f"{speaker_name}의 정규화된 파일이 생성되었습니다: {output_path}")

# 전체 데이터셋을 처리
def process_all_speakers(input_folder, output_folder):
    for region in os.listdir(input_folder):
        region_path = os.path.join(input_folder, region)
        if os.path.isdir(region_path):
            for speaker in os.listdir(region_path):
                speaker_path = os.path.join(region_path, speaker)
                if os.path.isdir(speaker_path):
                    process_speaker_audios(speaker_path, speaker, output_folder)

# 메인 함수
def main():
    parser = argparse.ArgumentParser(description="Process audio files for normalization")
    parser.add_argument("--input_path", required=True, help="Input folder path containing audio data")
    parser.add_argument("--output_path", required=True, help="Output folder path to save normalized audio files")
    
    args = parser.parse_args()

    input_folder = args.input_path
    output_folder = args.output_path

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_all_speakers(input_folder, output_folder)

if __name__ == "__main__":
    main()
