from collections.abc import Iterable

from .options import CompasRange, CompasSet, CompasVector
from .utils import ItemT, NumericT_co

###########################################################################
### Exported type aliases to enable or disable range/set/vector parsers ###
###  * NB the bare type is always placed last in case it is `str`,
###    which would always parse successfully
###########################################################################

AllowCompasRangeOrSet = (
    CompasRange[NumericT_co] | CompasSet[NumericT_co] | Iterable[NumericT_co] | NumericT_co | None
)
AllowCompasRange = CompasRange[NumericT_co] | Iterable[NumericT_co] | NumericT_co | None
AllowCompasSet = CompasSet[ItemT] | Iterable[ItemT] | ItemT | None
AllowCompasVector = CompasVector[ItemT] | Iterable[ItemT] | ItemT | None
