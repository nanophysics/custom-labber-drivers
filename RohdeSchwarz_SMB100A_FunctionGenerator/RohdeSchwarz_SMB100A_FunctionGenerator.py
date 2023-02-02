#!/usr/bin/env python
from VISA_Driver import VISA_Driver
import InstrumentDriver
#from InstrumentConfig import InstrumentQuantity
import numpy as np

__version__ = "0.1"

#class Error(Exception):
#	pass

class Driver(VISA_Driver):
	""" This class implements the Rohde&Schwarz Network Analyzer driver"""
	def performSetValue(self, quant, value, sweepRate=0.0, options={}):
		"""Perform the Set Value instrument operation. This function should return the actual value set by the instrument"""
		if quant.name == 'Output':
			if value: 
				VISA_Driver.writeAndLog(self,'OUTP ON')
				return True
			else:
				VISA_Driver.writeAndLog(self,'OUTP OFF')			
				return False
		else:
			# run standard VISA case 
			value = VISA_Driver.performSetValue(self, quant, value, sweepRate, options)
			return value


	def performGetValue(self, quant, options={}):
		"""Perform the Get Value instrument operation"""
		# check type of quantity
		if quant.name == 'Output':
			value = VISA_Driver.askAndLog(self, 'OUTP?')
			return int(value)
		else:
			# for all other cases, call VISA driver
			value = VISA_Driver.performGetValue(self, quant, options)
			return value
        
if __name__ == '__main__':
	pass
