import sys
import os
import collections
import logging
from subprocess import call
from time import sleep, localtime, time
from dispense_for_duration_thread import DispenseForDurationThread
import random


#import RPi GPIO if this is not available import the RPi GPIO simulation

try:
    import RPi.GPIO as GPIO
except ImportError:
  
    print "\nUnable to import RPi.GPIO! Automatically switched to simulation mode!!! If you are on a Raspberry Pi try sudo apt-get install python-rpi.gpio -y\n"
    import RPiSIM.GPIO as GPIO

#change this if you want to add more gpios / dispensers / valves / pumps
#add all gpios here which are connected to a pump/valve, they will be numerated in the order of appearance
GPIOOutputs = [17, 27, 22, 23, 24, 25]

MOTOR_DIRECTION_FORWARD       = 1
MOTOR_DIRECTION_BACKWARD      = 0

log = logging.getLogger('bartendro')

class Dispenser():
    
    def __init__(self, gpio):
        self.gpio = gpio
        self.dispensing = False
        self.dispensing_thread = None
        
    def get_gpio_number(self):
        return self.gpio
    
    def pour_for_duration(self, duration):
        self.dispensing_thread = DispenseForDurationThread(self, duration).start()
            
    def start_dispensing(self):
        GPIO.output(self.gpio, GPIO.HIGH)
        self.dispensing = True
        log.info("GPIO: " + str(self.gpio) + " start dispensing.\n")
        #todo error handling 
        return True
        
    def stop_dispensing(self):
        GPIO.output(self.gpio, GPIO.LOW)
        self.dispensing = False
        log.info("GPIO: " + str(self.gpio) + " stop dispensing.\n")
        #todo error handling 
        return True
        
    def is_dispensing(self):
        return self.dispensing
    

class RouterDriver(object):
    '''This object interacts with the rasppi'''

    def __init__(self):
        log.info("Starting Driver.\n")

        self.dispensers = []
        #add dispensers
        for gpio in GPIOOutputs:
            self.dispensers.append(Dispenser(gpio))
            
        self.startup_log = ""
        self.num_dispensers = len(self.dispensers)
        self.dispenser_version = 0
 
    def get_startup_log(self):
        return self.startup_log
    
    def get_dispenser_version(self):
        return self.dispenser_version

    def reset(self):
        """Reset the hardware. Do this if there is shit going wrong. All motors will be stopped
           and reset."""
        log.info("Reset Hardware. Not implemented.\n")
         
        #TODO: reset
   
    def count(self):
        return self.num_dispensers

    def open(self):
        '''Setup GPIOs'''
        log.info("Setup GPIOS.\n")

        # use GPIO pin numbering convention (not the actual pin numbers)
        GPIO.setmode(GPIO.BCM)
        
        #define all gpios given in gpiooutputs as outputs
        for dispenser in self.dispensers:
            GPIO.setup(dispenser.get_gpio_number(), GPIO.OUT)
            GPIO.output(dispenser.get_gpio_number(), GPIO.LOW)

        self._clear_startup_log()

    def close(self):    
        GPIO.cleanup()

    def log(self, msg):
        try:
            t = localtime()
            self.cl.write("%d-%d-%d %d:%02d %s" % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, msg))
            self.cl.flush()
        except IOError:
            pass

    def dispense_time(self, dispenser, duration):
        log.info("Start dispensing on dispenser " + str(dispenser) + " for " + str(duration) + " seconds.\n")
             
        self.dispensers[dispenser].pour_for_duration(duration)
        return True

    def ping(self, dispenser):
        log.info("Ping not implemented.\n")
        
        return True

    def start(self, dispenser):
        
        return self.dispensers[dispenser].start_dispensing()
  
    def stop(self, dispenser):
        
        return self.dispensers[dispenser].stop_dispensing()
       
    def is_dispensing(self, dispenser):
        """
        Returns a tuple of (dispensing, is_over_current) 
        """
        return (self.dispensers[dispenser].is_dispensing(), False)
       
    def set_motor_direction(self, dispenser, direction):
        #log.info("Set motor direction to " + str(direction) + ".\n")

        #todo set motor direction
        return True

    def update_liquid_levels(self):
        log.info("Update liquid level.\n")

        return True


    def get_liquid_level(self, dispenser):
        log.info("Get liquid level.\n")
        #todo liquid level?
        return 100

    def get_liquid_level_thresholds(self, dispenser):
        log.info("Get liquid level thersholds.\n")
        return True
        
                
    def set_liquid_level_thresholds(self, dispenser, low, out):
        log.info("Set liquid level thersholds. Low: " + str(low) + " Out: " + str(out) + "\n")
        return True


    def _clear_startup_log(self):
        self.startup_log = ""

    def _log_startup(self, txt):
        log.info(txt)
        self.startup_log += "%s\n" % txt
