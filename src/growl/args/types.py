from typing import Iterable, TypeAlias

from .options import CompasRange, CompasSet, CompasVector
from .utils import ItemT_co, NumericT_co

###########################################################################
### Exported type aliases to enable or disable range/set/vector parsers ###
###  * NB the bare type is always placed last in case it is `str`,
###    which would always parse successfully
###########################################################################

AllowCompasRangeOrSet: TypeAlias = (
    CompasRange[NumericT_co] | CompasSet[NumericT_co] | Iterable[NumericT_co] | NumericT_co | None
)
AllowCompasRange: TypeAlias = CompasRange[NumericT_co] | Iterable[NumericT_co] | NumericT_co | None
AllowCompasSet: TypeAlias = CompasSet[ItemT_co] | Iterable[ItemT_co] | ItemT_co | None
AllowCompasVector: TypeAlias = CompasVector[ItemT_co] | Iterable[ItemT_co] | ItemT_co | None
