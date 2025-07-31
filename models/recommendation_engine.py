from typing import Dict, Any, List, Tuple
import random


class RecommendationEngine:
    """Generates personalized diet and workout recommendations based on health analysis"""
    
    def __init__(self):
        self.diet_recommendations = self._initialize_diet_database()
        self.workout_recommendations = self._initialize_workout_database()
    
    def generate_recommendations(self, health_data_or_analysis, user_info_or_gender=None, age=None, strategy='optimal') -> Dict[str, Any]:
        """Generate comprehensive recommendations - supports both old and new interfaces"""
        
        # Handle different calling patterns for backward compatibility
        if isinstance(user_info_or_gender, dict):
            # New interface: generate_recommendations(analysis_results, user_info)
            analysis = health_data_or_analysis
            user_info = user_info_or_gender
        elif isinstance(user_info_or_gender, str):
            # Old interface: generate_recommendations(health_data, gender, age, strategy)
            health_data = health_data_or_analysis
            gender = user_info_or_gender
            age = age or 30
            strategy = strategy or 'optimal'
            
            user_info = {'gender': gender, 'age': age, 'strategy': strategy}
            
            # Create a mock analysis structure for compatibility
            analysis = {
                'parameter_analysis': {},
                'overall_score': 75,
                'risk_level': 'Moderate Risk'
            }
            
            # Add basic parameter analysis for key parameters
            for param, value in health_data.items():
                if isinstance(value, (int, float)) and value > 0:
                    analysis['parameter_analysis'][param] = {
                        'value': value,
                        'status': 'optimal' if param == 'bmi' and 18.5 <= value <= 24.9 else 'normal',
                        'deviation': 0,
                        'message': f'{param.replace("_", " ").title()} is within normal range'
                    }
        else:
            # Fallback - assume first parameter is analysis
            analysis = health_data_or_analysis
            user_info = user_info_or_gender or {}
        
        # Get priority parameters that need attention
        priority_params = self._get_priority_parameters(analysis)
        
        # Generate diet recommendations
        diet_plan = self._generate_diet_recommendations(analysis, user_info, priority_params)
        
        # Generate workout recommendations
        workout_plan = self._generate_workout_recommendations(analysis, user_info, priority_params)
        
        # Generate lifestyle recommendations
        lifestyle_tips = self._generate_lifestyle_recommendations(analysis, user_info)
        
        # Calculate timeline for improvements
        timeline = self._estimate_improvement_timeline(analysis, priority_params)
        
        return {
            'diet_plan': diet_plan,
            'workout_plan': workout_plan,
            'lifestyle_tips': lifestyle_tips,
            'timeline': timeline,
            'priority_focus': priority_params,
            'overall_strategy': self._generate_overall_strategy(analysis, user_info)
        }
    
    def _initialize_diet_database(self) -> Dict[str, Dict]:
        """Initialize diet recommendation database"""
        return {
            'high_glucose': {
                'foods_to_include': [
                    'Leafy greens (spinach, kale)',
                    'Whole grains (quinoa, brown rice)',
                    'Lean proteins (chicken, fish, tofu)',
                    'Nuts and seeds (almonds, chia seeds)',
                    'Berries (blueberries, strawberries)',
                    'Avocados',
                    'Greek yogurt (unsweetened)'
                ],
                'foods_to_avoid': [
                    'Refined sugars and sweets',
                    'White bread and pasta',
                    'Sugary drinks and sodas',
                    'Processed snacks',
                    'High-glycemic fruits (watermelon, pineapple)'
                ],
                'meal_timing': 'Eat smaller, frequent meals every 3-4 hours',
                'supplements': ['Chromium', 'Alpha-lipoic acid', 'Cinnamon extract']
            },
            'high_cholesterol': {
                'foods_to_include': [
                    'Oats and barley',
                    'Fatty fish (salmon, mackerel)',
                    'Nuts (walnuts, almonds)',
                    'Olive oil',
                    'Beans and legumes',
                    'Apples and citrus fruits',
                    'Vegetables (eggplant, okra)'
                ],
                'foods_to_avoid': [
                    'Saturated fats (red meat, butter)',
                    'Trans fats (fried foods)',
                    'Full-fat dairy products',
                    'Processed meats',
                    'Baked goods with shortening'
                ],
                'meal_timing': 'Include soluble fiber with each meal',
                'supplements': ['Plant sterols', 'Psyllium husk', 'Fish oil']
            },
            'high_blood_pressure': {
                'foods_to_include': [
                    'Bananas (potassium-rich)',
                    'Beets and beet juice',
                    'Dark chocolate (85% cacao)',
                    'Garlic',
                    'Pomegranates',
                    'Low-fat dairy',
                    'Leafy greens'
                ],
                'foods_to_avoid': [
                    'High-sodium foods',
                    'Processed and canned foods',
                    'Alcohol (limit intake)',
                    'Caffeine (if sensitive)',
                    'Pickled foods'
                ],
                'meal_timing': 'Reduce sodium to less than 2300mg daily',
                'supplements': ['Magnesium', 'Potassium', 'Coenzyme Q10']
            },
            'high_bmi': {
                'foods_to_include': [
                    'High-fiber vegetables',
                    'Lean proteins',
                    'Whole grains (portion-controlled)',
                    'Fruits (berries, apples)',
                    'Healthy fats (limited portions)',
                    'Green tea',
                    'Water-rich foods'
                ],
                'foods_to_avoid': [
                    'Calorie-dense processed foods',
                    'Sugary drinks',
                    'Large portions',
                    'Fried foods',
                    'Alcohol'
                ],
                'meal_timing': 'Practice portion control and mindful eating',
                'supplements': ['Green tea extract', 'Conjugated linoleic acid']
            },
            'low_muscle_mass': {
                'foods_to_include': [
                    'Lean proteins (chicken, fish, tofu, legumes)',
                    'Eggs and egg whites',
                    'Greek yogurt and cottage cheese',
                    'Quinoa and brown rice',
                    'Nuts and seeds (almonds, chia seeds)',
                    'Milk and dairy products',
                    'Lean beef and turkey'
                ],
                'foods_to_avoid': [
                    'Excessive processed foods',
                    'Empty calorie snacks',
                    'Excessive alcohol',
                    'High sugar foods without protein'
                ],
                'meal_timing': 'Include protein with every meal and post-workout',
                'supplements': ['Whey protein', 'Creatine', 'BCAAs', 'Vitamin D']
            },
            'high_visceral_fat': {
                'foods_to_include': [
                    'High-fiber vegetables',
                    'Whole grains in moderation',
                    'Lean proteins',
                    'Healthy fats (olive oil, avocado)',
                    'Green tea',
                    'Berries and low-sugar fruits',
                    'Fermented foods (yogurt, kimchi)'
                ],
                'foods_to_avoid': [
                    'Refined sugars and carbohydrates',
                    'Trans fats and fried foods',
                    'Excessive alcohol',
                    'Processed meats',
                    'High-sodium foods'
                ],
                'meal_timing': 'Intermittent fasting may be beneficial',
                'supplements': ['Omega-3', 'Probiotics', 'Green tea extract']
            },
            'low_body_water': {
                'foods_to_include': [
                    'Water-rich fruits (watermelon, cucumber)',
                    'Leafy greens',
                    'Coconut water',
                    'Herbal teas',
                    'Soups and broths',
                    'Electrolyte-rich foods'
                ],
                'foods_to_avoid': [
                    'Excessive caffeine',
                    'Alcohol',
                    'High-sodium processed foods',
                    'Diuretic substances'
                ],
                'meal_timing': 'Drink water throughout the day, especially before meals',
                'supplements': ['Electrolyte supplements', 'Magnesium']
            },
            'optimal': {
                'foods_to_include': [
                    'Variety of whole foods',
                    'Lean proteins (fish, poultry, legumes)',
                    'Whole grains (quinoa, brown rice, oats)',
                    'Fruits and vegetables',
                    'Healthy fats (olive oil, nuts, avocado)',
                    'Low-fat dairy or alternatives'
                ],
                'foods_to_avoid': [
                    'Excessive processed foods',
                    'Refined sugars',
                    'Trans fats',
                    'Excessive alcohol',
                    'High sodium foods'
                ],
                'meal_timing': 'Regular, balanced meals throughout the day',
                'supplements': ['Multivitamin', 'Omega-3', 'Vitamin D']
            }
        }
    
    def _initialize_workout_database(self) -> Dict[str, Dict]:
        """Initialize workout recommendation database"""
        return {
            'high_glucose': {
                'cardio': {
                    'frequency': '5-6 days per week',
                    'duration': '30-45 minutes',
                    'intensity': 'Moderate',
                    'exercises': ['Brisk walking', 'Swimming', 'Cycling', 'Elliptical']
                },
                'strength': {
                    'frequency': '2-3 days per week',
                    'duration': '30-40 minutes',
                    'exercises': ['Full body resistance training', 'Circuit training', 'Bodyweight exercises']
                },
                'special_notes': 'Monitor blood sugar before and after exercise'
            },
            'high_cholesterol': {
                'cardio': {
                    'frequency': '4-5 days per week',
                    'duration': '30-60 minutes',
                    'intensity': 'Moderate to vigorous',
                    'exercises': ['Running', 'Cycling', 'Swimming', 'Dancing']
                },
                'strength': {
                    'frequency': '2 days per week',
                    'duration': '30 minutes',
                    'exercises': ['Weight training', 'Resistance bands', 'Functional movements']
                },
                'special_notes': 'Focus on exercises that raise heart rate'
            },
            'high_blood_pressure': {
                'cardio': {
                    'frequency': '4-5 days per week',
                    'duration': '30-45 minutes',
                    'intensity': 'Moderate',
                    'exercises': ['Walking', 'Swimming', 'Low-impact aerobics', 'Yoga']
                },
                'strength': {
                    'frequency': '2 days per week',
                    'duration': '20-30 minutes',
                    'exercises': ['Light to moderate weight training', 'Avoid heavy lifting']
                },
                'special_notes': 'Avoid holding breath during exercises, monitor blood pressure'
            },
            'high_bmi': {
                'cardio': {
                    'frequency': '5-6 days per week',
                    'duration': '45-60 minutes',
                    'intensity': 'Moderate to vigorous',
                    'exercises': ['HIIT', 'Running', 'Cycling', 'Swimming', 'Group fitness classes']
                },
                'strength': {
                    'frequency': '3 days per week',
                    'duration': '30-45 minutes',
                    'exercises': ['Full body strength training', 'Compound movements', 'Circuit training']
                },
                'special_notes': 'Focus on calorie burning and muscle building'
            },
            'low_muscle_mass': {
                'cardio': {
                    'frequency': '3-4 days per week',
                    'duration': '20-30 minutes',
                    'intensity': 'Moderate',
                    'exercises': ['Walking', 'Light cycling', 'Swimming']
                },
                'strength': {
                    'frequency': '4-5 days per week',
                    'duration': '45-60 minutes',
                    'exercises': ['Progressive resistance training', 'Compound movements', 'Free weights', 'Bodyweight exercises']
                },
                'special_notes': 'Focus on progressive overload and adequate protein intake for muscle building'
            },
            'high_visceral_fat': {
                'cardio': {
                    'frequency': '5-6 days per week',
                    'duration': '30-45 minutes',
                    'intensity': 'Moderate to high',
                    'exercises': ['HIIT training', 'Running', 'Cycling', 'Rowing']
                },
                'strength': {
                    'frequency': '3 days per week',
                    'duration': '30-40 minutes',
                    'exercises': ['Full body circuits', 'Core strengthening', 'Metabolic training']
                },
                'special_notes': 'Combine cardio with strength training for optimal visceral fat reduction'
            },
            'optimal': {
                'cardio': {
                    'frequency': '3-4 days per week',
                    'duration': '30-45 minutes',
                    'intensity': 'Moderate',
                    'exercises': ['Variety of cardio activities', 'Mix of steady-state and intervals']
                },
                'strength': {
                    'frequency': '2-3 days per week',
                    'duration': '30-40 minutes',
                    'exercises': ['Progressive strength training', 'Functional movements']
                },
                'special_notes': 'Maintain current fitness level and continue variety'
            }
        }
    
    def _get_priority_parameters(self, analysis: Dict[str, Any]) -> List[str]:
        """Get parameters that need immediate attention"""
        priority = []
        
        # Extract parameter analysis from the new structure
        parameter_analysis = analysis.get('parameter_analysis', analysis)
        
        for param, data in parameter_analysis.items():
            if isinstance(data, dict) and 'deviation' in data:
                deviation = data.get('deviation', 0)
                status = data.get('status', 'unknown')
                
                # Add to priority if significant deviation or non-optimal status
                if deviation > 20 or status in ['high', 'low', 'very_high', 'very_low']:
                    priority.append(param)
        
        # Sort by deviation (highest first)
        priority.sort(key=lambda x: parameter_analysis.get(x, {}).get('deviation', 0), reverse=True)
        return priority
    
    def _generate_diet_recommendations(self, analysis: Dict[str, Any], user_info: Dict[str, Any], priority_params: List[str]) -> Dict[str, Any]:
        """Generate personalized diet recommendations"""
        
        # Determine primary diet strategy based on highest priority parameter
        if not priority_params:
            diet_strategy = 'optimal'
        else:
            primary_issue = priority_params[0]
            if 'glucose' in primary_issue:
                diet_strategy = 'high_glucose'
            elif 'cholesterol' in primary_issue:
                diet_strategy = 'high_cholesterol'
            elif 'blood_pressure' in primary_issue:
                diet_strategy = 'high_blood_pressure'
            elif 'bmi' in primary_issue or 'body_fat' in primary_issue or 'weight' in primary_issue:
                diet_strategy = 'high_bmi'
            elif 'muscle_mass' in primary_issue or 'protein' in primary_issue:
                diet_strategy = 'low_muscle_mass'
            elif 'visceral_fat' in primary_issue:
                diet_strategy = 'high_visceral_fat'
            elif 'body_water' in primary_issue:
                diet_strategy = 'low_body_water'
            else:
                diet_strategy = 'optimal'
        
        # Get base recommendations with fallback
        try:
            base_recommendations = self.diet_recommendations[diet_strategy].copy()
        except KeyError:
            # Fallback to optimal if strategy not found
            diet_strategy = 'optimal'
            base_recommendations = self.diet_recommendations[diet_strategy].copy()
        
        # Calculate daily caloric needs
        daily_calories = self._calculate_daily_calories(user_info)
        
        # Calculate macronutrients based on strategy
        macronutrients = self._calculate_macronutrients(daily_calories, diet_strategy, user_info)
        
        # Generate meal plan
        meal_plan = self._generate_sample_meal_plan(diet_strategy, daily_calories)
        
        return {
            'strategy': diet_strategy,
            'daily_calories': daily_calories,
            'macronutrients': macronutrients,
            'foods_to_include': base_recommendations['foods_to_include'],
            'foods_to_avoid': base_recommendations['foods_to_avoid'],
            'meal_timing': base_recommendations['meal_timing'],
            'supplements': base_recommendations['supplements'],
            'sample_meal_plan': meal_plan
        }
    
    def _generate_workout_recommendations(self, analysis: Dict[str, Any], user_info: Dict[str, Any], priority_params: List[str]) -> Dict[str, Any]:
        """Generate personalized workout recommendations"""
        
        # Determine workout strategy
        if not priority_params:
            workout_strategy = 'optimal'
        else:
            primary_issue = priority_params[0]
            if 'glucose' in primary_issue:
                workout_strategy = 'high_glucose'
            elif 'cholesterol' in primary_issue:
                workout_strategy = 'high_cholesterol'
            elif 'blood_pressure' in primary_issue:
                workout_strategy = 'high_blood_pressure'
            elif 'bmi' in primary_issue or 'body_fat' in primary_issue or 'weight' in primary_issue:
                workout_strategy = 'high_bmi'
            elif 'muscle_mass' in primary_issue or 'protein' in primary_issue:
                workout_strategy = 'low_muscle_mass'
            elif 'visceral_fat' in primary_issue:
                workout_strategy = 'high_visceral_fat'
            else:
                workout_strategy = 'optimal'
        
        # Get base recommendations with fallback
        try:
            base_recommendations = self.workout_recommendations[workout_strategy].copy()
        except KeyError:
            # Fallback to optimal if strategy not found
            workout_strategy = 'optimal'
            base_recommendations = self.workout_recommendations[workout_strategy].copy()
        
        # Generate detailed workout plans
        cardio_plan = self._generate_detailed_cardio_plan(workout_strategy, user_info)
        strength_plan = self._generate_detailed_strength_plan(workout_strategy, user_info)
        
        # Generate weekly workout schedule
        weekly_schedule = self._generate_weekly_workout_schedule(workout_strategy, user_info)
        
        return {
            'strategy': workout_strategy,
            'cardio_plan': cardio_plan,
            'strength_plan': strength_plan,
            'special_notes': base_recommendations['special_notes'],
            'weekly_schedule': weekly_schedule
        }
    
    def _generate_lifestyle_recommendations(self, analysis: Dict[str, Any], user_info: Dict[str, Any]) -> List[str]:
        """Generate general lifestyle recommendations"""
        tips = [
            'Maintain consistent sleep schedule (7-9 hours per night)',
            'Stay hydrated (8-10 glasses of water daily)',
            'Practice stress management techniques',
            'Avoid smoking and limit alcohol consumption',
            'Regular health check-ups and monitoring'
        ]
        
        # Add specific tips based on analysis
        overall_score = analysis.get('overall_score', 50)
        if overall_score < 60:
            tips.extend([
                'Consider working with healthcare professionals',
                'Track daily habits and progress',
                'Start with small, sustainable changes'
            ])
        
        return tips
    
    def _calculate_daily_calories(self, user_info: Dict[str, Any]) -> int:
        """Calculate recommended daily calories using Mifflin-St Jeor equation"""
        try:
            age = int(user_info.get('age', 30))
            weight = float(user_info.get('weight', 70))
            height = float(user_info.get('height', 170))
            gender = user_info.get('gender', 'male').lower()
            activity_level = user_info.get('activity_level', 'moderate')
            
            # Calculate BMR
            if gender == 'male':
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
            # Activity multipliers
            activity_multipliers = {
                'sedentary': 1.2,
                'light': 1.375,
                'moderate': 1.55,
                'active': 1.725,
                'very_active': 1.9
            }
            
            multiplier = activity_multipliers.get(activity_level, 1.55)
            daily_calories = int(bmr * multiplier)
            
            return daily_calories
            
        except (ValueError, TypeError):
            return 2000  # Default value
    
    def _calculate_macronutrients(self, daily_calories: int, strategy: str, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate macronutrient distribution based on strategy and user needs"""
        weight = float(user_info.get('weight', 70))
        
        # Macronutrient ratios based on strategy
        macro_ratios = {
            'low_muscle_mass': {'protein': 0.30, 'carbs': 0.40, 'fat': 0.30},  # High protein for muscle building
            'high_bmi': {'protein': 0.25, 'carbs': 0.35, 'fat': 0.40},  # Higher fat, lower carbs for weight loss
            'high_glucose': {'protein': 0.25, 'carbs': 0.30, 'fat': 0.45},  # Lower carbs for glucose control
            'high_cholesterol': {'protein': 0.25, 'carbs': 0.50, 'fat': 0.25},  # Lower fat for cholesterol
            'high_blood_pressure': {'protein': 0.20, 'carbs': 0.55, 'fat': 0.25},  # DASH diet style
            'optimal': {'protein': 0.25, 'carbs': 0.45, 'fat': 0.30}  # Balanced approach
        }
        
        ratios = macro_ratios.get(strategy, macro_ratios['optimal'])
        
        # Calculate grams
        protein_calories = daily_calories * ratios['protein']
        carb_calories = daily_calories * ratios['carbs']
        fat_calories = daily_calories * ratios['fat']
        
        # Convert to grams (protein: 4 cal/g, carbs: 4 cal/g, fat: 9 cal/g)
        protein_grams = round(protein_calories / 4)
        carb_grams = round(carb_calories / 4)
        fat_grams = round(fat_calories / 9)
        
        # Ensure protein meets minimum requirements (0.8-1.2g per kg body weight)
        min_protein = round(weight * 0.8)
        optimal_protein = round(weight * 1.2)
        
        if protein_grams < min_protein:
            protein_grams = min_protein
        elif strategy == 'low_muscle_mass' and protein_grams < optimal_protein:
            protein_grams = optimal_protein
        
        return {
            'protein_grams': protein_grams,
            'carb_grams': carb_grams,
            'fat_grams': fat_grams,
            'protein_calories': protein_grams * 4,
            'carb_calories': carb_grams * 4,
            'fat_calories': fat_grams * 9,
            'protein_percentage': round((protein_grams * 4 / daily_calories) * 100),
            'carb_percentage': round((carb_grams * 4 / daily_calories) * 100),
            'fat_percentage': round((fat_grams * 9 / daily_calories) * 100)
        }
    
    def _generate_sample_meal_plan(self, strategy: str, daily_calories: int) -> Dict[str, List[str]]:
        """Generate a sample daily meal plan"""
        
        meal_plans = {
            'high_glucose': {
                'breakfast': ['Steel-cut oats with berries and nuts', 'Greek yogurt with cinnamon'],
                'lunch': ['Grilled chicken salad with olive oil dressing', 'Quinoa with vegetables'],
                'dinner': ['Baked salmon with steamed broccoli', 'Small portion of brown rice'],
                'snacks': ['Apple with almond butter', 'Handful of walnuts']
            },
            'high_cholesterol': {
                'breakfast': ['Oatmeal with ground flaxseed and berries', 'Green tea'],
                'lunch': ['Lentil soup with whole grain roll', 'Mixed green salad'],
                'dinner': ['Grilled fish with roasted vegetables', 'Barley pilaf'],
                'snacks': ['Handful of almonds', 'Apple slices']
            },
            'high_blood_pressure': {
                'breakfast': ['Low-sodium whole grain cereal with banana', 'Low-fat milk'],
                'lunch': ['Turkey and vegetable wrap (low-sodium)', 'Fresh fruit'],
                'dinner': ['Herb-seasoned chicken breast', 'Steamed vegetables', 'Sweet potato'],
                'snacks': ['Unsalted nuts', 'Fresh berries']
            },
            'high_bmi': {
                'breakfast': ['Vegetable omelet with spinach', 'Whole grain toast (1 slice)'],
                'lunch': ['Large salad with grilled protein', 'Light vinaigrette'],
                'dinner': ['Lean protein with roasted vegetables', 'Small portion complex carbs'],
                'snacks': ['Raw vegetables with hummus', 'Greek yogurt']
            },
            'optimal': {
                'breakfast': ['Balanced meal with protein, healthy fats, and complex carbs'],
                'lunch': ['Lean protein with vegetables and whole grains'],
                'dinner': ['Variety of nutrients in appropriate portions'],
                'snacks': ['Nutritious options like fruits, nuts, or yogurt']
            }
        }
        
        return meal_plans.get(strategy, meal_plans['optimal'])
    
    def _generate_weekly_workout_schedule(self, strategy: str, user_info: Dict[str, Any]) -> Dict[str, str]:
        """Generate a weekly workout schedule"""
        
        schedules = {
            'high_glucose': {
                'Monday': 'Cardio (30 min walking) + Light strength training',
                'Tuesday': 'Moderate cardio (cycling or swimming)',
                'Wednesday': 'Strength training (full body)',
                'Thursday': 'Cardio (30 min)',
                'Friday': 'Strength training + Flexibility',
                'Saturday': 'Longer cardio session (45 min)',
                'Sunday': 'Active recovery (gentle yoga or walking)'
            },
            'high_cholesterol': {
                'Monday': 'Moderate cardio (30-45 min)',
                'Tuesday': 'Strength training (upper body)',
                'Wednesday': 'Cardio (running or cycling)',
                'Thursday': 'Strength training (lower body)',
                'Friday': 'High-intensity cardio',
                'Saturday': 'Full body strength training',
                'Sunday': 'Active recovery or light cardio'
            },
            'high_blood_pressure': {
                'Monday': 'Gentle cardio (walking or swimming)',
                'Tuesday': 'Light strength training',
                'Wednesday': 'Yoga or tai chi',
                'Thursday': 'Moderate cardio',
                'Friday': 'Strength training (avoid heavy lifting)',
                'Saturday': 'Cardio activity of choice',
                'Sunday': 'Relaxation and stretching'
            },
            'high_bmi': {
                'Monday': 'HIIT training (20-30 min)',
                'Tuesday': 'Strength training (full body)',
                'Wednesday': 'Cardio (45-60 min)',
                'Thursday': 'Strength training (upper body)',
                'Friday': 'Cardio + core work',
                'Saturday': 'Strength training (lower body)',
                'Sunday': 'Active recovery (hiking, sports)'
            },
            'optimal': {
                'Monday': 'Cardio workout',
                'Tuesday': 'Strength training',
                'Wednesday': 'Cardio or sports activity',
                'Thursday': 'Strength training',
                'Friday': 'Flexible workout (cardio or strength)',
                'Saturday': 'Longer activity session',
                'Sunday': 'Rest or gentle activity'
            }
        }
        
        return schedules.get(strategy, schedules['optimal'])
    
    def _estimate_improvement_timeline(self, analysis: Dict[str, Any], priority_params: List[str]) -> Dict[str, str]:
        """Estimate timeline for health improvements"""
        
        timeline = {}
        
        if not priority_params:
            timeline['overall'] = 'Continue current healthy habits for maintenance'
            return timeline
        
        # General improvement timelines
        parameter_timelines = {
            'glucose': '2-3 months for significant improvement',
            'cholesterol': '6-8 weeks for noticeable changes',
            'blood_pressure': '4-6 weeks with consistent lifestyle changes',
            'bmi': '3-6 months for healthy weight loss',
            'body_fat_percentage': '2-4 months with proper diet and exercise'
        }
        
        for param in priority_params:
            for key, timeline_text in parameter_timelines.items():
                if key in param:
                    timeline[param] = timeline_text
                    break
        
        overall_score = analysis.get('overall_score', 50)
        if overall_score < 40:
            timeline['overall'] = '6-12 months for comprehensive health improvement'
        elif overall_score < 60:
            timeline['overall'] = '3-6 months for significant improvements'
        else:
            timeline['overall'] = '1-3 months for optimization'
        
        return timeline
    
    def _generate_overall_strategy(self, analysis: Dict[str, Any], user_info: Dict[str, Any]) -> str:
        """Generate an overall strategy summary"""
        
        overall_score = analysis.get('overall_score', 50)
        
        if overall_score >= 80:
            return "Focus on maintenance and optimization of current healthy habits. Continue regular monitoring and make minor adjustments as needed."
        
        elif overall_score >= 60:
            return "Implement moderate lifestyle changes with emphasis on diet quality and regular exercise. Monitor progress closely and adjust as needed."
        
        elif overall_score >= 40:
            return "Significant lifestyle modifications required. Focus on fundamental changes in diet, exercise, and daily habits. Consider professional guidance."
        
        else:
            return "Comprehensive health overhaul needed. Implement immediate changes in diet and exercise. Strongly recommend consulting healthcare professionals for medical guidance."

    def _generate_detailed_cardio_plan(self, strategy: str, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed cardio workout plan"""
        cardio_plans = {
            'low_muscle_mass': {
                'frequency': '3-4 days per week',
                'duration': '20-30 minutes',
                'intensity': 'Moderate',
                'type': 'Low-impact cardio to preserve muscle',
                'examples': ['Brisk walking', 'Light cycling', 'Swimming', 'Elliptical'],
                'notes': 'Keep cardio moderate to avoid muscle loss'
            },
            'high_bmi': {
                'frequency': '5-6 days per week',
                'duration': '45-60 minutes',
                'intensity': 'Moderate to High',
                'type': 'Fat-burning cardio',
                'examples': ['HIIT training', 'Running', 'Cycling', 'Rowing', 'Dancing'],
                'notes': 'Mix steady-state and interval training'
            },
            'high_glucose': {
                'frequency': '5 days per week',
                'duration': '30-45 minutes',
                'intensity': 'Moderate',
                'type': 'Blood sugar control cardio',
                'examples': ['Walking after meals', 'Swimming', 'Cycling', 'Dancing'],
                'notes': 'Exercise within 30 minutes after meals'
            },
            'optimal': {
                'frequency': '3-4 days per week',
                'duration': '30-45 minutes',
                'intensity': 'Moderate',
                'type': 'General fitness cardio',
                'examples': ['Running', 'Cycling', 'Swimming', 'Group fitness'],
                'notes': 'Vary activities to prevent boredom'
            }
        }
        
        return cardio_plans.get(strategy, cardio_plans['optimal'])

    def _generate_detailed_strength_plan(self, strategy: str, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed strength training plan"""
        strength_plans = {
            'low_muscle_mass': {
                'frequency': '4-5 days per week',
                'duration': '45-60 minutes',
                'focus': 'Muscle building and strength',
                'sets_reps': '3-4 sets of 6-12 reps',
                'exercises': [
                    'Compound movements: Squats, Deadlifts, Bench Press',
                    'Pull-ups/Chin-ups or Lat Pulldowns',
                    'Overhead Press, Rows',
                    'Progressive overload essential'
                ],
                'notes': 'Focus on compound exercises with progressive overload'
            },
            'high_bmi': {
                'frequency': '3-4 days per week',
                'duration': '30-45 minutes',
                'focus': 'Fat loss and muscle preservation',
                'sets_reps': '2-3 sets of 12-15 reps',
                'exercises': [
                    'Full-body circuit training',
                    'Bodyweight exercises',
                    'Light to moderate weights',
                    'Functional movements'
                ],
                'notes': 'Higher reps with shorter rest periods'
            },
            'optimal': {
                'frequency': '3-4 days per week',
                'duration': '45 minutes',
                'focus': 'General strength and fitness',
                'sets_reps': '3 sets of 8-12 reps',
                'exercises': [
                    'Balanced upper/lower body',
                    'Core strengthening',
                    'Flexibility work',
                    'Progressive training'
                ],
                'notes': 'Maintain balanced muscle development'
            }
        }
        
        return strength_plans.get(strategy, strength_plans['optimal'])
