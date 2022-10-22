#Observer Design

from __future__ import annotations
from abc import ABC, abstractmethod
import time

class ADCBeep(ABC):


    @abstractmethod
    def attach(self, observer: Observer) -> None:
        '''
        Attach an observer to subject
        '''
        pass

    @abstractmethod
    def detach(self, observer : Observer) -> None:
        '''
        Detach observer from the subject
        '''
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class ADCBeepConcrete(ADCBeep):

    changeADC = False
    _state : int = 0
    timeout = 5

    _observers : List[Observer] = []

    def attach(self, observer : Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer : Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def gain_diff_beep(self):
        start_time = time.time()
        print("start timing for readstripin blood")
        while True :
            print(f"state is {self._state}")
            print(f"{time.time() - start_time} is running")
            test = input("give changeADC ?")
            if test == 'Y':
                self.changeADC = True
            elif test == 'N':
                self.changeADC = False
            if self.changeADC :
                self._state += 1
                self.notify()
            if self._state == 2:
                break

    def gain_beep_blood(self):
        start_time = time.time()
        print("blood ")

class Observer(ABC):

    @abstractmethod
    def update(self, adc_beep_concrete) -> None:
        pass


class ConcreteObserverA(Observer):
    def update(self, adc_beep : ADCBeep):
        if adc_beep._state == 3:
            print("Detected three beeps ")
            adc_beep._state = 0

class ConcreteObserverB(Observer):
    def update(self, adc_beep : ADCBeep):
        if adc_beep._state == 2:
            print("Detected two beeps")
            adc_beep._state = 0


if __name__ == "__main__":

    adcbeep = ADCBeepConcrete()

    observerA = ConcreteObserverA()
    adcbeep.attach(observerA)

    observerB = ConcreteObserverB()
    adcbeep.attach(observerB)

    adcbeep.gain_diff_beep()
