from abc import ABC,abstractmethod
import time
from datetime import datetime
import board
import busio
from digitalio import Direction
from adafruit_mcp230xx.mcp23017 import MCP23017
import RPi.GPIO as GPIO
import pygatt
import logging

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

class OxyInterface(ABC):
    @abstractmethod
    def init_relay_button(self):
        '''
        Setup relay and button pins to be output
        '''
        pass

    @abstractmethod
    def turn_on_off_device(self):
        '''
        Turn on relay over the device
        '''
        pass

    @abstractmethod
    def press_button_device(self):
        '''
        Press button on device
        '''
        pass

    @abstractmethod
    def run(self):
        '''
        Determine how to run the oxy device
        '''
        pass

class Oxymeter(OxyInterface):
    char_blood_pressure_measurement = 'CDEACB81-5235-4C07-8846-93A37EE6B86D'

    def __init__(self, ble ):
        self.name = 'oxy'
        self.pinButton = 0
        self.pinRelay = 2
        self.ble = ble

    def init_relay_button(self):

        #Use GPIO Raspberry Pi
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinButton , GPIO.OUT)
        GPIO.setup(self.pinRelay, GPIO.OUT)


    def initial_state_time(self):
        self.is_stop = False
        self.start_time = datetime.now()
        logging.debug(self.start_time)


    def turn_on_off_device(self, status):
        #MCP Mode
        self.init_relay_button()
        '''
        self.init_relay_button()
        if status:
            self.mcp_pin_relay.value = True
        else:
            self.mcp_pin_relay.value = False
        '''
        if status:
            GPIO.output(self.pinRelay, 1)
        else :
            GPIO.output(self.pinRelay,0)


    def press_button_device(self):
        GPIO.output(self.pinButton,1)
        time.sleep(0.5)
        GPIO.output(self.pinButton,0)

    def run(self):
        #take
        self.initial_state_time()
        self.turn_on_off_device(True)
        self.press_button_device()
        adapter = self.ble.create_adapter_ble()
        self.ble.scan_ble_device(adapter)
        #self.ble.connect_ble_device(adapter)

class HandleMeasurement:
    def handle_measurement(self, value,):
        print('value[0]: {}, value[1]: {}'.format(hex(value[0]), hex(value[1])))

        # Jari tidak terdeteksi
        if value[1] == 0x00 or value[1] == 0x2D :
            self.is_DetectHand = False
            msg = 'Finger not Detected'
            self.mqtt_client.publish('finger'.format(self.name),msg, 1, False)
            # print('time:', time.time() - self.time_finger)

            # Kondisi ketika oxy mati karena jari tidak terdeteksi setelah 4.7 detik
            if (time.time() - self.time_finger > 4.7) and (self.count_notDetected_hand > 3) :
                device.resubscribe_all()
                self.is_stopDetectingFinger = True
            self.count_notDetected_hand +=1

        # Jari Terdeteksi
        elif value[1] != 0xFF:
            print('there is finger detected')
            self.time_finger = time.time()
            self.count_notDetected_hand = 0
            self.is_DetectHand = True


        if value[0] == 0x81 and value[2] != 127:

            print('Spo  :',value[2])
            print('Bpm  :',value[1])
            print('Pi   :',value[0]/10)
            # print()
            if self.is_start and not self.is_stop:
                if self.first_measure:
                    self.time_measure = time.time()
                    self.first_measure = False
                    self.count_extend_time = 0

                if (time.time() - self.time_measure >= self.time_measurement):
                    if value[2] < 95 and self.count_extend_time<6:
                        self.time_measure = time.time()
                        self.count_extend_time +=1

                    else:
                        print("first measure is called and printing result")
                        self.finish_time = self.config.get_timeNow()
                        res = '{' + '"Spo": "{}", "Bpm": "{}", "Pi": "{}"'.format(value[2],value[1],value[3]/10) + '}'
                        msg = '{'+ '"result": {}, "start_time":"{}","finish_time":"{}","error": {}, "finished": {}'.format(res, self.start_time,self.finish_time,"false", "true") + '}'
                        self.mqtt_client.publish('res/{}'.format(self.name),msg, 1, False)
                        self.is_stop = True
                        self.first_measure = True
                else:
                    print("not first measure is called : waiting for next lines and printing result")
                    self.is_notified = True
                    self.time_notified = time.time()
                    res = '{' + '"Spo": "{}", "Bpm": "{}", "Pi": "{}"'.format(value[2],value[1],value[3]/10) + '}'
                    msg = '{'+ '"result": {}, "error": {}, "finished": {}'.format(res, "false", "false") + '}'
                    self.mqtt_client.publish('res/{}'.format(self.name),msg, 1, False)

