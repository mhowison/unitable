import delimited tips.csv

replace total_bill = total_bill - 2
generate new_bill = total_bill / 2
drop new_bill

list if total_bill > 10

generate bucket = "low" if total_bill < 10
replace bucket = "high" if total_bill >= 10

keep sex total_bill tip
rename total_bill total_bill_2

sort sex total_bill





export delimited tips2.csv