import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.routes.analytics import (
    build_hero_matchups,
    build_hero_overview,
    build_hero_synergies,
    build_hero_trend,
)
from app.db.session import get_db
from app.models.hero import Hero
from app.models.saved_report import SavedReport
from app.schemas.saved_report import (
    SavedReportCreate,
    SavedReportRead,
    SavedReportResultRead,
    SavedReportUpdate,
)


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


@router.post(
    "",
    response_model=SavedReportRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a saved report preset",
    description="Creates a reusable report definition that can later generate analytics results from stored filters.",
    responses={404: {"description": "Referenced hero was not found."}},
)
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


@router.get(
    "/{report_id}/result",
    response_model=SavedReportResultRead,
    summary="Generate a saved report result",
    description=(
        "Generates analytics output from a saved report preset. "
        "Currently supports hero_overview, hero_meta, hero_trend, hero_matchups, and hero_synergies."
    ),
    responses={
        400: {"description": "The saved report cannot generate a result because required fields are missing or the report type is unsupported."},
        404: {"description": "Saved report was not found."},
    },
)
def get_saved_report_result(report_id: int, db: Session = Depends(get_db)) -> SavedReportResultRead:
    saved_report = db.get(SavedReport, report_id)
    if saved_report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Saved report with id {report_id} was not found.",
        )

    if saved_report.hero_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This saved report does not define a hero_id and cannot generate a hero analytics result.",
        )

    if saved_report.report_type in {"hero_meta", "hero_overview"}:
        result = build_hero_overview(saved_report.hero_id, db).model_dump(mode="json")
    elif saved_report.report_type == "hero_trend":
        result = build_hero_trend(
            saved_report.hero_id,
            db,
            date_from=saved_report.date_from,
            date_to=saved_report.date_to,
        ).model_dump(mode="json")
    elif saved_report.report_type == "hero_matchups":
        result = build_hero_matchups(saved_report.hero_id, db).model_dump(mode="json")
    elif saved_report.report_type == "hero_synergies":
        result = build_hero_synergies(saved_report.hero_id, db).model_dump(mode="json")
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Saved report type '{saved_report.report_type}' is not supported for generated results."
            ),
        )

    return SavedReportResultRead(
        report_id=saved_report.id,
        name=saved_report.name,
        report_type=saved_report.report_type,
        result=result,
    )


@router.patch("/{report_id}", response_model=SavedReportRead)
def update_saved_report(
    report_id: int, payload: SavedReportUpdate, db: Session = Depends(get_db)
) -> SavedReportRead:
    saved_report = db.get(SavedReport, report_id)
    if saved_report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Saved report with id {report_id} was not found.",
        )

    if payload.hero_id is not None:
        hero = db.get(Hero, payload.hero_id)
        if hero is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hero with id {payload.hero_id} was not found.",
            )

    update_data = payload.model_dump(exclude_unset=True)

    if "filters_json" in update_data:
        saved_report.filters_json = (
            json.dumps(update_data["filters_json"]) if update_data["filters_json"] is not None else None
        )
        update_data.pop("filters_json")

    for field, value in update_data.items():
        setattr(saved_report, field, value)

    db.commit()
    db.refresh(saved_report)
    return _to_read_model(saved_report)


@router.delete("/{report_id}", status_code=status.HTTP_200_OK)
def delete_saved_report(report_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    saved_report = db.get(SavedReport, report_id)
    if saved_report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Saved report with id {report_id} was not found.",
        )

    db.delete(saved_report)
    db.commit()
    return {"message": "Saved report deleted successfully"}
