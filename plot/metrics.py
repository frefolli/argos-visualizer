import plot.generics
import numpy
import pandas

class GetDistance(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.A: pandas.DataFrame
    self.B: pandas.DataFrame
    return numpy.linalg.norm((numpy.array(self.A[['PosX', 'PosY', 'PosZ']])) - (numpy.array(self.B[['PosX', 'PosY', 'PosZ']])), axis=1)

class GetDistances(plot.generics.ServiceObject[dict[str, dict[str, numpy.ndarray]]]):
  def exec(self) -> dict[str, dict[str, numpy.ndarray]]:
    self.drones: dict
    return {ID_A: {ID_B:GetDistance.run(A=self.drones[ID_A], B=self.drones[ID_B]) for ID_B in self.drones if ID_B != ID_A} for ID_A in self.drones}

class GetMinDistances(plot.generics.ServiceObject[dict[str, numpy.ndarray]]):
  def exec(self) -> dict[str, numpy.ndarray]:
    self.distances: dict
    return {ID:numpy.min(numpy.array(list(self.distances[ID].values())), axis=0) for ID in self.distances}

class GetMeanDistances(plot.generics.ServiceObject[dict[str, numpy.ndarray]]):
  def exec(self) -> dict[str, numpy.ndarray]:
    self.distances: dict
    return {ID:numpy.mean(numpy.array(list(self.distances[ID].values())), axis=0) for ID in self.distances}

class GetMaxDistances(plot.generics.ServiceObject[dict[str, numpy.ndarray]]):
  def exec(self) -> dict[str, numpy.ndarray]:
    self.distances: dict
    return {ID:numpy.max(numpy.array(list(self.distances[ID].values())), axis=0) for ID in self.distances}
