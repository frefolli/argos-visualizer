project('argos-visualizer', 'cpp',
  version : '0.1',
  default_options : ['warning_level=3', 'cpp_std=c++20'])

raylib = dependency('raylib')
jsoncpp = dependency('jsoncpp')
includes = include_directories('./include')

executable('main.exe', [
    './src/main.cc',
    './src/prez/eyebot.cc',
    './src/prez/entity.cc',
    './src/prez/cluster.cc',
    './src/prez/configuration.cc',
    './src/prez/support.cc',
  ],
  include_directories: [includes],
  dependencies: [raylib, jsoncpp])
