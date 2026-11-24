
import os
import subprocess
import imageio_ffmpeg
import edge_tts
import asyncio
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(BASE, "audio", "astrixeno_voice.mp3")
OUTPUT = os.path.join(BASE, "output", "astrixeno_first_short.mp4")

SCRIPT = [
    ("THE FUTURE IS HERE", "Artificial intelligence is changing our world."),
    ("WORK SMARTER", "AI tools can help you create, learn and grow faster."),
    ("A NEW OPPORTUNITY", "But the biggest advantage belongs to those who take action."),
    ("WELCOME TO ASTRIXENO", "Follow for more technology and AI discoveries.")
]

VOICE = "en-US-GuyNeural"
WIDTH, HEIGHT = 1080, 1920
DURATION_PER_SCENE = 5

def font(size):
    paths = [
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\arial.ttf"
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

async def make_voice():
    text = " ".join(title + ". " + subtitle for title, subtitle in SCRIPT)
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(AUDIO)

def make_scene(title, subtitle, number):
    image = Image.new("RGB", (WIDTH, HEIGHT), (12, 18, 42))
    draw = ImageDraw.Draw(image)

    # Background design
    for y in range(HEIGHT):
        shade = int(15 + 30 * y / HEIGHT)
        draw.line((0, y, WIDTH, y), fill=(8, shade, 55))

    # Decorative circles
    draw.ellipse((750, 150, 1200, 600), outline=(30, 130, 230), width=8)
    draw.ellipse((-180, 1300, 350, 1830), outline=(30, 130, 230), width=8)

    draw.text((WIDTH//2, 260), "ASTRIXENO", font=font(52),
              fill=(100, 200, 255), anchor="mm")

    draw.text((WIDTH//2, 790), title, font=font(76),
              fill="white", anchor="mm", align="center",
              stroke_width=2, stroke_fill=(0, 70, 150))

    draw.text((WIDTH//2, 1050), subtitle, font=font(42),
              fill=(210, 225, 255), anchor="mm",
              align="center", spacing=18)

    draw.text((WIDTH//2, 1690), "FOLLOW FOR MORE", font=font(42),
              fill=(100, 200, 255), anchor="mm")

    draw.text((WIDTH//2, 1800), f"{number}/4", font=font(30),
              fill="white", anchor="mm")

    return image

def main():
    os.makedirs(os.path.dirname(AUDIO), exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    print("ASTRIXENO: Generating English voice...")
    asyncio.run(make_voice())

    print("ASTRIXENO: Creating scenes...")
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    scene_files = []

    for i, (title, subtitle) in enumerate(SCRIPT, 1):
        path = os.path.join(BASE, "assets", f"scene_{i}.png")
        make_scene(title, subtitle, i).save(path)
        scene_files.append(path)

    concat_file = os.path.join(BASE, "assets", "scenes.txt")
    with open(concat_file, "w", encoding="utf-8") as f:
        for path in scene_files:
            f.write(f"file '{path.replace(chr(92), '/')}'\n")
            f.write(f"duration {DURATION_PER_SCENE}\n")
        f.write(f"file '{scene_files[-1].replace(chr(92), '/')}'\n")

    silent_video = os.path.join(BASE, "assets", "silent.mp4")

    print("ASTRIXENO: Building video...")
    subprocess.run([
        ffmpeg, "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file, "-vf", "scale=1080:1920,fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        silent_video
    ], check=True)

    print("ASTRIXENO: Adding voice...")
    subprocess.run([
        ffmpeg, "-y", "-i", silent_video, "-i", AUDIO,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac",
        "-shortest", "-movflags", "+faststart", OUTPUT
    ], check=True)

    print("\nSUCCESS! ASTRIXENO SHORT CREATED")
    print("Video:", OUTPUT)

if __name__ == "__main__":
    main()
