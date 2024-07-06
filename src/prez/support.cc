#include <cstring>
#include <exception>
#include <random>
#include <prez/support.hh>
#include <string>
#include <iostream>

inline void Convert(uint32_t& value, char* token) {
  try {
    value = std::stol(token);
  } catch(std::exception& err) {
    std::cerr << err.what() << std::endl;
    std::cerr << "calling stol(\"" << token <<  "\")" << std::endl;
  }
}

inline void Convert(double_t& value, char* token) {
  value = std::stod(token);
}

template<typename T>
inline void First(char* line, T& value) {
  char* token = std::strtok(line, ",");
  Convert(value, token);
}

template<typename T>
inline void Next(T& value) {
  char* token = std::strtok(nullptr, ",");
  Convert(value, token);
}

void operator>>(std::istream& in, prez::LogEntry& entry) {
  std::string line;
  std::getline(in, line);
  First(line.data(), entry.Timestamp);
  Next(entry.PosX);
  Next(entry.PosZ);
  Next(entry.PosY);
  Next(entry.Target);
  Next(entry.DistanceFromTarget);
  Next(entry.Speed);
  Next(entry.TaskAllocatorState);
  Next(entry.TaskExecutorState);
}

std::ostream& operator<<(std::ostream& out, const Vector3& vec) {
  return out << "(" << vec.x << ", " << vec.y << ", " << vec.z << ")";
}

Vector3 operator-(const Vector3& A, const Vector3& B) {
  return Vector3 {
    A.x - B.x,
    A.y - B.y,
    A.z - B.z
  };
}

Vector3 operator+(const Vector3& A, const Vector3& B) {
  return Vector3 {
    A.x + B.x,
    A.y + B.y,
    A.z + B.z
  };
}

Vector3 operator/(const Vector3& A, float_t c) {
  return Vector3 {
    A.x / c,
    A.y / c,
    A.z / c
  };
}

Vector3 operator*(const Vector3& A, float_t c) {
  return Vector3 {
    A.x * c,
    A.y * c,
    A.z * c
  };
}

Vector3& operator-=(Vector3& A, const Vector3& B) {
  A.x -= B.x;
  A.y -= B.y;
  A.z -= B.z;
  return A;
}

Vector3& operator+=(Vector3& A, const Vector3& B) {
  A.x += B.x;
  A.y += B.y;
  A.z += B.z;
  return A;
}

Vector3& operator/=(Vector3& A, float_t c) {
  A.x /= c;
  A.y /= c;
  A.z /= c;
  return A;
}

Vector3& operator*=(Vector3& A, float_t c) {
  A.x *= c;
  A.y *= c;
  A.z *= c;
  return A;
}

float_t Norm(const Vector3& A) {
  return sqrt((A.x * A.x) + (A.y * A.y) + (A.z * A.z));
}

void Normalize(Vector3& A) {
  float_t norm = Norm(A);
  A.x /= norm;
  A.y /= norm;
  A.z /= norm;
}

float_t Distance(const Vector3& A, const Vector3& B) {
  return Norm(A - B);
}

float_t Potential(float target_distance, float_t distance) {
  /** Lennard Jones
  float_t fNormDistExp = ::pow(target_distance / distance, 1.5f);
  return -25.0f / distance * (fNormDistExp * fNormDistExp - fNormDistExp);
  */

  /** Newton */
  return target_distance / (distance * distance);
}

void Randomize(Vector3& A) {
  static std::random_device random_device;
  static std::uniform_real_distribution<float_t> distribution(-5, 5);
  A.x = distribution(random_device);
  A.y = distribution(random_device);
  A.z = distribution(random_device);
}

void operator<<(Json::Value& value, const Vector3& vec) {
  value = Json::objectValue;
  value["x"] = vec.x;
  value["y"] = vec.y;
  value["z"] = vec.z;
}

void operator<<(Json::Value& value, const Color& color) {
  value = Json::objectValue;
  value["r"] = color.r;
  value["g"] = color.g;
  value["b"] = color.b;
  value["a"] = color.a;
}

void operator<<(Vector3& vec, const Json::Value& value) {
  vec.x = value["x"].asFloat();
  vec.y = value["y"].asFloat();
  vec.z = value["z"].asFloat();
}

void operator<<(Color& color, const Json::Value& value) {
  color.r = value["r"].asInt();
  color.g = value["g"].asInt();
  color.b = value["b"].asInt();
  color.a = value["a"].asInt();
}
