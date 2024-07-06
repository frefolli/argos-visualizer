#ifndef ENTITY_HH
#define ENTITY_HH
/** @file entity.hh */
#include "prez/support.hh"
#include <raylib.h>
#include <prez/configuration.hh>
#include <cxxabi.h>
#include <fstream>

namespace prez {
  struct Entity {
  public:
    struct State {
      Vector3 pos;
      
      void Update(const Configuration& /*configuration*/);
    } state;
    std::ifstream logfile;
    LogEntry logentry;

    Entity(std::string logpath) {
      logfile.open(logpath);
      std::string line;
      std::getline(logfile, line);
    }
    virtual ~Entity() {
      logfile.close();
    }

    virtual void Init(const Configuration& /*configuration*/) {};
    virtual void Update(const Configuration& configuration) {
      if (logfile.good()) {
        logfile >> logentry;
        state.pos.x = logentry.PosX;
        state.pos.y = logentry.PosY;
        state.pos.z = logentry.PosZ;
        state.Update(configuration);
      }
    };
    virtual void Draw(const Configuration& /*configuration*/) const {};
    virtual void Reset() {};
    virtual void Destroy() {};
  };

  template<typename CEntity>
  std::string LabelOfEntity() {
    return abi::__cxa_demangle(typeid(CEntity).name(), nullptr, nullptr, nullptr);
  }
}
#endif//ENTITY_HH
