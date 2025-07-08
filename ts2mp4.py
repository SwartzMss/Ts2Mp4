import os
import subprocess
import sys
import re

# ts 文件目录（请根据实际情况修改）
ts_dir = r"E:\efa29ee11eac761eef3b848200b932bb\0bc36iazqaabg4aj7d3dlrrkf4wdtdzadgca.f307110.hls\0bc36iazqaabg4aj7d3dlrrkf4wdtdzadgca.f307110.hls_0_29"
local_m3u8 = os.path.join(ts_dir, "local.m3u8")
output_mp4 = os.path.join(ts_dir, "output.mp4")

# ffmpeg.exe 路径（假设和脚本在同一目录）
ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg.exe")

def natural_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'([0-9]+)', s)]

# 自动生成本地 m3u8
print("正在生成本地 m3u8...")
ts_files = [f for f in os.listdir(ts_dir) if f.endswith('.ts')]
ts_files.sort(key=natural_key)

with open(local_m3u8, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write("#EXT-X-VERSION:3\n")
    f.write("#EXT-X-TARGETDURATION:10\n")
    f.write("#EXT-X-MEDIA-SEQUENCE:0\n")
    for ts in ts_files:
        f.write("#EXTINF:10.000,\n")
        f.write(f"{ts}\n")
    f.write("#EXT-X-ENDLIST\n")
print(f"本地 m3u8 文件已生成：{local_m3u8}")

# 合成 mp4
cmd = [
    ffmpeg_path,
    "-allowed_extensions", "ALL",
    "-protocol_whitelist", "file,http,https,tcp,tls",
    "-y",  # 自动覆盖输出
    "-i", local_m3u8,
    "-c:v", "libx264",
    "-c:a", "aac",
    output_mp4
]
subprocess.run(cmd, check=True)

print(f"转换完成，输出文件：{output_mp4}") 