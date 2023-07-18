filepath = 'test_data.hdf5'

f = Labber.LoadData(filepath)
step_channels = f.getStepChannels()
log_channels = f.getLogChannels()
quants = np.concatenate((step_channels, log_channels))

print('Quantities in the Labber file:')
print(repr(quants))

#out of the quants, select those to be imported here
quants_import=['Idc_compact', 'B_yoko', 'Vtg', 'Vbg', 'Vdc']
print('Quantities to be imported:'); print(repr(quants_import))

#Dictionnary names into which the quants are imported
dictnames=['Idc_compact', 'B_yoko', 'V_tg', 'V_bog', 'V_']
print('New names of quantities:'); print(repr(dictnames))

#j is the number that will be converted to the key string
j=1; key=str(j)                            
for num,name in enumerate(quants_import,0):
    MainDict[dictnames[num]][key]=f.getData(name).transpose()
print('Idc_compact contains the keys: '+str(MainDict[dictnames[0]].keys()))