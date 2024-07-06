#ifndef SUPPORT_HH
#define SUPPORT_HH
/** @file support.hh */
#include <raylib.h>
#include <json/value.h>
#include <json/json.h>
#include <ostream>
#include <cmath>

namespace prez {
  struct LogEntry {
    uint32_t Timestamp;
    double_t PosX;
    double_t PosY;
    double_t PosZ;
    double_t Target;
    double_t DistanceFromTarget;
    double_t Speed;
    uint32_t TaskAllocatorState;
    uint32_t TaskExecutorState;
  };
};

void operator>>(std::istream& in, prez::LogEntry& entry);

std::ostream& operator<<(std::ostream& out, const Vector3& vec);

Vector3 operator-(const Vector3& A, const Vector3& B);

Vector3 operator+(const Vector3& A, const Vector3& B);

Vector3 operator/(const Vector3& A, float_t c);

Vector3 operator*(const Vector3& A, float_t c);

Vector3& operator-=(Vector3& A, const Vector3& B);

Vector3& operator+=(Vector3& A, const Vector3& B);

Vector3& operator/=(Vector3& A, float_t c);

Vector3& operator*=(Vector3& A, float_t c);

float_t Norm(const Vector3& A);

void Normalize(Vector3& A);

float_t Distance(const Vector3& A, const Vector3& B);

float_t Potential(float_t target_distance, float_t distance);

void Randomize(Vector3& A);

void operator<<(Json::Value& value, const Vector3& vec);

void operator<<(Json::Value& value, const Color& color);

void operator<<(Vector3& vec, const Json::Value& value);

void operator<<(Color& color, const Json::Value& value);
#endif//SUPPORT_HH
