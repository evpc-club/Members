#pragma once
struct Coordinate
{
	int x, y;
	Coordinate(int x = 0, int y = 0) { this->x = x; this->y = y; }
	bool operator==(const Coordinate& object) { return (this->x == object.x && this->y == object.y); }
};

enum class Direction { None, Up, Right, Down, Left};