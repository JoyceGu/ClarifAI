import os
from typing import Dict, Tuple, List, Set
import re
import random
import math

# 常见的业务词汇和指标
BUSINESS_METRICS = {
    'revenue', 'sales', 'profit', 'margin', 'roi', 'conversion', 'retention', 'churn', 'cac', 'ltv',
    'growth', 'revenue', 'engagement', 'acquisition', 'activation', 'referral', 'monetization',
    'kpi', 'metric', 'benchmark', 'performance'
}

# 数据相关词汇
DATA_TERMS = {
    'database', 'dataset', 'csv', 'excel', 'sql', 'nosql', 'api', 'json', 'xml', 'import',
    'export', 'file', 'data', 'source', 'schema', 'query', 'table', 'field', 'column',
    'record', 'entry', 'report', 'dashboard', 'visualization', 'chart', 'graph'
}

# 分析方法词汇
ANALYSIS_METHODS = {
    'regression', 'classification', 'clustering', 'recommendation', 'forecast', 'prediction',
    'segmentation', 'modeling', 'trend', 'correlation', 'causation', 'inference', 'hypothesis',
    'experiment', 'ab test', 'testing', 'significance', 'analysis', 'analytics', 'insight',
    'machine learning', 'algorithm', 'ai', 'artificial intelligence', 'deep learning', 'neural'
}

