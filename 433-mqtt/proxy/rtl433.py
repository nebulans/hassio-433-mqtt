
class RTL433Command(object):
    binary = 'rtl_433'

    def __init__(self, frequency, frequency_offset, gain, protocols, usb_device='0'):
        self.frequency = frequency
        self.frequency_offset = frequency_offset
        self.gain = gain
        self.protocols = protocols
        self.usb_device = usb_device

    def get_command(self):
        cmd = [
            self.binary,
            '-d', self.usb_device,
            '-F', 'json',
            '-f', self.frequency,
            '-p', self.frequency_offset,
            '-g', self.gain
        ]
        if self.usb_device:
            cmd.extend(['-d', self.usb_device])
        for protocol in self.protocols:
            cmd.extend(['-R', protocol])
        return cmd
