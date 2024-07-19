import plot.generics
import numpy
import pandas

class ComputeDistance(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.A: pandas.DataFrame
    self.B: pandas.DataFrame
    return numpy.linalg.norm((numpy.array(self.A[['PosX', 'PosY', 'PosZ']])) - (numpy.array(self.B[['PosX', 'PosY', 'PosZ']])), axis=1)

class ComputeDistancesGlobally(plot.generics.ServiceObject[dict[str, dict[str, numpy.ndarray]]]):
  def exec(self) -> dict[str, dict[str, numpy.ndarray]]:
    self.drones: dict
    return {ID_A: {ID_B:ComputeDistance.run(A=self.drones[ID_A], B=self.drones[ID_B]) for ID_B in self.drones if ID_B != ID_A} for ID_A in self.drones}

class ComputeMeanDistancesWithinSquadron(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.drones: dict
    self.targets: pandas.DataFrame
    results = {target:[] for target in self.targets.TargetID}
    for i in range(len(self.drones['sp0'])):
      distances = {target:[] for target in self.targets.TargetID}
      for A in self.drones:
        for B in self.drones:
          if A != B and self.drones[A].Target[i] == self.drones[B].Target[i]:
            distances[self.drones[B].Target[i]].append(numpy.linalg.norm([
              self.drones[A].PosX[i] - self.drones[B].PosX[i],
              self.drones[A].PosY[i] - self.drones[B].PosY[i],
              self.drones[A].PosZ[i] - self.drones[B].PosZ[i],
            ]))
      for target in distances:
        if len(distances[target]) == 0:
          distances[target] = [0]
        results[target].append(numpy.mean(distances[target]))
    return numpy.mean(list(results.values()), axis=0)

class ComputeMinDistancesGlobally(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.drones: dict
    self.distances: dict = ComputeDistancesGlobally.run(drones=self.drones)
    return numpy.min(numpy.array([numpy.min(numpy.array(list(self.distances[ID].values())), axis=0) for ID in self.distances]), axis=0)

class ComputeMeanDistanceFromTarget(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.drones: dict
    return numpy.mean(numpy.array([drone.DistanceFromTarget for drone in self.drones.values()]), axis=0)

class ComputeMeanSpeed(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.drones: dict
    return numpy.mean(numpy.array([drone.Speed for drone in self.drones.values()]), axis=0)

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
    for timestamp in range(length):
      for ID, df in self.drones.items():
        if timestamp < 1 or df.Target[timestamp] != df.Target[timestamp - 1]:
          result[df.Target[timestamp]][timestamp] += 1
    return result

class ComputeMeanTargetDensityOverTime(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.drones: dict[str, pandas.DataFrame]
    self.targets: pandas.DataFrame
    target_densities = ComputeTargetDensitiesOverTime.run(drones=self.drones, targets=self.targets)
    return numpy.mean(numpy.array([_ for _ in target_densities.values()]), axis=0)

class ComputeVarTargetDensityOverTime(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.drones: dict[str, pandas.DataFrame]
    self.targets: pandas.DataFrame
    target_densities = ComputeTargetDensitiesOverTime.run(drones=self.drones, targets=self.targets)
    return numpy.var(numpy.array([_ for _ in target_densities.values()]), axis=0)

class ComputeMeanTargetSwitchOverTime(plot.generics.ServiceObject[numpy.ndarray]):
  def exec(self) -> numpy.ndarray:
    self.drones: dict[str, pandas.DataFrame]
    self.targets: pandas.DataFrame
    target_densities = ComputeTargetSwitchesOverTime.run(drones=self.drones, targets=self.targets)
    return numpy.mean(numpy.array([_ for _ in target_densities.values()]), axis=0)

class CompressCurveLengths(plot.generics.ServiceObject[dict[str, numpy.ndarray]]):
  def exec(self) -> dict[str, numpy.ndarray]:
    self.curves: dict[str, numpy.ndarray]
    min_length = min([len(serie) for serie in self.curves.values()])
    for i in self.curves.keys():
      original_length = len(self.curves[i])
      if original_length > min_length:
        self.curves[i] = ApplyMovingAverageCompression.run(input=self.curves[i], length=min_length)
    return self.curves
