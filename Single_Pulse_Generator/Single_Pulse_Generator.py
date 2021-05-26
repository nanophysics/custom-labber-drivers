import numpy as np

from BaseDriver import LabberDriver


class Driver(LabberDriver):
    """This class implements a multi-qubit pulse generator."""

    def performOpen(self, options={}):
        """Perform the operation of opening the instrument connection."""
        self.memory = 32500 # Memory limit for UHFLI
        self.sequence = self.getValue("Sequence Type")
        self.sampling_rate = self.getValue("Sampling Rate")
        self.n_pulses = int(self.getValue("Number of Pulses"))
        self.init_pulses()

    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        """Perform the Set Value instrument operation."""
        if quant.name == "Number of Samples":
            self.init_pulses()

        if quant.name == "Number of Pulses":
            self.n_pulses = int(value)
            self.init_pulses()

        if quant.name == "Sampling Rate":
            self.sampling_rate = value
            self.init_pulses()

        if "Amplitude" in quant.name:
            index = int(quant.name.split()[1]) - 1
            if index + 1 <= len(self.pulses):
                value = self.pulses[index].set_amplitude(value)

        if "Length" in quant.name:
            index = int(quant.name.split()[1]) - 1
            if index + 1 <= len(self.pulses):
                value = self.pulses[index].set_length(value)

        return value

    def performGetValue(self, quant, options={}):
        """Perform the Get Value instrument operation."""
        if quant.name == "Trace":
            array = np.hstack([p.array[0] for p in self.pulses])
            dt = 1 / self.sampling_rate
            value = quant.getTraceDict(array, dt=dt)
            if array.size > self.memory:
                self.log("AWG out of memory", level=30)
                raise ValueError("AWG out of memory")
            
        else:
            value = quant.getValue()
        return value

    def init_pulses(self):
        self.pulses = []
        for i in range(self.n_pulses):
            pulse = SquarePulse(sampling_rate=self.sampling_rate)
            pulse.set_amplitude(self.getValue(f"Pulse {i+1} - Amplitude"))
            pulse.set_length(self.getValue(f"Pulse {i+1} - Length"))
            self.pulses.append(pulse)


class SquarePulse:
    def __init__(self, sampling_rate=1.8e9):
        self._sampling_rate = sampling_rate
        self._amplitude = None
        self._length = None

    def set_amplitude(self, amplitude):
        if abs(amplitude) > 1.0:
            self._amplitude = amplitude / abs(amplitude)
        else:
            self._amplitude = amplitude
        return self._amplitude

    @property
    def amplitude(self):
        return self._amplitude

    def set_length(self, length):
        self._n_points = int(length * self._sampling_rate)
        if self._n_points < 1:
            self._n_points = 1
        self._length = self._n_points / self._sampling_rate
        return self._length

    @property
    def length(self):
        return self._length

    @property
    def array(self):
        return (
            self.amplitude * np.ones(self._n_points),
            np.linspace(0, self.length, self._n_points),
        )


if __name__ == "__main__":
    pass

