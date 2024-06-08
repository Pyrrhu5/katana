"""Not really automated testing. But has to manually asses if the commands have been sent."""
from time import sleep

from katana_go import LOGGER
from katana_go.config import Config
from katana_go.connection import Bluetooth
from katana_go.roland_midi import create_katana_packet
from katana_go.roland_sysex import Parameter, ParameterValue, roland_sysex

def setup():
    config = Config()
    connection = Bluetooth.cli(config)

    return connection


def _simple_parameters_test(connection, parameter: Parameter, parameter_config: ParameterValue):
    for value in [parameter_config.max_value, parameter_config.min_value, parameter_config.max_value//2]:
        LOGGER.info(f"Testing {parameter.__class__.__name__} {parameter_config} at value {value}")
        packet = create_katana_packet(parameter, parameter_config, value)
        if connection:
            connection.send(packet)
            sleep(5)


def test_all(connection):
    for parameter in [roland_sysex.amp]:
        for parameter_config in [parameter.volume, parameter.gain, parameter.bass, parameter.middle, parameter.treble]:
            _simple_parameters_test(connection, parameter, parameter_config)


if __name__ == "__main__":
    connection = setup()
    test_all(connection)
