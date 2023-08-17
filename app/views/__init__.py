from .auth import auth_bp
from .lab import lab_bp
from .main import main_bp
from .task import task_bp
from .user import user_bp

__all__ = ['auth_bp', 'lab_bp', 'main_bp', 'task_bp', 'user_bp']