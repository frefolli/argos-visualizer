import matplotlib.pyplot

def plotter(func):
  def wrapper(out: str, *args, **kwargs):
    fig = matplotlib.pyplot.figure(figsize=(10, 10))
    func(*args, **kwargs)
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig(out)
    matplotlib.pyplot.close()
  return wrapper

@plotter
def PlotSeries(series: dict, xlabel: str, ylabel: str, colors: dict = {}):
  for label in sorted(series.keys()):
    (Xs, Ys) = series[label]
    matplotlib.pyplot.plot(Xs, Ys, label=label, color=colors.get(label))
  matplotlib.pyplot.xlabel(xlabel)
  matplotlib.pyplot.ylabel(ylabel)
