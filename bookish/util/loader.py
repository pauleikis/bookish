from typing import List

from bookish.model import NounTranslation, VerbTranslation, SimpleTranslation, Translation


def all_translations() -> List[Translation]:
    return list(NounTranslation.select()) + list(VerbTranslation.select()) + list(SimpleTranslation.select())