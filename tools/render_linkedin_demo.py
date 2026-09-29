from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from io import BytesIO
from pathlib import Path
import subprocess, imageio_ffmpeg

OUT = Path("media")
OUT.mkdir(parents=True, exist_ok=True)
VIDEO = OUT / "Krontinuum_Atlas_v2_LinkedIn_Demo_v085.mp4"
THUMB = OUT / "Krontinuum_Atlas_v2_LinkedIn_Thumbnail.jpg"
URL = "https://krontinuum-atlas-v2-production.up.railway.app/"
W, H, FPS = 1080, 1350, 15
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font_bold = ImageFont.truetype(FONT_BOLD, 52)
font_body = ImageFont.truetype(FONT_REG, 30)
font_small = ImageFont.truetype(FONT_REG, 23)
font_micro = ImageFont.truetype(FONT_REG, 18)

def wrap(draw, text, font, max_width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            cur = trial
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return "\n".join(lines)

def caption(img, kicker, headline, body=""):
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((60, 1000, 1020, 1270), 28, fill=(4, 8, 17, 226), outline=(255,255,255,36), width=2)
    d.text((92, 1025), kicker.upper(), font=font_small, fill=(130, 216, 240, 255))
    htxt = wrap(d, headline, font_bold, 845)
    d.multiline_text((92, 1063), htxt, font=font_bold, fill=(250,252,255,255), spacing=6)
    if body:
        hb = d.multiline_textbbox((0,0), htxt, font=font_bold, spacing=6)
        yy = 1063 + (hb[3]-hb[1]) + 16
        d.multiline_text((92, yy), wrap(d, body, font_body, 845), font=font_body, fill=(210,219,232,255), spacing=5)
    d.text((650, 82), "RAQS / KRONTINUUM  ·  ATLAS v2", font=font_micro, fill=(236,242,250,225))
    return img.convert("RGB")

def outro(base):
    im = ImageEnhance.Brightness(base.convert("RGB")).enhance(0.20).convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0,0,W,H), fill=(3,7,15,160))
    d.text((80, 120), "TRY THE ATLAS", font=font_bold, fill="white")
    d.text((80, 200), "Public source · noncommercial · attribution required", font=font_body, fill=(145,220,240))
    items = [
        ("LIVE ATLAS", "krontinuum-atlas-v2-production.up.railway.app"),
        ("GITHUB", "github.com/allenkearon-cyber/krontinuum-atlas-v2"),
        ("FROZEN EVIDENCE", "doi.org/10.5281/zenodo.23042784"),
    ]
    y = 350
    for label, value in items:
        d.text((80, y), label, font=font_small, fill=(155,170,192))
        d.multiline_text((80, y+40), wrap(d, value, font_body, 900), font=font_body, fill="white", spacing=4)
        y += 175
    d.rounded_rectangle((80, 1000, 1000, 1210), 26, fill=(255,255,255,20), outline=(255,255,255,45), width=2)
    d.text((110, 1035), "Explore the interface. Then follow the evidence.", font=font_body, fill="white")
    d.multiline_text((110,1095), wrap(d, "The Atlas is a demonstrator; the frozen Zenodo record is the evidentiary source.", font_small, 820), font=font_small, fill=(207,216,230), spacing=5)
    return im.convert("RGB")

cmd = [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
       "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
       "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(VIDEO)]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def push(im):
    proc.stdin.write(im.convert("RGB").tobytes())

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    page.goto(URL, wait_until="networkidle", timeout=60000)
    page.wait_for_selector("#sceneButtons button", timeout=30000)

    def shot():
        return Image.open(BytesIO(page.screenshot(type="jpeg", quality=90))).convert("RGB")

    def scene(seconds, button, kicker, title, body):
        page.get_by_role("button", name=button).click()
        page.wait_for_timeout(400)
        frame = caption(shot(), kicker, title, body)
        for _ in range(int(seconds * FPS)):
            push(frame)

    scene(3.0, "Dimensional emergence", "PUBLIC DEMO",
          "What if geometry is not the starting point?",
          "Explore a live atlas of structural coordinates, transport and collapse residue.")
    scene(3.2, "Discovered structural dimensions", "01 · DIMENSIONS",
          "Objects can differ along structural coordinates ordinary space does not record.",
          "The Atlas makes those dimensions explorable.")
    scene(3.2, "Hidden scaffold", "02 · CONSTRUCTION",
          "A finished object may not contain the support required to build it.",
          "Hidden scaffold is measured during construction.")
    scene(3.2, "Projective accessibility", "03 · ACCESSIBILITY",
          "Realized and forbidden directions both shape the geometry.",
          "Absence is rendered as structure.")
    scene(3.2, "Closure arrow", "04 · CLOSURE",
          "Generative dependence has direction.",
          "Closure reveals precedence rather than ordinary linear span.")
    scene(3.2, "Transport and holonomy", "05 · TRANSPORT",
          "A loop can return a changed state.",
          "Holonomy makes transport residue visible.")
    scene(3.2, "Collapse residue", "06 · COLLAPSE",
          "The order of collapse operations can leave a measurable residue.",
          "The commutator becomes something you can see.")
    scene(3.2, "CUF tier shedding", "07 · CUF",
          "Exact invariance can fail by losing an observable tier.",
          "The surviving tiers can remain coherent.")

    final = outro(shot())
    for _ in range(int(4.8 * FPS)):
        push(final)

    page.get_by_role("button", name="Dimensional emergence").click()
    page.wait_for_timeout(300)
    thumb = caption(shot(), "INTERACTIVE RESEARCH DEMO",
                    "Can geometry emerge from deeper structure?",
                    "Krontinuum Atlas v2 · public source + frozen evidence")
    thumb.save(THUMB, quality=94)
    browser.close()

proc.stdin.close()
err = proc.stderr.read().decode("utf-8", errors="ignore")
rc = proc.wait()
if rc:
    raise SystemExit(err[-4000:])
print(VIDEO)
print(THUMB)
