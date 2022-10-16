from app.models.common import IDModelMixin, DateTimeModelMixin
from app.models.domain.profiles import Profile
from app.models.domain.rwmodel import RWModel


class Comment(IDModelMixin, DateTimeModelMixin, RWModel):
    body: str
    author: Profile
