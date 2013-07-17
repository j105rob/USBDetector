import dbus
import gobject
import commands,os,sys
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
        
    def _filter(self, udi):
        device_obj = self.bus.get_object ("org.freedesktop.Hal", udi)
        device = dbus.Interface(device_obj, "org.freedesktop.Hal.Device")

        if device.QueryCapability("volume"):
            return self.do_something(device)
        
    def do_something(self, volume):
        print dir(volume)
        device_file = volume.GetProperty("block.device")
        label = volume.GetProperty("volume.label")
        fstype = volume.GetProperty("volume.fstype")
        mounted = volume.GetProperty("volume.is_mounted")
        mount_point = volume.GetProperty("volume.mount_point")
        uuid = volume.GetProperty("volume.uuid")
        try:
            size = volume.GetProperty("volume.size")
        except:
            size = 0

        print "New storage device detected:"
        print "  device_file: %s" % device_file
        print "  UUID: %s"%uuid
        print "  label: %s" % label
        print "  fstype: %s" % fstype
        if mounted:
            print "  mount_point: %s" % mount_point
        else:
            print "  not mounted"
        print "  size: %s (%.2fGB)" % (size, float(size) / 1024**3)
        mount_dir = "/mnt/" + label
        mkdir = 'sudo mkdir %s' % (mount_dir)
        mount = 'sudo mount -U %s %s' % (uuid, mount_dir)
        print 'Mounting device: %s (%s)' % (label, mount_dir)
        if not os.path.exists(mount_dir):
            result = commands.getstatusoutput(mkdir)
            if result[0] != 0:
                print 'dir creation failed, aborting USB mount...'
                sys.exit(1)
            else:
                result = commands.getstatusoutput(mount)
        else:
            print 'unclean mount directory, please clean up...'
            sys.exit(1)
        time.sleep(3)
        cp = "sudo cp ./payload.txt /mnt/"+label+"/payload.txt"
        result = commands.getstatusoutput(cp)
        if result[0] != 0:
           print 'Filed to copy file...'
           sys.exit(1)
        else:
            print "Copied file..."
        result = commands.getstatusoutput('sudo umount %s' % (mount_dir))
        if result[1] == 'umount: %s: not mounted' % (mount_dir):
            commands.getstatusoutput('sudo rm -rf %s' % (mount_dir))
        print 'sudo rm -rf %s' % (mount_dir)
        result = commands.getstatusoutput('sudo rm -rf %s' % (mount_dir))
        print "Cleaning up..."
        print result
        

if __name__ == '__main__':
    from dbus.mainloop.glib import DBusGMainLoop
    DBusGMainLoop(set_as_default=True)
    loop = gobject.MainLoop()
    DeviceAddedListener()
    loop.run()