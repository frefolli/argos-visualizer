import typing
import sys
import argparse
import logging
import plot.loaders
import plot.metrics

import matplotlib.pyplot
import matplotlib.figure
import pandas
import os

def plotter(func):
  def wrapper(*args, **kwargs):
    fig = matplotlib.pyplot.figure(figsize=(10, 10))
    func(*args, **kwargs)
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig(func.__qualname__)
    matplotlib.pyplot.close()
  return wrapper

@plotter
def SeriesDistanceFromTarget(series: dict):
  min_length = min([len(serie) for serie in series.values()])
  Xs = range(min_length)
  for i, Ys in series.items():
    original_length = len(Ys)
    if original_length > min_length:
      Ys = plot.metrics.ApplyMovingAverageCompression.run(input=Ys, length=min_length)
    matplotlib.pyplot.plot(Xs, Ys, label=("%s (original_length=%s)" % (i, original_length)))

def do_series(config: argparse.Namespace):
  series = {}
  for i in os.listdir("archive/outs/"):
    basepath: str = os.path.join("archive/outs/", i)
    drones = plot.loaders.DroneLogsLoader.run(path=basepath)
    targets = plot.loaders.TargetsLogLoader.run(path=basepath)
    mean_distance_from_target = plot.metrics.GetMeanDistanceFromTarget.run(drones=drones)
    assert(len(drones['sp0'].Timestamp) == len(mean_distance_from_target))
    series[i] = mean_distance_from_target
  SeriesDistanceFromTarget(series)

if __name__ == "__main__":
  action_map: dict[str, typing.Callable[[argparse.Namespace], None]] = {
    'series': do_series
  }

  cli = argparse.ArgumentParser()
  cli.add_argument('verb', type=str, choices=action_map.keys(), help='action to perform')
  cli.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose output')
  config = cli.parse_args(sys.argv[1:])

  if config.verbose:
    logging.getLogger().setLevel(logging.INFO)

  action_map[config.verb](config)
