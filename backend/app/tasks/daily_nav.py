# from app import db
# from app.models import NavSnapshot
# from app.services.nav import calculate_nav_snapshot

# def run_daily_snapshot():
#     nav_data = calculate_nav_snapshot()

#     snapshot = NavSnapshot(
#         eth_usd=nav_data["eth_usd"],
#         sol_usd=nav_data["sol_usd"],
#         total_aum=nav_data["total_aum"],
#         nav_per_share=nav_data["nav_per_share"]
#     )

#     db.session.add(snapshot)
#     db.session.commit()

#     print("Daily NAV snapshot saved:", snapshot.to_dict())


from app import db
from app.models import NavSnapshot, Config
from app.services.nav import calculate_nav_snapshot

def run_daily_snapshot():
    nav_data = calculate_nav_snapshot()

    # 📌 Update high watermark if needed
    high_config = Config.query.filter_by(key="high_nav_watermark").first()
    if nav_data["nav_per_share"] > high_config.value:
        high_config.value = nav_data["nav_per_share"]
        print(f"✅ High watermark updated to: {high_config.value}")

    # Save daily snapshot
    snapshot = NavSnapshot(
        eth_usd=nav_data["eth_usd"],
        sol_usd=nav_data["sol_usd"],
        total_aum=nav_data["total_aum"],
        nav_per_share=nav_data["nav_per_share"]
    )

    db.session.add(snapshot)
    db.session.commit()

    print("✅ Daily NAV snapshot saved:", snapshot.to_dict())
