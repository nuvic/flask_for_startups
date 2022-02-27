# Standard Library imports
import os
from dotenv import load_dotenv

# Core Flask imports

# Third-party imports

# App imports
from app import create_app, db_manager
from app.models import Account, User, Role, UserRole


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = create_app(os.getenv("FLASK_CONFIG") or "dev")


@app.shell_context_processor
def make_shell_context():
    return dict(db=db_manager, User=User, Account=Account, Role=Role, UserRole=UserRole)
