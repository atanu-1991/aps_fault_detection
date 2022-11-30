from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils import get_collection_as_dataframe
import sys,os
from sensor.entity import config_entity
from sensor.components.data_ingestion import Data_Ingestion


def test_logger_and_exception():
     try:
          logging.info("Starting the test_logger_and_exception")
          result = 3/0
          print(result)
          logging.info("Stopping the test_logger_and_exception")

     except Exception as e:
          logging.debug(str(e))
          raise SensorException(e, sys)



if __name__ == "__main__":
     try:
          # test_logger_and_exception()
          # get_collection_as_dataframe(database_name="aps", collection_name="sensor")
          training_pipeline_config = config_entity.TrainingPipelineConfig()
          data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())

          data_ingestion = Data_Ingestion(data_ingestion_config=data_ingestion_config)
          print(data_ingestion.initiate_data_ingestion())

          
     except Exception as e:
          print(e)