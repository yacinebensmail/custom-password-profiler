#  Advanced Custom Profiler (OSINT & Password Auditing)

##  Description
This project is an advanced, Python-based custom password profiler inspired by CUPP. It is designed for security auditing and raising awareness about password predictability. By collecting targeted OSINT information (names, dates, hobbies), the tool generates a highly optimized wordlist to test the robustness of password policies.

*This project was developed as part of my portfolio to demonstrate my skills in Python development and offensive security auditing.*

## ✨ Features
- **Strict Input Validation:** Mathematical date verification and automatic string sanitization to prevent generation errors.
- **Modular Architecture:** Structured as a professional Python package (`__main__.py`, `functions.py`, `helper.py`).
- **Advanced Mutation Engine:** 
  - Dynamic combinations (First Name + Last Name + Years).
  - Conditional appending of special characters and random numbers.
  - *Leet Speak* variant generation (e.g., a=@, e=3).
- **Interactive CLI:** Stylized and user-friendly menus powered by the `rich` library.

##  Installation & Usage

1. Clone the repository:
\`\`\`bash
git clone https://github.com/yacinebensmail/custom-password-profiler.git
cd custom-profiler
\`\`\`

2. Install the required dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Run the module:
\`\`\`bash
python -m custom_profiler
\`\`\`

## ⚠️ Disclaimer
This tool was developed for **strictly educational purposes and authorized auditing**. The author assumes no responsibility for any unauthorized or malicious use of this software.
