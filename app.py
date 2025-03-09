import streamlit as st
import re
import random
import string
import math
import time

# Set page configuration
st.set_page_config(
    page_title="Password Strength Analyzer",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #0D47A1;
        margin-top: 2rem;
    }
    .password-input {
        margin: 1.5rem 0;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .strong-text {
        font-weight: bold;
        color: #2E7D32;
    }
    .moderate-text {
        font-weight: bold;
        color: #F57F17;
    }
    .weak-text {
        font-weight: bold;
        color: #C62828;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #616161;
    }
    .emoji-large {
        font-size: 1.5rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class PasswordStrengthChecker:
    def __init__(self):
        # Define weights for different criteria
        self.weights = {
            "length": 0.25,
            "uppercase": 0.15,
            "lowercase": 0.15,
            "digits": 0.15,
            "special": 0.15,
            "common": 0.15,
            "repetition": 0.10,
            "sequential": 0.10
        }
        
        # Common password list
        self.common_passwords = [
            "password", "123456", "qwerty", "admin", "welcome", 
            "password123", "abc123", "letmein", "monkey", "1234567890",
            "admin123", "iloveyou", "sunshine", "princess", "football",
            "123123", "baseball", "dragon", "master", "superman"
        ]
        
    def check_password_strength(self, password):
        """
        Advanced password strength checker with weighted scoring
        """
        score = 0
        feedback = []
        details = {}
        
        # Length check (logarithmic scale)
        length_score = min(1.0, math.log(max(1, len(password))) / math.log(20))
        details["length"] = length_score
        if len(password) < 8:
            feedback.append("📏 Password should be at least 8 characters long.")
        
        # Character type checks
        has_upper = bool(re.search(r"[A-Z]", password))
        has_lower = bool(re.search(r"[a-z]", password))
        has_digit = bool(re.search(r"\d", password))
        has_special = bool(re.search(r"[!@#$%^&*]", password))
        
        details["uppercase"] = 1.0 if has_upper else 0.0
        details["lowercase"] = 1.0 if has_lower else 0.0
        details["digits"] = 1.0 if has_digit else 0.0
        details["special"] = 1.0 if has_special else 0.0
        
        if not has_upper or not has_lower:
            feedback.append("🔤 Include both uppercase and lowercase letters.")
        if not has_digit:
            feedback.append("🔢 Add at least one number (0-9).")
        if not has_special:
            feedback.append("🔣 Include at least one special character (!@#$%^&*).")
        
        # Check for common passwords
        is_common = password.lower() in self.common_passwords
        details["common"] = 0.0 if is_common else 1.0
        if is_common:
            feedback.append("⚠️ This is a commonly used password and easy to guess.")
        
        # Check for repetitive patterns (e.g., "aaa", "111")
        repetitive = bool(re.search(r"(.)\1{2,}", password))
        details["repetition"] = 0.0 if repetitive else 1.0
        if repetitive:
            feedback.append("🔁 Avoid repetitive characters (e.g., 'aaa', '111').")
        
        # Check for sequential patterns (e.g., "abc", "123")
        sequential_patterns = ["abcdefghijklmnopqrstuvwxyz", "0123456789"]
        is_sequential = False
        
        for pattern in sequential_patterns:
            for i in range(len(pattern) - 2):
                seq = pattern[i:i+3]
                if seq.lower() in password.lower():
                    is_sequential = True
                    break
        
        details["sequential"] = 0.0 if is_sequential else 1.0
        if is_sequential:
            feedback.append("📊 Avoid sequential characters (e.g., 'abc', '123').")
        
        # Calculate weighted score
        for criterion, weight in self.weights.items():
            score += details[criterion] * weight
        
        # Ensure the normalized score is between 0 and 1
        normalized_score = min(1.0, max(0.0, score))
        
        # Convert to 0-5 scale
        final_score = round(normalized_score * 5)
        
        # Determine strength category
        if final_score >= 4:
            strength = "Strong"
            message = "🛡️ Strong Password!"
            emoji = "✅"
        elif final_score >= 3:
            strength = "Moderate"
            message = "⚠️ Moderate Password"
            emoji = "⚠️"
        else:
            strength = "Weak"
            message = "❌ Weak Password"
            emoji = "❌"
        
        return {
            "score": final_score,
            "normalized_score": normalized_score,
            "strength": strength,
            "message": message,
            "emoji": emoji,
            "feedback": feedback,
            "details": details
        }
    
    def generate_strong_password(self, length=12):
        """
        Generates a strong random password
        """
        if length < 8:
            length = 12  # Ensure minimum length for security
            
        # Ensure we have at least one of each required character type
        lowercase = random.choice(string.ascii_lowercase)
        uppercase = random.choice(string.ascii_uppercase)
        digit = random.choice(string.digits)
        special = random.choice("!@#$%^&*")
        
        # Fill the rest with random characters
        remaining_length = length - 4
        all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
        rest = ''.join(random.choice(all_chars) for _ in range(remaining_length))
        
        # Combine all parts and shuffle
        password = lowercase + uppercase + digit + special + rest
        password_list = list(password)
        random.shuffle(password_list)
        return ''.join(password_list)

def main():
    # Initialize the password checker
    checker = PasswordStrengthChecker()
    
    # Define strength colors at the global level (outside of any tab)
    strength_color = {
        "Strong": "#2E7D32",
        "Moderate": "#F57F17",
        "Weak": "#C62828"
    }
    
    # Header
    st.markdown('<h1 class="main-header">🔐 Password Strength Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        Protect your digital identity with strong passwords. This tool helps you evaluate 
        and improve your password security using professional security standards.
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs with icons
    tab1, tab2, tab3 = st.tabs(["🔍 Check Password", "🔑 Generate Password", "📚 Security Tips"])
    
    with tab1:
        st.markdown('<h2 class="subheader">Analyze Your Password</h2>', unsafe_allow_html=True)
        
        # Password input
        password = st.text_input(
            "Enter your password:",
            type="password",
            help="Your password is never stored or transmitted",
            key="password_input"
        )
        
        if password:
            # Show a spinner while "analyzing"
            with st.spinner("Analyzing password strength..."):
                time.sleep(0.5)  # Simulate processing for better UX
                result = checker.check_password_strength(password)
            
            # Create a card for the result
            st.markdown(f"""
            <div class="card" style="background-color: {strength_color[result['strength']]}15;">
                <h3 style="color: {strength_color[result['strength']]};">
                    {result['emoji']} {result['message']}
                </h3>
                <p>Strength Score: {result['score']}/5</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create a progress bar with appropriate color
            st.progress(result["normalized_score"])
            
            # Display detailed analysis
            if result["feedback"]:
                st.markdown('<h3 class="subheader">📝 Improvement Suggestions</h3>', unsafe_allow_html=True)
                for suggestion in result["feedback"]:
                    st.markdown(f"- {suggestion}")
            else:
                st.markdown("""
                <div style="padding: 1rem; background-color: #E8F5E9; border-radius: 0.5rem; margin-top: 1rem;">
                    <p>🎉 Excellent! Your password meets all security criteria.</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 class="subheader">Generate a Secure Password</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            Need a strong password? Let us generate one for you that meets all security requirements.
        </div>
        """, unsafe_allow_html=True)
        
        # Password generation options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            length = st.slider(
                "Password Length", 
                min_value=8, 
                max_value=32, 
                value=16,
                help="Longer passwords are more secure"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            generate_button = st.button("🔄 Generate", use_container_width=True)
        
        if generate_button or 'generated_password' not in st.session_state:
            # Generate a password if button is clicked or no password exists yet
            st.session_state.generated_password = checker.generate_strong_password(length)
            
            # Check the strength of the generated password
            result = checker.check_password_strength(st.session_state.generated_password)
            st.session_state.password_strength = result
        
        # Display the generated password
        if 'generated_password' in st.session_state:
            st.markdown("""
            <h3 style="margin-top: 1.5rem;">Your Generated Password:</h3>
            """, unsafe_allow_html=True)
            
            # Display password in a styled box
            st.code(st.session_state.generated_password, language=None)
            
            # Copy button
            st.button("📋 Copy to Clipboard", key="copy_button")
            
            # Show strength of generated password
            if 'password_strength' in st.session_state:
                result = st.session_state.password_strength
                st.markdown(f"""
                <div style="margin-top: 1rem;">
                    <p>Password strength: <span style="color: {strength_color[result['strength']]}; font-weight: bold;">
                    {result['emoji']} {result['strength']}</span> (Score: {result['score']}/5)</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 class="subheader">Password Security Best Practices</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>🛡️ Creating Strong Passwords</h3>
            <ul>
                <li>Use at least 12 characters - the more characters, the better</li>
                <li>Include a mix of uppercase and lowercase letters, numbers, and symbols</li>
                <li>Avoid using easily guessable information (birthdays, names, etc.)</li>
                <li>Don't use the same password for multiple accounts</li>
                <li>Consider using a passphrase - a sequence of random words with numbers and symbols</li>
            </ul>
        </div>
        
        <div class="card">
            <h3>🔒 Managing Your Passwords</h3>
            <ul>
                <li>Use a password manager to store and generate unique passwords</li>
                <li>Enable two-factor authentication (2FA) whenever possible</li>
                <li>Change passwords regularly, especially for critical accounts</li>
                <li>Never share your passwords with others</li>
                <li>Check if your accounts have been compromised on sites like Have I Been Pwned</li>
            </ul>
        </div>
        
        <div class="card">
            <h3>⚠️ Common Password Mistakes</h3>
            <ul>
                <li>Using personal information (names, birthdays, etc.)</li>
                <li>Using common words or phrases ("password", "qwerty", etc.)</li>
                <li>Using sequential patterns ("123456", "abcdef", etc.)</li>
                <li>Using the same password across multiple sites</li>
                <li>Writing passwords down on paper or in unencrypted files</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🔐 Password Strength Analyzer | Created with Python & Streamlit</p>
        <p>Remember: A strong password is your first line of defense against cyber threats!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()