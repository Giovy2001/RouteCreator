import vercel_blob
from PIL import Image, ImageFile, ImageOps
from io import BytesIO

MAX_WIDTH: int = 1080

def init_glob_database() -> None:
    pass

def put(image_name: str, image_data):
    # Importa immagine per la conversione
    img: ImageFile = Image.open(BytesIO(image_data))
    
    # Applica la rotazione corretta dai metadati EXIF
    img = ImageOps.exif_transpose(img)

    # Rimuove eventuale trasparenza immagine
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Ridimensiona immagini di gradi dimensioni
    width, height = img.size
    if width > MAX_WIDTH:
        new_height = int((MAX_WIDTH / width) * height)
        img = img.resize((MAX_WIDTH, new_height), Image.LANCZOS)

    # Salva l'immagine in un buffer
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=85, optimize=True)
    image_bytes = buffer.getvalue()

    # Commit nel vercel blob database
    return vercel_blob.put(f"{image_name}.jpg", image_bytes, {"addRandomSuffix": "true"}).get("url")