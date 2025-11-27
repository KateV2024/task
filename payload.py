from dataclasses import dataclass, asdict
import random
import string

@dataclass
class Payload:
    title: str
    description: str

    @staticmethod
    def generate_payload(hardcoded_part_of_title: str) -> dict:
        random_title_part = ''.join(random.choices(string.ascii_letters, k=6))
        random_description = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        payload = Payload(
            title=f"{hardcoded_part_of_title}_{random_title_part}",
            description=random_description
        )

        return asdict(payload)


valid_payload = Payload.generate_payload("Event")
