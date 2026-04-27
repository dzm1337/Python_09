from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0, le=100)
    oxygen_level: float = Field(..., ge=0, le=100)
    is_operational: bool = True


def main() -> None:
    space_station = SpaceStation(
        station_id="IS001",
        name="Intertional Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        is_operational=False,
    )
    status: str = "Operational"
    if not space_station.is_operational:
        status = "Not Operational"

    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")
    print(f"ID: {space_station.station_id}")
    print(f"Name: {space_station.name}")
    print(f"Crew: {space_station.crew_size} people")
    print(f"Power: {space_station.power_level}%")
    print(f"Oxygen: {space_station.oxygen_level}%")
    print(f"Status: {status}")

    try:
        space_station = SpaceStation(
            station_id="IS001",
            name="Intertional Space Station",
            crew_size=39,
            power_level=85.5,
            oxygen_level=92.3,
            is_operational=False,
        )
        status: str = "Operational"
        if not space_station.is_operational:
            status = "Not Operational"
        print("Space Station Data Validation")
        print("========================================")
        print("Valid station created:")
        print(f"ID: {space_station.station_id}")
        print(f"Name: {space_station.name}")
        print(f"Crew: {space_station.crew_size} people")
        print(f"Power: {space_station.power_level}%")
        print(f"Oxygen: {space_station.oxygen_level}%")
        print(f"Status: {status}")
    except ValidationError as e:
        print("Expected validation error:")
        print(repr(exc.errors()[0]['type']))


if __name__ == "__main__":
    main()
