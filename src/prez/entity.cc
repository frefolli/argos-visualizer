#include <prez/entity.hh>

#define PACMAN_LOGIC(d, pos) \
  if (pos < -d) { \
    pos += d; \
  } else if (pos > d) { \
    pos -= d; \
  }

void inline Pacman(Vector3& pos, const prez::Configuration& configuration) {
  double_t dx = configuration.arena.size.x / 2,
           dy = configuration.arena.size.y / 2,
           dz = configuration.arena.size.z / 2;
  PACMAN_LOGIC(dx, pos.x)
  PACMAN_LOGIC(dy, pos.y)
  PACMAN_LOGIC(dz, pos.z)
}

#define BOUNCING_LOGIC(d, pos) \
  if (pos < -d) { \
    pos = -d; \
  } else if (pos > d) { \
    pos = d; \
  }

void inline Bouncing(Vector3& pos, const prez::Configuration& configuration) {
  double_t dx = configuration.arena.size.x / 2,
           dy = configuration.arena.size.y / 2,
           dz = configuration.arena.size.z / 2;
  BOUNCING_LOGIC(dx, pos.x)
  BOUNCING_LOGIC(dy, pos.y)
  BOUNCING_LOGIC(dz, pos.z)
}

void prez::Entity::State::Update(const Configuration& configuration) {
  // Pacman(pos, configuration);
  Bouncing(pos, configuration);
}
