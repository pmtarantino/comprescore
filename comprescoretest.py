
from __future__ import division
import bz2
import numpy as np
import random
import math

class CompreScoreTest(object):

    def __init__(self, dm, model, encoder=lambda x: x):
        self.dm = dm
        self.model = model()
        self.modelName = model.__name__
        self.encoder = encoder
        self.evaluation = {}
        self.evaluation_partial = {}

        self.trainMeans = []
        self.groups = []
        self.means = []
        self.actual = []
        self.logs = []

    def processPartition(self, partitionId, method):
        means = []
        std = []
        ind = []

        groups = list(range(1,20))

        for key in range(5,20):
            prom = []

            for j in range(0,200):

                total_per_round = 50

                perGroup = int(total_per_round/key)
                intLimits = [perGroup for _ in range(key)]
                toAdd = (total_per_round-sum(intLimits))
                for i in range(0,toAdd):
                    intLimits[i] = intLimits[i] + 1            

                sample_groups = random.sample(groups, key)
                long_string = ''

                group_order = 0

                dataRows = []

                for g in sample_groups:
                
                    data_rows = self.dm.getByPartition(g, partitionId, method, intLimits[group_order])

                    if(len(data_rows) > intLimits[group_order]):
                        import pdb
                        pdb.set_trace()

                    expected = int(intLimits[group_order])
                    actual = len(data_rows)
                    dataRows.extend(data_rows)              
                    group_order = group_order+1
                
                valor = self.model.score(dataRows)
                prom.append(valor)

            ind.append(key)
            means.append(np.average(prom))
            std.append(np.std(prom))

        return ind, means, std

    def trainOnePartition(self, partitionId):
        ind, means, std = self.processPartition(partitionId, 'training')

        self.trainMeans.append(means)

        logValues = self.model.fit(ind, means)
        
        return {
            'ind' : ind,
            'means' : means,
            'std' : std,
            'logValues' : logValues
        }

    def trainPartition(self, partitionId):
        self.evaluation_partial[partitionId] = self.trainOnePartition(partitionId)
        self.evaluation_partial[partitionId]['mse'] = self.crossValidation(partitionId)

    def crossValidation(self, partitionId):
        ind, means, std = self.processPartition(partitionId, 'testing')
        
        n = 0
        total = 0

        groups = []
        errors = []
        meansG = []
        actual = []

        group = 4
        for groupOld, mean in enumerate(means):
            group = group+1
            total = total + math.pow(self._aprox(mean, partitionId)-group, 2)
            self.mse.append(math.pow(self._aprox(mean, partitionId)-group, 2))
            actual.append(self._aprox(mean, partitionId))
            groups.append(group)
            meansG.append(mean)
            errors.append(self._aprox(mean, partitionId))
            n = n+1
        
        self.means.append(meansG)
        self.groups.append(groups)
        self.actual.append(actual)
        self.logs.append(self.evaluation_partial[partitionId]['logValues'])

        return total/n

    def train(self):
        self.mse = []
        allPartitions = self.dm.getPartitions()

        for i in allPartitions:
            self.trainPartition(i)

        self.evaluation['mse'] = np.average(self.mse)

        means = []
        groups = []
        for j in self.evaluation_partial:
            g = 1
            for m in self.evaluation_partial[j]['means']:
                groups.append(g)
                means.append(m)
                g = g+1

    def model_evaluation(self):
        return self.evaluation

    def _aprox(self, x, clusterId):
        return self.model.inverse(x, self.evaluation_partial[clusterId]['logValues'])

    def _expected(self, clusterId, groups):
        return self.evaluation_partial[clusterId]['means'][groups]
