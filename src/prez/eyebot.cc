#include <prez/eyebot.hh>
#include <prez/support.hh>
#include <raylib.h>

void prez::Eyebot::Draw(const Configuration& configuration) const {
  const prez::Configuration::Arena::Entity& entity = configuration.arena.entities.at("prez::Eyebot");
  DrawSphere(state.pos, entity.drawing.radius, entity.drawing.color);
}
