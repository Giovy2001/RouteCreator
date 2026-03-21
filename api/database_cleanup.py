from flask import Flask
import logging
from scripts import image_handler
from scripts.database_sql import sql_routes, sql_init

def database_cleanup() -> int:
    """
    Synchronize the database and image storage by removing orphaned entries.
    Compares routes stored in the database with images in the image handler.
    Removes any database routes that don't have corresponding images and deletes
    any images that don't have corresponding database routes.
    Returns:
        int: The total number of cleanup actions performed (deleted routes + deleted images).
    """
    
    images_urls: list = [entry for entry in image_handler.list()]
    database_entries: list = sql_routes.get_all_routes(global_values.conn)
    database_urls: list = [entry["image_url"] for entry in database_entries]
    
    cleanup_actions: int = 0
    
    for entry_dict in database_entries:
        if not entry_dict["image_url"].lower() in [i.lower() for i in images_urls]:
            sql_routes.del_route(global_values.conn, entry_dict["route_id"])
            cleanup_actions+=1
    
    for url in images_urls:
        if not url.lower() in [i.lower() for i in database_urls]:
            image_handler.delete(url)
            cleanup_actions+=1
    
    return cleanup_actions


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

import global_values
global_values.load_database()

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
    return {"status": "ok"}