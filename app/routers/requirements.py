from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Body, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import outerjoin
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from ..database import get_db
from ..models.models import User, Requirement, Feedback
from ..auth import get_current_active_user
from ..ai_service import analyze_requirement

router = APIRouter()

class RequirementCreate(BaseModel):
    title: str
    priority: str
    business_goal: str
    data_scope: str
    expected_output: Optional[str] = None
    deadline: Optional[datetime] = None

class FeedbackCreate(BaseModel):
    content: str

class RequirementVerify(BaseModel):
    title: str
    priority: str
    business_goal: str
    data_scope: str
    expected_output: Optional[str] = None

class RequirementUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = None
    business_goal: Optional[str] = None
    data_scope: Optional[str] = None
    expected_output: Optional[str] = None
    deadline: Optional[datetime] = None
    assigned_to_id: Optional[int] = None

@router.post("/requirements/")
async def create_requirement(
    title: str = Form(...),
    priority: str = Form(...),
    business_goal: str = Form(...),
    data_scope: str = Form(...),
    expected_output: Optional[str] = Form(None),
    deadline: Optional[str] = Form(None),
    files: List[UploadFile] = File(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "pm":
        raise HTTPException(
            status_code=403,
            detail="Only PMs can create requirements"
        )
    
    # Convert string date to datetime
    deadline_dt = None
    if deadline and deadline.strip():
        try:
            deadline_dt = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            # Handle invalid date format
            pass
        
    # Process uploaded files (if needed)
    file_info = []
    if files:
        for file in files:
            # In a real app, you would save the file content to disk or cloud storage
            # Here we just store the filename and size
            file_info.append(f"{file.filename} ({len(await file.read()) / 1024:.1f} KB)")
            # Reset file position after reading
            await file.seek(0)
    
    # Append file information to data_scope if files were uploaded
    if file_info:
        data_scope = f"{data_scope} - Files: {', '.join(file_info)}"
        
    # Use AI service to analyze requirement
    clarity_score, feasibility_score, completeness_score, ai_feedback = await analyze_requirement(
        title,
        business_goal,
        data_scope,
        expected_output,
        priority
    )
    
    requirement = Requirement(
        creator_id=current_user.id,
        title=title,
        priority=priority,
        business_goal=business_goal,
        data_scope=data_scope,
        expected_output=expected_output,
        deadline=deadline_dt,
        clarity_score=clarity_score,
        feasibility_score=feasibility_score,
        completeness_score=completeness_score,
        ai_feedback=ai_feedback
    )
    
    async with db as session:
        session.add(requirement)
        await session.commit()
        await session.refresh(requirement)
        
    return requirement

@router.post("/verify-requirement/")
async def verify_requirement(
    req: RequirementVerify,
    current_user: User = Depends(get_current_active_user)
):
    """Verify a requirement before submission using AI"""
    if current_user.role != "pm":
        raise HTTPException(
            status_code=403,
            detail="Only PMs can verify requirements"
        )
    
    # For verification, we don't actually process files, just 
    # acknowledge their existence in the data_scope field
    data_scope = req.data_scope
    
    # Set default empty string for expected_output if None
    expected_output = req.expected_output if req.expected_output is not None else ""
    
    # Use AI service to analyze requirement
    clarity_score, feasibility_score, completeness_score, ai_feedback = await analyze_requirement(
        req.title,
        req.business_goal,
        data_scope,
        expected_output,
        req.priority
    )
    
    return {
        "clarity_score": clarity_score,
        "feasibility_score": feasibility_score,
        "completeness_score": completeness_score,
        "ai_feedback": ai_feedback
    }

@router.get("/requirements/")
async def get_requirements(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    async with db as session:
        if current_user.role == "pm":
            # PMs see their own requirements
            query = select(Requirement, User.email.label("assigned_email")).outerjoin(
                User, Requirement.assigned_to_id == User.id
            ).where(Requirement.creator_id == current_user.id)
            result = await session.execute(query)
        else:
            # Researchers see requirements assigned to them and unassigned ones
            query = select(Requirement, User.email.label("assigned_email")).outerjoin(
                User, Requirement.assigned_to_id == User.id
            ).where(
                (Requirement.assigned_to_id == current_user.id) | 
                (Requirement.assigned_to_id == None)
            )
            result = await session.execute(query)
            
        requirements_with_assignment = []
        for req, assigned_email in result:
            req_dict = {
                "id": req.id,
                "creator_id": req.creator_id,
                "title": req.title,
                "priority": req.priority,
                "business_goal": req.business_goal,
                "data_scope": req.data_scope,
                "expected_output": req.expected_output,
                "deadline": req.deadline,
                "created_at": req.created_at,
                "clarity_score": req.clarity_score,
                "feasibility_score": req.feasibility_score,
                "completeness_score": req.completeness_score,
                "ai_feedback": req.ai_feedback,
                "assigned_to_id": req.assigned_to_id,
                "assigned_to": assigned_email
            }
            requirements_with_assignment.append(req_dict)
        
    return requirements_with_assignment

@router.post("/requirements/{requirement_id}/feedback")
async def create_feedback(
    requirement_id: int,
    feedback: FeedbackCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "researcher":
        raise HTTPException(
            status_code=403,
            detail="Only researchers can provide feedback"
        )
        
    async with db as session:
        # Check if requirement exists
        result = await session.execute(
            select(Requirement).filter(Requirement.id == requirement_id)
        )
        requirement = result.scalar_one_or_none()
        
        if not requirement:
            raise HTTPException(
                status_code=404,
                detail="Requirement not found"
            )
            
        feedback_obj = Feedback(
            requirement_id=requirement_id,
            researcher_id=current_user.id,
            content=feedback.content
        )
        
        session.add(feedback_obj)
        await session.commit()
        await session.refresh(feedback_obj)
        
    return feedback_obj

@router.get("/researchers/")
async def get_researchers(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all researchers for assignment"""
    if current_user.role != "pm":
        raise HTTPException(
            status_code=403,
            detail="Only PMs can view researchers list"
        )
        
    async with db as session:
        result = await session.execute(
            select(User).filter(User.role == "researcher")
        )
        researchers = result.scalars().all()
        
    return [{"id": user.id, "email": user.email} for user in researchers]

# Legacy helper functions - keeping these for fallback
def calculate_clarity_score(business_goal: str, data_scope: str) -> float:
    # Simple scoring based on length and completeness
    score = 0.0
    if len(business_goal) > 50:
        score += 0.5
    if len(data_scope) > 50:
        score += 0.5
    return min(score, 1.0)

def calculate_feasibility_score(business_goal: str, expected_output: str) -> float:
    # Simple scoring based on length and completeness
    score = 0.0
    if len(business_goal) > 50:
        score += 0.5
    if len(expected_output) > 30:
        score += 0.5
    return min(score, 1.0)

def calculate_completeness_score(business_goal: str, data_scope: str, expected_output: str) -> float:
    # Simple scoring based on all components being present
    score = 0.0
    if business_goal:
        score += 0.33
    if data_scope:
        score += 0.33
    if expected_output:
        score += 0.34
    return score

def generate_ai_feedback(business_goal: str, data_scope: str, expected_output: str) -> str:
    feedback = []
    
    # Check business goal
    if len(business_goal) < 50:
        feedback.append("Consider providing more details about your business goal.")
    
    # Check data scope
    if len(data_scope) < 50:
        feedback.append("The data scope could be more specific. Consider including time range, geographic scope, or user segments.")
    
    # Check expected output
    if len(expected_output) < 30:
        feedback.append("Please clarify what type of output you expect from this requirement.")
        
    if not feedback:
        feedback.append("Your requirement is well-defined. Consider adding any additional context that might help researchers.")
        
    return " ".join(feedback)

@router.put("/requirements/{requirement_id}")
async def update_requirement(
    requirement_id: int,
    update_data: RequirementUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update an existing requirement or assign it to a researcher"""
    if current_user.role != "pm":
        raise HTTPException(
            status_code=403,
            detail="Only PMs can update requirements"
        )
        
    async with db as session:
        # Check if requirement exists and belongs to the current user
        result = await session.execute(
            select(Requirement).filter(
                Requirement.id == requirement_id,
                Requirement.creator_id == current_user.id
            )
        )
        requirement = result.scalar_one_or_none()
        
        if not requirement:
            raise HTTPException(
                status_code=404,
                detail="Requirement not found or you don't have permission to edit it"
            )
            
        # Update fields if provided
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            if field == 'assigned_to_id' and value is not None:
                # Verify that the assigned user exists and is a researcher
                user_result = await session.execute(
                    select(User).filter(User.id == value, User.role == "researcher")
                )
                user = user_result.scalar_one_or_none()
                if not user:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid user ID or user is not a researcher"
                    )
            setattr(requirement, field, value)
        
        await session.commit()
        await session.refresh(requirement)
        
    return requirement

@router.delete("/requirements/{requirement_id}")
async def delete_requirement(
    requirement_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a requirement"""
    if current_user.role != "pm":
        raise HTTPException(
            status_code=403,
            detail="Only PMs can delete requirements"
        )
        
    async with db as session:
        # Check if requirement exists and belongs to the current user
        result = await session.execute(
            select(Requirement).filter(
                Requirement.id == requirement_id,
                Requirement.creator_id == current_user.id
            )
        )
        requirement = result.scalar_one_or_none()
        
        if not requirement:
            raise HTTPException(
                status_code=404,
                detail="Requirement not found or you don't have permission to delete it"
            )
            
        # Delete the requirement
        await session.delete(requirement)
        await session.commit()
        
    return {"message": "Requirement deleted successfully"} 