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
def PlotSeriesMeanTargetSwitchOverTime(series: dict):
  for i, Ys in series.items():
    Xs = range(Ys.size)
    matplotlib.pyplot.plot(Xs, Ys, label=("%s" % (i)))
  matplotlib.pyplot.xlabel('Timestamp')
  matplotlib.pyplot.ylabel('Mean Target Switch')
