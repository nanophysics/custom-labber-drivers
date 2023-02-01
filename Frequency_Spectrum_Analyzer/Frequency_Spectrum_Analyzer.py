import numpy as np
import cmath
from BaseDriver import LabberDriver


class Driver(LabberDriver):
    """This class implements a multi-qubit pulse generator."""

    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        """Perform the Set Value instrument operation."""
        if quant.name != "Output":
            quant.setValue(value)
            self.getValue("Output")
        return value

    def performGetValue(self, quant, options={}):
        """Perform the Get Value instrument operation."""
        if quant.name == "Output":
            signal = self.getValue("Signal")
            reference = self.getValue("Reference")
            slope = self.getValue("Slope")
            freq = self.getValue("Frequency")
            phase = np.angle(reference) - np.angle(signal) - slope * 1e-7 * freq
            value = cmath.rect(np.abs(signal), -phase)
        else:
            value = quant.getValue()
        return value


