# ts2mp4 使用方法

## 依赖环境
- 需要 Python 3.x
- 需要 ffmpeg.exe 及相关 .dll 文件（已包含在本目录）

## 使用步骤
1. 将所有 .ts 文件放入同一个文件夹（如：E:\...\0bc36iazqaabg4aj7d3dlrrkf4wdtdzadgca.f307110.hls_0_29）
2. 修改 ts2mp4.py 中的 `ts_dir` 路径为你的 ts 文件夹路径
3. 在命令行运行：

```bash
python ts2mp4.py
```

4. 程序会自动生成 local.m3u8 并用 ffmpeg 合成 output.mp4，输出文件在 ts 文件夹下

## 注意事项
- ts 文件需按原始顺序命名（如 0.ts、1.ts、2.ts...），否则顺序可能不对
- ffmpeg.exe 及 .dll 文件需与 ts2mp4.py 在同一目录
- 如有新 ts 文件，直接重新运行脚本即可

---
如有问题可随时反馈！
