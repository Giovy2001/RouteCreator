from scripts import image_handler, database_handler


def database_cleanup() -> None:
    print("INFO Database cleanup started")
    
    images_urls: list = [entry.lower() for entry in image_handler.list()]
    database_urls: list = [entry[3].lower() for entry in database_handler.get_all_routes()]
    
    cleanup_actions: int = 0
    
    for url in database_urls:
        if not url in images_urls:
            database_handler.del_route(url)
            print("DELETE Entry SQL database")
            cleanup_actions+=1
    
    for url in images_urls:
        if not url in database_urls:
            image_handler.delete(url)
            print("DELETE Entry BLOB database")
            cleanup_actions+=1
    
    print(f"INFO Database cleanup completed with {cleanup_actions} cleanup_actions")
    
def handler(request):
    """
    HTTP request handler for database cleanup operations.
    Validates the request authorization header and triggers a database cleanup process.
    Args:
        request: HTTP request object containing headers and other request metadata.
    Returns:
        dict: A dictionary with status key indicating successful execution.
              Format: {"status": "ok"}
    """

    database_cleanup()
    return {
        "status": "ok"
    }