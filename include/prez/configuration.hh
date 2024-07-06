#ifndef CONFIGURATION_HH
#define CONFIGURATION_HH
/** @file configuration.hh */
#include <raylib.h>
#include <cstdint>
#include <cmath>
#include <string>
#include <unordered_map>

namespace prez {
  struct Configuration {
    struct Window {
      uint32_t width = 800;
      uint32_t height = 600;
      const char* icon = "resources/images/icon.png";
      const char* title = "Sulla statale che porta a Cremona";
      uint32_t fps = 30;
      Color background_color = WHITE;
    } window;

    struct Arena {
      Vector3 size = {100.0f, 100.0f, 100.0f};
      struct Entity {
        struct Drawing {
          float_t radius = 2;
          Color color = BLACK;
        } drawing;
      };
      std::unordered_map<std::string, Entity> entities;
    } arena;

    struct Camera {
      Vector3 position = { 50.0f, 100.0f, 50.0f };
      Vector3 target = { 0.0f, 0.0f, 0.0f };
      Vector3 up = { 0.0f, 1.0f, 0.0f };
      float_t fovy = 45.0f;
      CameraProjection projection = CAMERA_PERSPECTIVE;
    } camera;

    void Load(const std::string& filepath);
    void Dump(const std::string& filepath) const;
  };
}
#endif//CONFIGURATION_HH
