from sqlalchemy.orm import Session
from database import Issue
from database import IssueDetail
import io

def get_issue(db: Session, issue_id: int):
    return db.query(Issue).filter(Issue.id == issue_id).first()

def get_issue_details(db: Session, issue_id: int):
    return db.query(IssueDetail).filter(IssueDetail.issue_id == issue_id).order_by(IssueDetail.date.asc()).all()