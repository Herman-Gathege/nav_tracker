from . import db
from datetime import datetime

class NavSnapshot(db.Model):
    __tablename__ = 'nav_snapshots'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    eth_usd = db.Column(db.Float, nullable=False)
    sol_usd = db.Column(db.Float, nullable=False)
    total_aum = db.Column(db.Float, nullable=False)
    nav_per_share = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "eth_usd": self.eth_usd,
            "sol_usd": self.sol_usd,
            "total_aum": self.total_aum,
            "nav_per_share": self.nav_per_share
        }


# The Config model is used to store configuration settings for the application.
class Config(db.Model):
    __tablename__ = 'config'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Float, nullable=False)


class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    amount_usd = db.Column(db.Float, nullable=False)
    shares_issued = db.Column(db.Float, nullable=False)
    fee_applied = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    shares_sold = db.Column(db.Float, nullable=False)
    amount_returned_usd = db.Column(db.Float, nullable=False)
    fee_applied = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
