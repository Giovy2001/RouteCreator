import vercel_blob
from uuid import uuid4
from PIL import Image, ImageOps
from io import BytesIO

def init_glob_database() -> None:
    """
    Initialize the vercel glob database and set the upload function name.
    """
    global upload_function_name
    upload_function_name = "blob"

def init_local_database() -> None:
    """
    Initialize the local database and set the upload function name.
    """
    global upload_function_name
    upload_function_name = "local"

def put(image_full_name: str, image_data) -> str:
    """
    Processes the image to optimize it and commit it to the initialized database.
    It supports deletion from two storage backends:
    - 'blob': Deletes from Vercel Blob storage
    - 'local': Deletes from the local filesystem

    Args:
        image_full_name (str): Name of the image
        image_data (_type_): Image data retrived from the html request

    Returns:
        str: url to the image in the database
    """
    
    # Raise an error when  the ImageHandler is not initialized properly
    if upload_function_name == "":
        raise Exception("ERROR ImageHandler not initialized")
    
    image_name: str = image_full_name.split(".")[0]
    image_name = "_".join(image_name.split(" "))
    MAX_WIDTH: int = 1080
    
    # Import image and metadatas
    img: Image.Image = Image.open(BytesIO(image_data))
    img = ImageOps.exif_transpose(img)

    # Remove transparancy if needed
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    # Scale the image to fit the given MAX_WIDTH
    cropped_img: Image.Image = crop(img)
    width, height = cropped_img.size
    if width > MAX_WIDTH:
        new_height = int((MAX_WIDTH / width) * height)
        cropped_img = cropped_img.resize((MAX_WIDTH, new_height), Image.LANCZOS)

    # Returns the result of the commit function
    return UPLOAD_FUNCTIONS[upload_function_name](image_name, cropped_img)

def list() -> list:
    """
    Retrieve a list of URLs from the configured storage backend.
    Dynamically fetches URLs based on the `upload_function_name` configuration:
    - "blob": Retrieves URLs from Vercel Blob storage
    - "local": Retrieves file paths from local storage directory
    
    Returns:
        list: A list of URLs or file paths from the storage backend.
    Note:
        The actual storage backend used is determined by the `upload_function_name`
        variable, which must be set in the calling scope.
    """
    
    match upload_function_name:
        case "blob":
            urls = [i["url"] for i in vercel_blob.list()["blobs"]]
        case "local":
            from glob import glob
            urls = glob(r"static\local_database\Images\*")
      
    return urls
        
def delete(image_url: str) -> None:
    """
    Delete an image from the specified storage service.
    This function removes an image based on the configured upload function.
    It supports deletion from two storage backends:
    - 'blob': Deletes from Vercel Blob storage
    - 'local': Deletes from the local filesystem
    
    Args:
        image_url (str): The URL or path of the image to delete.
                        For blob storage: the blob URL or identifier.
                        For local storage: the file path to the image.
    Returns:
        None
    Raises:
        FileNotFoundError: If the local file does not exist (local storage only).
        Exception: If deletion from Vercel Blob fails (blob storage only).
    Note:
        The actual storage backend used is determined by the `upload_function_name`
        variable, which must be set in the calling scope.
    """
    
    match upload_function_name:
        case "blob":
            vercel_blob.delete(image_url)
        case "local":
            from os import remove
            remove(image_url)

def local_commit(image_name: str, img: Image.Image) -> str:
    """
    Commit the image to the local database and returns its path.

    Args:
        image_name (str): Name of the image
        img (Image.Image): PIL image type

    Returns:
        str: path of the image relative to the webapp
    """
    
    path: str = f"static\\local_database\\images\\{image_name}_{uuid4()}.jpg"
    img.save(path)
    return path

def blob_commit(image_name: str, img: Image.Image) -> str:
    """
    Commit the image to the vercel blob database and returns its url.

    Args:
        image_name (str): Name of the image
        img (Image.Image): PIL image type

    Returns:
        str: url of the image in the database
    """
    
    # Salva l'immagine in un buffer
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=85, optimize=True)
    image_bytes = buffer.getvalue()
    
    # Commit to the vercel blob database
    return vercel_blob.put(f"{image_name}.jpg", image_bytes, {"addRandomSuffix": "true"}).get("url")

def crop(img: Image.Image) -> Image.Image:
    """
    Crop an image to a 2:3 (width:height) vertical aspect ratio.
    Maintains the center of the original image while removing excess width or height
    as needed to achieve the target aspect ratio.
    Args:
        img (Image.Image): The PIL Image object to crop.
    Returns:
        Image.Image: A new Image object cropped to 2:3 aspect ratio.
    """
    
    W, H = img.size    
    target_ratio = 7 / 10
    current_ratio = W / H

    if current_ratio > target_ratio:
        new_W = int(H * target_ratio)
        new_H = H
    else:
        new_W = W
        new_H = int(W / target_ratio)

    left = (W - new_W) // 2
    top = (H - new_H) // 2
    right = left + new_W
    bottom = top + new_H

    return img.crop((left, top, right, bottom))

""" Dictionary containg all the functions used to commit changes to the databases """
UPLOAD_FUNCTIONS: dict = {"blob":blob_commit, "local":local_commit}
upload_function_name: str = ""