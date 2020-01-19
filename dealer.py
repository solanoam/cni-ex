"""
Written by
Noam Solan - 204484703
Yarin Kimhi - 308337641
"""

from options.ClientOptions import logging_level
from src.Logger import Logger
from src.Server import Server
from options.ServerOptions import server_params

Server(Logger(logging_level), **server_params).await_game_requests()
