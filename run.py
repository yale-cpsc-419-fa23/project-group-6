import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from app import create_app
from app.utils.recommendation_utils import update_clusters

app = create_app('DevelopmentConfig')

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_clusters, args=[app], trigger="interval", hours=24)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    app.run()

