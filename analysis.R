library(reshape)
setwd("~/github/textprase")
a <- read.csv('statistic.csv',header=F)
b <- transform(a,dt=as.Date(as.character(a$V1),format='%Y%m%d'),kw=as.character(a$V2),fq=as.integer(a$V3))
b <- b[4:6]
winb <- b[b$dt>=as.Date('2012-01-01') & b$dt <= as.Date('2014-12-31'),]
wb <- melt(data = winb,id=c('dt','kw','fq'))
#wbc <- cast(wb,dt~kw)
aa <- zoo(x=b$fq[b$kw=='商业银行'], b$dt[b$kw=='商业银行'])
aa1 <-zoo(x=b$fq[b$kw=='汇率'], b$dt[b$kw=='汇率'])
aa2 <-zoo(x=b$fq[b$kw=='流动性'], b$dt[b$kw=='流动性'])
rmb <- zoo(x=b$fq[b$kw=='人民币'], b$dt[b$kw=='人民币'])
deposit <- zoo(x=b$fq[b$kw=='存款'], b$dt[b$kw=='存款'])
loan <- zoo(b$fq[b$kw=='贷款'], b$dt[b$kw=='贷款'])
bank <- zoo(b$fq[b$kw=='银行'], b$dt[b$kw=='银行'])
risk <- zoo(b$fq[b$kw=='风险'], b$dt[b$kw=='风险'])
coinp <- zoo(b$fq[b$kw=='货币政策'], b$dt[b$kw=='货币政策'])
sh01 <- read.csv('000001SH.csv')
sh01 <- transform(sh01,dt=as.Date(as.character(sh01$日期),format='%Y/%m/%d'),avgpoint=as.numeric((sh01$开盘+sh01$收盘)/2))
sh <- sh01[11:12]
g <- zoo(sh$avgpoint,sh$dt)
defg <- merge.zoo(aa1,aa2,g)
m2window <- window(x = defg,start=as.Date('2012-01-01'),end=as.Date('2013-12-31'))
plot.zoo(m2window)

#d <- zoo(x=c$fq[c$kw=='存款'], c$dt[c$kw=='存款'])
#e <- zoo(c$fq[c$kw=='贷款'], c$dt[c$kw=='贷款'])
#sh01 <- read.csv('000001SH.csv')
#sz <- read.csv('399001.csv')
#sh01 <- transform(sh01,dt=as.Date(as.character(sh01$日期),format='%Y/%m/%d'),avgpoint=as.numeric((sh01$开盘+sh01$收盘)/2))
#sh <- sh01[11:12]
#f <- zoo(sh$avgpoint,sh$dt)

m2window <- window(x = m2,start=as.Date('2012-01-01'),end=as.Date('2015-01-31'))
plot.zoo(m2window)

x1<-vector()
ldt <- length(b$dt)

xxr1 <- subset(xxratio,xxratio >=1.653759e-06 & xxratio <=1.323007e-05,select = F)
save.image("~/github/textprase/fnews.RData")
