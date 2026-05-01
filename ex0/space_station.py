from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0, le=100)
    oxygen_level: float = Field(..., ge=0, le=100)
    last_maintenance: datetime
    notes: str | None = Field(default=None, max_length=200)
    is_operational: bool = True


def main() -> None:
    try:
        print("========================================")
        space_station = SpaceStation(
            station_id="IS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
            is_operational=True,
        )
        status: str = (
            "Operational"
            if space_station.is_operational
            else "Not Operational"
        )
        print("Space Station Data Validation")
        print("Valid station created:")
        print(f"ID: {space_station.station_id}")
        print(f"Name: {space_station.name}")
        print(f"Crew: {space_station.crew_size} people")
        print(f"Power: {space_station.power_level}%")
        print(f"Oxygen: {space_station.oxygen_level}%")
        print(f"Status: {status}\n")
    except ValidationError as e:
        print(e.errors()[0]["msg"])

    try:
        print("========================================")
        space_station = SpaceStation(
            station_id="IS001",
            name="Intertional Space Station",
            crew_size=39,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
            is_operational=False,
        )
        print("Space Station Data Validation")
        print("Valid station created:")
        print(f"ID: {space_station.station_id}")
        print(f"Name: {space_station.name}")
        print(f"Crew: {space_station.crew_size} people")
        print(f"Power: {space_station.power_level}%")
        print(f"Oxygen: {space_station.oxygen_level}%")
        print(f"Status: {status}")
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
