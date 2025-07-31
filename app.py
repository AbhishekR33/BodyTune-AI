from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from models.health_analyzer import HealthAnalyzer
from models.recommendation_engine import RecommendationEngine
from utils.report_parser import ReportParser
from utils.database import init_db, User, HealthReport, db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bodytune.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
from utils.database import db
db.init_app(app)

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def safe_float_conversion(value, default=0.0):
    """Safely convert a value to float, handling empty strings and None"""
    if value is None or value == '' or value == 'None':
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int_conversion(value, default=0):
    """Safely convert a value to int, handling empty strings and None"""
    if value is None or value == '' or value == 'None':
        return default
    try:
        return int(float(value))  # Convert to float first to handle decimal strings
    except (ValueError, TypeError):
        return default

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    """Upload page for medical reports"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    user_info = {
        'name': request.form.get('name', ''),
        'age': request.form.get('age', ''),
        'gender': request.form.get('gender', ''),
        'weight': request.form.get('weight', ''),
        'height': request.form.get('height', '')
    }
    
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Parse the medical report
            parser = ReportParser()
            health_data = parser.parse_report(file_path)
            
            # Analyze health parameters
            analyzer = HealthAnalyzer()
            analysis_results = analyzer.analyze_parameters(health_data, user_info)
            
            # Generate recommendations
            recommendation_engine = RecommendationEngine()
            recommendations = recommendation_engine.generate_recommendations(
                analysis_results, user_info
            )
            
            # Save to database
            # (Implementation for database saving would go here)
            
            return render_template('results.html', 
                                 health_data=health_data,
                                 analysis=analysis_results,
                                 recommendations=recommendations,
                                 user_info=user_info)
                                 
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('upload_page'))
    
    else:
        flash('Invalid file type. Please upload PDF, PNG, JPG, JPEG, or GIF files.')
        return redirect(request.url)

@app.route('/analyze', methods=['POST'])
def analyze_manual():
    """Handle manual parameter entry and analysis"""
    try:
        health_data = {
            # Basic health parameters
            'glucose': safe_float_conversion(request.form.get('glucose')),
            'cholesterol_total': safe_float_conversion(request.form.get('cholesterol_total')),
            'cholesterol_hdl': safe_float_conversion(request.form.get('cholesterol_hdl')),
            'cholesterol_ldl': safe_float_conversion(request.form.get('cholesterol_ldl')),
            'blood_pressure_systolic': safe_float_conversion(request.form.get('bp_systolic')),
            'blood_pressure_diastolic': safe_float_conversion(request.form.get('bp_diastolic')),
            'bmi': safe_float_conversion(request.form.get('bmi')),
            'body_fat_percentage': safe_float_conversion(request.form.get('body_fat')),
            # InBody specific parameters
            'weight': safe_float_conversion(request.form.get('weight')),
            'muscle_mass': safe_float_conversion(request.form.get('muscle_mass')),
            'protein': safe_float_conversion(request.form.get('protein')),
            'minerals': safe_float_conversion(request.form.get('minerals')),
            'total_body_water': safe_float_conversion(request.form.get('total_body_water')),
            'visceral_fat_level': safe_float_conversion(request.form.get('visceral_fat_level')),
            'basal_metabolic_rate': safe_float_conversion(request.form.get('basal_metabolic_rate')),
            'waist_hip_ratio': safe_float_conversion(request.form.get('waist_hip_ratio')),
            'inbody_score': safe_float_conversion(request.form.get('inbody_score'))
        }
        
        user_info = {
            'name': request.form.get('name', ''),
            'age': safe_int_conversion(request.form.get('age'), 25),
            'gender': request.form.get('gender', ''),
            'weight': safe_float_conversion(request.form.get('weight')),
            'height': safe_float_conversion(request.form.get('height')),
            'activity_level': request.form.get('activity_level', 'moderate')
        }
        
        # Validate that we have basic required information
        if not user_info['name']:
            flash('Please enter your name.')
            return redirect(url_for('manual_entry'))
        
        if user_info['age'] < 10 or user_info['age'] > 120:
            flash('Please enter a valid age between 10 and 120.')
            return redirect(url_for('manual_entry'))
        
        if not user_info['gender']:
            flash('Please select your gender.')
            return redirect(url_for('manual_entry'))
        
        # Check if at least some health parameters are provided
        non_zero_params = [v for v in health_data.values() if v > 0]
        if len(non_zero_params) < 2:
            flash('Please enter at least 2 health parameters for analysis.')
            return redirect(url_for('manual_entry'))
        
        # Analyze health parameters
        analyzer = HealthAnalyzer()
        analysis_results = analyzer.analyze_parameters(health_data, user_info)
        
        # Generate recommendations with error handling
        try:
            recommendation_engine = RecommendationEngine()
            recommendations = recommendation_engine.generate_recommendations(
                analysis_results, user_info
            )
        except KeyError as e:
            flash(f'Error generating recommendations: Missing strategy {str(e)}. Using default recommendations.')
            # Provide minimal recommendations as fallback
            recommendations = {
                'diet_plan': {'strategy': 'optimal', 'daily_calories': 2000},
                'workout_plan': {'strategy': 'optimal'},
                'timeline': {'overall': 'Contact healthcare provider for personalized advice'}
            }
        except Exception as e:
            flash(f'Error generating recommendations: {str(e)}. Please try again.')
            return redirect(url_for('manual_entry'))
        
        return render_template('results.html', 
                             health_data=health_data,
                             analysis=analysis_results,
                             recommendations=recommendations,
                             user_info=user_info)
                             
    except Exception as e:
        flash(f'Error analyzing data: {str(e)}. Please check your input values.')
        return redirect(url_for('manual_entry'))

@app.route('/manual-entry')
def manual_entry():
    """Manual parameter entry page"""
    return render_template('manual_entry.html')

@app.route('/api/health-check')
def health_check():
    """API endpoint for health check"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500



@app.route('/visibility_test')
def visibility_test():
    """Test page for checking text visibility"""
    return render_template('visibility_test.html')

if __name__ == '__main__':
    # Initialize database
    init_db(app)
    app.run(debug=True, host='0.0.0.0', port=5000)
