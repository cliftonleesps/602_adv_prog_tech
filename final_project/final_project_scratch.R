library(tidyverse)

colleges <- read.csv("Most-Recent-Cohorts-Institution.csv")

colleges$STABBR


2989 colleges

sum(colleges$ACCREDAGENCY == "NULL")
nrow(colleges) - sum(colleges$ACCREDAGENCY == "NULL")

# 6347 accredited colleges

mean(colleges$MDCOST_ALL)

median(colleges$MDEARN_ALL)
mean(colleges$MN_EARN_WNE_P10)
mean(colleges$GRAD_DEBT_MDN10YR)

debt <- colleges[ which(colleges$DEBT_MDN != "PrivacySuppressed" & colleges$DEBT_MDN != "NULL"),]
mean(debt$DEBT_MDN)

d <- debt$DEBT_MDN
median(strtoi(d))
# median amount of debt
