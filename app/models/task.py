from app.extensions import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.String(50), default="Medium", nullable=False)
    completed = db.Column(db.Boolean, default=False)

    # Relación con el usuario
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Task {self.content} (Priority: {self.priority}, Completed: {self.completed})>"
