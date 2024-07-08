import plot.generics
import numpy
import pandas

class ComputeDistance(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.A: pandas.DataFrame
    self.B: pandas.DataFrame
    return numpy.linalg.norm((numpy.array(self.A[['PosX', 'PosY', 'PosZ']])) - (numpy.array(self.B[['PosX', 'PosY', 'PosZ']])), axis=1)

class ComputeDistances(plot.generics.ServiceObject[dict[str, dict[str, numpy.ndarray]]]):
  def exec(self) -> dict[str, dict[str, numpy.ndarray]]:
    self.drones: dict
    return {ID_A: {ID_B:ComputeDistance.run(A=self.drones[ID_A], B=self.drones[ID_B]) for ID_B in self.drones if ID_B != ID_A} for ID_A in self.drones}

class ComputeMinDistances(plot.generics.ServiceObject[dict[str, numpy.ndarray]]):
  def exec(self) -> dict[str, numpy.ndarray]:
    self.distances: dict
    return {ID:numpy.min(numpy.array(list(self.distances[ID].values())), axis=0) for ID in self.distances}

class ComputeMeanDistances(plot.generics.ServiceObject[dict[str, numpy.ndarray]]):
  def exec(self) -> dict[str, numpy.ndarray]:
    self.distances: dict
    return {ID:numpy.mean(numpy.array(list(self.distances[ID].values())), axis=0) for ID in self.distances}

class ComputeMaxDistances(plot.generics.ServiceObject[dict[str, numpy.ndarray]]):
  def exec(self) -> dict[str, numpy.ndarray]:
    self.distances: dict
    return {ID:numpy.max(numpy.array(list(self.distances[ID].values())), axis=0) for ID in self.distances}

class ComputeMeanDistanceFromTarget(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.drones: dict
    return numpy.mean(numpy.array([drone.DistanceFromTarget for drone in self.drones.values()]), axis=0)

class ApplyMovingAverageCompression(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.input: numpy.ndarray
    self.length: int
    W = len(self.input) - self.length + 1
    return numpy.array([
      numpy.mean(self.input[i : i + W])
      for i in range(self.length)
    ])

class ComputeTargetDensitiesOverTime(plot.generics.ServiceObject[dict[int, numpy.ndarray]]):
  def exec(self) -> dict[int, numpy.ndarray]:
    self.drones: dict[str, pandas.DataFrame]
    self.targets: pandas.DataFrame
    length = len(self.drones['sp0'])
    result: dict[int, numpy.ndarray] = {k:numpy.zeros(length) for k in range(len(self.targets))}
    for ID, df in self.drones.items():
      for timestamp in range(length):
        result[df.Target[timestamp]][timestamp] += 1
    return result

class ComputeTargetSwitchesOverTime(plot.generics.ServiceObject[dict[int, numpy.ndarray]]):
  def exec(self) -> dict[int, numpy.ndarray]:
    self.drones: dict[str, pandas.DataFrame]
    self.targets: pandas.DataFrame
    length = len(self.drones['sp0'])
    result: dict[int, numpy.ndarray] = {k:numpy.zeros(length) for k in range(len(self.targets))}
    for ID, df in self.drones.items():
      for timestamp in range(length):
        if timestamp < 1 or df.Target[timestamp] != df.Target[timestamp - 1]:
          result[df.Target[timestamp]][timestamp] += 1
    return result

class ComputeMeanTargetDensityOverTime(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.drones: dict[str, pandas.DataFrame]
    self.targets: pandas.DataFrame
    target_densities = ComputeTargetDensitiesOverTime.run(drones=self.drones, targets=self.targets)
    return numpy.mean(numpy.array([_ for _ in target_densities.values()]), axis=0)

class ComputeMeanTargetSwitchOverTime(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.drones: dict[str, pandas.DataFrame]
    self.targets: pandas.DataFrame
    target_densities = ComputeTargetSwitchesOverTime.run(drones=self.drones, targets=self.targets)
    return numpy.mean(numpy.array([_ for _ in target_densities.values()]), axis=0)
