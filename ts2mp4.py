import os, subprocess, sys, re, math

# ts 文件目录
ts_dir = r"C:\N-20N3PF2E83B6-Data\yuefshi\Downloads\0bc3tqai4aaaieait53crzrkhhgdr2oabdsa.f306110.hls\0bc3tqai4aaaieait53crzrkhhgdr2oabdsa.f306110.hls_0_29"
local_m3u8 = os.path.join(ts_dir, "local.m3u8")
output_mp4 = os.path.join(ts_dir, "output.mp4")

# ffmpeg / ffprobe 可执行文件
BIN_DIR = os.path.join(os.path.dirname(__file__), "ffmpeg")
FFMPEG_PATH  = os.path.join(BIN_DIR, "ffmpeg.exe")
FFPROBE_PATH = os.path.join(BIN_DIR, "ffprobe.exe")

def natural_key(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

def get_duration(ts_path: str) -> float:
    out = subprocess.check_output(
        [FFPROBE_PATH, "-v", "error",
         "-show_entries", "format=duration",
         "-of", "default=nokey=1:noprint_wrappers=1",
         ts_path],
        encoding="utf-8"
    )
    return float(out.strip())

# 1. 收集 ts
ts_files = sorted(
    [f for f in os.listdir(ts_dir) if f.endswith(".ts")],
    key=natural_key
)
if not ts_files:
    sys.exit("❌ 目录下没找到 ts 文件")

# 2. 生成带真实时长的 m3u8
durations = [get_duration(os.path.join(ts_dir, ts)) for ts in ts_files]
target_duration = math.ceil(max(durations))

with open(local_m3u8, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n#EXT-X-VERSION:3\n")
    f.write(f"#EXT-X-TARGETDURATION:{target_duration}\n")
    f.write("#EXT-X-PLAYLIST-TYPE:VOD\n#EXT-X-MEDIA-SEQUENCE:0\n")
    for ts, dur in zip(ts_files, durations):
        f.write(f"#EXTINF:{dur:.3f},\n{ts}\n")
    f.write("#EXT-X-ENDLIST\n")
print("✅ 已生成本地 m3u8：", local_m3u8)

# 3. 纯流拷贝无损合并为 MP4
cmd = [
    FFMPEG_PATH,
    # 让 demuxer 肯往后探
    "-probesize", "100M",
    "-analyzeduration", "30M",
    "-allowed_extensions", "ALL",
    "-protocol_whitelist", "file,http,https,tcp,tls",
    "-y",
    "-i", local_m3u8,
    # 不重编码，先确认时长
    "-c", "copy",
    # 遇到第一组 SPS/PPS 就塞进 header
    "-bsf:v", "dump_extra",
    "-movflags", "+faststart",
    output_mp4
]
subprocess.run(cmd, check=True)

print(f"转换完成，输出文件：{output_mp4}") 
