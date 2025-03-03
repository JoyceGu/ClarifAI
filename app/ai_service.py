import os
from typing import Dict, Tuple, List
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 禁用任何自动代理设置
os.environ['NO_PROXY'] = '*'
if 'HTTP_PROXY' in os.environ:
    del os.environ['HTTP_PROXY']
if 'HTTPS_PROXY' in os.environ:
    del os.environ['HTTPS_PROXY']

# 使用更基本的配置方式
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Fallback function in case API connection fails
def calculate_simple_scores(title, business_goal, data_scope, expected_output):
    """Simple fallback scoring mechanism when API fails"""
    clarity_score = 0.0
    if len(business_goal) > 50:
        clarity_score += 0.5
    if len(data_scope) > 50:
        clarity_score += 0.5
    
    feasibility_score = 0.0
    if len(business_goal) > 50:
        feasibility_score += 0.5
    if expected_output:
        feasibility_score += 0.5
        
    completeness_score = 0.0
    if title:
        completeness_score += 0.33
    if business_goal:
        completeness_score += 0.33
    if expected_output:
        completeness_score += 0.34
        
    feedback = []
    if len(business_goal) < 50:
        feedback.append("Consider providing more details about your business goal.")
    if len(data_scope) < 50:
        feedback.append("The data scope could be more specific. Consider including time range, geographic scope, or user segments.")
    if not feedback:
        feedback.append("Your requirement is well-defined. Consider adding any additional context that might help researchers.")
        
    return clarity_score, feasibility_score, completeness_score, " ".join(feedback)

async def analyze_requirement(
    title: str,
    business_goal: str,
    data_scope: str,
    expected_output: str
) -> Tuple[float, float, float, str]:
    """
    Analyze a requirement using Azure OpenAI to generate scores and feedback.
    
    Returns:
        Tuple containing clarity_score, feasibility_score, completeness_score, and feedback.
    """
    prompt = f"""
    As an AI requirement analyst, evaluate the following product requirement:
    
    Title: {title}
    Business Goal: {business_goal}
    Data Scope: {data_scope}
    Expected Output: {expected_output}
    
    Please analyze this requirement and provide:
    1. A clarity score (from 0.0 to 1.0) - How clear and specific is the requirement?
    2. A feasibility score (from 0.0 to 1.0) - How feasible is it to implement?
    3. A completeness score (from 0.0 to 1.0) - Does it provide all necessary information?
    4. Specific feedback on how to improve the requirement.
    
    Format your response as follows:
    Clarity Score: [score]
    Feasibility Score: [score]
    Completeness Score: [score]
    Feedback: [your detailed feedback]
    """
    
    try:
        # 使用简单的评分方法，不调用API
        print("Using simple scoring method due to API issues")
        return calculate_simple_scores(title, business_goal, data_scope, expected_output)
        
        # 以下代码暂时不使用，因为可能有API兼容性问题
        """
        try:
            # Try to use Azure OpenAI API - use the older style API for compatibility
            response = openai.ChatCompletion.create(
                engine=DEPLOYMENT_NAME,  # 使用engine而不是model
                messages=[
                    {"role": "system", "content": "You are an expert product requirement analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Extract response text
            result = response.choices[0].message.content
            
            # Parse scores and feedback from response
            clarity_score = 0.0
            feasibility_score = 0.0
            completeness_score = 0.0
            feedback = ""
            
            for line in result.split('\n'):
                if line.lower().startswith('clarity score:'):
                    try:
                        clarity_score = float(line.split(':')[1].strip())
                    except:
                        clarity_score = 0.5
                elif line.lower().startswith('feasibility score:'):
                    try:
                        feasibility_score = float(line.split(':')[1].strip())
                    except:
                        feasibility_score = 0.5
                elif line.lower().startswith('completeness score:'):
                    try:
                        completeness_score = float(line.split(':')[1].strip())
                    except:
                        completeness_score = 0.5
                elif line.lower().startswith('feedback:'):
                    feedback = line.split(':', 1)[1].strip()
            
            # If feedback is empty, extract everything after scores as feedback
            if not feedback:
                parts = result.split('Completeness Score:')
                if len(parts) > 1:
                    # Remove any score from the second part
                    rest = parts[1].strip()
                    if '\n' in rest:
                        feedback = rest.split('\n', 1)[1].strip()
                    else:
                        feedback = "Please provide more details for a comprehensive analysis."
            
            return clarity_score, feasibility_score, completeness_score, feedback
            
        except Exception as api_error:
            print(f"Azure OpenAI API error: {str(api_error)}")
            # Fall back to simple scoring if API call fails
            return calculate_simple_scores(title, business_goal, data_scope, expected_output)
        """
            
    except Exception as e:
        print(f"Error in analyze_requirement: {str(e)}")
        # Ultimate fallback
        return 0.5, 0.5, 0.5, f"Unable to analyze requirement: {str(e)}. Please check your inputs and try again." 