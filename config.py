"""-*- coding: utf-8 -*-
 DateTime   : 2019/4/19 17:22
 Author  : Peter_Bonnie
 FileName    : Config_1.py
 Software: PyCharm
"""

import json

class Config(object):
    """
    model configuration parameters
    """
    def __init__(self):

        self.decay_rate=0.0
        self.data_paths=None
        self.target_cols=[]
        self.drop_cols=[]
        self.m=64
        self.p=64
        self.sep=','
        self.T=10
        self.learning_rate=0.001
        self.decay_frequency=1000
        self.max_gradient_norm=5
        self.optimizer="adam"
        self.batch_size=128
        self.num_epochs=10
        self.log_dir='/log'
        self.train_ratio=0.8
        self.report_frequency=50
        self.plot_frequency=5
        self.seed=42
        self.inp_att_enabled=True
        self.temporal_att_enabled=True


    def get_drop_cols(self,default_file):
        """get drop_cols

        Args:
            default_file(str):read the json parameters drop_cols from the file

        Returns:
             None
        """
        drop_cols=self.from_json(default_file)

        if "drop_cols" not in drop_cols.keys() or len(drop_cols["drop_cols"])<=0:
            self.drop_cols=[]
        else:
            self.drop_cols=drop_cols["drop_cols"]


    def get_target_cols(self,default_file):
        """get target cols

        Args:
            default_file(str):read the json parameter target_cols from the file

        Returns:
            None
        """
        target_cols=self.from_json(default_file)

        if "target_cols" not in target_cols.keys() or len(target_cols["target_cols"])<=0:
            raise ValueError("target col can not empty.")
        else:
            self.target_cols=target_cols["target_cols"]

    def get_data_path(self,default_file):
        """get data paths

        Args:
            default_file(str):read the json parameter data_paths from the file

        Returns:
            None
        """
        data_paths=self.from_json(default_file)

        if "data_paths" not in data_paths.keys() or len(data_paths["data_paths"])<=0:
            raise ValueError("data paths can not empty.")
        else:
            self.data_paths=data_paths["data_paths"]

    def log_path(self):
        """logger file path"""
        return self.log_dir

    def  usecols(self):
        """columns would be used"""
        path=self.data_paths[0]
        with open(path) as f:
            header=f.readline().strip().split(self.sep)
        return [col for col in header if col not in self.drop_cols]

    def driving_series(self):
        """total feats"""
        return [col for col in self.usecols() if col not in self.target_cols]

    def n(self):
        """compute total avliable feats"""
        return len(self.driving_series())

    def from_json(self,path):
        """load from json file"""
        with open(path,'r') as f:
            c=json.load(f)
        return c

    def to_json(self,path,json_data):
        """save file with json format"""
        with open(path,'w') as f:
            json.dump(json_data,f)

#test
if __name__=='__main__':

    config=Config()
    config.get_drop_cols("conf/SML2010.json")
    config.get_target_cols("conf/SML2010.json")
    config.get_data_path("conf/SML2010.json")
    print(config.drop_cols)
    print(config.target_cols)
    print(config.data_paths)
    print(config.driving_series())
    print(config.usecols())







