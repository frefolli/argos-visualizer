#include <prez/cluster.hh>
#include <prez/support.hh>

void prez::Cluster::Update(const Configuration& configuration) {
  for (Entity* entity : entities) {
    entity->Update(configuration);
  }
}

void prez::Cluster::Draw(const Configuration& configuration) const {
  for (const Entity* entity : entities) {
    entity->Draw(configuration);
  }
}

void prez::Cluster::Destroy() {
  for (Entity* entity : entities) {
    entity->Destroy();
    delete entity;
  }
  entities.clear();
}
