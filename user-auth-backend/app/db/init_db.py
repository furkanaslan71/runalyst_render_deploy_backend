from app.db.base import Base
from app.db.session import engine
from app.models.user import User  # Import all models

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized!")

if __name__ == "__main__":
    init_db()