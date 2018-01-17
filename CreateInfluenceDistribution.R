tuesday1 <- read.csv("birds_NOT_culm.csv")

eaglesTable = array(dim = c(11,2))
eaglesTable[1,1] = "Interval"
eaglesTable[1,2] = "Frequency"
eaglesTable[2,1] = "0 <= influence score < 1"
eaglesTable[3,1] = "1 <= influence score < 2"
eaglesTable[4,1] = "2 <= influence score < 3"
eaglesTable[5,1] = "3 <= influence score < 4"
eaglesTable[6,1] = "4 <= influence score < 5"
eaglesTable[7,1] = "5 <= influence score < 6"
eaglesTable[8,1] = "6 <= influence score < 7"
eaglesTable[9,1] = "7 <= influence score < 8"
eaglesTable[10,1] = "8 <= influence score < 9"
eaglesTable[11,1] = "9 <= influence score <= 10"
for (j in 2:11 ) {
  eaglesTable[j,2] = 0
}

for (i in colnames(tuesday1)){
  #print(i)
  #print(substr(i,2,8))
  j <- substr(i, 2, 8)
  #print(substr(j,4,4))
  if (substr(j,4,4) == ".") {
    j = paste(substr(j,1,3),substr(j,5,8), sep = "")
    #print(j)
  }
  
  #print(j)
  k <- as.numeric(j) 
  if (k < 1) {
    eaglesTable[2,2] = as.numeric(as.character(eaglesTable[2,2])) + 1
  }
  else if (k < 2) {
    eaglesTable[3,2] = as.numeric(as.character(eaglesTable[3,2])) + 1
  }
  else if (k < 3) {
    eaglesTable[4,2] = as.numeric(as.character(eaglesTable[4,2])) + 1
  }
  else if (k < 4) {
    eaglesTable[5,2] = as.numeric(as.character(eaglesTable[5,2])) + 1
  }
  else if (k < 5) {
    eaglesTable[6,2] = as.numeric(as.character(eaglesTable[6,2])) + 1
  }
  else if (k < 6) {
    eaglesTable[7,2] = as.numeric(as.character(eaglesTable[7,2])) + 1
  }
  else if (k < 7) {
    eaglesTable[8,2] = as.numeric(as.character(eaglesTable[8,2])) + 1
  }
  else if (k < 8) {
    eaglesTable[9,2] = as.numeric(as.character(eaglesTable[9,2])) + 1
  }
  else if (k < 9) {
    eaglesTable[10,2] = as.numeric(as.character(eaglesTable[10,2])) + 1
  }
  else {
    eaglesTable[11,2] = as.numeric(as.character(eaglesTable[11,2])) + 1
  }
  # k is the number
  
  vector <- c(vector,k)
  print(k)
}

#print(as.integer(vector))
#hist(vector)
hist(as.numeric(as.character(vector)))

