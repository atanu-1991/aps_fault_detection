import pandas as pd
import numpy as np
from sensor.config import mongo_client
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
import yaml
import dill

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    Params:
    database_name: database name
    collection_name: collection name
    =========================================
    return Pandas dataframe of a collection
    """
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found Columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping Column: _id")
            df = df.drop("_id",axis=1)
        logging.info(f"Row and Columns in df: {df.shape}")
        return df

    except Exception  as e:
        logging.debug(str(e))
        raise SensorException(e, sys)


def write_yaml_file(file_path,data:dict):
    """
    This function create yaml file and write report in yaml file

    file_path: path of file
    ==========================================================
    this function does not return
    """
    try:
        file_dir = os.path.dirname(file_path)

        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,'w') as file_writer:
            yaml.dump(data,file_writer)

    except Exception  as e:
        logging.debug(str(e))
        raise SensorException(e, sys)


def convert_column_float(df:pd.DataFrame,exclude_column_list:list):
    """
    This function will change the type of column from object to float
    
    df: pandas data frame
    exclude_column_list: column list of data frame which are not changable
    ======================================================================
    this function returns pandas dataframe
    """
    try:
        for column in df.columns:
            if column not in exclude_column_list:
                df[column] = df[column].astype("float")

        return df
    except Exception  as e:
        logging.debug(str(e))
        raise SensorException(e, sys)


def save_object(file_path:str, obj:object):
    """
    This function save object in dill format

    file_path: str location of file to save
    obj: object which will be saved
    ================================
    return: none
    """
    try:
        logging.info("Entered the save_object method of Utils")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
        logging.info("Exited the save_object method of Utils")

    except Exception  as e:
        logging.debug(str(e))
        raise SensorException(e, sys)


def load_object(file_path:str)->object:
    """
    This function load object 

    file_path: str location of file to save
    ================================
    return: object
    """
    try:
        if not os.path.exists(file_path):
            raise SensorException(f"The file: {file_path} is not exsist", sys)
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)

    except Exception  as e:
        logging.debug(str(e))
        raise SensorException(e, sys) from e


def sav_numpy_array_data(file_path: str, array: np.array):
    """
    This function save numpy array data to file

    file_path: str location of file to save
    array: np.array data to save
    ======================================================
    This function return none
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)

    except Exception  as e:
        logging.debug(str(e))
        raise SensorException(e, sys) from e


def load_numpy_array_data(file_path: str)->np.array:
    """
    This function load numpy array data from file

    file_path: str location of file to save
    ==================================================
    return: np.array data to load
    """
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)

    except Exception  as e:
        logging.debug(str(e))
        raise SensorException(e, sys) from e

























