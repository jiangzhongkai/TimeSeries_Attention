import tensorflow as tf
import pandas as pd
import numpy as np

from typing import Tuple, List
import json
from config import *
"""
数据加载
"""
def window(size,driving_series,target_series,df=pd.DataFrame()):
    X = df[driving_series].values
    y = df[target_series].values
    X_T = []
    y_T = []
    for i in range(len(X) - size + 1):
        X_T.append(X[i : i + size])
        y_T.append(y[i : i + size])

    return np.array(X_T), np.array(y_T)


def get_np_dataset(config=Config(), cat_before_window= False,default_file="conf/SML2010.json"):
    dfs = []
    config.get_data_path(default_file)
    config.get_target_cols(default_file)
    config.get_drop_cols(default_file)

    for path in config.data_paths:
        dfs.append(pd.read_csv(path, sep=config.sep, usecols=config.usecols()))
    df = None
    X_T = None
    y_T = None
    if cat_before_window:
        df = pd.concat(dfs)  #进行拼接
        X_T, y_T = window(df=df, size=config.T, driving_series=config.driving_series(), target_series=config.target_cols)
        X_T = X_T.transpose((0, 2, 1))
    else:
        X_Ts = []
        y_Ts = []
        for df in dfs:
            X_T, y_T = window(df=df, size=config.T, driving_series=config.driving_series(), target_series=config.target_cols)
            X_T = X_T.transpose((0, 2, 1))
            X_Ts.append(X_T)
            y_Ts.append(np.squeeze(y_T))
        X_T = np.vstack(X_Ts)
        y_T = np.vstack(y_Ts)
    return X_T, y_T

def get_datasets(config=Config(), cat_before_window= False, shuffled= True,default_file="conf/SML2010.json"):
    """
    Returns X and y of the data passed as config.

    Parameters
    ----------
    config : Config
    cat_before_window : bool
        Whether to concatenate the files before transforming it
        into windows

    Returns
    -------
    train_d : tensorflow.data.Dataset(tuples)
        The tuples are
            X : (config.batch_size, config.n, config.T)
            y : (config.batch_size, config.T, 1)
    val_d
    test_d

    Usage
    -----

    Graph Mode:
    ```
    dataset = get_train_test_dataset(config)
    dataset = dataset.batch(batch_size) # .shuffle() if necessary
    iterator = dataset.make_initializable_iterator()
    next_element = iterator.get_next()
    for _ in range(epochs):
        sess.run(iterator.initializer)
        while True:
            try:
                sess.run(next_element)
            except tf.errors.OutOfRangeError:
                break

        # [Perform end-of-epoch calculations here.]
    ```

    Eager Mode:
    ```
        dataset = get_train_test_dataset(config)
        it = dataset.batch(batch_size)
        for x, y in it:
            print(x, y)
    ```
    """
    X_T, y_T = get_np_dataset(config)
    train_size = int(len(X_T) * config.train_ratio)
    val_size = int(((1 - config.train_ratio) / 2) * len(X_T))
    test_size = val_size

    #数据的读取
    dataset = tf.data.Dataset.zip(
        (
            tf.data.Dataset.from_tensor_slices(X_T),
            tf.data.Dataset.from_tensor_slices(y_T),
        )
    )
    train_dataset = dataset.take(train_size)
    if shuffled:
        train_dataset = train_dataset.shuffle(
            train_size, reshuffle_each_iteration=True
        )
    val_dataset = dataset.skip(train_size).take(val_size)
    test_dataset = dataset.skip(train_size + val_size).take(test_size)
    return train_dataset, val_dataset, test_dataset

# Test
if __name__ == "__main__":
    tf.enable_eager_execution()
    # with open("conf/SML2010.json",'r') as f:
    #     config=json.load(f)
    #     # config = Config.from_json(f.read())
    # print(config)
    # print(config["data_paths"])

    config=Config()

    tr, val, te = get_datasets(config)

    it = tr.make_one_shot_iterator()
    lit = val.make_one_shot_iterator()
    tit = te.make_one_shot_iterator()
    print("len(list(it)):{}".format(len(list(it))))
    print("len(list(lit)):{}".format(len(list(lit))))
    print("len(list(tit)):{}".format(len(list(tit))))

    it = tr.make_one_shot_iterator()
    print(next(it))

    it = tr.make_one_shot_iterator()
    print(next(it))
