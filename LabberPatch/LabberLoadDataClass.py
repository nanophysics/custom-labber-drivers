import h5py
import numpy as np

class LoadData:
    def __init__(self, filepath):
        self.filepath = filepath
        self.file = h5py.File(filepath, 'r')

    def getStepChannels(self):
        result = np.array(self.file['Step list'][:].tolist())
        result_array = self.formatArray(result.transpose()[0])
        return(result_array)
    
    def getLogChannels(self):
        result = np.array(self.file['Log list'][:].tolist())
        result_array = self.formatArray(result.transpose()[0])
        return(result_array)
    
    def getData(self, name):

        channels_array = np.array(self.file['Channels'][:].tolist())
        gain_index = np.where(channels_array == bytes(name, 'utf-8'))[0][0]
        gain = float(channels_array[gain_index][5].decode())

        name_raw_array = np.array(self.file['Data'].get('Channel names')[:].tolist()).transpose()[0]
        length = name_raw_array.shape[0]
        name_array = []
        for i in range(0, length):
            name_array.append(name_raw_array[i].decode())
        name_array = np.array(name_array)

        if name in name_array:
            index = np.where(name_array == name)[0][0]
            result = self.file['Data'].get('Data')[:, index, :]

            return(result/gain)
        
        else:
            value = self.file['Step config'].get(name).get('Step items')[:][0][2]
            result_shape = self.file['Data'].get('Data')[:, 0, :].shape
            result = np.ones(result_shape)*value

            return(result/gain)
        
    def getThirdDimensionSplitting(self, name):
        dimension_step_number_1 = len(np.unique(self.getData(name)[0]))
        dimension_step_number_2 = len(np.unique(self.getData(name).transpose()[0]))

        if (dimension_step_number_1 == 1):
            dimension_step_size_1 = int(len(self.getData(name)[0])/dimension_step_number_1)

        else:
            # We now remove the last 'bloc' of elements to compute the step size.
            # This is because when one truncates a measurement in Labber the last bloc 
            # does not have the same size as the rest and that messes up things.
            last_bloc_value_1 = np.unique(self.getData(name)[0])[-1]
            substracted_array_1 = self.getData(name)[0] - last_bloc_value_1
            truncated_array_1 = substracted_array_1[substracted_array_1 != 0]

            dimension_step_size_1 = int(len(truncated_array_1)/(dimension_step_number_1 - 1))

        if (dimension_step_number_2 == 1):
            dimension_step_size_2 = int(len(self.getData(name).transpose()[0])/dimension_step_number_2)

        else:
            # We now remove the last 'bloc' of elements to compute the step size.
            # This is because when one truncates a measurement in Labber the last bloc 
            # does not have the same size as the rest and that messes up things.
            last_bloc_value_2 = np.unique(self.getData(name).transpose()[0])[-1]
            substracted_array_2 = self.getData(name)[0] - last_bloc_value_2
            truncated_array_2 = substracted_array_1[substracted_array_2 != 0]

            dimension_step_size_2 = int(len(truncated_array_2)/(dimension_step_number_2 - 1))

        if (dimension_step_number_1 < 1) and (dimension_step_number_2 < 1):
            return('This does not look like the proper 3rd dimension')
        
        else:
            if (dimension_step_number_1 < dimension_step_number_2):
                result_array = np.array([dimension_step_number_2, dimension_step_size_2, 2])
            
            else:
                result_array = np.array([dimension_step_number_1, dimension_step_size_1, 1])
            
            return(result_array)

    def formatArray(self, input_array):
        length = input_array.shape[0]
        result_list = []
        for i in range(0, length):
            string = input_array[i]
            string = string.decode('utf-8')
            result_list.append(string)
            result_array = np.array(result_list)

        return(result_array)
