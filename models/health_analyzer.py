from typing import Dict, Any, List

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import numpy as np
except ImportError:
    # Fallback for systems without numpy
    class NumpyFallback:
        def mean(self, values):
            return sum(values) / len(values) if values else 0
    np = NumpyFallback()


class HealthAnalyzer:
    """Analyzes health parameters and compares them with ideal ranges"""
    
    def __init__(self):
        # Define ideal ranges for various health parameters
        self.ideal_ranges = {
            # Basic health parameters
            'glucose': {'min': 70, 'max': 100, 'unit': 'mg/dL'},
            'cholesterol_total': {'min': 0, 'max': 200, 'unit': 'mg/dL'},
            'cholesterol_hdl': {'min': 40, 'max': 999, 'unit': 'mg/dL'},  # Higher is better
            'cholesterol_ldl': {'min': 0, 'max': 100, 'unit': 'mg/dL'},
            'blood_pressure_systolic': {'min': 90, 'max': 120, 'unit': 'mmHg'},
            'blood_pressure_diastolic': {'min': 60, 'max': 80, 'unit': 'mmHg'},
            'bmi': {'min': 18.5, 'max': 24.9, 'unit': 'kg/m²'},
            'body_fat_percentage': {
                'male': {'min': 10, 'max': 18, 'unit': '%'},
                'female': {'min': 16, 'max': 24, 'unit': '%'}
            },
            # InBody specific parameters
            'weight': {
                'male': {'min': 50, 'max': 85, 'unit': 'kg'},
                'female': {'min': 40, 'max': 70, 'unit': 'kg'}
            },
            'muscle_mass': {
                'male': {'min': 30, 'max': 50, 'unit': 'kg'},
                'female': {'min': 20, 'max': 35, 'unit': 'kg'}
            },
            'protein': {
                'male': {'min': 8, 'max': 12, 'unit': 'kg'},
                'female': {'min': 6, 'max': 9, 'unit': 'kg'}
            },
            'minerals': {'min': 2.0, 'max': 4.0, 'unit': 'kg'},
            'total_body_water': {
                'male': {'min': 25, 'max': 40, 'unit': 'L'},
                'female': {'min': 20, 'max': 30, 'unit': 'L'}
            },
            'visceral_fat_level': {'min': 1, 'max': 9, 'unit': 'level'},
            'basal_metabolic_rate': {
                'male': {'min': 1400, 'max': 1800, 'unit': 'kcal'},
                'female': {'min': 1000, 'max': 1400, 'unit': 'kcal'}
            },
            'waist_hip_ratio': {
                'male': {'min': 0.85, 'max': 0.95, 'unit': 'ratio'},
                'female': {'min': 0.75, 'max': 0.85, 'unit': 'ratio'}
            },
            'inbody_score': {'min': 80, 'max': 100, 'unit': 'points'}
        }
    
    def analyze_parameters(self, health_data: Dict[str, float], user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health parameters and return detailed analysis"""
        parameter_analysis = {}
        
        # Analyze all parameters, even if they are 0 (might be valid values)
        for parameter, value in health_data.items():
            parameter_analysis[parameter] = self._analyze_single_parameter(
                parameter, value, user_info
            )
        
        # Calculate overall health score based on analyzed parameters
        overall_score = self._calculate_overall_score(parameter_analysis)
        risk_level = self._determine_risk_level(overall_score)
        
        return {
            'parameter_analysis': parameter_analysis,
            'overall_score': overall_score,
            'risk_level': risk_level,
            'analyzed_parameters': list(parameter_analysis.keys()),
            'total_parameters': len(parameter_analysis)
        }
    
    def _analyze_single_parameter(self, parameter: str, value: float, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single health parameter"""
        if parameter not in self.ideal_ranges:
            return {
                'value': value,
                'status': 'unknown', 
                'message': 'Parameter not in database',
                'ideal_range': 'N/A'
            }
        
        ranges = self.ideal_ranges[parameter]
        
        # Handle gender-specific parameters
        if parameter in ['body_fat_percentage', 'weight', 'muscle_mass', 'protein', 'total_body_water', 'basal_metabolic_rate', 'waist_hip_ratio']:
            gender = user_info.get('gender', 'male').lower()
            if isinstance(ranges, dict) and gender in ranges:
                ranges = ranges[gender]
            elif isinstance(ranges, dict) and 'male' in ranges:
                ranges = ranges['male']  # Default to male if gender not found
        
        # Handle special cases for zero values
        if value == 0:
            if parameter in ['glucose', 'cholesterol_total', 'cholesterol_hdl', 'cholesterol_ldl', 
                           'blood_pressure_systolic', 'blood_pressure_diastolic']:
                return {
                    'value': value,
                    'status': 'not_provided',
                    'message': 'Value not provided - please enter for analysis',
                    'ideal_range': f"{ranges['min']}-{ranges['max']} {ranges['unit']}"
                }
        
        # Calculate BMI if not provided but weight and height are available
        if parameter == 'bmi' and value == 0:
            weight = user_info.get('weight', 0)
            height = user_info.get('height', 0)
            if weight and height:
                height_m = height / 100  # Convert cm to meters
                value = weight / (height_m ** 2)
            else:
                return {
                    'value': 0,
                    'status': 'not_calculated',
                    'message': 'Cannot calculate BMI - missing weight or height',
                    'ideal_range': f"{ranges['min']}-{ranges['max']} {ranges['unit']}"
                }
        
        # Determine status
        status = self._get_parameter_status(value, ranges)
        message = self._get_parameter_message(parameter, value, ranges, status)
        
        return {
            'value': value,
            'ideal_min': ranges['min'],
            'ideal_max': ranges['max'],
            'unit': ranges['unit'],
            'status': status,
            'message': message,
            'deviation': self._calculate_deviation(value, ranges),
            'ideal_range': f"{ranges['min']}-{ranges['max']} {ranges['unit']}"
        }
    
    def _get_parameter_status(self, value: float, ranges: Dict[str, float]) -> str:
        """Determine if parameter is within ideal range"""
        if ranges['min'] <= value <= ranges['max']:
            return 'optimal'
        elif value < ranges['min']:
            return 'low'
        else:
            return 'high'
    
    def _get_parameter_message(self, parameter: str, value: float, ranges: Dict[str, float], status: str) -> str:
        """Generate descriptive message for parameter"""
        messages = {
            'glucose': {
                'optimal': 'Blood glucose levels are within the normal range.',
                'low': 'Blood glucose is below normal. Consider consulting a healthcare provider.',
                'high': 'Blood glucose is elevated. Monitor diet and consider medical consultation.'
            },
            'cholesterol_total': {
                'optimal': 'Total cholesterol is at a healthy level.',
                'high': 'Total cholesterol is elevated. Diet and exercise modifications recommended.'
            },
            'cholesterol_hdl': {
                'optimal': 'HDL (good) cholesterol is at a healthy level.',
                'low': 'HDL cholesterol is low. Increase physical activity and healthy fats intake.'
            },
            'cholesterol_ldl': {
                'optimal': 'LDL (bad) cholesterol is at a healthy level.',
                'high': 'LDL cholesterol is elevated. Reduce saturated fats and increase fiber intake.'
            },
            'blood_pressure_systolic': {
                'optimal': 'Systolic blood pressure is normal.',
                'low': 'Systolic blood pressure is low. Monitor for symptoms.',
                'high': 'Systolic blood pressure is elevated. Lifestyle changes recommended.'
            },
            'blood_pressure_diastolic': {
                'optimal': 'Diastolic blood pressure is normal.',
                'low': 'Diastolic blood pressure is low. Monitor for symptoms.',
                'high': 'Diastolic blood pressure is elevated. Reduce sodium intake and increase exercise.'
            },
            'bmi': {
                'optimal': 'BMI is within the healthy range.',
                'low': 'BMI indicates underweight. Consider increasing caloric intake with nutritious foods.',
                'high': 'BMI indicates overweight/obesity. Weight management recommended.'
            },
            'body_fat_percentage': {
                'optimal': 'Body fat percentage is within the healthy range.',
                'low': 'Body fat percentage is low. Ensure adequate nutrition.',
                'high': 'Body fat percentage is elevated. Increase cardio and strength training.'
            },
            'weight': {
                'optimal': 'Body weight is within the healthy range.',
                'low': 'Body weight is below normal. Consider increasing caloric intake with nutritious foods.',
                'high': 'Body weight is above normal. Consider a balanced diet and regular exercise.'
            },
            'muscle_mass': {
                'optimal': 'Muscle mass is at a healthy level.',
                'low': 'Muscle mass is below optimal. Focus on strength training and protein intake.',
                'high': 'Excellent muscle mass. Continue strength training for maintenance.'
            },
            'protein': {
                'optimal': 'Protein levels are adequate.',
                'low': 'Protein levels are low. Increase protein-rich foods in your diet.',
                'high': 'Protein levels are above normal range.'
            },
            'minerals': {
                'optimal': 'Mineral levels are within normal range.',
                'low': 'Mineral levels are low. Consider mineral-rich foods or supplements.',
                'high': 'Mineral levels are elevated.'
            },
            'total_body_water': {
                'optimal': 'Body water percentage is normal.',
                'low': 'Body water is low. Increase fluid intake and monitor hydration.',
                'high': 'Body water levels are elevated. Monitor for fluid retention.'
            },
            'visceral_fat_level': {
                'optimal': 'Visceral fat level is healthy.',
                'low': 'Visceral fat level is very low.',
                'high': 'Visceral fat level is elevated. Focus on cardio exercise and diet.'
            },
            'basal_metabolic_rate': {
                'optimal': 'Metabolic rate is within normal range.',
                'low': 'Metabolic rate is low. Consider strength training to build muscle.',
                'high': 'Metabolic rate is high, which can be beneficial for weight management.'
            },
            'waist_hip_ratio': {
                'optimal': 'Waist-hip ratio is within healthy range.',
                'low': 'Waist-hip ratio is low.',
                'high': 'Waist-hip ratio is elevated. Focus on reducing waist circumference.'
            },
            'inbody_score': {
                'optimal': 'InBody score indicates good overall body composition.',
                'low': 'InBody score suggests room for improvement in body composition.',
                'high': 'Excellent InBody score indicating optimal body composition.'
            }
        }
        
        return messages.get(parameter, {}).get(status, 'Status determined.')
    
    def _calculate_deviation(self, value: float, ranges: Dict[str, float]) -> float:
        """Calculate how far the value deviates from ideal range"""
        if ranges['min'] <= value <= ranges['max']:
            return 0.0
        elif value < ranges['min']:
            return (ranges['min'] - value) / ranges['min'] * 100
        else:
            return (value - ranges['max']) / ranges['max'] * 100
    
    def _calculate_overall_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate InBody Score based on official InBody methodology and body composition analysis"""
        
        # InBody Score Components with Official Weights
        inbody_components = {
            # Primary Body Composition (60% total weight)
            'skeletal_muscle_mass': 0.25,      # 25% - Most important for strength and metabolism
            'body_fat_percentage': 0.20,       # 20% - Key obesity indicator
            'visceral_fat': 0.15,              # 15% - Health risk indicator
            
            # Body Water Analysis (20% total weight)
            'total_body_water': 0.10,          # 10% - Hydration status
            'ecw_tbw_ratio': 0.10,             # 10% - Inflammation/swelling indicator
            
            # Supporting Metrics (20% total weight)
            'bmi': 0.08,                       # 8% - Basic weight assessment
            'lean_body_mass': 0.07,            # 7% - Non-fat body mass
            'basal_metabolic_rate': 0.05       # 5% - Metabolic efficiency
        }
        
        component_scores = []
        total_weight_used = 0
        
        for component, weight in inbody_components.items():
            if component in analysis and isinstance(analysis[component], dict):
                data = analysis[component]
                
                # Calculate component score based on InBody standards
                if component == 'body_fat_percentage':
                    score = self._calculate_body_fat_score(data)
                elif component == 'skeletal_muscle_mass':
                    score = self._calculate_muscle_score(data)
                elif component == 'visceral_fat':
                    score = self._calculate_visceral_fat_score(data)
                elif component == 'ecw_tbw_ratio':
                    score = self._calculate_ecw_ratio_score(data)
                else:
                    # Standard scoring for other components
                    score = self._calculate_standard_score(data)
                
                component_scores.append(score * weight)
                total_weight_used += weight
        
        # Calculate base InBody score
        if total_weight_used > 0:
            base_score = sum(component_scores) / total_weight_used
        else:
            base_score = 50.0
        
        # Apply InBody scoring adjustments
        # Bonus for optimal muscle-fat balance (C-shape, I-shape, D-shape analysis)
        balance_bonus = self._calculate_body_type_bonus(analysis)
        
        # Final InBody Score (scaled to 0-100)
        final_score = min(100, max(0, base_score + balance_bonus))
        
        return final_score
    
    def _calculate_body_fat_score(self, data: Dict[str, Any]) -> float:
        """Calculate score based on InBody body fat percentage standards"""
        value = data.get('value', 0)
        status = data.get('status', 'unknown')
        
        if status == 'optimal':
            return 100
        elif status == 'normal':
            return 85
        elif status in ['low', 'high']:
            deviation = data.get('deviation', 0)
            if deviation <= 15:
                return 70
            elif deviation <= 30:
                return 50
            else:
                return 30
        return 40
    
    def _calculate_muscle_score(self, data: Dict[str, Any]) -> float:
        """Calculate score based on skeletal muscle mass development"""
        value = data.get('value', 0)
        status = data.get('status', 'unknown')
        
        if status == 'optimal':
            return 100
        elif status == 'normal':
            return 85
        elif status == 'low':
            deviation = data.get('deviation', 0)
            if deviation <= 10:
                return 65
            elif deviation <= 25:
                return 40
            else:
                return 20
        elif status == 'high':
            return 95  # High muscle mass is generally positive
        return 50
    
    def _calculate_visceral_fat_score(self, data: Dict[str, Any]) -> float:
        """Calculate score based on visceral fat area (optimal < 100 cm²)"""
        value = data.get('value', 0)
        status = data.get('status', 'unknown')
        
        if status == 'optimal':
            return 100
        elif status == 'normal':
            return 80
        elif status == 'high':
            deviation = data.get('deviation', 0)
            if deviation <= 20:
                return 60
            elif deviation <= 50:
                return 30
            else:
                return 10
        return 50
    
    def _calculate_ecw_ratio_score(self, data: Dict[str, Any]) -> float:
        """Calculate score based on ECW/TBW ratio (optimal: 0.360-0.390)"""
        value = data.get('value', 0.38)
        
        if 0.360 <= value <= 0.390:
            return 100
        elif 0.350 <= value <= 0.400:
            return 80
        elif 0.340 <= value <= 0.410:
            return 60
        else:
            return 30
    
    def _calculate_standard_score(self, data: Dict[str, Any]) -> float:
        """Standard scoring for other parameters"""
        status = data.get('status', 'unknown')
        
        if status == 'optimal':
            return 100
        elif status == 'normal':
            return 85
        elif status in ['low', 'high']:
            deviation = data.get('deviation', 0)
            return max(20, 100 - deviation * 2)
        return 50
    
    def _calculate_body_type_bonus(self, analysis: Dict[str, Any]) -> float:
        """Calculate bonus based on InBody body type classification (C, I, D shape)"""
        # This is a simplified implementation of the C-I-D shape analysis
        
        weight_data = analysis.get('weight', {})
        muscle_data = analysis.get('skeletal_muscle_mass', {})
        fat_data = analysis.get('body_fat_mass', {})
        
        if not all([weight_data, muscle_data, fat_data]):
            return 0
        
        # Simplified shape calculation based on relative percentages
        weight_pct = weight_data.get('value', 100) / weight_data.get('ideal_max', 100) * 100
        muscle_pct = muscle_data.get('value', 100) / muscle_data.get('ideal_max', 100) * 100
        fat_pct = fat_data.get('value', 100) / fat_data.get('ideal_max', 100) * 100
        
        # D-Shape (Athletic): High muscle, optimal fat
        if muscle_pct >= 100 and fat_pct <= 100:
            return 5  # 5 point bonus
        # I-Shape (Balanced): All parameters near normal
        elif 90 <= muscle_pct <= 110 and 90 <= fat_pct <= 110:
            return 2  # 2 point bonus
        # C-Shape (Needs improvement): Low muscle, high fat
        else:
            return 0  # No bonus
        
        return 0
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine body composition category based on InBody Score"""
        if score >= 90:
            return 'Excellent (D-Shape)'      # Athletic body type
        elif score >= 80:
            return 'Very Good (I-Shape)'      # Balanced body type
        elif score >= 70:
            return 'Good Composition'         # Above average
        elif score >= 60:
            return 'Fair Composition'         # Average, some improvement needed
        elif score >= 50:
            return 'Needs Improvement'        # Below average
        else:
            return 'Poor (C-Shape)'           # High risk, significant improvement needed
    
    def get_priority_parameters(self, analysis: Dict[str, Any]) -> List[str]:
        """Get list of parameters that need immediate attention"""
        priority = []
        
        for param, data in analysis.items():
            if isinstance(data, dict) and 'deviation' in data:
                if data['deviation'] > 25:  # More than 25% deviation
                    priority.append(param)
        
        return sorted(priority, key=lambda x: analysis[x]['deviation'], reverse=True)
