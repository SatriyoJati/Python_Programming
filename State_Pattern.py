from __future__ import annotations
from abc import ABC, abstractmethod
import logging
from Glucosemeter_observer import *

logging.basicConfig()

class Glucosemeter:
    _state = None

    def __init__(self, state: State) -> None:
        self.setState(state)

    def setState(self, state: State):

        print(f"Glucosemeter: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def presentState(self):
        print(f"Glucosemeter is in {type(self._state).__name__}")

    #methods for transititons
    def detect_strip_in(self):
        self._state.detect_strip_in()

    def check_blood_in(self):
        self._state.check_blood_in()

    def ble_send(self):
        self._state.ble_send()

class State(ABC):

    @property
    def glucosemeter(self) -> Glucosemeter:
        return self._context

    @glucosemeter.setter
    def context(self,context: Context)-> None:
        self._context = context

    @abstractmethod
    def detect_strip_in(self) ->None:
        pass

    @abstractmethod
    def check_blood_in(self) -> None:
        pass

    @abstractmethod
    def ble_send(self) -> None:
        pass

#Concrete states
class ReadyStripIn(State):
    def __init__(self, adc : ADCBeepConcrete ):
        self.isDetectStrip = False
        self.myinput = ''
        self.adc = adc

    def waitForBeeps(self):
            self.adc.gain_diff_beep()

    def detect_strip_in(self) -> None:
        print("Ready for strip in")
        self.waitForBeeps()
        if self.adc._state == 2:
            self.glucosemeter.setState(ReadyBloodIn(adc))

    def check_blood_in(self) -> None:
        pass

    def ble_send(self):
        pass


class ReadyBloodIn(State):
    def __init__(self, adc : ADCBeepConcrete ):
        self.adc = adc

    def detect_strip_in(self) ->None:
        pass

    def check_blood_in(self) -> None:
        isDetectStrip = False
        while True:
            isDetectStrip = str(input("Insert Blood T/F?"))
            if isDetectStrip == "T" :
                isDetectStrip = True
                print("--->Break from loop")
                break
            elif isDetectStrip == "F" :
                isDetectStrip = False
                print("Still in while loop")

        if isDetectStrip == True:
            self.glucosemeter.setState(BLEState(adc))

    def ble_send(self) -> None:
        pass


class BLEState(State):
    def __init__(self, adc : ADCBeepConcrete ):
        self.adc = adc

    def detect_strip_in(self) ->None:
        pass


    def check_blood_in(self) -> None:
        pass


    def ble_send(self):
        self.glucosemeter.setState(ReadyStripIn(adc))


if __name__ == "__main__":

    #Setup Observer
    adc = ADCBeepConcrete()
    observerA = ConcreteObserverA()
    adc.attach(observerA)

    #States
    rdin = ReadyStripIn(adc)
    rbin = ReadyBloodIn(adc)
    bls = BLEState(adc)


    gluco = Glucosemeter(rdin)
    gluco.detect_strip_in()
    gluco.presentState()
    gluco.check_blood_in()
    gluco.presentState()
    gluco.ble_send()
    gluco.presentState()
