import paho.mqtt.client as mqtt
import pygatt
import time
import subprocess
import logging
import sys
import os
from abc import ABC,abstractmethod

import logging

from datetime import datetime
from utils.logger import LoggerKiosk

class RunnerOxy(ABC):
    @abstactmethod
    def run(self):
        pass

class Oxymeter(RunnerOxy):
    char_blood_pressure_measurement = 'CDEACB81-5235-4C07-8846-93A37EE6B86D'
    def __init__(self, configuration, time_up=180):
        self.logger = LoggerKiosk()
        self.config = configuration
        self.time_measurement = 8
        self.name = 'oxy'
        self.address = self.config.alkes.get_addr(self.name)

        self.set_mqtt()
        self.pin_button_servo = 13
        self.angle_servo = 15

        self.start_run = time.time()
        self.start_time = self.config.get_timeNow()
        self.time_finger = time.time()

        self.is_done = False
        self.is_start = False
        self.is_on = False
        self.is_stop = False
        self.is_notified = False
        self.is_DetectHand = False
        self.is_stopDetectingFinger = False

        self.time_up = time_up
        self.time_notified = time.time()

        self.count_extend_time = 0
        self.count_notDetected_hand = 0

        # self.id_hci = self.config.bt.get_addr()
        self.id_hci = self.config.bt.manual_scan("UART")
        self.status_run_measurement, self.state = 0, 0
        self.first_measure = True

        self.config.alkes.init_relay()

        self.ble_name = "My Oximeter"

    def handle_measurement(self, handle, value):
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

            # print('measured!')
            # print('Spo: {}'.format(value[2]))
            # print('bpm: {}'.format(value[1]))
            # print('pi : {}'.format(value[3]/10))

    def msg_callback(self, client, userdata, msg):
        # print('cek')
        if  msg.topic.split('/')[0] == 'req' and msg.topic.split('/')[1] != self.name:
            self.is_done = True
            # self.logger.info("Masuk split pertama")
        elif msg.topic.split('/')[0] == 'state' and msg.topic.split('/')[1] == 'alkes':
            payload = str(msg.payload.decode('utf-8'))
            if payload == 'home':
                # self.logger.info("Get home msg")
                self.is_done = True
        else:
            payload = str(msg.payload.decode('utf-8'))
            if payload == 'stop' or payload == 'done':
                # self.logger.info("CEK")
                self.is_done = True
            elif payload.split(',')[0] == 'start':
                # print('start')
                self.is_start = True

    def check_time(self, time_delay=0.5):
        try:
            self.mqtt_client.loop(time_delay)
        except Exception as e:
            self.logger.error('{} : checktime :: {}'.format(self.name, e))

    def set_mqtt(self):
        self.mqtt_client = mqtt.Client(self.name)
        self.mqtt_client.on_message = self.msg_callback
        self.mqtt_client.connect("localhost", 1883, 60)
        self.mqtt_client.subscribe('req/+')
        self.mqtt_client.subscribe('state/+')
        self.logger.test('Requesting {}'.format(self.name))

    def error_report(self, error_flag, e):
        self.logger.error('{} >> {}'.format(error_flag, e))
        self.mqtt_client.publish('res/{}/status'.format(self.name), 'error', 0, False)
        self.mqtt_client.publish('res/{}/error'.format(self.name), '{}'.format(e), 0, False)

    def search(self):
        try:
            self.config.led.on_off_led(self.name, True)
            self.config.alkes.on_off_alkes(self.name, True)
            self.config.alkes.buttonPress(self.name)
            self.is_on = True
            adapter = pygatt.GATTToolBackend(hci_device=self.id_hci)
            time.sleep(1)
            adapter.start()

            all_result = ''
            res = ''

            for discover in adapter.scan(run_as_root=True, timeout=1):
                if discover['name'] == None:
                    pass
                elif (discover['name'] == self.ble_name):
                    res = '{' + '"name" : "{} - {}", "address": "{}"'.format(discover['name'], discover['address'], discover['address']) + '}'
                    msg = '{'+ '"result": {}, "finished": {}'.format('[' + res + ']',  'false') + '}'
                    # print('msg:',msg)
                    self.mqtt_client.publish('res/{}/list'.format(self.name), msg, 1, False)
                    all_result += res + ','

            res = '[' + all_result[:-1] + ']'
            msg = '{'+ '"result": {}, "finished": {}'.format(res, 'true') + '}'
            # print('msg:',msg)
            self.mqtt_client.publish('res/{}/list'.format(self.name), msg, 1, False)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logger.error('Runner {} Error {} in line {} file {}'.format(self.name, e,exc_tb.tb_lineno,fname))

        finally:
            adapter.stop()
            self.logger.test('Finish request Search {}'.format(self.name))
            self.config.alkes.on_off_alkes(self.name, False)
            self.config.led.on_off_led(self.name, False)

    def run(self):
        try:
            # logging.basicConfig()
            # logging.getLogger('pygatt').setLevel(logging.DEBUG)

            while not self.is_done:
                self.is_stop = False
                self.start_time = self.config.get_timeNow()

                self.config.led.on_off_led(self.name, True)
                self.config.alkes.on_off_alkes(self.name, True)

                time.sleep(3)
                while not self.is_start and not self.is_done:
                    self.check_time()

                if self.is_start:
                    self.config.alkes.buttonPress(self.name)

                if not self.is_done:
                    adapter = pygatt.GATTToolBackend(hci_device=self.id_hci)
                    time.sleep(1)
                    adapter.start()

                is_device_found = False
                is_subscribed = False
                is_timeOut = False
                timeOut_count = 0

                while not is_device_found and not self.is_done:
                    self.check_time()
                    for discover in adapter.scan(run_as_root=True, timeout=1):
                        self.check_time()
                        if self.is_done:
                            break
                        if discover['address'] == self.address: #self.bluetooth_address:
                            # print('name: ', discover['name'])
                            self.logger.info('Device is found, try to connect with device')
                            is_device_found = True
                            retry = True
                            while retry and not self.is_done:
                                try:
                                    self.check_time(0.5)
                                    if not self.is_done:
                                        self.logger.info('connecting...')
                                        device = adapter.connect(discover['address'],auto_reconnect=True)#, address_type=pygatt.BLEAddressType.random) # ADF Type Random
                                        #time.sleep(1)
                                    retry = False
                                    self.logger.info('connected!')
                                except Exception as e:
                                    retry = True
                                    print('{} reconnecting...'.format(e))

                            # print('connected!')
                            is_subscribed = False
                            subscribe_count = 0
                            while not is_subscribed and not self.is_done:
                                try:
                                    self.check_time()
                                    device.discover_characteristics().keys()
                                    self.logger.info("subscribing...")
                                    device.subscribe(self.char_blood_pressure_measurement, callback=self.handle_measurement, wait_for_response=False)
                                    self.logger.info('subcribed!')
                                    is_subscribed = True
                                except Exception as e:
                                    is_timeOut = True
                                    self.is_stop = True
                                    self.logger.error('Runner {} Exception {}'.format('subscribe', e))
                                    self.appendFile("Failed to Subscribe")
                                    if subscribe_count == 3:
                                        break
                                    subscribe_count+=1

                            self.time_notified = time.time()
                            print("this is the next lines waited")
                            while not self.is_stop:
                                self.check_time()
                                if self.is_done:
                                    break
                                elif time.time() - self.time_notified > 5 and self.is_notified:
                                    if not self.is_DetectHand:
                                        self.appendFile("BLE Notification failed and finger not detected")
                                        raise Exception("BLE Notification failed and finger not detected")

                                    else:
                                        self.appendFile("BLE Notification failed")
                                        #raise Exception("BLE Notification failed")
                                        #device.disconnect()
                                        device.resubscribe_all()

                                elif time.time() - self.time_notified > 10 and not self.is_notified:
                                    if not self.is_DetectHand:
                                        self.appendFile("BLE Notification failed and never notified and finger not detected")
                                        raise Exception("BLE Notification failed and never notified and finger not detected")
                                    else:
                                        self.appendFile("BLE Notification failed and never notified or finger not detected")
                                        #raise Exception("BLE Notification failed and never notified or finger not detected")
                                        #device.disconnect()
                                        device.resubscribe_all()

                                elif self.is_stopDetectingFinger:
                                    self.appendFile("no finger detected")
                                    raise Exception("No Finger Detected")

                            if not self.is_done:
                                self.logger.info('stopping adapter...')
                                adapter.stop()

                            self.is_notified = False
                            self.config.alkes.on_off_alkes(self.name, False)
                            self.is_start = False
                            break

                    if not self.is_done:
                        if is_timeOut:
                            self.is_done = True
                            self.finish_time = self.config.get_timeNow()

                            res = 'Err-2'
                            msg = '{'+ '"result": "{}", "start_time":"{}","finish_time":"{}", "error": {}, "finished": {}'.format(res, self.start_time,self.finish_time, 'true', 'true') + '}'
                            # print('msg:',msg)
                            self.mqtt_client.publish('res/{}'.format(self.name),msg, 1, False)

                        elif not is_device_found:
                            # print('Device not found')
                            timeOut_count+=1
                            if timeOut_count == 5:
                                is_timeOut = True

                            res = 'Err-2'
                            msg = '{'+ '"result": "{}", "error": {}, "finished": {}'.format(res, 'true', 'false') + '}'
                            # print('msg:',msg)
                            self.mqtt_client.publish('res/{}'.format(self.name),msg, 1, False)
                            # time.sleep(0.5)

                        elif not is_subscribed:
                            res = 'Err-2'
                            msg = '{'+ '"result": "{}", "error": {}, "finished": {}'.format(res, 'true', 'false') + '}'
                            # print('msg:',msg)
                            self.mqtt_client.publish('res/{}'.format(self.name),msg, 1, False)
                            time.sleep(0.5)

        except Exception as e:
            self.finish_time = self.config.get_timeNow()
            res = 'Err-2'
            msg = '{'+ '"result": "{}", "start_time":"{}","finish_time":"{}", "error": {}, "finished": {}'.format(res, self.start_time,self.finish_time, 'true', 'true') + '}'
            # print('msg:',msg)
            self.mqtt_client.publish('res/{}'.format(self.name),msg, 1, False)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)
            self.logger.error('Runner {} Error {} in line {} file {}'.format(self.name, e,exc_tb.tb_lineno,fname))
        finally:
            try:
                #device.disconnect()
                adapter.stop()
            except Exception as e:
                self.logger.error('Runner {} not set adapter yet'.format(self.name))
            # if self.self.is_on:
            #     self.config.buttonPress(self.pin_button_servo, self.angle_servo, 2)
            self.logger.test('Finish request {}'.format(self.name))
            self.config.led.on_off_led(self.name, False)
            self.config.alkes.on_off_alkes(self.name, False)
            self.config.turnOffServo(self.pin_button_servo)

    def appendFile(self, msg):
        heading = datetime.now().strftime("--%H:%M:%S--")
        data = "{} {} -> {}\n".format(heading, datetime.now().strftime("%d %B %Y"), msg)
        file = 'log_oxy.txt'
        hs = open(file,"a")
        hs.write(data)
        hs.close()


