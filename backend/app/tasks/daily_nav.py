from app import db
from app.models import NavSnapshot
from app.services.nav import calculate_nav_snapshot

def run_daily_snapshot():
    nav_data = calculate_nav_snapshot()

    snapshot = NavSnapshot(
        eth_usd=nav_data["eth_usd"],
        sol_usd=nav_data["sol_usd"],
        total_aum=nav_data["total_aum"],
        nav_per_share=nav_data["nav_per_share"]
    )

    db.session.add(snapshot)
    db.session.commit()

    print("Daily NAV snapshot saved:", snapshot.to_dict())
