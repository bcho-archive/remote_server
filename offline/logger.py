#coding: utf-8

import logging

import config


def build_logger(logger, format, level):
    logger.setFormatter(format)
    logger.setLevel(level)
    return logger


def get_file_logging_handler(format, level=None, log_path=None):
    level = level or config.log_level
    log_path = log_path or config.log_path
    logger = logging.FileHandler(log_path)
    return build_logger(logger, format, level)


def get_console_logging_handler(format, level=None):
    level = level or config.log_level
    logger = logging.StreamHandler()
    return build_logger(logger, format, level)
