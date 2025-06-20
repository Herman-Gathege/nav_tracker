from dotenv import load_dotenv
load_dotenv()

from app.services.nav import calculate_nav_snapshot
print(calculate_nav_snapshot())