class RequirementAnalyzer:
    """模拟AI分析需求的类"""
    
    def __init__(self):
        # 添加一些随机性，使每次分析结果稍有不同
        self.randomness = 0.1
    
    def _check_keywords(self, text: str, keyword_set: Set[str]) -> float:
        """检查文本中包含关键词集合中词汇的比例"""
        if not text:
            return 0.0
        
        text = text.lower()
        found = 0
        for keyword in keyword_set:
            if keyword in text:
                found += 1
        
        # 如果文本很短但包含关键词，应该得到较高分数
        text_length_factor = min(1.0, len(text) / 200.0)
        if text_length_factor < 0.3 and found > 0:
            text_length_factor = 0.3
            
        # 计算分数，最高为1.0
        score = min(1.0, (found / min(10, len(keyword_set))) * text_length_factor)
        return score
    
    def _analyze_title(self, title: str) -> Dict[str, float]:
        """分析标题质量"""
        results = {}
        
        # 标题长度评分
        title_length = len(title)
        if title_length < 5:
            results['length'] = 0.2
        elif title_length < 10:
            results['length'] = 0.5
        elif title_length < 50:
            results['length'] = 0.9
        else:
            results['length'] = 0.7  # 太长的标题也不好
            
        # 标题描述性评分
        words = len(title.split())
        if words < 2:
            results['descriptive'] = 0.3
        elif words < 4:
            results['descriptive'] = 0.6
        elif words < 8:
            results['descriptive'] = 0.9
        else:
            results['descriptive'] = 0.7  # 太多词的标题可能不够聚焦
            
        return results
    
    def _analyze_business_goal(self, business_goal: str) -> Dict[str, float]:
        """分析业务目标质量"""
        results = {}
        
        # 长度评分
        length = len(business_goal)
        if length < 30:
            results['length'] = 0.2
        elif length < 100:
            results['length'] = 0.5
        elif length < 500:
            results['length'] = 0.9
        else:
            results['length'] = 0.8  # 太长可能有冗余
            
        # 业务指标词汇评分
        results['metrics'] = self._check_keywords(business_goal, BUSINESS_METRICS)
        
        # 段落结构评分
        paragraphs = business_goal.count('\n') + 1
        if paragraphs == 1 and length > 200:
            results['structure'] = 0.4  # 长文本应该有段落
        elif paragraphs > 1:
            results['structure'] = 0.8
        else:
            results['structure'] = 0.6
            
        return results
    
    def _analyze_data_scope(self, data_scope: str) -> Dict[str, float]:
        """分析数据范围质量"""
        results = {}
        
        # 检查是否包含文件上传信息
        has_files = "Files uploaded:" in data_scope or "Files:" in data_scope
        if has_files:
            results['files'] = 0.9
            # 检查文件数量
            file_count_match = re.search(r'(\d+)\s+file', data_scope)
            if file_count_match:
                file_count = int(file_count_match.group(1))
                if file_count > 3:
                    results['file_quantity'] = 0.9
                elif file_count > 0:
                    results['file_quantity'] = 0.7
                else:
                    results['file_quantity'] = 0.0
        else:
            results['files'] = 0.0
            
            # 如果没有文件，检查文本描述
            length = len(data_scope)
            if length < 30:
                results['description'] = 0.2
            elif length < 100:
                results['description'] = 0.6
            else:
                results['description'] = 0.9
                
            # 检查是否包含数据术语
            results['data_terms'] = self._check_keywords(data_scope, DATA_TERMS)
            
        return results
    
    def _analyze_expected_output(self, expected_output: str, priority: str = "Medium") -> Dict[str, float]:
        """分析预期输出质量"""
        results = {}
        
        # 检查是否是预定义选项之一
        valid_outputs = {"Actionable Insights", "Data Visualization", "Statistical Analysis", "Predictive Model"}
        if expected_output in valid_outputs:
            results['validity'] = 1.0
            
            # 根据优先级调整期望
            if expected_output == "Predictive Model" and priority == "Low":
                results['priority_alignment'] = 0.4  # 预测模型通常不是低优先级的好选择
            elif expected_output == "Actionable Insights" and priority == "High":
                results['priority_alignment'] = 0.9  # 可操作洞见适合高优先级
            else:
                results['priority_alignment'] = 0.7
        else:
            # 自定义输出
            results['validity'] = 0.5
            results['custom'] = 0.7  # 鼓励定制化
            
            # 检查是否包含分析方法术语
            results['analysis_terms'] = self._check_keywords(expected_output, ANALYSIS_METHODS)
            
        return results
    
    def _generate_title_feedback(self, title_scores: Dict[str, float]) -> List[str]:
        """生成标题反馈"""
        feedback = []
        
        if title_scores.get('length', 1.0) < 0.5:
            feedback.append("标题过短，建议提供更具描述性的标题，以便研究人员更好地理解需求内容。")
        elif title_scores.get('length', 0.0) > 0.9:
            feedback.append("标题较长，考虑精简以突出重点。")
            
        if title_scores.get('descriptive', 1.0) < 0.6:
            feedback.append("标题不够具体，建议使用更多描述性词汇来清晰表达需求的核心目标。")
            
        return feedback
    
    def _generate_business_goal_feedback(self, goal_scores: Dict[str, float]) -> List[str]:
        """生成业务目标反馈"""
        feedback = []
        
        if goal_scores.get('length', 1.0) < 0.5:
            feedback.append("业务目标描述过于简短，建议详细阐述业务背景、具体目标和期望达成的业务价值。")
        
        if goal_scores.get('metrics', 1.0) < 0.5:
            feedback.append("业务目标中缺乏具体的业务指标，建议明确定义需要改进或跟踪的关键绩效指标(KPI)。")
            
        if goal_scores.get('structure', 1.0) < 0.6:
            feedback.append("业务目标的结构可以优化，考虑分段描述业务背景、具体问题、解决方案期望等。")
            
        return feedback
    
    def _generate_data_scope_feedback(self, scope_scores: Dict[str, float]) -> List[str]:
        """生成数据范围反馈"""
        feedback = []
        
        if scope_scores.get('files', 0.0) > 0.5:
            if scope_scores.get('file_quantity', 0.0) < 0.6:
                feedback.append("已上传文件，但数量较少。如有更多相关数据文件，建议一并提供以便更全面分析。")
        else:
            if scope_scores.get('description', 0.0) < 0.6:
                feedback.append("未上传文件，且数据范围描述不足。建议详细说明需要分析的数据内容、时间范围、数据格式等。")
            
            if scope_scores.get('data_terms', 0.0) < 0.4:
                feedback.append("数据描述中缺少关键的数据术语，建议具体说明数据来源、数据格式、数据量级等信息。")
                
        return feedback
    
    def _generate_expected_output_feedback(self, output_scores: Dict[str, float]) -> List[str]:
        """生成预期输出反馈"""
        feedback = []
        
        if output_scores.get('validity', 0.0) < 1.0:
            feedback.append("所选预期输出不在标准选项中，可能会导致研究人员对需求理解产生歧义。")
            
        if output_scores.get('priority_alignment', 1.0) < 0.6:
            feedback.append("所选预期输出与设定的优先级不太匹配，建议重新考虑输出形式或调整优先级。")
            
        if output_scores.get('analysis_terms', 0.0) < 0.4 and 'custom' in output_scores:
            feedback.append("预期输出中缺少具体的分析方法描述，建议明确说明希望使用的分析技术或方法论。")
            
        return feedback
    
    def _add_randomness(self, score: float) -> float:
        """添加随机波动，使结果更自然"""
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
        """分析需求并生成分数和反馈"""
        
        # 分析各部分内容
        title_scores = self._analyze_title(title)
        goal_scores = self._analyze_business_goal(business_goal)
        scope_scores = self._analyze_data_scope(data_scope)
        output_scores = self._analyze_expected_output(expected_output, priority)
        
        # 计算总体分数
        clarity_score = self._add_randomness(
            (sum(title_scores.values()) / len(title_scores) * 0.2) +
            (sum(goal_scores.values()) / len(goal_scores) * 0.4) +
            (sum(scope_scores.values()) / len(scope_scores) * 0.4)
        )
        
        feasibility_score = self._add_randomness(
            (sum(scope_scores.values()) / len(scope_scores) * 0.6) +
            (sum(output_scores.values()) / len(output_scores) * 0.4)
        )
        
        completeness_score = self._add_randomness(
            (0.8 if title else 0.0) * 0.1 +
            (min(1.0, len(business_goal) / 200) * 0.4) +
            (0.9 if "Files" in data_scope else min(1.0, len(data_scope) / 150) * 0.3) +
            (0.8 if expected_output else 0.0) * 0.2
        )
        
        # 生成反馈
        feedback_parts = []
        
        # 明确采用的评分标准
        feedback_parts.append("需求分析结果基于以下维度：标题描述性、业务目标清晰度、数据范围明确度和预期输出合理性。")
        
        # 生成总体评价
        avg_score = (clarity_score + feasibility_score + completeness_score) / 3
        if avg_score >= 0.8:
            feedback_parts.append("总体评价：您的需求定义非常全面，研究人员可以直接开始工作。")
        elif avg_score >= 0.6:
            feedback_parts.append("总体评价：您的需求基本合理，但有一些地方可以进一步优化。")
        else:
            feedback_parts.append("总体评价：您的需求定义需要显著改进，才能使研究人员理解并开始工作。")
        
        # 各部分具体反馈
        title_feedback = self._generate_title_feedback(title_scores)
        if title_feedback:
            feedback_parts.append("标题反馈：" + " ".join(title_feedback))
            
        goal_feedback = self._generate_business_goal_feedback(goal_scores)
        if goal_feedback:
            feedback_parts.append("业务目标反馈：" + " ".join(goal_feedback))
            
        scope_feedback = self._generate_data_scope_feedback(scope_scores)
        if scope_feedback:
            feedback_parts.append("数据范围反馈：" + " ".join(scope_feedback))
            
        output_feedback = self._generate_expected_output_feedback(output_scores)
        if output_feedback:
            feedback_parts.append("预期输出反馈：" + " ".join(output_feedback))
        
        # 最后提供一些鼓励
        if avg_score >= 0.7:
            feedback_parts.append("您的需求定义已经很好，只需要小幅调整即可进一步提高清晰度。")
        else:
            feedback_parts.append("根据以上反馈调整您的需求，可以大幅提高研究人员理解和实施的效率。")
        
        # 组合所有反馈
        feedback = " ".join(feedback_parts)
        
        # 返回三个评分和反馈
        return clarity_score, feasibility_score, completeness_score, feedback

# 创建全局分析器实例
analyzer = RequirementAnalyzer()

async def analyze_requirement(
    title: str,
    business_goal: str,
    data_scope: str,
    expected_output: str,
    priority: str = "Medium"
) -> Tuple[float, float, float, str]:
    """
    分析需求并生成分数和反馈
    
    Returns:
        Tuple containing clarity_score, feasibility_score, completeness_score, and feedback.
    """
    return analyzer.analyze(title, business_goal, data_scope, expected_output, priority) 