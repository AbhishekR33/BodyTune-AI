# BodyTune AI - Professional Health Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive Flask web application that analyzes medical test reports and provides personalized diet and workout recommendations using professional InBody methodology.

## 🚀 Features

- **InBody Analysis**: Professional body composition analysis with official InBody scoring methodology
- **Medical Report Processing**: Secure upload and analysis of PDF and image medical reports
- **Personalized Recommendations**: AI-powered diet plans and workout routines
- **Body Shape Analysis**: D-Shape, I-Shape, and C-Shape classification system
- **Progress Tracking**: Visual analytics and improvement timelines
- **Print-Ready Reports**: Professional medical report generation

## 🛠️ Technology Stack

- **Backend**: Python Flask, SQLite
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **AI/ML**: Custom health analysis algorithms, scikit-learn
- **File Processing**: PDF parsing, OCR for medical documents
- **Scoring System**: Professional InBody methodology implementation

## 📋 Prerequisites

- Python 3.8 or higher
- Virtual environment support
- Modern web browser

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/AbhishekR33/BodyTune-AI.git
cd BodyTune-AI
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
# Option 1: One command (Windows)
run.bat

# Option 2: Manual start
python app.py
```

### 5. Access the Application
Open your browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
BodyTune-AI/
├── app.py                 # Main Flask application
├── models/               # Health analysis and AI models
│   └── health_analyzer.py
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   └── results.html
├── static/              # CSS, JS, and assets
│   ├── css/
│   ├── js/
│   └── images/
├── utils/               # Utility functions
├── uploads/             # Uploaded medical reports
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## 🎯 Key Components

### InBody Analysis Engine
- Professional scoring algorithm based on official InBody standards
- Multi-factor analysis including skeletal muscle, body fat, visceral fat
- Body shape classification (D-Shape, I-Shape, C-Shape)
- Risk assessment and improvement recommendations

### Recommendation System
- Personalized diet plans with calorie targets
- Custom workout routines for gym training
- Lifestyle optimization suggestions
- Timeline-based improvement tracking

### Medical Report Processing
- Secure file upload handling
- PDF and image format support
- OCR text extraction
- Data validation and normalization

## 🔧 Configuration

### Environment Variables
Create a `.env` file based on `.env.example`:
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Database
The application uses SQLite for data storage. The database is automatically initialized on first run.

## 📊 Usage

1. **Upload Medical Report**: Upload your medical test report (PDF or image)
2. **View Analysis**: Get comprehensive InBody analysis with professional scoring
3. **Review Recommendations**: Receive personalized diet and workout plans
4. **Track Progress**: Monitor improvements with visual analytics
5. **Print Results**: Generate professional medical reports

## 🧪 Testing

Run the test suite to verify functionality:
```bash
python test_complete.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `/docs` folder
- Review the troubleshooting guide

## 🎯 Roadmap

- [ ] Machine learning model improvements
- [ ] Mobile app development
- [ ] API for third-party integrations
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

---

**BodyTune AI** - Transforming health analysis with professional-grade technology.
