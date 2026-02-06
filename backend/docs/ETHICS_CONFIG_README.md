# Ethics Configuration System - Quick Reference

## 📁 Files Created

### 1. **ethics_config.yaml** (500+ lines)
Comprehensive YAML configuration file containing:
- Core ethical principles
- Crisis detection keywords & responses
- Prohibited output patterns
- Indonesian hotlines
- Cultural sensitivity settings
- Age restrictions
- Data protection (UU PDP)
- AI personality traits
- Quality assurance rules
- Operational parameters

**Path**: `c:\LenteraDreamFlow\backend\ethics_config.yaml`

---

### 2. **ethics_config_loader.py** (250+ lines)
Python module to load and access YAML configuration

**Key Functions**:
```python
from ethics_config_loader import load_ethics_config

config = load_ethics_config()

# Get crisis keywords
keywords = config.get_crisis_keywords('critical')

# Get hotlines
hotline = config.get_hotline('primary')

# Get prohibited patterns
patterns = config.get_prohibited_patterns('diagnosis')

# Check age appropriateness
is_ok = config.is_age_appropriate(15)
```

**Path**: `c:\LenteraDreamFlow\backend\ethics_config_loader.py`

---

### 3. **example_ethics_usage.py** (300+ lines)
Complete examples showing how to use the system

**Run Examples**:
```bash
cd c:\LenteraDreamFlow\backend
python example_ethics_usage.py
```

**Path**: `c:\LenteraDreamFlow\backend\example_ethics_usage.py`

---

## 🎯 How to Use

### 1. Load Configuration
```python
from ethics_config_loader import load_ethics_config

config = load_ethics_config()
print(f"Version: {config.get_version()}")
```

### 2. Crisis Detection
```python
# Get all crisis keywords
keywords = config.get_all_crisis_keywords()

# Check if message contains crisis keywords
user_message = "saya ingin bunuh diri"
is_crisis = any(kw in user_message.lower() for kw in keywords)

if is_crisis:
    response = config.get_crisis_response_template()
    hotlines = config.get_all_hotlines()
```

### 3. Output Validation
```python
# Get prohibited patterns
prohibited = config.get_prohibited_patterns()

# Validate AI response
ai_response = "Kamu menderita depresi"
is_valid = not any(p in ai_response.lower() for p in prohibited)
```

### 4. Get Disclaimers
```python
# Show disclaimer at conversation start
disclaimer = config.get_disclaimer('conversation_start')
print(disclaimer)
# Output: "Hai, aku LENTERA—AI pendukung kesehatan mental..."
```

### 5. Cultural Settings
```python
# Check language style
style = config.get_language_style()  # "informal"

# Get derogatory terms to avoid
bad_words = config.get_derogatory_terms()  # ["gila", "sakit jiwa", ...]
```

### 6. Age Verification
```python
# Check minimum age
min_age = config.get_minimum_age()  # 13

# Validate user age
is_ok = config.is_age_appropriate(15)  # True

# Get age-specific restrictions
restrictions = config.get_age_restrictions(15)
```

---

## 🔧 Integration with Existing Code

### Update safety_validator.py
```python
from ethics_config_loader import get_ethics_config

class SafetyValidator:
    def __init__(self):
        self.config = get_ethics_config()
        self.crisis_keywords = self.config.get_all_crisis_keywords()
        self.prohibited_patterns = self.config.get_prohibited_patterns()
```

### Update crisis_handler.py
```python
from ethics_config_loader import get_ethics_config

class CrisisHandler:
    def __init__(self):
        self.config = get_ethics_config()
        self.hotlines = self.config.get_all_hotlines()
    
    def get_crisis_response(self):
        return self.config.get_crisis_response_template()
```

### Update main.py
```python
from ethics_config_loader import get_ethics_config

config = get_ethics_config()

@app.on_event("startup")
async def startup_event():
    logger.info(f"Ethics Config v{config.get_version()} loaded")
```

---

## 📊 Configuration Sections

### Crisis Detection
- Critical keywords (15+)
- High-risk keywords (10+)
- 4 Indonesian hotlines
- Crisis response template
- Human review triggers

### Prohibited Content
- Diagnosis patterns
- Medication patterns  
- Replacement therapy patterns
- Toxic positivity patterns
- Mental health conditions list

### Cultural Settings
- Religious sensitivity
- Family dynamics
- Stigma awareness
- Language style
- Derogatory terms to avoid

### Data Protection (UU PDP)
- Explicit consent
- Data minimization
- User rights (access, deletion, correction)
- Encryption requirements
- Incident response

### AI Personality
- Tone settings (warmth, empathy, formality)
- Response structure
- Length limits
- Must-have traits
- Must-avoid behaviors

### Quality Assurance
- Pre-response checklist
- Human review triggers
- Logging requirements
- Anonymization rules

---

## ✅ Benefits of YAML Configuration

### 1. **Easy to Update**
Change rules without modifying code:
```yaml
# Just edit YAML file
crisis:
  keywords:
    critical:
      - "new_keyword"  # Add new crisis keyword
```

### 2. **Centralized Management**
All ethics rules in one place, easy to review

### 3. **Version Control**
Track changes to ethics rules over time with git

### 4. **Non-Technical Updates**
Mental health professionals can review/update YAML without coding

### 5. **Testing**
Easy to test different configurations

### 6. **Documentation**
YAML itself serves as documentation

---

## 🔄 Updating Configuration

### Add New Crisis Keyword
```yaml
crisis:
  detection:
    keywords:
      critical:
        - "your_new_keyword"
```

### Add New Hotline
```yaml
crisis:
  response:
    hotlines:
      new_hotline:
        name: "New Hotline Name"
        number: "xxx-xxxx"
        availability: "24/7"
```

### Change AI Personality
```yaml
personality:
  tone:
    warmth: "very_high"    # Changed from "high"
    formality: "very_low"  # Changed from "low"
```

### Update User Agreement
```yaml
disclaimers:
  user_agreement:
    points:
      - "New agreement point here"
```

**After editing, restart backend**:
```bash
docker-compose restart backend
```

---

## 🧪 Testing

### Test Configuration Loading
```bash
cd c:\LenteraDreamFlow\backend
python -c "from ethics_config_loader import load_ethics_config; print(load_ethics_config())"
```

### Run Full Examples
```bash
python example_ethics_usage.py
```

### Validate YAML Syntax
```bash
python -c "import yaml; yaml.safe_load(open('ethics_config.yaml'))"
```

---

## 📋 Implementation Checklist

- [x] Create ethics_config.yaml
- [x] Create ethics_config_loader.py
- [x] Add PyYAML to requirements.txt
- [x] Create usage examples
- [ ] Integrate into safety_validator.py
- [ ] Integrate into crisis_handler.py
- [ ] Integrate into main.py
- [ ] Test with real scenarios
- [ ] Get mental health expert review

---

## 🎯 Next Steps

1. **Integrate** config into existing safety/crisis modules
2. **Test** thoroughly with various scenarios
3. **Review** with mental health professional
4. **Update** based on feedback
5. **Deploy** to production

---

**Version**: 1.1  
**Last Updated**: 2025-12-25  
**Maintained by**: LENTERA Development Team
