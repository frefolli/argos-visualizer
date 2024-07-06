#include <prez/configuration.hh>
#include <prez/support.hh>
#include <json/value.h>
#include <json/json.h>
#include <fstream>
#include <cassert>
#include <raylib.h>

inline void operator<<(Json::Value& value, const prez::Configuration::Window& window) {
  value = Json::objectValue;
  value["width"] = window.width;
  value["height"] = window.height;
  value["icon"] = window.icon;
  value["title"] = window.title;
  value["fps"] = window.fps;
  value["background_color"] << window.background_color;
}

inline void operator<<(prez::Configuration::Window& window, const Json::Value& value) {
  window.width = value["width"].asInt();
  window.height = value["height"].asInt();
  window.icon = value["icon"].asCString();
  window.title = value["title"].asCString();
  window.fps = value["fps"].asInt();
  window.background_color << value["background_color"];
}

inline void operator<<(Json::Value& value, const prez::Configuration::Arena::Entity& entity) {
  value = Json::objectValue;
  value["drawing"] = Json::objectValue;
  value["drawing"]["radius"] = entity.drawing.radius;
  value["drawing"]["color"] << entity.drawing.color;
}

inline void operator<<(prez::Configuration::Arena::Entity& entity, const Json::Value& value) {
  entity.drawing.radius = value["drawing"]["radius"].asFloat();
  entity.drawing.color << value["drawing"]["color"];
}

void prez::Configuration::Load(const std::string& filepath) {
  std::ifstream in;
  in.open(filepath);
  Json::Value jconf;
  Json::Reader text_reader;
  assert(text_reader.parse(in, jconf));
  in.close();

  window << jconf["window"];
  arena.size << jconf["arena"]["size"];
  arena.entities["prez::Eyebot"] << jconf["arena"]["entities"]["prez::Eyebot"];
  camera.position << jconf["camera"]["position"];
  camera.target << jconf["camera"]["target"];
  camera.up << jconf["camera"]["up"];
  camera.fovy = jconf["camera"]["fovy"].asFloat();
  camera.projection = (CameraProjection) jconf["camera"]["projection"].asInt();
}

void prez::Configuration::Dump(const std::string& filepath) const {
  Json::Value jconf = Json::objectValue;
  jconf["window"] << window;
  {
    jconf["arena"] = Json::objectValue;
    jconf["arena"]["size"] << arena.size;
    jconf["arena"]["entities"] = Json::objectValue;
    jconf["arena"]["entities"]["prez::Eyebot"] << arena.entities.at("prez::Eyebot");
  }
  {
    jconf["camera"] = Json::objectValue;
    jconf["camera"]["position"] << camera.position;
    jconf["camera"]["target"] << camera.target;
    jconf["camera"]["up"] << camera.up;
    jconf["camera"]["fovy"] = camera.fovy;
    jconf["camera"]["projection"] = camera.projection;
  }

  Json::StreamWriterBuilder stream_writer_builder;
  Json::StreamWriter* json_writer = stream_writer_builder.newStreamWriter();
  std::ofstream out;
  out.open(filepath);
  json_writer->write(jconf, &out);
  out.close();
  delete json_writer;
}
