library(reshape)
library(smacof)
library(xts)
library(parallel)
library(fpc)

setwd("~/github/textprase")
a <- read.csv('statistic.csv',header=F)
b <- transform(a,dt=as.Date(as.character(a$V1),format='%Y%m%d'),kw=as.character(a$V2),fq=as.integer(a$V3))
b <- b[4:6]
winb <- b[b$dt>=as.Date('2012-01-01') & b$dt <= as.Date('2014-12-31'),]
table1 <- table(b$kw)
subt1 <- subset(x = table1, table1 >365, drop=F)
subb <- subset(b,b$kw %in% names(subt1), drop=F)
wb <- melt(data = subb,id=c('dt','kw','fq'))
wbc <- cast(wb,dt~kw)
wbctotal <- xts(x=wbc, wbc$dt)
wbctotal <- na.fill(wbctotal,0)
rmb <- xts(x=b$fq[b$kw=='人民币'], b$dt[b$kw=='人民币'])
bank <- xts(b$fq[b$kw=='银行'], b$dt[b$kw=='银行'])
market <- xts(x=b$fq[b$kw=='市场'], b$dt[b$kw=='市场'])
rate <- xts(b$fq[b$kw=='利率'], b$dt[b$kw=='利率'])

sh01 <- read.csv('000001SH.csv')
sh01 <- transform(sh01,dt=as.Date(as.character(sh01$日期),format='%Y/%m/%d'),avgpoint=as.numeric((sh01$开盘+sh01$收盘)/2))
sh <- sh01[11:12]
g <- xts(sh$avgpoint,sh$dt)
defg <- merge.xts(rmb,bank,market,rate,g)
m2window <- window(x = defg,start=as.Date('2012-01-01'),end=as.Date('2014-12-31'))
plot.zoo(m2window)
plot.xts(as.xts(m2window))
res.rect <- smacofRect(window(x = wbctotal,start=as.Date('2012-01-01'),end=as.Date('2013-12-31')),itmax=3000,reg = T)
plot(res.rect, joint = T)
acf(m2window[,1:2],na.action = na.pass)
plot.xts(m2window[,1:2],col=c('red','green'),legend.loc = 'top',main = '银行+市场')
plot.xts(m2window[,1],col=c('red'),main = '银行')
plot.xts(m2window[,2],col=c('green'),main = '市场')
plot.xts(m2window[,3],col='blue')
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



kst <- kmeans(x = wbc2,centers = 3)
plotcluster(wbc2,kst$cluster)

kc<- NULL
system.time(for(i in 2:50){ kc<- append(kc,weighted.mean(kmeans(x = wbc2,centers = i)$centers))})
mc <-   getOption("mc.cores", 3)
doit2 <- function(x) weighted.mean(kmeans(x = wbc2,centers = x)$centers)
system.time(res <- mclapply(2:50,  doit2,mc.cores = mc))
kc1 <- NULL
for (i in 1:49) {kc1 <- append(kc1, res[[i]])}

#stopCluster(mc)
plot(kc1,type='l')

kmtest <- kmeans(x = wbc2, centers = 21)
plotcluster(wbc2,kmtest$cluster)
sort(kmtest$cluster)

for(i in 1:15){ print(names(kmtest$cluster[kmtest$cluster==i]))}




save.image("~/github/textprase/fnews.RData")

