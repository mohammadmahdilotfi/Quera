from typing import List,Optional

from sqlalchemy import create_engine, MetaData
from sqlalchemy import URL
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

DB_NAME = 'Transfermarkt_database'

url_object = URL.create(
    "mysql+mysqlconnector",
    username="root",
    password="1234",
    host="localhost",
    database=DB_NAME

)


# engine = create_engine(url_object)


def create_database():
    with engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {DB_NAME}"))


def show_database():
    with engine.connect() as conn:
        results = conn.execute(text('SHOW DATABASES;'))
        for res in results:
            return res


engine = create_engine(url_object)



class Base(DeclarativeBase):
    pass


class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255))
    market_value: Mapped[float] = mapped_column(Float, nullable=True)
    # average_age: Mapped[float] = mapped_column(Float, nullable=True)

    players_stats: Mapped["PlayerStat"] = relationship('PlayerStat', back_populates="team")
    teams_stats: Mapped["TeamStat"] = relationship('TeamStat', back_populates="team")
    achievements: Mapped["Achievement"] = relationship('Achievement', back_populates="team")


def __repr__(self):
    return f"Team(id={self.id}, team_name='{self.team_name}', market_value={self.market_value}, average_age={self.average_age})"


class Season(Base):
    __tablename__ = "season"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_at: Mapped[int] = mapped_column(Integer)

    players_stats: Mapped[List["PlayerStat"]] = relationship(back_populates="season")
    teams_stats: Mapped[List["TeamStat"]] = relationship(back_populates="season")
    transfers: Mapped[List["Transfer"]] = relationship(back_populates="season")


class Competition(Base):
    __tablename__ = "competition"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    competition_name: Mapped[str] = mapped_column(String(128))

    players_stats: Mapped[List["PlayerStat"]] = relationship(back_populates="competition")

    def __repr__(self):
        return f"Season(id={self.id}, name='{self.name}', start_at={self.start_at}, end_at={self.end_at})"


class Achievement(Base):
    __tablename__ = "achievement"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cup_name: Mapped[str] = mapped_column(String(128))
    cup_count: Mapped[int] = mapped_column(Integer)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))

    team: Mapped["Team"] = relationship(back_populates="achievements")


class Transfer(Base):
    __tablename__ = "transfer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("season.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    origin_team_id: Mapped[int] = mapped_column(Integer)
    destination_team_id: Mapped[int] = mapped_column(Integer)
    mv: Mapped[Optional[float]] = mapped_column(Float,nullable=True)
    fee: Mapped[Optional[str]] = mapped_column(String(64),nullable=True)
    joined: Mapped[str] = mapped_column(String(128))
    left: Mapped[str] = mapped_column(String(128))

    player: Mapped["Player"] = relationship(back_populates="transfers")
    season: Mapped["Season"] = relationship(back_populates="transfers")


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    current_team: Mapped[str] = mapped_column(String(128),nullable=True)
    full_name: Mapped[str] = mapped_column(String(128),nullable=True)
    age: Mapped[int] = mapped_column(Integer,nullable=True)
    birth_place: Mapped[str] = mapped_column(String(128),nullable=True)
    height: Mapped[float] = mapped_column(Float,nullable=True)
    citizenship: Mapped[str] = mapped_column(String(255),nullable=True)
    nationality: Mapped[str] = mapped_column(String(64),nullable=True)
    main_position: Mapped[str] = mapped_column(String(64),nullable=True)
    other_position: Mapped[str] = mapped_column(String(255),nullable=True)
    foot: Mapped[str] = mapped_column(String(32),nullable=True)
    total_goals_in_clubs: Mapped[int] = mapped_column(Integer,nullable=True)
    total_assists: Mapped[int] = mapped_column(Integer,nullable=True)
    international_goals: Mapped[int] = mapped_column(Integer,nullable=True)
    caps: Mapped[int] = mapped_column(Integer,nullable=True)
    total_squad: Mapped[int] = mapped_column(Integer,nullable=True)
    total_appearance: Mapped[int] = mapped_column(Integer,nullable=True)
    total_own_goal: Mapped[int] = mapped_column(Integer,nullable=True)
    total_sub_off: Mapped[int] = mapped_column(Integer,nullable=True)
    total_sub_on: Mapped[int] = mapped_column(Integer,nullable=True)
    total_yellow_card: Mapped[int] = mapped_column(Integer,nullable=True)
    total_second_yellow_card: Mapped[int] = mapped_column(Integer,nullable=True)
    total_red_card: Mapped[int] = mapped_column(Integer,nullable=True)
    total_penalty: Mapped[int] = mapped_column(Integer,nullable=True)
    total_minutes_per_goal: Mapped[float] = mapped_column(Float,nullable=True)
    total_minutes_play: Mapped[float] = mapped_column(Float,nullable=True)
    total_goal_conceded: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    total_clean_sheet: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    total_PPG: Mapped[float] = mapped_column(Float,nullable=True)
    highest_market_value: Mapped[float] = mapped_column(Float,nullable=True)
    current_market_value: Mapped[float] = mapped_column(Float,nullable=True)

    players_stats: Mapped[List["PlayerStat"]] = relationship('PlayerStat', back_populates="player")
    transfers: Mapped[List["Transfer"]] = relationship(back_populates="player")


class PlayerStat(Base):
    __tablename__ = "player_stat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    competition_id: Mapped[int] = mapped_column(ForeignKey("competition.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    squad: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    appearance: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    PPG: Mapped[Optional[float]] = mapped_column(Float,nullable=True)
    goals: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    assists: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("season.id"))
    own_goal: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    sub_off: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    sub_on: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    yellow_card: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    second_yellow_card: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    red_card: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    penalty_goals: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    clean_sheets: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    goal_conceded: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    minutes_per_goal: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    minutes_play: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)

    team: Mapped["Team"] = relationship(back_populates="players_stats")
    player: Mapped["Player"] = relationship(back_populates="players_stats")
    competition: Mapped["Competition"] = relationship(back_populates="players_stats")
    season: Mapped["Season"] = relationship(back_populates="players_stats")


class TeamStat(Base):
    __tablename__ = "teamstat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    season_id: Mapped[int] = mapped_column(ForeignKey("season.id"))
    league:Mapped[str] = mapped_column(String(64))
    matches: Mapped[int] = mapped_column(Integer)
    wins: Mapped[int] = mapped_column(Integer)
    losts: Mapped[int] = mapped_column(Integer)
    draws: Mapped[int] = mapped_column(Integer)
    goals: Mapped[str] = mapped_column(String(32))
    goal_differenece: Mapped[int] = mapped_column(Integer)
    pts: Mapped[int] = mapped_column(Integer)
    rank : Mapped[int] = mapped_column(Integer)
    
    team: Mapped["Team"] = relationship(back_populates="teams_stats")
    season: Mapped["Season"] = relationship(back_populates="teams_stats")


Base.metadata.create_all(engine)
