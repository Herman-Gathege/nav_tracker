from dotenv import load_dotenv
load_dotenv()




from app import create_app, db
from app.tasks.daily_nav import run_daily_snapshot

app = create_app()

with app.app_context():
    db.create_all()  # 💥 Create all tables if they don't exist
    run_daily_snapshot()
