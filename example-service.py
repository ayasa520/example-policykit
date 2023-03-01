#!/usr/bin/env python3

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib


class NotPrivilegedException (dbus.DBusException):
    _dbus_error_name = "org.example.HelloWorld.dbus.service.PolKit.NotPrivilegedException"
    def __init__ (self, action_id, *p, **k):
        self._dbus_error_name = self.__class__._dbus_error_name + "." + action_id
        super (NotPrivilegedException, self).__init__ (*p, **k)


class HelloWorld(dbus.service.Object):
    def __init__(self, conn=None, object_path=None, bus_name=None):
        self.dbus_info = None
        self.polkit = None
        dbus.service.Object.__init__(self, conn, object_path, bus_name)

    @dbus.service.method(dbus_interface="com.example.HelloWorldInterface", in_signature="s", out_signature="s", sender_keyword="sender", connection_keyword="conn")
    def SayHello(self, name, sender=None, conn=None):
        self._check_polkit_privilege(
            sender, conn, "com.example.HelloWorld.auth")
        return "Hello " + name
        

    def _check_polkit_privilege(self, sender, conn, action_id):
        # Get Peer PID
        if self.dbus_info is None:
            # Get DBus Interface and get info thru that
            self.dbus_info = dbus.Interface(conn.get_object("org.freedesktop.DBus",
                                                            "/org/freedesktop/DBus/Bus", False),
                                            "org.freedesktop.DBus")
        pid = self.dbus_info.GetConnectionUnixProcessID(sender)

        # Query polkit
        if self.polkit is None:
            self.polkit = dbus.Interface(dbus.SystemBus().get_object(
                "org.freedesktop.PolicyKit1",
                "/org/freedesktop/PolicyKit1/Authority", False),
                "org.freedesktop.PolicyKit1.Authority")

        # Check auth against polkit; if it times out, try again
        try:
            auth_response = self.polkit.CheckAuthorization(
                ("unix-process", {"pid": dbus.UInt32(pid, variant_level=1),
                                  "start-time": dbus.UInt64(0, variant_level=1)}),
                action_id, {"AllowUserInteraction": "true"}, dbus.UInt32(1), "", timeout=600)
            print(auth_response)
            (is_auth, _, details) = auth_response
        except dbus.DBusException as e:
            if e._dbus_error_name == "org.freedesktop.DBus.Error.ServiceUnknown":
                # polkitd timeout, retry
                self.polkit = None
                return self._check_polkit_privilege(sender, conn, action_id)
            else:
                # it's another error, propagate it
                raise

        if not is_auth:
            # Aww, not authorized :(
            print(":(")
            raise NotPrivilegedException(action_id)

        print("Successful authorization!")
        return True


if __name__ == "__main__":
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    name = dbus.service.BusName("com.example.HelloWorld", bus)
    helloworld = HelloWorld(bus, "/HelloWorld")
    mainloop = GLib.MainLoop()
    mainloop.run()
