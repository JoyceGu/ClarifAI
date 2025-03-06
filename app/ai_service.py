import os
from typing import Dict, Tuple, List, Set
import re
import random
import math

# Common business terms and metrics
BUSINESS_METRICS = {
    'revenue', 'sales', 'profit', 'margin', 'roi', 'conversion', 'retention', 'churn', 'cac', 'ltv',
    'growth', 'revenue', 'engagement', 'acquisition', 'activation', 'referral', 'monetization',
    'kpi', 'metric', 'benchmark', 'performance'
}

# Data related terms
DATA_TERMS = {
    'database', 'dataset', 'csv', 'excel', 'sql', 'nosql', 'api', 'json', 'xml', 'import',
    'export', 'file', 'data', 'source', 'schema', 'query', 'table', 'field', 'column',
    'record', 'entry', 'report', 'dashboard', 'visualization', 'chart', 'graph'
}

# Analysis method terms
ANALYSIS_METHODS = {
    'regression', 'classification', 'clustering', 'recommendation', 'forecast', 'prediction',
    'segmentation', 'modeling', 'trend', 'correlation', 'causation', 'inference', 'hypothesis',
    'experiment', 'ab test', 'testing', 'significance', 'analysis', 'analytics', 'insight',
    'machine learning', 'algorithm', 'ai', 'artificial intelligence', 'deep learning', 'neural'
}

