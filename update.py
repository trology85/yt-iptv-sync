import json
import subprocess

try:
    with open("channels.json", "r", encoding="utf-8") as f:
        channels = json.load(f)
except Exception:
    channels = []

m3u_content = "#EXTM3U\n"

for ch in channels:
    try:
        # YouTube bot korumasını aşmak için Android istemci parametresi eklendi
        result = subprocess.run(
            [
                "yt-dlp",
                "--extractor-args", "youtube:player_client=android",
                "-g",
                ch["url"]
            ],
            capture_output=True,
            text=True,
            check=True
        )
        m3u8_link = result.stdout.strip().split("\n")[0]
        
        m3u_content += f'#EXTINF:-1 tvg-name="{ch["name"]}" group-title="YouTube Canlı Filmler", {ch["name"]}\n'
        m3u_content += f"{m3u8_link}\n"
        print(f"{ch['name']} başarıyla çözüldü.")
        
    except subprocess.CalledProcessError as e:
        print(f"--- HATA: {ch['name']} çözülemedi ---")
        print(f"STDERR Çıktısı:\n{e.stderr}")
    except Exception as e:
        print(f"{ch['name']} için beklenmeyen hata: {e}")

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("M3U dosyası güncellendi.")
