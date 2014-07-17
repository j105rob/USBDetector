import dbus
import gobject
import commands,os,sys,random
import time

class DeviceAddedListener:
    
    def __init__(self):
        
        self.bus = dbus.SystemBus()
        self.hal_manager_obj = self.bus.get_object(
                                              "org.freedesktop.Hal",
                                              "/org/freedesktop/Hal/Manager")
        self.hal_manager = dbus.Interface(self.hal_manager_obj,
                                          "org.freedesktop.Hal.Manager")
        self.hal_manager.connect_to_signal("DeviceAdded", self._filter)
        self.hal_manager.connect_to_signal("DeviceRemoved", self._removal)

    def _filter(self, udi):
        
        device_obj = self.bus.get_object ("org.freedesktop.Hal", udi)
        device = dbus.Interface(device_obj, "org.freedesktop.Hal.Device")

        if device.QueryCapability("volume"):
            
            self.usb = True
            return self.do_something(device)

    def _removal(self, udi):

        if self.usb:
            
            if self.mounted:
                result = commands.getstatusoutput('sudo umount -f %s' % (self.mount_dir))
                result = commands.getstatusoutput('sudo rm -rf %s' % (self.mount_dir))
                print "Device Removed."

            else:
                print "Device removed, something was wrong with it."
            self.mounted = False
            self.usb = False

    def do_something(self, volume):
        
        self.device_file = volume.GetProperty("block.device")
        self.label = volume.GetProperty("volume.label")
        self.fstype = volume.GetProperty("volume.fstype")
        self.mounted = volume.GetProperty("volume.is_mounted")
        self.mount_point = volume.GetProperty("volume.mount_point")
        self.uuid = volume.GetProperty("volume.uuid")
        
        try:
            size = volume.GetProperty("volume.size")
        except:
            size = 0

        print "New storage device detected:"
        print "  Device File: %s" % self.device_file
        print "  UUID: %s"%self.uuid
        print "  Label: %s" % self.label
        print "  Fstype: %s" % self.fstype
        print "  Size: %s (%.2fGB)" % (size, float(size) / 1024**3)

        self.mount_dir = "/mnt/" + self.label
        mkdir = 'sudo mkdir %s' % (self.mount_dir)
        mount = 'sudo mount -U %s %s' % (self.uuid, self.mount_dir)
        print 'Mounting Device: %s (%s)' % (self.label, self.mount_dir)

        if not os.path.exists(self.mount_dir):
            
            result = commands.getstatusoutput(mkdir)

            if result[0] != 0:
                print 'dir creation failed, aborting USB mount.'

            else:
                result = commands.getstatusoutput(mount)
                self.mounted = True

                if random.randint(1, 4) > 1:
                    cp = "sudo sed -n 1p payload.txt > /media/"+self.label+"/payload.txt"
                    result = commands.getstatusoutput(cp)

                else:
                    line = random.choice(open('badluck.txt').readlines())
                    cp = "sudo echo "+line+" > /media/"+self.label+"/payload.txt"
                    result = commands.getstatusoutput(cp)
                    
        else:
            print 'Unclean mount directory, please clean up.'

        if result[0] != 0:
            print 'Failed to copy egg...'

        else:
            dl = "sudo sed -i 1d payload.txt"
            result = commands.getstatusoutput(dl)

        result = commands.getstatusoutput('sudo umount -f %s' % (self.mount_dir))
        result = commands.getstatusoutput('sudo rm -rf %s' % (self.mount_dir))
        time.sleep(2)
        print "Jobs Done."
        
if __name__ == '__main__':
    
    from dbus.mainloop.glib import DBusGMainLoop
    DBusGMainLoop(set_as_default=True)
    loop = gobject.MainLoop()
    DeviceAddedListener()
    loop.run()