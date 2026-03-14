from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.hero import Hero
from app.models.match import Match
from app.models.match_participant import MatchParticipant
from app.schemas.match import MatchDetailRead, MatchParticipantRead, MatchRead


router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("", response_model=list[MatchRead])
def list_matches(
    hero_id: int | None = Query(default=None),
    region_mode: str | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[MatchRead]:
    statement = select(Match)

    if hero_id is not None:
        hero = db.get(Hero, hero_id)
        if hero is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hero with id {hero_id} was not found.",
            )
        statement = statement.join(MatchParticipant, MatchParticipant.match_id == Match.id).where(
            MatchParticipant.hero_id == hero_id
        )

    if region_mode is not None:
        statement = statement.where(Match.region_mode == region_mode)

    if date_from is not None:
        statement = statement.where(Match.start_time >= date_from.isoformat())

    if date_to is not None:
        statement = statement.where(Match.start_time < date_to.replace(day=date_to.day).isoformat())

    statement = statement.distinct().order_by(Match.start_time.desc(), Match.id.desc())
    matches = list(db.scalars(statement).all())
    return [MatchRead.model_validate(match) for match in matches]


@router.get("/{match_id}", response_model=MatchDetailRead)
def get_match_detail(match_id: int, db: Session = Depends(get_db)) -> MatchDetailRead:
    match = db.get(Match, match_id)
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} was not found.",
        )

    statement = (
        select(MatchParticipant, Hero.name)
        .join(Hero, Hero.id == MatchParticipant.hero_id)
        .where(MatchParticipant.match_id == match_id)
        .order_by(MatchParticipant.team.asc(), MatchParticipant.account_id.asc())
    )
    rows = db.execute(statement).all()

    participants = [
        MatchParticipantRead(
            account_id=participant.account_id,
            team=participant.team,
            hero_id=participant.hero_id,
            hero_name=hero_name,
            hero_level=participant.hero_level,
            match_result=participant.match_result,
            player_kills=participant.player_kills,
            player_deaths=participant.player_deaths,
            player_assists=participant.player_assists,
            last_hits=participant.last_hits,
            denies=participant.denies,
            net_worth=participant.net_worth,
            player_damage=participant.player_damage,
            damage_taken=participant.damage_taken,
            boss_damage=participant.boss_damage,
            creep_damage=participant.creep_damage,
            neutral_damage=participant.neutral_damage,
            shots_hit=participant.shots_hit,
            shots_missed=participant.shots_missed,
        )
        for participant, hero_name in rows
    ]

    return MatchDetailRead(
        id=match.id,
        start_time=match.start_time,
        game_mode=match.game_mode,
        match_mode=match.match_mode,
        region_mode=match.region_mode,
        duration_seconds=match.duration_seconds,
        winning_team=match.winning_team,
        net_worth_team_0=match.net_worth_team_0,
        net_worth_team_1=match.net_worth_team_1,
        objectives_mask_team0=match.objectives_mask_team0,
        objectives_mask_team1=match.objectives_mask_team1,
        participants=participants,
    )
