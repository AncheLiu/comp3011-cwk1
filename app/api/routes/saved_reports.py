import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.hero import Hero
from app.models.saved_report import SavedReport
from app.schemas.saved_report import SavedReportCreate, SavedReportRead


router = APIRouter(prefix="/saved-reports", tags=["saved-reports"])


def _to_read_model(saved_report: SavedReport) -> SavedReportRead:
    return SavedReportRead(
        id=saved_report.id,
        name=saved_report.name,
        report_type=saved_report.report_type,
        hero_id=saved_report.hero_id,
        region_mode=saved_report.region_mode,
        rank_min=saved_report.rank_min,
        rank_max=saved_report.rank_max,
        date_from=saved_report.date_from,
        date_to=saved_report.date_to,
        filters_json=json.loads(saved_report.filters_json) if saved_report.filters_json else None,
        created_at=saved_report.created_at,
        updated_at=saved_report.updated_at,
    )


@router.post("", response_model=SavedReportRead, status_code=status.HTTP_201_CREATED)
def create_saved_report(payload: SavedReportCreate, db: Session = Depends(get_db)) -> SavedReportRead:
    if payload.hero_id is not None:
        hero = db.get(Hero, payload.hero_id)
        if hero is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hero with id {payload.hero_id} was not found.",
            )

    saved_report = SavedReport(
        name=payload.name,
        report_type=payload.report_type,
        hero_id=payload.hero_id,
        region_mode=payload.region_mode,
        rank_min=payload.rank_min,
        rank_max=payload.rank_max,
        date_from=payload.date_from,
        date_to=payload.date_to,
        filters_json=json.dumps(payload.filters_json) if payload.filters_json is not None else None,
    )
    db.add(saved_report)
    db.commit()
    db.refresh(saved_report)
    return _to_read_model(saved_report)


@router.get("", response_model=list[SavedReportRead])
def list_saved_reports(db: Session = Depends(get_db)) -> list[SavedReportRead]:
    statement = select(SavedReport).order_by(SavedReport.created_at.desc(), SavedReport.id.desc())
    saved_reports = list(db.scalars(statement).all())
    return [_to_read_model(saved_report) for saved_report in saved_reports]


@router.get("/{report_id}", response_model=SavedReportRead)
def get_saved_report(report_id: int, db: Session = Depends(get_db)) -> SavedReportRead:
    saved_report = db.get(SavedReport, report_id)
    if saved_report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Saved report with id {report_id} was not found.",
        )
    return _to_read_model(saved_report)
