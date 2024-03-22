from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, computed_field, RootModel, SerializeAsAny


class Game(BaseModel):
    date: str
    game: str
    points: int
    round: str


class PlayerStats(BaseModel):
    player: str
    team: str
    games: Optional[List[Game]] = List

    @computed_field
    @property
    def totalPoints(self) -> int:
        total: int = 0
        for game in self.games:
            total += game.points
        return total
    

class Squad(BaseModel):
    coach: str
    players: List[PlayerStats]

    @computed_field
    @property
    def totalPoints(self) -> int:
        total: int = 0
        for game in self.players:
            total += game.totalPoints
        return total
    
class Squads(RootModel):
    root: List[SerializeAsAny[Squad]]
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    

class SquadRow(BaseModel):
    coach: str
    player: str
    team: str
    round1: Optional[int] = 0
    round2: Optional[int] = 0
    round3: Optional[int] = 0 
    round4: Optional[int] = 0 
    round5: Optional[int] = 0
    round6: Optional[int] = 0
