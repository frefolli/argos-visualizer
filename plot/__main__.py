import typing
import sys
import argparse
import logging
import plot.loaders
import plot.metrics
import plot.plotters
import os
import numpy

def do_series(config: argparse.Namespace):
  series = {}
  for i in os.listdir("archive/outs/"):
    basepath: str = os.path.join("archive/outs/", i)
    drones = plot.loaders.DroneLogsLoader.run(path=basepath)
    targets = plot.loaders.TargetsLogLoader.run(path=basepath)
    metric = plot.metrics.__getattribute__("Compute%s" % config.function).run(drones=drones, targets=targets)
    assert(len(drones['sp0'].Timestamp) == len(metric))
    series[i] = metric
  series = plot.metrics.CompressCurveLengths.run(curves=series)
  plot.plotters.__getattribute__("PlotSeries%s" % config.function)(series)

def do_variants(config: argparse.Namespace):
  variants = {}
  for variant in os.listdir("archive/outs/"):
    series = {}
    for i in os.listdir(os.path.join("archive/outs/", variant)):
      basepath: str = os.path.join("archive/outs/", variant, i)
      drones = plot.loaders.DroneLogsLoader.run(path=basepath)
      targets = plot.loaders.TargetsLogLoader.run(path=basepath)
      metric = plot.metrics.__getattribute__("Compute%s" % config.function).run(drones=drones, targets=targets)
      assert(len(drones['sp0'].Timestamp) == len(metric))
      series[i] = metric
    series = plot.metrics.CompressCurveLengths.run(curves=series)
    data = numpy.mean(numpy.array([_ for _ in series.values()]), axis=0)
    variants[variant] = data
  variants = plot.metrics.CompressCurveLengths.run(curves=variants)
  plot.plotters.__getattribute__("PlotSeries%s" % config.function)(variants)

if __name__ == "__main__":
  action_map: dict[str, typing.Callable[[argparse.Namespace], None]] = {
    'series': do_series,
    'variants': do_variants
  }

  cli = argparse.ArgumentParser()
  cli.add_argument('verb', type=str, choices=action_map.keys(), help='action to perform')
  cli.add_argument('-f', '--function', type=str, default='MeanDistanceFromTarget', choices=[
    'MeanDistanceFromTarget', 'MeanSpeed',
    'MeanTargetDensityOverTime', 'MeanTargetSwitchOverTime', 'VarTargetDensityOverTime',
    'MeanDistancesGlobally', 'MeanDistancesWithinSquadron'
  ], help='function to use for generating a compared study between multiple runs.')
  cli.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose output')
  config = cli.parse_args(sys.argv[1:])

  if config.verbose:
    logging.getLogger().setLevel(logging.INFO)

  action_map[config.verb](config)
