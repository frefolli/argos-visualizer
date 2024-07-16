import matplotlib.pyplot

def plotter(func):
  def wrapper(*args, **kwargs):
    fig = matplotlib.pyplot.figure(figsize=(10, 10))
    func(*args, **kwargs)
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig(func.__qualname__)
    matplotlib.pyplot.close()
  return wrapper

@plotter
def PlotSeriesMeanSpeed(series: dict):
  for i, Ys in series.items():
    Xs = range(Ys.size)
    matplotlib.pyplot.plot(Xs, Ys, label=("%s" % (i)))
  matplotlib.pyplot.xlabel('Timestamp')
  matplotlib.pyplot.ylabel('Mean Speed Module')

@plotter
def PlotSeriesMeanDistanceFromTarget(series: dict):
  for i, Ys in series.items():
    Xs = range(Ys.size)
    matplotlib.pyplot.plot(Xs, Ys, label=("%s" % (i)))
  matplotlib.pyplot.xlabel('Timestamp')
  matplotlib.pyplot.ylabel('Mean Distance From Target')

@plotter
def PlotSeriesMeanTargetDensityOverTime(series: dict):
  for i, Ys in series.items():
    Xs = range(Ys.size)
    matplotlib.pyplot.plot(Xs, Ys, label=("%s" % (i)))
  matplotlib.pyplot.xlabel('Timestamp')
  matplotlib.pyplot.ylabel('Mean Target Density')

@plotter
def PlotSeriesVarTargetDensityOverTime(series: dict):
  for i, Ys in series.items():
    Xs = range(Ys.size)
    matplotlib.pyplot.plot(Xs, Ys, label=("%s" % (i)))
  matplotlib.pyplot.xlabel('Timestamp')
  matplotlib.pyplot.ylabel('Var Target Density')

@plotter
def PlotSeriesMeanTargetSwitchOverTime(series: dict):
  for i, Ys in series.items():
    Xs = range(Ys.size)
    matplotlib.pyplot.plot(Xs, Ys, label=("%s" % (i)))
  matplotlib.pyplot.xlabel('Timestamp')
  matplotlib.pyplot.ylabel('Mean Target Switch')

@plotter
def PlotSeriesMeanDistancesGlobally(series: dict):
  for i, Ys in series.items():
    Xs = range(Ys.size)
    matplotlib.pyplot.plot(Xs, Ys, label=("%s" % (i)))
  matplotlib.pyplot.xlabel('Timestamp')
  matplotlib.pyplot.ylabel('Mean Distances Globally')


@plotter
def PlotSeriesMeanDistancesWithinSquadron(series: dict):
  length = 0
  for i, Ys in series.items():
    length = Ys.size
    Xs = range(Ys.size)
    matplotlib.pyplot.plot(Xs, Ys, label=("%s" % (i)))

  Xs = range(length)
  Ys = [2.0 for _ in Xs]
  matplotlib.pyplot.plot(Xs, Ys, label=("Target Distance"))

  matplotlib.pyplot.xlabel('Timestamp')
  matplotlib.pyplot.ylabel('Mean Distances Within Squadron')

