from uuid import uuid4 
from .base_otc import BaseOTC


class RegistrationOTC(BaseOTC):
    def __init__(self):
        super().__init__('user_registration')

    def create_otc(self):
        self._code = str(uuid4())
