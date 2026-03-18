from apscheduler.schedulers.background import BackgroundScheduler
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


def init_cleanup() -> None:
    """
    Initialize and start a background scheduler for periodic database cleanup.
    Sets up a BackgroundScheduler that executes the database_cleanup function
    at regular intervals of one week. The scheduler runs in the background
    without blocking the main application flow.
    Returns:
        None
    """    
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(database_cleanup, 'cron', day_of_week='wed', hour=16, minute=0)
    scheduler.start()