class OxyWithMCP(OxyInterface):
    char_blood_pressure_measurement = 'CDEACB81-5235-4C07-8846-93A37EE6B86D'
    def __init__(self, ble ):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.mcp = MCP23017(self.i2c, address= 0x27)
        self.name = 'oxy'

        self.pinButton = 0
        self.pinRelay = 2
        self.handle = handle
        self.ble = ble

    def initial_state_time(self):
        self.is_stop = False
        self.start_time = datetime.now()
        print(self.start_time)

    def init_relay_button(self):
        self.mcp_pin_button = self.mcp.get_pin(self.pinButton)
        self.mcp_pin_button.direction = Direction.OUTPUT
        self.mcp_pin_relay  = self.mcp.get_pin(self.pinRelay)
        self.mcp_pin_relay.direction = Direction.OUTPUT

    def turn_on_off_device(self, status):
        self.init_relay_button()
        print("Setup Pins")
        if status:
            self.mcp_pin_relay.value = True
            print("Turning on device")
        else:
            self.mcp_pin_relay.value = False
            print('Turning off device')

    def press_button_device(self):
        print('button is pressed')
        self.mcp_pin_button.value = True
        time.sleep(0.5)
        self.mcp_pin_button.value = False

    def run(self):
        #take
        self.initial_state_time()
        self.turn_on_off_device(True)
        self.press_button_device()
        adapter = self.ble.create_adapter_ble()
        device = self.ble.scan_ble_device(adapter)
        self.ble.subscribe_ble_device(device)


class Bluetooth:
    char_blood_pressure_measurement = 'CDEACB81-5235-4C07-8846-93A37EE6B86D'
    def __init__(self, handle : HandleMeasurement, address_ble_device):
        self.is_device_found = False
        self.is_connected = False
        self.is_subscribed = False
        self.is_timeOut = False
        self.timeOut_count = 0
        self.id_hci = "hci0"
        self.address = address_ble_device
        self.handle = handle

    def create_adapter_ble(self):
        adapter = pygatt.GATTToolBackend(hci_device=self.id_hci)
        time.sleep(1)
        adapter.start(reset_on_start=True, initialization_timeout=3)
        print("Starting the adapter")
        return adapter

    def scan_ble_device(self, adapter):
        # while not self.is_device_found :
            #self.check_time()
        device = None
        try :
            for discover in adapter.scan(run_as_root=True, timeout=1):
                print(discover)
                if discover['address'] == self.address: #self.bluetooth_address:
                    self.is_device_found = True
                    # adapter.reset()
                    device = self.connect_ble_device(adapter, discover['address'])
        except pygatt.exceptions.BLEError:
            adapter.reset()
            adapter.stop()

        return device
        # for discover in adapter.scan(run_as_root=True, timeout=3):
        #     print(discover)
        #     if discover['address'] == self.address: #self.bluetooth_address:
        #         print("Device is found")
        #         self.is_device_found = True
        #         adapter.reset()
        #         self.connect_ble_device(adapter, discover['address'])

    def connect_ble_device(self, adapter, discover_device):
        # print('name: ', discover['name'])
        # retry = True
        # while retry :
        #     try:
        #         #self.logger.info('connecting...')
        #         device = adapter.connect(discover['address'],auto_reconnect=True)#, address_type=pygatt.BLEAddressType.random) # ADF Type Random
        #     except Exception as e:
        #         retry = True
        #         print('{} reconnecting...'.format(e))
        #     else:
        #         retry = False
        #         #self.logger.info('connected!')
        device = adapter.connect(discover_device,auto_reconnect=True)
        print("Connected")
        return device

    def subscribe_ble_device(self, device):
        print("Try to subscribe")
        chars = None
        is_subscribed = False
        subscribe_count = 0
        while not is_subscribed :

            # self.check_time()
            chars = device.discover_characteristics().keys()
            print(chars)
            device.subscribe(self.char_blood_pressure_measurement, callback=self.handle.handle_measurement, wait_for_response=False)
            print("subscribed")

            is_subscribed = True

if __name__ == "__main__":


    handle = HandleMeasurement()
    #'00:65:00:07:ED:C3'
    ble = Bluetooth(address_ble_device = '00:65:00:07:ED:C3', handle=handle)
    oxy = OxyWithMCP(ble = ble)
    oxy.run()
    oxy.turn_on_off_device(False)
