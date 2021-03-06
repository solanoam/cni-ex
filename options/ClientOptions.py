"""
Written by
Noam Solan - 204484703
Yarin Kimhi - 308337641
repo - https://github.com/solanoam/cni-ex
"""

from src.Logger import LoggingLevel

logging_level = LoggingLevel.DEBUG.value
client_params = {
    "ip": "127.0.0.1",
    "port": 7000,
    "pack_size": 1024
}