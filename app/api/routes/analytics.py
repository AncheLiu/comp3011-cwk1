from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session, aliased

from app.db.session import get_db
from app.models.hero import Hero
from app.models.match import Match
from app.models.match_participant import MatchParticipant
from app.schemas.analytics import (
    HeroMatchupRead,
    HeroMatchupsRead,
    HeroOverviewRead,
    HeroTrendPointRead,
    HeroTrendRead,
)


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/heroes/{hero_id}/overview", response_model=HeroOverviewRead)
def get_hero_overview(hero_id: int, db: Session = Depends(get_db)) -> HeroOverviewRead:
    hero = db.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id {hero_id} was not found.",
        )

    statement = select(
        func.count(MatchParticipant.id),
        func.coalesce(func.sum(case((MatchParticipant.match_result == 1, 1), else_=0)), 0),
        func.coalesce(func.avg(MatchParticipant.player_kills), 0.0),
        func.coalesce(func.avg(MatchParticipant.player_deaths), 0.0),
        func.coalesce(func.avg(MatchParticipant.player_assists), 0.0),
        func.coalesce(func.avg(MatchParticipant.net_worth), 0.0),
    ).where(MatchParticipant.hero_id == hero_id)

    matches, wins, avg_kills, avg_deaths, avg_assists, avg_net_worth = db.execute(statement).one()

    matches = int(matches or 0)
    wins = int(wins or 0)
    losses = matches - wins
    win_rate = round((wins / matches) * 100, 2) if matches else 0.0

    return HeroOverviewRead(
        hero_id=hero.id,
        hero_name=hero.name,
        matches=matches,
        wins=wins,
        losses=losses,
        win_rate=win_rate,
        avg_kills=round(float(avg_kills or 0.0), 2),
        avg_deaths=round(float(avg_deaths or 0.0), 2),
        avg_assists=round(float(avg_assists or 0.0), 2),
        avg_net_worth=round(float(avg_net_worth or 0.0), 2),
    )


@router.get("/heroes/{hero_id}/trend", response_model=HeroTrendRead)
def get_hero_trend(
    hero_id: int,
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db),
) -> HeroTrendRead:
    hero = db.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id {hero_id} was not found.",
        )

    trend_date = func.date(Match.start_time)
    statement = (
        select(
            trend_date.label("trend_date"),
            func.count(MatchParticipant.id),
            func.coalesce(func.sum(case((MatchParticipant.match_result == 1, 1), else_=0)), 0),
            func.coalesce(func.avg(MatchParticipant.player_kills), 0.0),
            func.coalesce(func.avg(MatchParticipant.player_deaths), 0.0),
            func.coalesce(func.avg(MatchParticipant.player_assists), 0.0),
        )
        .join(Match, Match.id == MatchParticipant.match_id)
        .where(MatchParticipant.hero_id == hero_id)
        .group_by(trend_date)
        .order_by(trend_date)
    )

    if date_from is not None:
        statement = statement.where(trend_date >= date_from.isoformat())
    if date_to is not None:
        statement = statement.where(trend_date <= date_to.isoformat())

    rows = db.execute(statement).all()
    points = []
    for trend_point_date, matches, wins, avg_kills, avg_deaths, avg_assists in rows:
        matches = int(matches or 0)
        wins = int(wins or 0)
        losses = matches - wins
        points.append(
            HeroTrendPointRead(
                date=str(trend_point_date),
                matches=matches,
                wins=wins,
                losses=losses,
                win_rate=round((wins / matches) * 100, 2) if matches else 0.0,
                avg_kills=round(float(avg_kills or 0.0), 2),
                avg_deaths=round(float(avg_deaths or 0.0), 2),
                avg_assists=round(float(avg_assists or 0.0), 2),
            )
        )

    return HeroTrendRead(
        hero_id=hero.id,
        hero_name=hero.name,
        bucket="day",
        points=points,
    )


@router.get("/heroes/{hero_id}/matchups", response_model=HeroMatchupsRead)
def get_hero_matchups(hero_id: int, db: Session = Depends(get_db)) -> HeroMatchupsRead:
    hero = db.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id {hero_id} was not found.",
        )

    target_participant = aliased(MatchParticipant)
    enemy_participant = aliased(MatchParticipant)
    enemy_hero = aliased(Hero)

    statement = (
        select(
            enemy_participant.hero_id,
            enemy_hero.name,
            func.count(enemy_participant.id),
            func.coalesce(func.sum(case((target_participant.match_result == 1, 1), else_=0)), 0),
        )
        .join(
            enemy_participant,
            (enemy_participant.match_id == target_participant.match_id)
            & (enemy_participant.team != target_participant.team),
        )
        .join(enemy_hero, enemy_hero.id == enemy_participant.hero_id)
        .where(target_participant.hero_id == hero_id)
        .group_by(enemy_participant.hero_id, enemy_hero.name)
        .order_by(func.count(enemy_participant.id).desc(), enemy_hero.name.asc())
    )

    rows = db.execute(statement).all()
    items = []
    for enemy_hero_id, enemy_hero_name, matches, wins in rows:
        matches = int(matches or 0)
        wins = int(wins or 0)
        losses = matches - wins
        items.append(
            HeroMatchupRead(
                enemy_hero_id=int(enemy_hero_id),
                enemy_hero_name=enemy_hero_name,
                matches=matches,
                wins=wins,
                losses=losses,
                win_rate=round((wins / matches) * 100, 2) if matches else 0.0,
            )
        )

    return HeroMatchupsRead(
        hero_id=hero.id,
        hero_name=hero.name,
        items=items,
    )
