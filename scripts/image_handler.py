import vercel_blob


def put(image_name, image_data):
    return vercel_blob.put(f"{image_name}.jpg", image_data, {"addRandomSuffix": "true"}).get("url")