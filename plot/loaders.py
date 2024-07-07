"""
Service Loaders
"""
import plot.generics
import pandas
import os

class DataFrameLoader(plot.generics.ServiceObject[pandas.DataFrame]):
  def exec(self) -> pandas.DataFrame:
    self.path: str
    return pandas.read_csv(self.path)

class CsvLoader(plot.generics.ServiceObject[dict]):
  def exec(self) -> dict:
    self.path: str
    df = DataFrameLoader.run(path=self.path)
    return {k:list(df[k]) for k in df}

class DroneLogsLoader(plot.generics.ServiceObject[dict[str, pandas.DataFrame]]):
  def exec(self) -> dict[str, pandas.DataFrame]:
    self.path: str
    drones_dir: str = os.path.join(self.path, 'drones')
    drones = {}
    for file in os.listdir(drones_dir):
      ID = file.replace('.csv', '')
      path = os.path.join(drones_dir, file)
      df = DataFrameLoader.run(path=path)
      drones[ID] = df
    return drones

class TargetsLogLoader(plot.generics.ServiceObject[pandas.DataFrame]):
  def exec(self) -> pandas.DataFrame:
    self.path: str
    return DataFrameLoader.run(path=os.path.join(self.path, 'targets.csv'))
