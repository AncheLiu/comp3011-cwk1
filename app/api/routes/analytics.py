from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session, aliased

from app.db.session import get_db
from app.models.hero import Hero
from app.models.match import Match
from app.models.match_participant import MatchParticipant
from app.schemas.analytics import (
    HeroMetaEntryRead,
    HeroMetaRead,
    HeroMatchupRead,
    HeroMatchupsRead,
    HeroOverviewRead,
    HeroSynergiesRead,
    HeroSynergyRead,
    HeroTrendPointRead,
    HeroTrendRead,
)


router = APIRouter(prefix="/analytics", tags=["analytics"])


def _get_existing_hero(hero_id: int, db: Session) -> Hero:
    hero = db.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id {hero_id} was not found.",
        )
    return hero


def build_hero_overview(hero_id: int, db: Session) -> HeroOverviewRead:
    hero = _get_existing_hero(hero_id, db)
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


def build_hero_trend(
    hero_id: int,
    db: Session,
    date_from: date | None = None,
    date_to: date | None = None,
) -> HeroTrendRead:
    hero = _get_existing_hero(hero_id, db)
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


def build_hero_matchups(hero_id: int, db: Session) -> HeroMatchupsRead:
    hero = _get_existing_hero(hero_id, db)
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


def build_hero_synergies(hero_id: int, db: Session) -> HeroSynergiesRead:
    hero = _get_existing_hero(hero_id, db)
    target_participant = aliased(MatchParticipant)
    ally_participant = aliased(MatchParticipant)
    ally_hero = aliased(Hero)

    statement = (
        select(
            ally_participant.hero_id,
            ally_hero.name,
            func.count(ally_participant.id),
            func.coalesce(func.sum(case((target_participant.match_result == 1, 1), else_=0)), 0),
        )
        .join(
            ally_participant,
            (ally_participant.match_id == target_participant.match_id)
            & (ally_participant.team == target_participant.team)
            & (ally_participant.account_id != target_participant.account_id),
        )
        .join(ally_hero, ally_hero.id == ally_participant.hero_id)
        .where(target_participant.hero_id == hero_id)
        .group_by(ally_participant.hero_id, ally_hero.name)
        .order_by(func.count(ally_participant.id).desc(), ally_hero.name.asc())
    )

    rows = db.execute(statement).all()
    items = []
    for ally_hero_id, ally_hero_name, matches, wins in rows:
        matches = int(matches or 0)
        wins = int(wins or 0)
        losses = matches - wins
        items.append(
            HeroSynergyRead(
                ally_hero_id=int(ally_hero_id),
                ally_hero_name=ally_hero_name,
                matches=matches,
                wins=wins,
                losses=losses,
                win_rate=round((wins / matches) * 100, 2) if matches else 0.0,
            )
        )

    return HeroSynergiesRead(
        hero_id=hero.id,
        hero_name=hero.name,
        items=items,
    )


def build_hero_meta(db: Session, sort_by: str = "win_rate", limit: int = 10) -> HeroMetaRead:
    statement = (
        select(
            Hero.id,
            Hero.name,
            func.count(MatchParticipant.id),
            func.coalesce(func.sum(case((MatchParticipant.match_result == 1, 1), else_=0)), 0),
            func.coalesce(func.avg(MatchParticipant.player_kills), 0.0),
            func.coalesce(func.avg(MatchParticipant.player_deaths), 0.0),
            func.coalesce(func.avg(MatchParticipant.player_assists), 0.0),
        )
        .join(MatchParticipant, MatchParticipant.hero_id == Hero.id)
        .group_by(Hero.id, Hero.name)
    )

    rows = db.execute(statement).all()
    items = []
    for hero_id, hero_name, matches, wins, avg_kills, avg_deaths, avg_assists in rows:
        matches = int(matches or 0)
        wins = int(wins or 0)
        losses = matches - wins
        items.append(
            HeroMetaEntryRead(
                hero_id=hero_id,
                hero_name=hero_name,
                matches=matches,
                wins=wins,
                losses=losses,
                win_rate=round((wins / matches) * 100, 2) if matches else 0.0,
                avg_kills=round(float(avg_kills or 0.0), 2),
                avg_deaths=round(float(avg_deaths or 0.0), 2),
                avg_assists=round(float(avg_assists or 0.0), 2),
            )
        )

    sort_options = {
        "win_rate": lambda item: (item.win_rate, item.matches, item.hero_name),
        "matches": lambda item: (item.matches, item.win_rate, item.hero_name),
        "avg_kills": lambda item: (item.avg_kills, item.win_rate, item.hero_name),
    }
    key_fn = sort_options.get(sort_by, sort_options["win_rate"])
    items.sort(key=key_fn, reverse=True)

    return HeroMetaRead(items=items[:limit])


@router.get(
    "/heroes/meta",
    response_model=HeroMetaRead,
    summary="Get ranked hero meta overview",
    description="Returns a ranked summary of imported hero performance across all stored match participant records.",
)
def get_hero_meta(
    sort_by: str = Query(default="win_rate"),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
) -> HeroMetaRead:
    return build_hero_meta(db, sort_by=sort_by, limit=limit)


@router.get(
    "/heroes/{hero_id}/overview",
    response_model=HeroOverviewRead,
    summary="Get hero overview analytics",
    description="Returns aggregate performance metrics for a single hero across imported matches.",
    responses={404: {"description": "Hero was not found."}},
)
def get_hero_overview(hero_id: int, db: Session = Depends(get_db)) -> HeroOverviewRead:
    return build_hero_overview(hero_id, db)


@router.get(
    "/heroes/{hero_id}/trend",
    response_model=HeroTrendRead,
    summary="Get hero trend analytics",
    description="Returns day-by-day hero performance trends, optionally filtered by an inclusive date range.",
    responses={404: {"description": "Hero was not found."}},
)
def get_hero_trend(
    hero_id: int,
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db),
) -> HeroTrendRead:
    return build_hero_trend(hero_id, db, date_from=date_from, date_to=date_to)


@router.get(
    "/heroes/{hero_id}/matchups",
    response_model=HeroMatchupsRead,
    summary="Get hero matchup analytics",
    description="Returns performance against enemy heroes based on imported match participant records.",
    responses={404: {"description": "Hero was not found."}},
)
def get_hero_matchups(hero_id: int, db: Session = Depends(get_db)) -> HeroMatchupsRead:
    return build_hero_matchups(hero_id, db)


@router.get(
    "/heroes/{hero_id}/synergies",
    response_model=HeroSynergiesRead,
    summary="Get hero synergy analytics",
    description="Returns performance alongside allied heroes based on imported match participant records.",
    responses={404: {"description": "Hero was not found."}},
)
def get_hero_synergies(hero_id: int, db: Session = Depends(get_db)) -> HeroSynergiesRead:
    return build_hero_synergies(hero_id, db)
