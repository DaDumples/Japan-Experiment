from numpy import *
import pandas as pd
import os
import matplotlib.pyplot as plt

pristine = pd.read_pickle('pristine.pkl')
exposure1 = pd.read_pickle('exposure1.pkl')


pristine_mono_mean = pristine['monofilament'].mean()/1000
pristine_mono_std = pristine['monofilament'].std()/1000
pristine_flouro_mean = pristine['flourocarbon'].mean()/1000
pristine_flouro_std = pristine['flourocarbon'].std()/1000

exposed_mono_mean = exposure1['monofilament'].mean()/1000
exposed_mono_std = exposure1['monofilament'].std()/1000
exposed_flouro_mean = exposure1['flourocarbon'].mean()/1000
exposed_flouro_std = exposure1['flourocarbon'].std()/1000


pstresses = [pristine_mono_mean, pristine_flouro_mean]
perrors = [pristine_mono_std, pristine_flouro_std]

estresses = [exposed_mono_mean, exposed_flouro_mean]
eerrors = [exposed_mono_std, exposed_flouro_std]

indexs = array([0, 1])
width = .35



fig, ax = plt.subplots()
ax.bar(indexs - width/2, pstresses, width, yerr = perrors, capsize = 10)
ax.bar(indexs + width/2, estresses, width, yerr = eerrors, capsize = 10)
ax.set_ylabel('Max Stress [kPa]')
ax.set_xlabel('Material')
ax.set_xticks([0,1])
ax.set_xticklabels(['Monofilament', 'Flourocarbon'])
ax.set_title('Exposure 1 Material Properties')
ax.legend(['Pristine', 'Exposed'])
plt.savefig('All Material Properties.png',bbox_inches = 'tight')

plt.show()