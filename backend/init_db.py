from app import app, db
from models import User
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init_db():
    with app.app_context():
        try:
            # Drop all tables
            db.drop_all()
            logger.info("Dropped all tables")
            
            # Create all tables
            db.create_all()
            logger.info("Created all tables")
            
            # Create admin user
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            logger.info("Admin user created successfully")
            
            # Verify admin user
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                logger.error("Admin user not found after creation")
                sys.exit(1)
                
            if admin.check_password('admin123'):
                logger.info("Admin user verified successfully")
            else:
                logger.error("Admin user password verification failed")
                sys.exit(1)
                
            logger.info("Database initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Error during database initialization: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    init_db() 