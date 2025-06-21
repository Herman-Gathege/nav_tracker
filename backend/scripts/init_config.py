from app import create_app, db
from app.models import Config

app = create_app()

with app.app_context():
    if not Config.query.filter_by(key="total_shares").first():
        total_shares = Config(key="total_shares", value=10000)
        db.session.add(total_shares)

    if not Config.query.filter_by(key="high_nav_watermark").first():
        high_watermark = Config(key="high_nav_watermark", value=0)
        db.session.add(high_watermark)

    db.session.commit()
    print(" Default config values inserted.")
