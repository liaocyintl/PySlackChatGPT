from src import app
import logging

if __name__ == "__main__":
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)
  logger.addHandler(logging.StreamHandler())
  app.start(port=9999)