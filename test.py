from unitable import *

read_csv("example/tips.csv")

dropna()

generate("double_tip", 2*tip)
rename(double_tip, "tip2x")

generate("adjusted_bill", total_bill * 1.03)
drop(total_bill)

sort(sex, adjusted_bill)

drop_duplicates()
