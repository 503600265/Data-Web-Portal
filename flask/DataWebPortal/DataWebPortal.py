from app import app, db
from app.models import Users, Jobs, Activity


@app.shell_context_processor
def make_shell_context():
    return {'Users': Users, 'Jobs': Jobs, 'Activity': Activity}