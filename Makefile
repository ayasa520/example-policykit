PREFIX := /usr
BIN_DIR := $(PREFIX)/bin
DBUS_DIR := $(PREFIX)/share/dbus-1
POLKIT_DIR := $(PREFIX)/share/polkit-1

INSTALL_BIN_DIR := $(DESTDIR)$(BIN_DIR)
INSTALL_DBUS_DIR := $(DESTDIR)$(DBUS_DIR)
INSTALL_POLKIT_DIR := $(DESTDIR)$(POLKIT_DIR)

install:
	install -d $(INSTALL_BIN_DIR) $(INSTALL_DBUS_DIR)/system.d $(INSTALL_POLKIT_DIR)/actions $(INSTALL_DBUS_DIR)/system-services
	cp example-service.py $(INSTALL_BIN_DIR)
	cp example-client.py $(INSTALL_BIN_DIR)/example-client
	cp com.example.HelloWorld.conf $(INSTALL_DBUS_DIR)/system.d/
	cp com.example.HelloWorld.policy $(INSTALL_POLKIT_DIR)/actions/
	cp com.example.HelloWorld.service $(INSTALL_DBUS_DIR)/system-services/

uninstall:
	rm -rf $(INSTALL_BIN_DIR)/example-service.py $(INSTALL_DBUS_DIR)/system.d/com.example.HelloWorld.conf  $(INSTALL_POLKIT_DIR)/actions/com.example.HelloWorld.policy $(INSTALL_DBUS_DIR)/system-services/com.example.HelloWorld.service $(INSTALL_BIN_DIR)/example-client
	