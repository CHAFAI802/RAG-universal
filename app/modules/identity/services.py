from sqlalchemy.orm import Session

from app.modules.identity.models import Identity, IdentityType


class IdentityService:
    def __init__(self, session: Session):
        self.session = session

    def create_human_identity(self, display_name: str) -> Identity:
        display_name = display_name.strip()

        if not display_name:
            raise ValueError("Le nom d'affichage est obligatoire.")

        if len(display_name) > 150:
            raise ValueError("Le nom d'affichage ne peut pas dépasser 150 caractères.")

        identity = Identity(
            identity_type=IdentityType.HUMAN,
            display_name=display_name,
        )

        try:
            self.session.add(identity)
            self.session.flush()
            self.session.refresh(identity)
            self.session.commit()
            return identity

        except Exception:
            self.session.rollback()
            raise
