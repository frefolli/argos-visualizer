import typing
import sys
import argparse
import logging
import plot.loaders
import plot.metrics
import plot.plotters
import os

def do_series(config: argparse.Namespace):
  series = {}
  for i in os.listdir("archive/outs/"):
    basepath: str = os.path.join("archive/outs/", i)
    drones = plot.loaders.DroneLogsLoader.run(path=basepath)
    targets = plot.loaders.TargetsLogLoader.run(path=basepath)
    mean_distance_from_target = plot.metrics.__getattribute__("Compute%s" % config.function).run(drones=drones, targets=targets)
    assert(len(drones['sp0'].Timestamp) == len(mean_distance_from_target))
    series[i] = mean_distance_from_target
  plot.plotters.__getattribute__("PlotSeries%s" % config.function)(series)

if __name__ == "__main__":
  action_map: dict[str, typing.Callable[[argparse.Namespace], None]] = {
    'series': do_series
  }

  cli = argparse.ArgumentParser()
  cli.add_argument('verb', type=str, choices=action_map.keys(), help='action to perform')
  cli.add_argument('-f', '--function', type=str, default='MeanDistanceFromTarget', choices=['MeanDistanceFromTarget', 'MeanTargetDensityOverTime', 'MeanTargetSwitchOverTime'], help='function to use for generating a compared study between multiple runs.')
  cli.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose output')
  config = cli.parse_args(sys.argv[1:])

  if config.verbose:
    logging.getLogger().setLevel(logging.INFO)

  action_map[config.verb](config)
