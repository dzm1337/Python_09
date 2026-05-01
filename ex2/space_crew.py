from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class CrewRanks(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: CrewRanks
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_time: datetime
    duration_days: int = Field(..., ge=1, le=3650)  # max 10 years
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1, le=10000)

    @model_validator(mode="after")
    def mission_validations(self) -> "SpaceMission":
        if self.mission_id[0] != "M":
            raise ValueError("[ERROR]: mission_id must start with 'M'")

        required_rank: bool = any(
            member.rank == CrewRanks.captain
            or member.rank == CrewRanks.commander
            for member in self.crew
        )
        if not required_rank:
            raise ValueError(
                "[ERROR]: Crew must have at least one captain or commander"
            )

        if self.duration_days > 365:
            experienced: list[CrewMember] = []
            for member in self.crew:
                if member.years_experience >= 5:
                    experienced.append(member)
            if len(experienced) < len(self.crew) / 2:
                raise ValueError(
                    "[ERROR]: Long missions (> 365 days) "
                    "need 50% experienced crew (5+ years)"
                )

        active_members: bool = all(member.is_active for member in self.crew)
        if not active_members:
            raise ValueError("[ERROR]: All crew members must be active")

        return self


if __name__ == "__main__":
    print("Space Mission Crew Validation")

    sarah_connor = CrewMember(
        member_id="AC2024",
        name="Sarah Connor",
        rank=CrewRanks.commander,
        age=34,
        specialization="Mission Commander",
        years_experience=6,
        is_active=True,
    )

    john_smith = CrewMember(
        member_id="AC1996",
        name="John Smith",
        rank=CrewRanks.lieutenant,
        age=42,
        specialization="Navigation",
        years_experience=5,
        is_active=True,
    )

    alice_johnson = CrewMember(
        member_id="AC2042",
        name="Alice Johnson",
        rank=CrewRanks.officer,
        age=23,
        specialization="Engineering",
        years_experience=6,
        is_active=True,
    )
    print("=========================================")
    space_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        duration_days=900,
        crew=[sarah_connor, john_smith, alice_johnson],
        budget_millions=2500,
        launch_time=datetime.now(),
    )
    print(f"""Mission: {space_mission.mission_name}
ID: {space_mission.mission_id}
Destination: {space_mission.destination}
Duration: {space_mission.duration_days} days
Budget: ${space_mission.budget_millions}M
Crew size: {len(space_mission.crew)}
""")
    print("Crew members:")
    for member in space_mission.crew:
        print(
            f"- {member.name} ({member.rank.name}) - {member.specialization}"
        )
    try:
        print("=========================================")
        space_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            duration_days=900,
            crew=[alice_johnson, john_smith],
            budget_millions=2500,
            launch_time=datetime.now(),
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["ctx"]["error"])
