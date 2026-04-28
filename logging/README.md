# log script

This is the file used to logging data to the 'state.log'

## To import, use 
'''python
from log import logs
'''

## To use logs
'''python
#This is an example
logs.d_log('debug2 working')
logs.i_log('info working')
logs.e_log('error working ')
logs.w_log('warning working')
'''

## Warning
The class is set to print the kind of logging you do when it is triggered, to in you terminal you should see something like:
'''
warning logged
'''