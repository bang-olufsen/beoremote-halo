import sys

from zeroconf import ServiceBrowser, Zeroconf


class BeoremoteHaloListener:

    def remove_service(self, zeroconf, type, name):
        """

        :param zeroconf:
        :param type:
        :param name:
        :return:
        """
        return

    def add_service(self, zeroconf, type, name):
        """

        :param zeroconf:
        :param type:
        :param name:
        """
        info = zeroconf.get_service_info(type, name)
        print("%s" % info.server[:-1])

    def update_service(self, zeroconf, type, name):
        """

        :param zeroconf:
        :param type:
        :param name:
        :return:
        """
        return


if __name__ == "__main__":
    zeroconf = Zeroconf()
    listener = BeoremoteHaloListener()
    browser = ServiceBrowser(zeroconf, "_zenith._tcp.local.", listener)
    try:
        input(
            "Discovering Beoremote Halo on network...\r\n"
            "If Beoremote Halo does not appear on the list, try waking it "
            "up while discovering in running.\r\nPress enter to exit...\n\n")
    finally:
        zeroconf.close()
    sys.exit()
