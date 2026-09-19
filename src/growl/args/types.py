from typing import Iterable, TypeAlias

from .options import CompasRange, CompasSet, CompasVector
from .utils import ItemT, NumericT

###########################################################################
### Exported type aliases to enable or disable range/set/vector parsers ###
###  * NB the bare type is always placed last in case it is `str`,
###    which would always parse successfully
###########################################################################

AllowCompasRangeOrSet: TypeAlias = (
    CompasRange[NumericT] | CompasSet[NumericT] | Iterable[NumericT] | NumericT | None
)
AllowCompasRange: TypeAlias = CompasRange[NumericT] | Iterable[NumericT] | NumericT | None
AllowCompasSet: TypeAlias = CompasSet[ItemT] | Iterable[ItemT] | ItemT | None
AllowCompasVector: TypeAlias = CompasVector[ItemT] | Iterable[ItemT] | ItemT | None
