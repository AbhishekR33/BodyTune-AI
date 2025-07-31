from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask

db = SQLAlchemy()

class User(db.Model):
    """User model for storing user information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    weight = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    activity_level = db.Column(db.String(20), default='moderate')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with health reports
    health_reports = db.relationship('HealthReport', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.name}>'

class HealthReport(db.Model):
    """Model for storing health report data"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Health parameters
    glucose = db.Column(db.Float, nullable=True)
    cholesterol_total = db.Column(db.Float, nullable=True)
    cholesterol_hdl = db.Column(db.Float, nullable=True)
    cholesterol_ldl = db.Column(db.Float, nullable=True)
    blood_pressure_systolic = db.Column(db.Float, nullable=True)
    blood_pressure_diastolic = db.Column(db.Float, nullable=True)
    bmi = db.Column(db.Float, nullable=True)
    body_fat_percentage = db.Column(db.Float, nullable=True)
    
    # Analysis results
    overall_score = db.Column(db.Float, nullable=True)
    risk_level = db.Column(db.String(20), nullable=True)
    
    # Report metadata
    report_file_path = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<HealthReport {self.id} - Score: {self.overall_score}>'

class Recommendation(db.Model):
    """Model for storing generated recommendations"""
    id = db.Column(db.Integer, primary_key=True)
    health_report_id = db.Column(db.Integer, db.ForeignKey('health_report.id'), nullable=False)
    
    # Recommendation data (stored as JSON strings)
    diet_plan = db.Column(db.Text, nullable=True)
    workout_plan = db.Column(db.Text, nullable=True)
    lifestyle_tips = db.Column(db.Text, nullable=True)
    timeline = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Recommendation {self.id}>'

def init_db(app: Flask):
    """Initialize the database"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        print("Database initialized successfully!")

def create_sample_user():
    """Create a sample user for testing"""
    sample_user = User(
        name="John Doe",
        email="john.doe@example.com",
        age=30,
        gender="male",
        weight=75.0,
        height=180.0,
        activity_level="moderate"
    )
    
    db.session.add(sample_user)
    db.session.commit()
    
    return sample_user

def save_health_report(user_id: int, health_data: dict, analysis_results: dict) -> HealthReport:
    """Save health report to database"""
    
    health_report = HealthReport(
        user_id=user_id,
        glucose=health_data.get('glucose'),
        cholesterol_total=health_data.get('cholesterol_total'),
        cholesterol_hdl=health_data.get('cholesterol_hdl'),
        cholesterol_ldl=health_data.get('cholesterol_ldl'),
        blood_pressure_systolic=health_data.get('blood_pressure_systolic'),
        blood_pressure_diastolic=health_data.get('blood_pressure_diastolic'),
        bmi=health_data.get('bmi'),
        body_fat_percentage=health_data.get('body_fat_percentage'),
        overall_score=analysis_results.get('overall_score'),
        risk_level=analysis_results.get('risk_level')
    )
    
    db.session.add(health_report)
    db.session.commit()
    
    return health_report

def get_user_history(user_id: int) -> list:
    """Get user's health report history"""
    return HealthReport.query.filter_by(user_id=user_id).order_by(HealthReport.created_at.desc()).all()