class OxyFiturReconnect(Oxymeter):
    '''
    Kelas fitur tambahan reconnect oxymeter
    '''
    def initial_state_time(self):
        self.is_stop = False
        self.start_time = self.config.get_timeNow()

    def turn_on_device(self):
        self.config.led.on_off_led(self.name, True)
        self.config.alkes.on_off_alkes(self.name, True)

    def press_button_device(self):
        while not self.is_start and not self.is_done:
            #self.check_time()
            print("waiting for start")

        if self.is_start:
            self.config.alkes.buttonPress(self.name)

    def run(self, ble : Bluetooth):
        initial_state_time()
        turn_on_device()
        press_button_device()

        handle = HandleMeasurement()
        ble = Bluetooth(handle)
        adapter = ble.create_adapter_ble()
        ble.scan_ble_device(adapter)
        ble.connect_ble_device(adapter)

class Bluetooth:
    def __init__(self, handle : HandleMeasurement):
        self.is_device_found = False
        self.is_connected = False
        self.is_subscribed = False
        self.is_timeOut = False
        self.timeOut_count = 0
        self.id_hci = "hci0"
        self.address = ""
        self.handle = handle

    def create_adapter_ble(self):
        adapter = pygatt.GATTToolBackend(hci_device=self.id_hci)
        time.sleep(1)
        adapter.start()
        return adapter

    def scan_ble_device(self, adapter):
        while not self.is_device_found :
            #self.check_time()
            for discover in adapter.scan(run_as_root=True, timeout=1):
                if discover['address'] == self.address: #self.bluetooth_address:
                    is_device_found = True
                    connect_ble_device(adapter)

    def connect_ble_device(self, adapter):
        # print('name: ', discover['name'])
        retry = True
        while retry :
            try:
                self.logger.info('connecting...')
                device = adapter.connect(discover['address'],auto_reconnect=True)#, address_type=pygatt.BLEAddressType.random) # ADF Type Random
            except Exception as e:
                retry = True
                print('{} reconnecting...'.format(e))
            else:
                retry = False
                self.logger.info('connected!')
        return device

    def subscribe_ble_device(self, device ):
        is_subscribed = False
        subscribe_count = 0
        while not is_subscribed :
            try:
                self.check_time()
                device.discover_characteristics().keys()
                self.logger.info("subscribing...")
                device.subscribe(self.char_blood_pressure_measurement, callback=self.handle.handle_measurement, wait_for_response=False)
                self.logger.info('subcribed!')
                is_subscribed = True
            except Exception as e:
                is_timeOut = True
                self.is_stop = True
                self.logger.error('Runner {} Exception {}'.format('subscribe', e))
                self.appendFile("Failed to Subscribe")
                if subscribe_count == 3:
                    break
                subscribe_count+=1

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
