#ifndef EYEBOT_HH
#define EYEBOT_HH
/** @file eyebot.hh */
#include <raylib.h>
#include <prez/entity.hh>
#include <prez/configuration.hh>

namespace prez {
  struct Eyebot : public Entity {
    Eyebot(std::string logpath) : Entity(logpath) {}
    void Draw(const Configuration& configuration) const;

    Vector3 target;
  };
}
#endif//EYEBOT_HH
