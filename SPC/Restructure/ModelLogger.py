import matplotlib.pyplot as plt
from SPC.misc.extra import PartiallyLoadable
from SPC.Restructure.ml_models.MLModel import MLModel
from SPC.Restructure.ml_models.RLNNModel_CorrectSequence import RLNNModel_CorrectSequence
from SPC.Restructure.cores.CoreGenerator import CoreGenerator
from keras.models import load_model
from keras.utils import custom_object_scope
import importlib

class ModelLogger(PartiallyLoadable):
    
    def __init__(self):
        super().__init__(["step", "all_scores", "bestscore_history", "meanscore_history", "bestfilter_history", 
                          "calculationtime_history", "partition", "core_generator_type", "core_length", "core_representation_length",
                          "RL_n_graphs", "ml_model_type", "ml_training_algorithm_type", "condition_rows",
                          "residuals", "current_bestgraph"])
        self.step = 0
        self.all_scores = {} # {filter_as_tuple:score}
        self.bestscore_history = [] # history of best score
        self.bestfilter_history = []
        self.meanscore_history = [] # history of mean score
        self.calculationtime_history = []
        self.residuals = []
        self.model : MLModel

    def setParameters(self, partition, core_generator_type:str, RL_n_graphs:int, ml_training_algorithm_type:str, ml_model_type:str, condition_rows:int):
        self.partition = partition
        self.RL_n_graphs = RL_n_graphs
        self.core_generator_type = core_generator_type
        self.ml_training_algorithm_type = ml_training_algorithm_type
        self.ml_model_type = ml_model_type
        self.condition_rows = condition_rows

        self.core_generator_class_ = getattr(importlib.import_module("SPC.Restructure.cores."+core_generator_type), core_generator_type)
        self.core_generator_class_ : CoreGenerator
        self.core_length = self.core_generator_class_.getCoreLength(partition)
        self.core_representation_length = self.core_generator_class_.getCoreRepresentationLength(partition)


    def load_model_logger(self, model_path:str):
        assert model_path[len(model_path)-6:] == ".keras", "wrong file format"
        self.load(model_path[:len(model_path)-6]+".my_meta")
        self.model = load_model(model_path)
        self.model.setParameters(self.partition, self.condition_rows, self.core_length, self.core_representation_length)

    def set_model(self, model):
        self.model = model

    def get_model(self):
        return self.model
    
    def save_model_logger(self, model_path):
        self.model.save(model_path)
        self.save(model_path[:len(model_path)-6]+".my_meta")

    def make_plots(self):
        n = len(self.bestscore_history)
        times = list(range(n))
        plt.title("best score ("+str(self.bestscore_history[-1])+")")
        plt.plot(times, self.bestscore_history)
        plt.show()
        plt.title("mean score ("+str(self.meanscore_history[-1])+")")
        plt.plot(times, self.meanscore_history)
        plt.show()
        plt.title("number of different conditions checked")
        plt.title("computation time of the i'th step")
        plt.plot(times, self.calculationtime_history)
        plt.show()

        print("looking for best score...")
        bestscore = -99999999999
        beststate = None
        for state in self.all_scores:
            if self.all_scores[state] > bestscore:
                bestscore = self.all_scores[state]
                beststate = state
        print("bestscore:", bestscore, "from", beststate)

        # implement this again(?):
        #from SPC.Restructure.ml_algorithms.RLAlgorithm import RLAlgorithm
        #condmat = RLAlgorithm.convertStateToConditionMatrix(beststate)
        #conditiontext = evaluator.convertConditionMatrixToText(condmat)
        #print(conditiontext, "\nhas a score of ", evaluator.evaluate(condmat))