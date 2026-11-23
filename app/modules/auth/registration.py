from sqlalchemy.orm import Session

from app.modules.credentials.models import Credential
from app.modules.credentials.services import CredentialService
from app.modules.identity.models import Identity
from app.modules.identity.services import IdentityService


class RegistrationService:
    def __init__(self, session: Session):
        self.session = session
        self.identity_service = IdentityService(session)
        self.credential_service = CredentialService(session)

    def register(
        self,
        *,
        display_name: str,
        username: str,
        password: str,
    ) -> tuple[Identity, Credential]:
        """
        Crée une identité humaine et son credential dans une seule transaction.

        Aucun commit intermédiaire n'est effectué.
        Toute erreur après le début de la transaction provoque un rollback.
        """

        # Construction et validation sans écriture en base.
        identity = self.identity_service.build_human_identity(display_name)

        try:
            # Première écriture : Identity.
            self.session.add(identity)
            self.session.flush()

            # Deuxième écriture : Credential.
            credential = self.credential_service.create_username_password_credential(
                identity_id=identity.identity_id,
                username=username,
                password=password,
            )

            # Commit unique pour les deux objets.
            self.session.commit()

            return identity, credential

        except Exception:
            self.session.rollback()
            raise
