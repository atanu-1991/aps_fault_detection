from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils import get_collection_as_dataframe
import sys,os
from sensor.entity import config_entity
from sensor.components.data_ingestion import Data_Ingestion
from sensor.components.data_validation import Data_Validation
from sensor.components.data_transformation import Data_Transformation
from sensor.components.model_trainer import Model_Trainer
from sensor.components.model_evaluation import Model_Evaluation


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

          # Data Ingestion
          data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          # print(data_ingestion_config.to_dict())

          data_ingestion = Data_Ingestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

          # Data Validation
          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = Data_Validation(data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)

          data_validation_artifact = data_validation.initiate_data_validation()
          # print(data_validation_artifact)

          # Data Transformation
          data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation = Data_Transformation(data_transformation_config=data_transformation_config, data_ingestion_artifact=data_ingestion_artifact)

          data_transformation_artifact = data_transformation.initiate_data_transformation()

          # Model Trainer
          model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
          model_trainer = Model_Trainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)

          model_trainer_artifact = model_trainer.initiate_model_trainer()
          # print(model_trainer_artifact)

          # Model Evaluation
          model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
          model_eval = Model_Evaluation(model_eval_config=model_eval_config, data_ingestion_artifact=data_ingestion_artifact, data_transformation_artifact=data_transformation_artifact, model_trainer_artifact=model_trainer_artifact)

          model_eval_artifact = model_eval.initiate_model_evaluation()
          print(model_eval_artifact)

          
     except Exception as e:
          logging.debug(str(e))
          print(e)