from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime = Field(...)
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0, le=10)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def alien_contact_validator(self):
        self.contact_id = self.contact_id.upper()
        if self.contact_id[0] != "A" or self.contact_id[1] != "C":
            raise ValueError("[ERROR]: contact_id does not start with 'AC'")

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError(
                "[ERROR]: Physical contact reports must be verified"
            )

        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            raise ValueError(
                "[ERROR]: Telepathic contact requires at least 3 witnesses"
            )

        if self.signal_strength > 7 and not self.message_received:
            raise ValueError(
                "[ERROR]: Strong signals (> 7.0) require a message"
            )

        return self


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    alien_contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime.now(),
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
    )
    print(f"""ID: {alien_contact.contact_id}
Type: {alien_contact.contact_type.name}
Location: {alien_contact.location}
Signal: {alien_contact.signal_strength}/10
Duration: {alien_contact.duration_minutes} minutes
Witnesses: {alien_contact.witness_count}
Message: '{alien_contact.message_received}'""")

    print("======================================")
    try:
        alien_contact = AlienContact(
            contact_id="ac_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.telepathic,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli",
        )
    except ValidationError as e:
        print("Expected validation error:")
        msg = e.errors()[0]["msg"].replace("Value error, ", "")
        print(msg)
