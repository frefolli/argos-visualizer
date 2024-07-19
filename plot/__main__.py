import typing
import sys
import argparse
import logging

import plot.loaders
import plot.metrics
import plot.plotters
import os
import numpy
import random

TARGET_DISTANCE_WITHIN_SQUADRON = 2.0

def append_compendium(series: dict):
  if config.function == "MeanDistancesWithinSquadron":
    min_timestamp = min([min(_[0]) for _ in series.values()])
    max_timestamp = max([max(_[0]) for _ in series.values()])
    Xs = range(min_timestamp, max_timestamp)
    Ys = numpy.ones((len(Xs),)) * TARGET_DISTANCE_WITHIN_SQUADRON
    series["Target Distance"] = (Xs, Ys)

BASE_COLORS = [
  [255, 0, 0],
  [0, 255, 0],
  [0, 0, 255],
]

def pick_color():
  return BASE_COLORS.pop()

def random_color_shade(base_color, distorsion = 0.1):
  return numpy.clip(numpy.rint(base_color + (numpy.random.uniform(-distorsion, distorsion, size=3) * 255)), 0, 255)

def color_distance(A, B):
  return numpy.linalg.norm(A - B)

def same_colors(A, B):
  return color_distance(A, B) < 10

def generate_new_color(existing_colors, distorsion = 0.1):
  base_color = existing_colors[0]
  shade = random_color_shade(base_color, distorsion)
  not_ok: bool = True
  while not_ok:
    not_ok = False
    for color in existing_colors:
      if same_colors(shade, color):
        not_ok = True
        shade = random_color_shade(base_color, distorsion)
        break
  return shade

def define_colors_for_curves(series: dict, group_by: list|None) -> dict:
  if group_by is None:
    # Every curve get coloured at random by providing None to matplotlib
    return {}

  colors: dict = {group:[pick_color()] for group in group_by}
  pairings: dict = {}
  for key in series.keys():
    for group in group_by:
      if group in key.split('__'):
        color = generate_new_color(colors[group], distorsion=0.4)
        colors[group].append(color)
        pairings[key] = color
  return {k:[_/255 for _ in v] for k,v in pairings.items()}


def do_variants(config: argparse.Namespace):
  os.makedirs(config.output, exist_ok=True)
  series = {}
  for variant in os.listdir("%s/outs/" % config.input):
    for i in os.listdir(os.path.join("%s/outs/" % config.input, variant)):
      basepath: str = os.path.join("%s/outs/" % config.input, variant, i)
      drones = plot.loaders.DroneLogsLoader.run(path=basepath)
      targets = plot.loaders.TargetsLogLoader.run(path=basepath)
      metric = plot.metrics.__getattribute__("Compute%s" % config.function).run(drones=drones, targets=targets)
      assert(len(drones['sp0'].Timestamp) == len(metric))
      series[variant] = (drones['sp0'].Timestamp, metric)
      break
  append_compendium(series)
  colors = define_colors_for_curves(series, config.group_by)
  plot.plotters.PlotSeries("%s/%s.png" % (config.output, config.function), series, "Timestamp", config.function, colors)

if __name__ == "__main__":
  action_map: dict[str, typing.Callable[[argparse.Namespace], None]] = {
    'variants': do_variants
  }

  cli = argparse.ArgumentParser()
  cli.add_argument('verb', type=str, choices=action_map.keys(), help='action to perform')
  cli.add_argument('-i', '--input', type=str, default='archive', help='directory where to search for logs')
  cli.add_argument('-o', '--output', type=str, default='output', help='directory where to put plots')
  cli.add_argument('-f', '--function', type=str, default='MeanDistanceFromTarget', help='function to use for generating a compared study between multiple runs.')
  cli.add_argument('-g', '--group-by', type=str, nargs='+', help="group colors by this grouping clause")
  cli.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose output')
  config = cli.parse_args(sys.argv[1:])

  if config.verbose:
    logging.getLogger().setLevel(logging.INFO)

  action_map[config.verb](config)
