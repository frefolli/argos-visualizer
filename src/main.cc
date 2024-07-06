#include <filesystem>
#include <prez/eyebot.hh>
#include <prez/cluster.hh>
#include <prez/configuration.hh>
#include <prez/support.hh>
#include <raylib.h>
#include <cassert>
#include <iostream>

inline void UpdateView(const prez::Configuration& configuration, Camera3D& camera, const prez::Cluster& entities) {
  BeginDrawing();
  BeginMode3D(camera);
  ClearBackground(configuration.window.background_color);
  DrawPlane({0,0,0}, {configuration.arena.size.x, configuration.arena.size.z}, LIGHTGRAY);
  entities.Draw(configuration);
  EndMode3D();
  DrawFPS(10, 10);
  EndDrawing();
}

int main(int argc, char **argv) {
  prez::Configuration configuration;
  configuration.Load("simulation.json");

  SetConfigFlags(FLAG_VSYNC_HINT);
  InitWindow(configuration.window.width, configuration.window.height, configuration.window.title);
  SetWindowIcon(LoadImage(configuration.window.icon));
  SetTargetFPS(configuration.window.fps);
  assert(IsWindowReady());

  Camera3D camera = {
    .position = configuration.camera.position,
    .target = configuration.camera.target,
    .up = configuration.camera.up,
    .fovy = configuration.camera.fovy,
    .projection = configuration.camera.projection
  };

  prez::Cluster entities;
  for (auto entry : std::filesystem::directory_iterator("./out/drones")) {
    entities.entities.push_back(new prez::Eyebot(entry.path()));
    std::cout << "Loaded " << entry << std::endl;
  }

  UpdateView(configuration, camera, entities);
  while(!WindowShouldClose()) {
    UpdateCamera(&camera, CAMERA_THIRD_PERSON);
    entities.Update(configuration);
    UpdateView(configuration, camera, entities);
  }
  CloseWindow();

  configuration.Dump("simulation.json");
}