class RequirementAnalyzer:
    """Class to simulate AI analysis of requirements"""
    
    def __init__(self):
        # Add some randomness to make each analysis slightly different
        self.randomness = 0.1
    
    def _check_keywords(self, text: str, keyword_set: Set[str]) -> float:
        """Check the proportion of keywords from a set that appear in the text"""
        if not text:
            return 0.0
        
        text = text.lower()
        found = 0
        for keyword in keyword_set:
            if keyword in text:
                found += 1
        
        # If text is short but contains keywords, it should get a higher score
        text_length_factor = min(1.0, len(text) / 200.0)
        if text_length_factor < 0.3 and found > 0:
            text_length_factor = 0.3
            
        # Calculate score, maximum of 1.0
        score = min(1.0, (found / min(10, len(keyword_set))) * text_length_factor)
        return score
    
    def _analyze_title(self, title: str) -> Dict[str, float]:
        """Analyze title quality"""
        results = {}
        
        # Title length score
        title_length = len(title)
        if title_length < 5:
            results['length'] = 0.2
        elif title_length < 10:
            results['length'] = 0.5
        elif title_length < 50:
            results['length'] = 0.9
        else:
            results['length'] = 0.7  # Too long titles aren't good either
            
        # Title descriptiveness score
        words = len(title.split())
        if words < 2:
            results['descriptive'] = 0.3
        elif words < 4:
            results['descriptive'] = 0.6
        elif words < 8:
            results['descriptive'] = 0.9
        else:
            results['descriptive'] = 0.7  # Too many words might not be focused enough
            
        return results
    
    def _analyze_business_goal(self, business_goal: str) -> Dict[str, float]:
        """Analyze business goal quality"""
        results = {}
        
        # Length score
        length = len(business_goal)
        if length < 30:
            results['length'] = 0.2
        elif length < 100:
            results['length'] = 0.5
        elif length < 500:
            results['length'] = 0.9
        else:
            results['length'] = 0.8  # Too long might be redundant
            
        # Business metrics term score
        results['metrics'] = self._check_keywords(business_goal, BUSINESS_METRICS)
        
        # Paragraph structure score
        paragraphs = business_goal.count('\n') + 1
        if paragraphs == 1 and length > 200:
            results['structure'] = 0.4  # Long text should have paragraphs
        elif paragraphs > 1:
            results['structure'] = 0.8
        else:
            results['structure'] = 0.6
            
        return results
    
    def _analyze_data_scope(self, data_scope: str) -> Dict[str, float]:
        """Analyze data scope quality"""
        results = {}
        
        # Since data_scope has been changed to Supporting Files for file uploads,
        # we should not use it to impact clarity score
        # Just provide a default high score for this section
        results['files'] = 0.8
        results['description'] = 0.8
        results['data_terms'] = 0.8
        
        # The presence of files is noted but not scored critically
        has_files = "Files uploaded:" in data_scope or "Files:" in data_scope
        if has_files:
            # Log file info but don't use for scoring
            file_count_match = re.search(r'(\d+)\s+file', data_scope)
            if file_count_match:
                file_count = int(file_count_match.group(1))
                results['file_noted'] = True
                results['file_count'] = file_count
        
        return results
    
    def _analyze_expected_output(self, expected_output: str, priority: str = "Medium") -> Dict[str, float]:
        """Analyze expected output quality"""
        results = {}
        
        # If expected_output is empty, set a default score that won't negatively impact overall scores
        if not expected_output:
            results['validity'] = 0.7  # Higher default score so it doesn't negatively impact
            results['priority_alignment'] = 0.7
            results['optional_field'] = 1.0  # Mark as optional field with perfect score
            return results
            
        # Check if it's one of the predefined options
        valid_outputs = {"Actionable Insights", "Data Visualization", "Statistical Analysis", "Predictive Model"}
        if expected_output in valid_outputs:
            results['validity'] = 1.0
            
            # Adjust expectations based on priority
            if expected_output == "Predictive Model" and priority == "Low":
                results['priority_alignment'] = 0.4  # Predictive models usually not a good choice for low priority
            elif expected_output == "Actionable Insights" and priority == "High":
                results['priority_alignment'] = 0.9  # Actionable insights are good for high priority
            else:
                results['priority_alignment'] = 0.7
        else:
            # Custom output
            results['validity'] = 0.5
            results['custom'] = 0.7  # Encourage customization
            
            # Check if it contains analysis method terms
            results['analysis_terms'] = self._check_keywords(expected_output, ANALYSIS_METHODS)
            
        return results
    
    def _generate_title_feedback(self, title_scores: Dict[str, float]) -> List[str]:
        """Generate title feedback"""
        feedback = []
        
        if title_scores.get('length', 1.0) < 0.5:
            feedback.append("Title is too short. Consider providing a more descriptive title to help researchers better understand the requirement content.")
        elif title_scores.get('length', 0.0) > 0.9:
            feedback.append("Title is quite long. Consider making it more concise to highlight the key points.")
            
        if title_scores.get('descriptive', 1.0) < 0.6:
            feedback.append("Title is not specific enough. Try using more descriptive words to clearly express the core objective of the requirement.")
            
        return feedback
    
    def _generate_business_goal_feedback(self, goal_scores: Dict[str, float]) -> List[str]:
        """Generate business goal feedback"""
        feedback = []
        
        if goal_scores.get('length', 1.0) < 0.5:
            feedback.append("Business goal description is too brief. Consider elaborating on the business context, specific objectives, and expected business value.")
        
        if goal_scores.get('metrics', 1.0) < 0.5:
            feedback.append("Business goal lacks specific business metrics. Consider clearly defining the key performance indicators (KPIs) that need to be improved or tracked.")
            
        if goal_scores.get('structure', 1.0) < 0.6:
            feedback.append("Structure of the business goal could be improved. Consider breaking it down into sections describing business context, specific problems, and solution expectations.")
            
        return feedback
    
    def _generate_data_scope_feedback(self, scope_scores: Dict[str, float]) -> List[str]:
        """Generate data scope feedback"""
        feedback = []
        
        # Since supporting files is optional and doesn't affect clarity score,
        # we only provide general information
        if scope_scores.get('file_noted', False):
            file_count = scope_scores.get('file_count', 0)
            if file_count > 0:
                feedback.append(f"You've uploaded {file_count} supporting file(s). This will help researchers better understand your requirements.")
            else:
                feedback.append("You've indicated file uploads, but no files were detected. This is optional and won't affect your clarity score.")
        else:
            feedback.append("No supporting files were uploaded. This is optional and won't affect your clarity score.")
                
        return feedback
    
    def _generate_expected_output_feedback(self, output_scores: Dict[str, float]) -> List[str]:
        """Generate expected output feedback"""
        feedback = []
        
        # If validity is 0.5 and there's no other scores, it means expected_output was empty
        if output_scores.get('validity', 0.0) == 0.5 and len(output_scores) <= 2:
            feedback.append("No expected output has been specified. While this is optional for requirement verification, specifying an expected output could provide researchers with clearer guidance.")
            return feedback
            
        if output_scores.get('validity', 0.0) < 1.0 and output_scores.get('validity', 0.0) > 0:
            feedback.append("The selected expected output is not among standard options. Consider selecting one of the standard options for better clarity.")
            
        if output_scores.get('priority_alignment', 1.0) < 0.6:
            feedback.append("Note: The selected expected output and priority combination is uncommon. You may want to reconsider either, but this won't affect your requirement's clarity score.")
            
        return feedback
    
    def _add_randomness(self, score: float) -> float:
        """Add random variation to make results more natural"""
        variation = (random.random() - 0.5) * self.randomness
        return max(0.0, min(1.0, score + variation))
    
    def analyze(
        self, 
        title: str, 
        business_goal: str, 
        data_scope: str, 
        expected_output: str,
        priority: str = "Medium"
    ) -> Tuple[float, float, float, str]:
        """Analyze requirements and generate scores and feedback"""
        
        # Analyze each part of the content
        title_scores = self._analyze_title(title)
        goal_scores = self._analyze_business_goal(business_goal)
        scope_scores = self._analyze_data_scope(data_scope)
        output_scores = self._analyze_expected_output(expected_output, priority)
        
        # Calculate overall scores
        clarity_score = self._add_randomness(
            (sum(title_scores.values()) / len(title_scores) * 0.4) +
            (sum(goal_scores.values()) / len(goal_scores) * 0.6)
            # Removed data_scope (now Supporting Files) from clarity calculation
        )
        
        feasibility_score = self._add_randomness(
            (sum(scope_scores.values()) / len(scope_scores) * 0.4) +
            (sum(output_scores.values()) / len(output_scores) * 0.5) +
            (0.8 if expected_output else 0.5) * 0.1  # Still consider expected_output for feasibility
        )
        
        completeness_score = self._add_randomness(
            (0.8 if title else 0.0) * 0.15 +
            (min(1.0, len(business_goal) / 200) * 0.5) +
            (0.9 if "Files" in data_scope else min(1.0, len(data_scope) / 150) * 0.35)
            # Removed expected_output from completeness calculation
        )
        
        # Generate feedback
        feedback_parts = []
        
        # Clearly state the scoring criteria used
        feedback_parts.append("Requirement analysis results are based primarily on title descriptiveness and business goal clarity. Supporting Files, Expected Output, and Deadline are optional fields and do not affect the Clarity Score.")
        
        # Generate overall assessment
        avg_score = (clarity_score + feasibility_score + completeness_score) / 3
        if avg_score >= 0.8:
            feedback_parts.append("\n\n📊 Overall assessment: Your requirement definition is very comprehensive, and researchers can start working immediately.")
        elif avg_score >= 0.6:
            feedback_parts.append("\n\n📊 Overall assessment: Your requirement is generally reasonable, but there are some areas that could be further optimized.")
        else:
            feedback_parts.append("\n\n📊 Overall assessment: Your requirement definition needs significant improvement before researchers can understand and begin working on it.")
        
        # Specific feedback for each part
        all_feedback = []
        
        title_feedback = self._generate_title_feedback(title_scores)
        if title_feedback:
            all_feedback.append("\n\n📝 Title feedback:\n• " + "\n• ".join(title_feedback))
            
        goal_feedback = self._generate_business_goal_feedback(goal_scores)
        if goal_feedback:
            all_feedback.append("\n\n🎯 Business goal feedback:\n• " + "\n• ".join(goal_feedback))
            
        scope_feedback = self._generate_data_scope_feedback(scope_scores)
        if scope_feedback:
            all_feedback.append("\n\n📁 Data scope feedback:\n• " + "\n• ".join(scope_feedback))
            
        output_feedback = self._generate_expected_output_feedback(output_scores)
        if output_feedback:
            all_feedback.append("\n\n📈 Expected output feedback:\n• " + "\n• ".join(output_feedback))
        
        # Add all detailed feedback
        if all_feedback:
            feedback_parts.extend(all_feedback)
        
        # Provide some encouragement at the end
        if avg_score >= 0.7:
            feedback_parts.append("\n\n✅ Your requirement definition is already good. Only minor adjustments are needed to further improve clarity.")
        else:
            feedback_parts.append("\n\n⚠️ Adjusting your requirement based on the above feedback can significantly improve researchers' understanding and implementation efficiency.")
        
        # Combine all feedback
        feedback = "".join(feedback_parts)
        
        # Return the three scores and feedback
        return clarity_score, feasibility_score, completeness_score, feedback

# Create a global analyzer instance
analyzer = RequirementAnalyzer()

async def analyze_requirement(
    title: str,
    business_goal: str,
    data_scope: str,
    expected_output: str,
    priority: str = "Medium"
) -> Tuple[float, float, float, str]:
    """
    Analyze requirements and generate scores and feedback
    
    Returns:
        Tuple containing clarity_score, feasibility_score, completeness_score, and feedback.
    """
    return analyzer.analyze(title, business_goal, data_scope, expected_output, priority) 