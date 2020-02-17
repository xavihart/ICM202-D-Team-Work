import matplotlib.pylab as plt
import numpy as np
import pandas as pd

plt.style.use('ggplot')
plt.rcParams['savefig.dpi'] = 500
plt.rcParams['figure.dpi'] = 500

f = open("./triadic.txt", "r")
s = []
for lines in f:
    k = []
   # print(lines.split(","))
    lines = lines[:-2]
   # print(lines)
    [k.append(int(i)) for i in lines.split(",")]
    s.append(k)

data = pd.DataFrame(s)
data.to_csv("./kk.csv")




plt.savefig("./pic/triadic.png")