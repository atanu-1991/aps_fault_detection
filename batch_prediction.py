from sensor.pipeline.training_pipeline import start_training_pipeline
from sensor.pipeline.batch_prediction import start_batch_prediction
from sensor.logger import logging


print(__name__)
if __name__ == "__main__":
    try:
          # test_logger_and_exception()
          # get_collection_as_dataframe(database_name="aps", collection_name="sensor")
          
          # start_training_pipeline()
          output_file = start_batch_prediction(input_file_path = file_path)
          print(output_file)

    except Exception as e:
          logging.debug(str(e))
          print(e)