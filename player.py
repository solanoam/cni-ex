"""
Written by
Noam Solan - 204484703
Yarin Kimhi - 308337641
"""

from options.ClientOptions import client_params, logging_level
from src.Client import Client
from src.Logger import Logger

Client(Logger(logging_level), **client_params).init_game()
