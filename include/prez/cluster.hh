#ifndef CLUSTER_HH
#define CLUSTER_HH
/** @file cluster.hh */
#include <prez/configuration.hh>
#include <prez/entity.hh>
#include <prez/support.hh>
#include <vector>

namespace prez {
  struct Cluster {
    std::vector<Entity*> entities;
    void Update(const Configuration& configuration);
    void Draw(const Configuration& configuration) const;
    void Destroy();
  };
}
#endif//CLUSTER_HH
