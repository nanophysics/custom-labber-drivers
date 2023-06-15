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
        name_raw_array = np.array(self.file['Data'].get('Channel names')[:].tolist()).transpose()[0]
        length = name_raw_array.shape[0]
        name_array = []
        for i in range(0, length):
            name_array.append(name_raw_array[i].decode())
        name_array = np.array(name_array)

        if name in name_array:
            index = np.where(name_array == name)[0][0]
            result = self.file['Data'].get('Data')[:, index, :]

            return(result)
        
        else:
            value = self.file['Step config'].get(name).get('Step items')[:][0][2]
            result_shape = self.file['Data'].get('Data')[:, 0, :].shape
            result = np.ones(result_shape)*value

            return(result)
        
    def getThirdDimensionSplitting(self, name):
        dimension_step_number_1 = len(np.unique(self.getData(name)[0]))
        dimension_step_number_2 = len(np.unique(self.getData(name).transpose()[0]))

        dimension_step_size_1 = int(len(self.getData(name)[0])/dimension_step_number_1)
        dimension_step_size_2 = int(len(self.getData(name).transpose()[0])/dimension_step_number_2)

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
