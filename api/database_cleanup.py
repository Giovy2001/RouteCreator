from flask import Flask
import logging
from scripts import image_handler, database_handler


def database_cleanup() -> int:
    """
    Synchronize the database and image storage by removing orphaned entries.
    Compares routes stored in the database with images in the image handler.
    Removes any database routes that don't have corresponding images and deletes
    any images that don't have corresponding database routes.
    Returns:
        int: The total number of cleanup actions performed (deleted routes + deleted images).
    """
    
    images_urls: list = [entry.lower() for entry in image_handler.list()]
    database_urls: list = [entry[3].lower() for entry in database_handler.get_all_routes()]
    
    cleanup_actions: int = 0
    
    for url in database_urls:
        if not url in images_urls:
            database_handler.del_route(url)
            cleanup_actions+=1
    
    for url in images_urls:
        if not url in database_urls:
            image_handler.delete(url)
            cleanup_actions+=1
    
    return cleanup_actions


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

database_handler.init_sql_database()
image_handler.init_glob_database()

@app.route('/api/database_cleanup', methods=['GET'])
def init_cron():
    """
    Initialize and execute a scheduled database cleanup task.
    This function logs the receipt of a cleanup request, performs database cleanup operations,
    and logs the completion status with the number of cleanup actions performed.
    Returns:
        Logs cleanup request initiation and completion status.
    """
    
    logging.info('Received cleanup request at /api/database_cleanup')
    cleanup_actions: int = database_cleanup()
    logging.info(f'Database cleanup completed with {cleanup_actions} cleanup_actions')