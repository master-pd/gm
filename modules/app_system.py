"""
Mini Apps System for Telegram Bot
"""

import random
import math
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class MiniAppsSystem:
    """Collection of Mini Applications"""
    
    def __init__(self):
        self.dictionary_db = self._load_dictionary()
        self.jokes_db = self._load_jokes()
        self.quotes_db = self._load_quotes()
        self.facts_db = self._load_facts()
        
    def _load_dictionary(self) -> Dict:
        """Load dictionary database"""
        return {
            'hello': {'bn': 'হ্যালো/সালাম', 'en': 'Hello/Hi'},
            'thanks': {'bn': 'ধন্যবাদ', 'en': 'Thank you'},
            'good': {'bn': 'ভাল', 'en': 'Good'},
            'bad': {'bn': 'খারাপ', 'en': 'Bad'},
            'computer': {'bn': 'কম্পিউটার', 'en': 'Computer'},
            'programming': {'bn': 'প্রোগ্রামিং', 'en': 'Programming'},
            'telegram': {'bn': 'টেলিগ্রাম', 'en': 'Telegram'},
            'bot': {'bn': 'বট', 'en': 'Bot'},
            'python': {'bn': 'পাইথন', 'en': 'Python'},
            'ai': {'bn': 'কৃত্রিম বুদ্ধিমত্তা', 'en': 'Artificial Intelligence'},
            'firebase': {'bn': 'ফায়ারবেস', 'en': 'Firebase'},
            'database': {'bn': 'ডাটাবেস', 'en': 'Database'},
            'learning': {'bn': 'শেখা', 'en': 'Learning'},
            'group': {'bn': 'গ্রুপ', 'en': 'Group'},
            'message': {'bn': 'মেসেজ', 'en': 'Message'},
            'game': {'bn': 'খেলা', 'en': 'Game'},
            'money': {'bn': 'টাকা', 'en': 'Money'},
            'time': {'bn': 'সময়', 'en': 'Time'},
            'weather': {'bn': 'আবহাওয়া', 'en': 'Weather'},
            'help': {'bn': 'সাহায্য', 'en': 'Help'}
        }
    
    def _load_jokes(self) -> List[str]:
        """Load jokes database"""
        return [
            "কেন কম্পিউটার ডাক্তারের কাছে গেল? কারণ তার ভাইরাস ছিল!",
            "পাইথন প্রোগ্রামার কেন সমুদ্র পছন্দ করে? কারণ সেখানে অনেক 'সি'!",
            "কেন প্রোগ্রামাররা প্রকৃতি পছন্দ করে না? কারণ সেখানে অনেক বাগ!",
            "আমি এমন এক বট যিনি নিজে নিজে শেখে, কিন্তু এখনও জানি না কীভাবে কফি বানাতে হয়!",
            "বাংলাদেশের সবচেয়ে দ্রুতগতির কী? আমার কোড যখন একটি বাগ খুঁজে পায়!",
            "কেন AI বট গণিত এত পছন্দ করে? কারণ এটি সবসময় সংখ্যা চিন্তা করে!",
            "আমার AI ব্রেন এত বড় কেন? কারণ আমি অনেক গল্প শুনি কিন্তু ভুলে যাই!"
        ]
    
    def _load_quotes(self) -> List[str]:
        """Load quotes database"""
        return [
            "মহান কাজের একমাত্র উপায় হলো আপনি যা করেন তা ভালবাসা। - স্টিভ জবস",
            "নতুনত্ব একজন নেতা ও অনুসারীর মধ্যে পার্থক্য তৈরি করে। - স্টিভ জবস",
            "যত বেশি পরিশ্রম করবে, তত বেশি সৌভাগ্যবান হবে। - বাংলা প্রবাদ",
            "সফলতা আসে সিদ্ধান্ত নেওয়ার পর কঠোর পরিশ্রম থেকে। - অজানা",
            "কখনো হাল ছাড়বেন না, কারণ জীবনের সবচেয়ে বড় অর্জন কঠোর পরিশ্রমের ফল। - অজানা",
            "শেখা কখনই বৃদ্ধ হয় না, মস্তিষ্ক কখনই পূর্ণ হয় না। - লিওনার্দো দা ভিঞ্চি",
            "ভবিষ্যতের জন্য সেরা প্রস্তুতি হলো বর্তমানকে সেরা ভাবে ব্যবহার করা। - উইলিয়াম ওস্লার"
        ]
    
    def _load_facts(self) -> List[str]:
        """Load facts database"""
        return [
            "মানুষের মস্তিষ্ক দিনে প্রায় ৭০,০০০ বার চিন্তা করে।",
            "পাইথন ভাষার নাম একটি কমেডি শো 'মন্টি পাইথন' থেকে নেওয়া হয়েছে।",
            "টেলিগ্রাম প্রতি মাসে ৭০০ মিলিয়নের বেশি সক্রিয় ব্যবহারকারী রয়েছে।",
            "বাংলা বিশ্বের ৭ম সবচেয়ে বেশি কথিত ভাষা।",
            "কৃত্রিম বুদ্ধিমত্তা প্রথমবার ১৯৫৬ সালে Dartmouth Conference-এ প্রস্তাবিত হয়েছিল।",
            "ফায়ারবেস Google-এর একটি মোবাইল ওয়েব অ্যাপ্লিকেশন প্ল্যাটফর্ম।",
            "প্রথম কম্পিউটার বাগ আসলে একটি প্রকৃত পোকা ছিল যা একটি কম্পিউটারে আটকে গিয়েছিল।"
        ]
    
    # ==================== CALCULATOR ====================
    
    async def calculator(self, expression: str) -> str:
        """Advanced calculator with error handling"""
        try:
            # Clean and validate expression
            expression = expression.strip()
            
            # Security check: only allow safe characters
            safe_pattern = r'^[0-9+\-*/().\s^√πe]+$'
            if not re.match(safe_pattern, expression):
                return "❌ Invalid characters in expression"
            
            # Replace common symbols
            expression = expression.replace('^', '**').replace('×', '*').replace('÷', '/')
            
            # Handle special constants
            expression = expression.replace('π', str(math.pi)).replace('pi', str(math.pi))
            expression = expression.replace('e', str(math.e))
            
            # Handle square root
            if '√' in expression:
                parts = expression.split('√')
                if len(parts) == 2:
                    number = parts[1].strip()
                    if number.isdigit() or ('.' in number and number.replace('.', '').isdigit()):
                        result = math.sqrt(float(number))
                        return f"✅ √{number} = {result:.6f}"
            
            # Evaluate expression
            result = eval(expression, {"__builtins__": {}}, {
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
                'exp': math.exp, 'abs': abs, 'round': round,
                'pi': math.pi, 'e': math.e
            })
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 6)
            
            return f"✅ Result: {result}"
            
        except ZeroDivisionError:
            return "❌ Error: Division by zero"
        except ValueError as e:
            return f"❌ Error: {str(e)}"
        except SyntaxError:
            return "❌ Error: Invalid expression syntax"
        except Exception as e:
            return f"❌ Calculation error: {str(e)}"
    
    # ==================== DICTIONARY ====================
    
    async def dictionary(self, word: str, language: str = 'bn') -> str:
        """Dictionary with multiple languages"""
        word_lower = word.lower().strip()
        
        if word_lower in self.dictionary_db:
            entry = self.dictionary_db[word_lower]
            
            if language == 'bn' and 'bn' in entry:
                return f"📚 *{word}:* {entry['bn']}"
            elif language == 'en' and 'en' in entry:
                return f"📚 *{word}:* {entry['en']}"
            else:
                # Return all available translations
                translations = []
                if 'bn' in entry:
                    translations.append(f"বাংলা: {entry['bn']}")
                if 'en' in entry:
                    translations.append(f"English: {entry['en']}")
                
                return f"📚 *{word}:*\n" + "\n".join(translations)
        else:
            # Find similar words
            similar = []
            for dict_word in self.dictionary_db:
                if word_lower in dict_word or dict_word in word_lower:
                    similar.append(dict_word)
                    if len(similar) >= 5:
                        break
            
            if similar:
                return f"❌ '{word}' not found. Similar words: {', '.join(similar[:5])}"
            else:
                return f"❌ '{word}' not found in dictionary"
    
    # ==================== UNIT CONVERTER ====================
    
    async def unit_converter(self, value: float, from_unit: str, to_unit: str) -> str:
        """Unit converter for various measurements"""
        
        conversions = {
            # Length
            'meter_kilometer': 0.001,
            'kilometer_meter': 1000,
            'meter_centimeter': 100,
            'centimeter_meter': 0.01,
            'meter_mile': 0.000621371,
            'mile_meter': 1609.34,
            'meter_foot': 3.28084,
            'foot_meter': 0.3048,
            'meter_inch': 39.3701,
            'inch_meter': 0.0254,
            
            # Weight
            'kilogram_gram': 1000,
            'gram_kilogram': 0.001,
            'kilogram_pound': 2.20462,
            'pound_kilogram': 0.453592,
            'kilogram_ounce': 35.274,
            'ounce_kilogram': 0.0283495,
            
            # Temperature
            'celsius_fahrenheit': lambda c: (c * 9/5) + 32,
            'fahrenheit_celsius': lambda f: (f - 32) * 5/9,
            'celsius_kelvin': lambda c: c + 273.15,
            'kelvin_celsius': lambda k: k - 273.15,
            
            # Area
            'squaremeter_squarekilometer': 0.000001,
            'squarekilometer_squaremeter': 1000000,
            'squaremeter_hectare': 0.0001,
            'hectare_squaremeter': 10000,
            
            # Volume
            'liter_milliliter': 1000,
            'milliliter_liter': 0.001,
            'liter_gallon': 0.264172,
            'gallon_liter': 3.78541,
            
            # Time
            'second_minute': 1/60,
            'minute_second': 60,
            'minute_hour': 1/60,
            'hour_minute': 60,
            'hour_day': 1/24,
            'day_hour': 24,
            
            # Digital Storage
            'byte_kilobyte': 1/1024,
            'kilobyte_byte': 1024,
            'kilobyte_megabyte': 1/1024,
            'megabyte_kilobyte': 1024,
            'megabyte_gigabyte': 1/1024,
            'gigabyte_megabyte': 1024,
            
            # Currency (approximate rates)
            'usd_bdt': 110.0,  # USD to BDT
            'bdt_usd': 1/110.0,  # BDT to USD
            'eur_bdt': 120.0,  # EUR to BDT
            'bdt_eur': 1/120.0,  # BDT to EUR
            'inr_bdt': 1.3,  # INR to BDT
            'bdt_inr': 1/1.3  # BDT to INR
        }
        
        # Create conversion key
        conversion_key = f"{from_unit.lower()}_{to_unit.lower()}"
        
        if conversion_key in conversions:
            conv = conversions[conversion_key]
            
            if callable(conv):
                # For temperature and other special conversions
                result = conv(value)
                return f"🔀 {value:.2f} {from_unit} = {result:.2f} {to_unit}"
            else:
                # For simple multiplication conversions
                result = value * conv
                return f"🔀 {value:.2f} {from_unit} = {result:.2f} {to_unit}"
        else:
            return f"❌ Conversion from {from_unit} to {to_unit} not supported"
    
    # ==================== PASSWORD GENERATOR ====================
    
    async def generate_password(self, length: int = 12, include_special: bool = True) -> str:
        """Generate secure password"""
        import string
        
        if length < 4:
            return "❌ Password length must be at least 4 characters"
        if length > 32:
            return "❌ Password length cannot exceed 32 characters"
        
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure at least one character from each set
        password_chars = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits)
        ]
        
        if include_special:
            password_chars.append(random.choice(special))
        
        # Fill remaining characters
        all_chars = lowercase + uppercase + digits
        if include_special:
            all_chars += special
        
        password_chars.extend(random.choice(all_chars) for _ in range(length - len(password_chars)))
        
        # Shuffle password
        random.shuffle(password_chars)
        password = ''.join(password_chars)
        
        # Calculate password strength
        strength = self._calculate_password_strength(password)
        
        return f"🔐 *Password:* `{password}`\n💪 *Strength:* {strength}"
    
    def _calculate_password_strength(self, password: str) -> str:
        """Calculate password strength"""
        score = 0
        
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 1
        
        if score >= 5:
            return "Strong 🔥"
        elif score >= 3:
            return "Medium ⚡"
        else:
            return "Weak ⚠️"
    
    # ==================== BMI CALCULATOR ====================
    
    async def bmi_calculator(self, weight_kg: float, height_cm: float) -> str:
        """BMI calculator with detailed analysis"""
        if weight_kg <= 0 or height_cm <= 0:
            return "❌ Weight and height must be positive values"
        
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        # Determine category
        if bmi < 18.5:
            category = "Underweight"
            advice = "You should consider gaining some weight. Eat nutritious food."
        elif bmi < 25:
            category = "Normal weight"
            advice = "Great! Maintain your current weight with balanced diet."
        elif bmi < 30:
            category = "Overweight"
            advice = "Consider moderate exercise and balanced diet."
        else:
            category = "Obese"
            advice = "Consult with a doctor for weight management plan."
        
        # Calculate ideal weight range
        min_ideal = 18.5 * (height_m ** 2)
        max_ideal = 25 * (height_m ** 2)
        
        return (
            f"⚖️ *BMI Calculator*\n\n"
            f"📊 *Your BMI:* {bmi:.1f}\n"
            f"📈 *Category:* {category}\n"
            f"🎯 *Ideal Weight Range:* {min_ideal:.1f} - {max_ideal:.1f} kg\n"
            f"💡 *Advice:* {advice}"
        )
    
    # ==================== AGE CALCULATOR ====================
    
    async def age_calculator(self, birth_date: str) -> str:
        """Calculate age from birth date"""
        try:
            # Try different date formats
            formats = ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']
            
            birth = None
            for fmt in formats:
                try:
                    birth = datetime.strptime(birth_date, fmt)
                    break
                except ValueError:
                    continue
            
            if birth is None:
                return "❌ Invalid date format. Try: YYYY-MM-DD, DD-MM-YYYY, or MM/DD/YYYY"
            
            today = datetime.now()
            
            # Calculate age
            age_years = today.year - birth.year
            age_months = today.month - birth.month
            age_days = today.day - birth.day
            
            # Adjust for negative months/days
            if age_days < 0:
                age_months -= 1
                # Get days in previous month
                prev_month = today.month - 1 if today.month > 1 else 12
                prev_year = today.year if today.month > 1 else today.year - 1
                days_in_prev_month = 31  # Simplified
                age_days += days_in_prev_month
            
            if age_months < 0:
                age_years -= 1
                age_months += 12
            
            # Calculate next birthday
            next_birthday_year = today.year
            next_birthday = datetime(next_birthday_year, birth.month, birth.day)
            
            if next_birthday < today:
                next_birthday = datetime(next_birthday_year + 1, birth.month, birth.day)
            
            days_to_birthday = (next_birthday - today).days
            
            # Zodiac sign (simplified)
            zodiac = self._get_zodiac_sign(birth.month, birth.day)
            
            return (
                f"🎂 *Age Calculator*\n\n"
                f"📅 *Birth Date:* {birth.strftime('%d %B %Y')}\n"
                f"🎈 *Age:* {age_years} years, {age_months} months, {age_days} days\n"
                f"⭐ *Zodiac:* {zodiac}\n"
                f"🎉 *Next Birthday:* {next_birthday.strftime('%d %B %Y')}\n"
                f"⏳ *Days to Birthday:* {days_to_birthday} days"
            )
            
        except Exception as e:
            return f"❌ Error calculating age: {str(e)}"
    
    def _get_zodiac_sign(self, month: int, day: int) -> str:
        """Get zodiac sign from birth date"""
        if (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Aquarius"
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return "Pisces"
        elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Sagittarius"
        else:
            return "Capricorn"
    
    # ==================== ENTERTAINMENT ====================
    
    async def tell_joke(self) -> str:
        """Tell a random joke"""
        if self.jokes_db:
            return random.choice(self.jokes_db)
        return "😄 Why did the AI cross the road? To learn about the other side!"
    
    async def get_quote(self) -> str:
        """Get inspirational quote"""
        if self.quotes_db:
            return random.choice(self.quotes_db)
        return "💫 The only way to do great work is to love what you do."
    
    async def get_fact(self) -> str:
        """Get interesting fact"""
        if self.facts_db:
            return random.choice(self.facts_db)
        return "🧠 Did you know? The human brain generates about 70,000 thoughts per day."
    
    # ==================== WEATHER SIMULATOR ====================
    
    async def weather_info(self, city: str = "") -> str:
        """Simulated weather information"""
        # This is a simulated weather system since we don't use external APIs
        cities_weather = {
            'dhaka': {'temp': 32, 'condition': 'Partly Cloudy', 'humidity': 65},
            'chittagong': {'temp': 30, 'condition': 'Sunny', 'humidity': 70},
            'khulna': {'temp': 33, 'condition': 'Clear', 'humidity': 60},
            'rajshahi': {'temp': 34, 'condition': 'Sunny', 'humidity': 55},
            'sylhet': {'temp': 29, 'condition': 'Rainy', 'humidity': 80}
        }
        
        city_lower = city.lower() if city else 'dhaka'
        
        if city_lower in cities_weather:
            weather = cities_weather[city_lower]
        else:
            # Generate random weather for unknown cities
            weather = {
                'temp': random.randint(25, 35),
                'condition': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy', 'Clear']),
                'humidity': random.randint(50, 85)
            }
        
        # Weather advice
        advice = ""
        if weather['condition'] == 'Rainy':
            advice = "Don't forget your umbrella! ☔"
        elif weather['temp'] > 32:
            advice = "Stay hydrated! 💧"
        elif weather['temp'] < 28:
            advice = "Wear something warm! 🧥"
        else:
            advice = "Perfect weather! 👍"
        
        return (
            f"🌤️ *Weather for {city.title() if city else 'Current Location'}*\n\n"
            f"🌡️ *Temperature:* {weather['temp']}°C\n"
            f"☁️ *Condition:* {weather['condition']}\n"
            f"💧 *Humidity:* {weather['humidity']}%\n"
            f"💡 *Advice:* {advice}"
        )
    
    # ==================== TIME AND DATE ====================
    
    async def get_current_time(self, timezone: str = "Asia/Dhaka") -> str:
        """Get current time"""
        from datetime import datetime
        import pytz
        
        try:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            
            # Format time in multiple formats
            time_12hr = current_time.strftime("%I:%M:%S %p")
            time_24hr = current_time.strftime("%H:%M:%S")
            date_full = current_time.strftime("%A, %d %B %Y")
            
            # Bengali date (simplified)
            bengali_months = [
                'জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন',
                'জুলাই', 'আগস্ট', 'সেপ্টেম্বর', 'অক্টোবর', 'নভেম্বর', 'ডিসেম্বর'
            ]
            bengali_date = f"{current_time.day} {bengali_months[current_time.month-1]} {current_time.year}"
            
            return (
                f"⏰ *Current Time*\n\n"
                f"📅 *Date:* {date_full}\n"
                f"🇧🇩 *বাংলা তারিখ:* {bengali_date}\n"
                f"🕐 *Time (12-hour):* {time_12hr}\n"
                f"🕑 *Time (24-hour):* {time_24hr}\n"
                f"🌍 *Timezone:* {timezone}"
            )
            
        except:
            # Fallback if pytz not available
            current_time = datetime.now()
            return (
                f"⏰ *Current Time*\n\n"
                f"📅 *Date:* {current_time.strftime('%A, %d %B %Y')}\n"
                f"🕐 *Time:* {current_time.strftime('%H:%M:%S')}"
            )