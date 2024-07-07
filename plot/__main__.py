import typing
import sys
import argparse
import logging
import plot.loaders
import plot.metrics

import matplotlib.pyplot
import matplotlib.figure
import pandas

def plotter(func):
  def wrapper(*args, **kwargs):
    fig = matplotlib.pyplot.figure(figsize=(10, 10))
    func(*args, **kwargs)
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig(func.__qualname__)
    matplotlib.pyplot.close()
  return wrapper

def plot_drone_metrics(ID: str, df: pandas.DataFrame, x: str, y: str) -> None:
  matplotlib.pyplot.plot(df[x], df[y], label=ID)

def plot_drones_metrics(drones: dict, x: str, y: str) -> None:
  for ID in drones:
    plot_drone_metrics(ID, drones[ID], x, y)
  matplotlib.pyplot.xlabel(x)
  matplotlib.pyplot.ylabel(y)

@plotter
def plot_drones_distance_from_target_over_time(drones: dict) -> None:
  plot_drones_metrics(drones, 'Timestamp', 'DistanceFromTarget')

@plotter
def plot_drones_speed_over_time(drones: dict) -> None:
  plot_drones_metrics(drones, 'Timestamp', 'Speed')

@plotter
def plot_drones_min_distance_from_drones_over_time(drones: dict) -> None:
  plot_drones_metrics(drones, 'Timestamp', 'MinDistanceFromDrones')

@plotter
def plot_drones_mean_distance_from_drones_over_time(drones: dict) -> None:
  plot_drones_metrics(drones, 'Timestamp', 'MeanDistanceFromDrones')

@plotter
def plot_drones_max_distance_from_drones_over_time(drones: dict) -> None:
  plot_drones_metrics(drones, 'Timestamp', 'MaxDistanceFromDrones')

def do_action():
  drones = plot.loaders.DroneLogsLoader.run(path="./out")
  targets = plot.loaders.TargetsLogLoader.run(path="./out")

  distances = plot.metrics.GetDistances.run(drones=drones)
  min_distances = plot.metrics.GetMinDistances.run(distances=distances)
  mean_distances = plot.metrics.GetMeanDistances.run(distances=distances)
  max_distances = plot.metrics.GetMaxDistances.run(distances=distances)
  for ID in drones:
    drones[ID]['MinDistanceFromDrones'] = min_distances[ID]
    drones[ID]['MeanDistanceFromDrones'] = mean_distances[ID]
    drones[ID]['MaxDistanceFromDrones'] = max_distances[ID]

  plot_drones_distance_from_target_over_time(drones)
  plot_drones_speed_over_time(drones)
  plot_drones_min_distance_from_drones_over_time(drones)
  plot_drones_mean_distance_from_drones_over_time(drones)
  plot_drones_max_distance_from_drones_over_time(drones)

if __name__ == "__main__":
  action_map: dict[str, typing.Callable[[argparse.Namespace], None]] = {
  }

  cli = argparse.ArgumentParser()
  cli.add_argument('verb', type=str, choices=action_map.keys(), help='action to perform')
  cli.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose output')
  config = cli.parse_args(sys.argv[1:])

  if config.verbose:
    logging.getLogger().setLevel(logging.INFO)

  action_map[config.verb](config)
