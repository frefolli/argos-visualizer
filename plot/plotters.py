import matplotlib.pyplot
import plot.metrics

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
  min_length = min([len(serie) for serie in series.values()])
  Xs = range(min_length)
  for i, Ys in series.items():
    original_length = len(Ys)
    if original_length > min_length:
      Ys = plot.metrics.ApplyMovingAverageCompression.run(input=Ys, length=min_length)
    matplotlib.pyplot.plot(Xs, Ys, label=("%s (original_length=%s)" % (i, original_length)))
  matplotlib.pyplot.xlabel('Timestamp')
  matplotlib.pyplot.ylabel('Mean Distance From Target')

@plotter
def PlotSeriesMeanTargetDensityOverTime(series: dict):
  min_length = min([len(serie) for serie in series.values()])
  Xs = range(min_length)
  for i, Ys in series.items():
    original_length = len(Ys)
    if original_length > min_length:
      Ys = plot.metrics.ApplyMovingAverageCompression.run(input=Ys, length=min_length)
    matplotlib.pyplot.plot(Xs, Ys, label=("%s (original_length=%s)" % (i, original_length)))
  matplotlib.pyplot.xlabel('Timestamp')
  matplotlib.pyplot.ylabel('Mean Target Density')

@plotter
def PlotSeriesMeanTargetSwitchOverTime(series: dict):
  min_length = min([len(serie) for serie in series.values()])
  Xs = range(min_length)
  for i, Ys in series.items():
    original_length = len(Ys)
    if original_length > min_length:
      Ys = plot.metrics.ApplyMovingAverageCompression.run(input=Ys, length=min_length)
    matplotlib.pyplot.plot(Xs, Ys, label=("%s (original_length=%s)" % (i, original_length)))
  matplotlib.pyplot.xlabel('Timestamp')
  matplotlib.pyplot.ylabel('Mean Target Switch')
