#%%
import os
import argparse
from pydub import AudioSegment
import math

def get_file_size_mb(file_path):
    """获取文件大小（MB）"""
    return os.path.getsize(file_path) / (1024 * 1024)

def get_format(ext):
    """根据文件扩展名获取正确的格式名称"""
    format_map = {
        '.mp3': 'mp3',
        '.wav': 'wav',
        '.flac': 'flac',
        '.ogg': 'ogg',
        '.aac': 'aac',
        '.m4a': 'ipod',  # 对于m4a文件使用ipod格式
        '.wma': 'wma',
    }
    ext = ext.lower()
    return format_map.get(ext, ext.replace('.', ''))

def split_audio(input_file, output_dir, max_size_mb=25, max_duration_sec=1500):
    """
    分割音频文件
    
    参数:
    - input_file: 输入音频文件路径
    - output_dir: 输出目录
    - max_size_mb: 最大文件大小（MB）
    - max_duration_sec: 最大时长（秒）
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 获取文件大小和文件名
    file_size_mb = get_file_size_mb(input_file)
    file_name = os.path.basename(input_file)
    name, ext = os.path.splitext(file_name)
    
    # 获取正确的格式名称
    audio_format = get_format(ext)
    
    # 加载音频文件
    print(f"正在加载音频文件: {input_file}")
    try:
        audio = AudioSegment.from_file(input_file)
    except Exception as e:
        print(f"加载音频文件时出错: {e}")
        print("请确保安装了ffmpeg并且文件格式正确")
        return
    
    # 获取时长（秒）
    duration_sec = len(audio) / 1000
    
    # 判断是否需要分割
    if file_size_mb <= max_size_mb and duration_sec <= max_duration_sec:
        print(f"文件大小（{file_size_mb:.2f}MB）和时长（{duration_sec:.2f}秒）均在限制范围内，无需分割。")
        return
    
    # 根据大小和时长计算需要分割的段数
    segments_by_size = math.ceil(file_size_mb / max_size_mb)
    segments_by_duration = math.ceil(duration_sec / max_duration_sec)
    segments = max(segments_by_size, segments_by_duration)
    
    print(f"音频文件大小: {file_size_mb:.2f}MB, 时长: {duration_sec:.2f}秒")
    print(f"需要分割成 {segments} 个部分")
    
    # 计算每段的时长（毫秒）
    segment_duration_ms = len(audio) // segments
    
    # 分割并保存
    for i in range(segments):
        start_ms = i * segment_duration_ms
        end_ms = min((i + 1) * segment_duration_ms, len(audio))
        
        segment = audio[start_ms:end_ms]
        output_file = os.path.join(output_dir, f"{name}_part{i+1}{ext}")
        
        print(f"正在导出第 {i+1}/{segments} 部分到 {output_file}")
        
        try:
            # 尝试导出文件，使用正确的格式
            segment.export(output_file, format=audio_format)
        except Exception as e:
            print(f"导出文件 {output_file} 时出错: {e}")
            # 尝试使用默认的 mp3 格式作为备选
            try:
                mp3_output_file = output_file.rsplit('.', 1)[0] + '.mp3'
                print(f"尝试以 MP3 格式导出到 {mp3_output_file}")
                segment.export(mp3_output_file, format="mp3")
                print(f"成功导出为 MP3 格式")
            except Exception as e2:
                print(f"导出为 MP3 格式也失败: {e2}")
                continue
        
    print(f"分割完成！共生成 {segments} 个文件，保存在 {output_dir}")

if __name__ == "__main__":
    input_file='./0_raw_audio/hype 交接1.m4a'
    output_dir='./0_processed_audio'
    max_size=25
    max_duration=1500
    split_audio(input_file, output_dir, max_size, max_duration)