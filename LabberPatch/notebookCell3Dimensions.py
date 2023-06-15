filepath = 'test_data_2.hdf5'

f = Labber.LoadData(filepath)
step_channels = f.getStepChannels()
log_channels = f.getLogChannels()
quants = np.concatenate((step_channels, log_channels))
print('Quantities in the Labber file:'); print(repr(quants))

#out of the quants, select those to be imported here
quants_import=['Idc_compact', 'B_yoko', 'Vtg', 'Vbg', 'Vdc']
print('Quantities to be imported:'); print(repr(quants_import))

#Dictionnary names into which the quants are imported
dictnames=['Idc_compact', 'B_yoko', 'V_tg', 'V_bog', 'V_']
print('New names of quantities:'); print(repr(dictnames))

#j is the number that will be converted to the key string
j=2   

z_dimension = 'Vtg'

z_dimension_step_number, z_dimension_step_size, z_dimension_indicator = f.getThirdDimensionSplitting(z_dimension)

for i in range(0, z_dimension_step_number):
    if z_dimension_indicator == 1:
        for num,name in enumerate(quants_import,0):
            MainDict[dictnames[num]][str(j + i)]=f.getData(name)[:, i*z_dimension_step_size : (i + 1)*z_dimension_step_size - 1]

    else:
        for num,name in enumerate(quants_import,0):
            MainDict[dictnames[num]][str(j + i)]=f.getData(name)[i*z_dimension_step_size : (i + 1)*z_dimension_step_size - 1, :]
        
print('Idc_compact contains the keys: '+str(Idc_compact.keys()))
