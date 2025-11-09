# 🚀 KrishiKavach AI - Complete Installation Guide

This guide will walk you through setting up the entire KrishiKavach AI project on a new device that doesn't have Python, Node.js, or any dependencies installed.

## 📋 Prerequisites
- Windows 10/11 or Linux/macOS
- Internet connection (for downloading installers)
- At least 4GB RAM recommended
- 2GB free disk space

---

## 🛠️ Step 1: Install Python

### For Windows:
1. **Download Python Installer**
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.11.x" (latest stable version)
   - Or use direct link: https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe

2. **Run the Installer**
   - **IMPORTANT**: Check "Add Python to PATH" checkbox at the bottom
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**
   ```cmd
   python --version
   pip --version
   ```

### For macOS:
1. **Using Homebrew (Recommended)**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install python@3.11
   ```

2. **Using Python.org**
   - Download from: https://www.python.org/downloads/mac-osx/
   - Run the .pkg installer

### For Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---

## 🛠️ Step 2: Install Git (Optional but Recommended)

### For Windows:
1. Download from: https://git-scm.com/download/win
2. Run installer with default settings
3. Verify: `git --version`

### For macOS:
```bash
brew install git
```

### For Linux:
```bash
sudo apt install git
```

---

## 📁 Step 3: Download/Clone the Project

### Option A: Using Git (Recommended)
```bash
git clone https://github.com/your-repo/krishikavach-ai.git
cd krishikavach-ai
```

### Option B: Download ZIP
1. Go to your repository
2. Click "Code" → "Download ZIP"
3. Extract to desired location
4. Open terminal/command prompt in extracted folder

---

## 🏗️ Step 4: Set Up Virtual Environment

### For Windows:
```cmd
# Navigate to project folder
cd ml\crop-prediction

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### For macOS/Linux:
```bash
# Navigate to project folder
cd ml/crop-prediction

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**Note**: You should see `(venv)` in your terminal prompt when activated

---

## 📦 Step 5: Install Project Dependencies

### Install Python Packages
```bash
# Make sure you're in the ml/crop-prediction folder with venv activated
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

### If requirements.txt doesn't exist, install manually:
```bash
pip install flask flask-cors tensorflow keras scikit-learn pandas numpy pillow opencv-python python-dotenv google-generativeai xgboost joblib
```

---

## 🔑 Step 6: Set Up Environment Variables

1. **Create `.env` file** in the `ml/crop-prediction` folder:
```bash
# For Windows
echo. > .env

# For macOS/Linux
touch .env
```

2. **Edit the `.env` file** and add your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

**How to get API keys:**
- **Gemini API**: https://makersuite.google.com/app/apikey
- **Google API**: https://console.cloud.google.com/

---

## 🧠 Step 7: Download Model Files

If your project uses pre-trained models, you'll need to download them:

1. **Create models directory** (if not exists):
```bash
mkdir models
```

2. **Download model files** from your storage/backup and place in:
   - `ml/crop-prediction/models/`
   - `ml/crop-prediction/*.pkl` files

**Common model files needed:**
- `crop_recommendation_model.pkl`
- `preprocessor_pickle.pkl`
- `xgb_model_pickle.pkl`
- Any `.joblib` or `.h5` model files

---

## 🚀 Step 8: Test Installation

### Quick Test
```bash
# Test Python imports
python -c "import flask, tensorflow, sklearn, pandas, numpy; print('All packages installed successfully!')"
```

### Test Model Loading
```bash
python -c "import joblib; print('Joblib working')"
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"
```

---

## 🌐 Step 9: Run the Application

### Start the Flask Server
```bash
# Make sure you're in ml/crop-prediction folder with venv activated
python app.py
```

### Expected Output:
```
Loading AI-based pest detection model...
Pest detection model loaded successfully!
Gemini 1.5 Flash configured
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Open in Browser
- Navigate to: http://localhost:5000
- You should see the KrishiKavach AI homepage

---

## 🧪 Step 10: Test All Features

1. **Homepage**: http://localhost:5000
2. **Crop Recommendation**: Test the form
3. **Pest Detection**: Upload a plant image
4. **Chatbot**: Click the AI Assistant button
5. **Fertilizer Recommendation**: Test the form

---

## 🛠️ Troubleshooting

### Common Issues:

#### 1. **"Python not found" error**
- Make sure Python is added to PATH during installation
- Restart your terminal/command prompt
- Try `py` instead of `python` on Windows

#### 2. **"Module not found" errors**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

#### 3. **TensorFlow Issues**
```bash
# Install TensorFlow separately
pip install tensorflow --upgrade

# For older CPUs
pip install tensorflow-cpu
```

#### 4. **Port 5000 already in use**
```bash
# Kill existing process
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

#### 5. **Model Loading Errors**
- Ensure all `.pkl` files are in correct locations
- Check file permissions
- Verify model file integrity

#### 6. **API Key Errors**
- Double-check `.env` file syntax
- Ensure no spaces around `=` in `.env`
- Verify API keys are valid and active

---

## 📱 Optional: Install Node.js (for Frontend Development)

### For Windows:
1. Download from: https://nodejs.org/
2. Install LTS version with default settings
3. Verify: `node --version` and `npm --version`

### For macOS:
```bash
brew install node
```

### For Linux:
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## 🔧 Development Commands

### Start Development Server
```bash
# With debug mode
python app.py

# With specific port
python app.py --port 8080
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Reactivate Virtual Environment (when returning to project)
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

---

## 📁 Project Structure Overview
```
krishikavach-ai/
├── ml/crop-prediction/          # Main Flask application
│   ├── app.py                   # Main Flask app
│   ├── requirements.txt         # Python dependencies
│   ├── templates/               # HTML templates
│   ├── static/                  # CSS, JS, images
│   ├── models/                  # ML models
│   └── *.pkl                   # Model files
├── templates/                   # Additional templates
└── README.md                    # Project documentation
```

---

## 🆘 Need Help?

If you encounter any issues:

1. **Check the terminal output** for specific error messages
2. **Verify all installations** with the test commands
3. **Ensure all files are in correct locations**
4. **Check internet connection** for API calls
5. **Review the troubleshooting section** above

**Common files to check:**
- `app.py` - Main application file
- `requirements.txt` - Dependencies list
- `.env` - Environment variables
- Model files (`.pkl`, `.joblib`)

---

## ✅ Installation Checklist

- [ ] Python installed and added to PATH
- [ ] Virtual environment created and activated
- [ ] All requirements installed successfully
- [ ] Environment variables configured
- [ ] Model files downloaded and placed correctly
- [ ] Flask app runs without errors
- [ ] Homepage loads at localhost:5000
- [ ] All features (crop rec, pest det, chatbot) work

---

**🎉 Congratulations!** Your KrishiKavach AI system should now be fully operational. The application provides AI-powered crop recommendations, pest detection, fertilizer suggestions, and an intelligent chatbot assistant for farmers.