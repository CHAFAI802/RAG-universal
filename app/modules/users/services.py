import uuid

from sqlalchemy.orm import Session

from app.modules.credentials.models import Credential, CredentialOwnerType
from app.modules.credentials.services import CredentialService
from app.modules.users.models import User


class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.credential_service = CredentialService(session)

    def create_user(
        self,
        *,
        identity_id: uuid.UUID,
        username: str,
        password: str,
    ) -> tuple[User, Credential]:
        """
        Crée un User et son Credential dans une seule transaction.

        L'Identity provient exclusivement de l'administrateur authentifié.
        Aucun commit intermédiaire n'est effectué : toute erreur provoque
        le rollback complet.
        """

        try:
            user = User(identity_id=identity_id)
            self.session.add(user)
            self.session.flush()

            credential = self.credential_service.create_username_password_credential(
                identity_id=identity_id,
                username=username,
                password=password,
                owner_type=CredentialOwnerType.USER,
                user_id=user.user_id,
            )

            self.session.commit()

            return user, credential

        except Exception:
            self.session.rollback()
            raise
