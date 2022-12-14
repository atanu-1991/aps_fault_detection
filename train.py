from sensor.pipeline.training_pipeline import start_training_pipeline
from sensor.logger import logging

print(__name__)
if __name__ == "__main__":
     try:
        start_training_pipeline()

     except Exception as e:
          logging.debug(str(e))
          print(e)