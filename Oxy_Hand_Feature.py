class OxyFiturReconnect(Oxymeter):
    '''
    Kelas fitur tambahan reconnect oxymeter
    '''
    def handle_measurement(self, handle, value):
        # print('value[0]: {}, value[1]: {}'.format(hex(value[0]), hex(value[1])))

        # Jari tidak terdeteksi
        if value[1] == 0x00 or value[1] == 0x2D :
            self.is_DetectHand = False
            msg = 'Finger not Detected'
            self.mqtt_client.publish('finger'.format(self.name),msg, 1, False)
            # print('time:', time.time() - self.time_finger)

            # Kondisi ketika oxy mati karena jari tidak terdeteksi setelah 4.7 detik
            if (time.time() - self.time_finger > 4.7) and (self.count_notDetected_hand > 3) :
                self.is_stopDetectingFinger = True
            self.count_notDetected_hand +=1

        # Jari Terdeteksi
        elif value[1] != 0xFF:
            self.time_finger = time.time()
            self.count_notDetected_hand = 0
            self.is_DetectHand = True


        if value[0] == 0x81 and value[2] != 127:

            # print('Spo  :',value[2])
            # print('Bpm  :',value[1])
            # print('Pi   :',value[0]/10)
            # print()
            if self.is_start and not self.is_stop:
                if self.first_measure:
                    self.time_measure = time.time()
                    self.first_measure = False
                    self.count_extend_time = 0

                if (time.time() - self.time_measure >= 20):
                    if value[2] < 95 and self.count_extend_time<6:
                        self.time_measure = time.time()
                        self.count_extend_time +=1

                    else:
                        self.finish_time = self.config.get_timeNow()
                        res = '{' + '"Spo": "{}", "Bpm": "{}", "Pi": "{}"'.format(value[2],value[1],value[3]/10) + '}'
                        msg = '{'+ '"result": {}, "start_time":"{}","finish_time":"{}","error": {}, "finished": {}'.format(res, self.start_time,self.finish_time,"false", "true") + '}'
                        self.mqtt_client.publish('res/{}'.format(self.name),msg, 1, False)
                        self.is_stop = True
                        self.first_measure = True
                else:
                    self.is_notified = True
                    self.time_notified = time.time()
                    res = '{' + '"Spo": "{}", "Bpm": "{}", "Pi": "{}"'.format(value[2],value[1],value[3]/10) + '}'
                    msg = '{'+ '"result": {}, "error": {}, "finished": {}'.format(res, "false", "false") + '}'
                    self.mqtt_client.publish('res/{}'.format(self.name),msg, 1, False)


        def reconnect_oxy():
