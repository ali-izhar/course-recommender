from .auth import auth_bp
from .task import task_bp
from .main import main_bp
from .user import user_bp

__all__ = ['auth_bp', 'task_bp', 'main_bp', 'user_bp']