from unitable import *

import_delimited("tips.csv")

replace(total_bill, total_bill)
generate("adjusted_bill", total_bill * 1.03)
drop(total_bill)

list_if(total_bill > 10)

sort(sex, total_bill)

