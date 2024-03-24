import time

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pygame
from pygame import midi


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

min_f, max_f, inc_f = volume.GetVolumeRange()

class MidiInput():
    def __init__(self):
        pygame.init()
        pygame.midi.init()
        self.devid = midi.get_default_input_id()
        self.midiInput = pygame.midi.Input(self.devid)

        # Print all MIDI devices and which one is being used
        for i in range(midi.get_count()):
            print(midi.get_device_info(i), i)
        print ("Using device ", self.devid)

    def run(self):
        self.read = self.midiInput.read(100)

        for e in self.read:
            data = e[0]
            ts = e[1]
            
            state = data[0]>>4
            channel = data[0]&0xF

            if state != 0xB or channel != 0xF:
                return

            cc = data[1]
            val = data[2]

            if cc == 111:
                vol = val / 127
                print("Volume is ", vol*100)
                volume.SetMasterVolumeLevelScalar(vol, None)


cur_f = volume.GetMasterVolumeLevel()
cur_p = 100 * volume.GetMasterVolumeLevelScalar()
print("Master Volume: ", round(cur_p))

test = MidiInput()
while True:
   test.run()
   time.sleep(.100)
