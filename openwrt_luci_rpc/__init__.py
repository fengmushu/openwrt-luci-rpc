# -*- coding: utf-8 -*-

"""Top-level package for openwrt-luci-rpc."""

__author__ = """Finbarr Brady"""
__email__ = 'fbradyirl@github.io'
__version__ = '1.1.16'

from .openwrt_luci_rpc import OpenWrtLuciRPC
from .constants import Constants


class OpenWrtRpc:
    """
    Class to interact with OpenWrt router running luci-mod-rpc package.
    """

    def __init__(self, host_url=Constants.DEFAULT_LOCAL_HOST,
                 username=Constants.DEFAULT_USERNAME,
                 password=Constants.DEFAULT_PASSWORD,
                 is_https=Constants.DEFAULT_HTTPS,
                 verify_https=Constants.DEFAULT_VERIFY_HTTPS):
        """
        Initiate an instance with a default local ip (192.168.1.1)
        :param host_url: string - host url. Defaults to 192.168.1.1
        :param username: string - username. Defaults to root
        :param password: string - password. Default is blank
        :param is_https: boolean - use https? Default is false
        :param verify_https: boolean - verify https? Default is true
        """
        self.router = OpenWrtLuciRPC(host_url, username, password,
                                     is_https, verify_https)
        self.iface = 'ath16'

    def is_logged_in(self):
        """Returns true if a token has been aquired"""
        return self.router.token is not None

    def get_all_connected_devices(self,
                                  only_reachable=Constants.DEFAULT_ONLY_REACH,
                                  wlan_interfaces=Constants.DEFAULT_WLAN_IF):
        """Get details of all devices"""
        return self.router.get_all_connected_devices(
            only_reachable=only_reachable, wlan_interfaces=wlan_interfaces)

    def get_rssi(self, iface = None):
        ''' Return the link quality <n/s>, rssi, noise floor of ap client '''
        if iface != None:
            self.iface = iface
        try:
            linkq = self.router.get_rssi(self.iface)
            # print(linkq)
            rssi = int(linkq[2])
            if rssi <= -90:
                if self.iface == 'ath16':
                    self.iface = 'ath06'
                else:
                    self.iface = 'ath16'
                linkq = self.router.get_rssi(self.iface)
        except Exception as e:
            # ath06/16 not exisited
            linkq = ['0', '100', '-127', '-101']
            print(e)
            pass

        return int(linkq[0]), int(linkq[1]), int(linkq[2])

    def get_trx(self):
        return self.router.get_trx()
