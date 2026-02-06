# Python Installation & Setup Guide for Fine-Tuning

## 🐍 **Step 1: Install Python**

### **Download Python 3.11:**
1. Go to: https://www.python.org/downloads/
2. Click "Download Python 3.11.x" (latest 3.11 version)
3. **IMPORTANT**: Check ✅ "Add Python to PATH" during installation!
4. Click "Install Now"
5. Wait ~5 minutes

### **Verify Installation:**
```powershell
python --version
# Should show: Python 3.11.x

pip --version
# Should show: pip 23.x.x
```

---

## 📦 **Step 2: Install Dependencies**

### **After Python is installed:**

```powershell
# Navigate to backend
cd C:\LenteraDreamFlow\backend

# Install required packages
pip install openai python-dotenv pandas pyyaml
```

**Packages:**
- `openai`: OpenAI API client
- `python-dotenv`: Load .env files
- `pandas`: Data manipulation
- `pyyaml`: YAML config files

---

## 🔑 **Step 3: Create .env File**

```powershell
cd C:\LenteraDreamFlow\backend

# Create .env file
notepad .env
```

**Paste this in notepad:**
```
OPENAI_API_KEY=your-openai-api-key-here
```

**Save & close!**

---

## 🚀 **Step 4: Generate Training Data**

```powershell
cd C:\LenteraDreamFlow\backend

# Run data generator (1000 examples, ~$25-30)
python generate_training_data.py
```

**This will:**
- Generate 1000 Indonesian conversations
- Validate ethics compliance
- Save to `training_data.jsonl`
- Take ~2-3 hours
- Cost ~$25-30

**You can monitor progress** - it will show:
```
Generating example 1/1000...
Generating example 2/1000...
...
✅ Complete! Cost: $28.50
```

---

## ⏰ **Timeline:**

1. **Install Python**: 5-10 min
2. **Install packages**: 2-3 min
3. **Create .env**: 1 min
4. **Generate data**: 2-3 hours (automated!)

**Total active work**: ~15 minutes!  
**Total time**: ~3 hours (mostly running!)

---

## 🎯 **Current Step: Install Python!**

**Click here to download**: https://www.python.org/downloads/

**Remember**: ✅ Check "Add Python to PATH"!

**After install, come back and tell me!** Then we'll install packages & start generating! 🚀
