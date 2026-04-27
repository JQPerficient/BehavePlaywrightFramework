from configparser import ConfigParser


def readConfig(section, key):
    """
    :param section:
    :param key:
    :return:
    """
    config = ConfigParser()
    config.read(".\\ConfigurationData\\conf.ini")
    return config.get(section, key)
