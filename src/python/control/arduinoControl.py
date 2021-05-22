from PySide2.QtCore import Qt, Signal
from PySide2.QtCore import QThread
import datetime, time
import serial
value = 0

class ControlArduino(QThread):
    newValue = Signal(object, object)
    testRS232 = Signal(object)

    def __init__(self, event):
        QThread.__init__(self)
        self.stopped = event
        self.altValue = 0

    def run(self):
        try:
            # self.serArduino = serial.Serial('COM1', 9600, timeout=0)  # Windows PC
            self.serArduino = serial.Serial("/dev/ttyS0",9600,timeout=1)       #Linux PC - Raspberry
            self.noRS232_UNO = 1
            self.testRS232.emit(1)
        except:
            print("ESP32 not found")
            self.noRS232_UNO = 0
            self.testRS232.emit(0)

        while not self.stopped.wait(0.1):  # 1 max 0.3
            self.ArduinoLoop()

    def ArduinoLoop(self):
        global value
        if self.noRS232_UNO:
            self.serArduino.write(b'p')
            time.sleep(0.01)
            wert = self.serArduino.read(5)
            try:
                wert1 = wert.split()
                intwert = int(wert1[0])
                value = int(22 + (intwert / 3.84))
                self.newValue.emit(intwert, value)

                print(intwert)
            except:
                print("error Arduino Serial")
