#pragma once
#include <SFML/Graphics.hpp>

#include "Util.h"
#include "Snake.h"

// A struct represent a wall in the snake game. It is a separated object to make it convenience to create more walls.
struct Wall
{
	Coordinate topLeft;
	Coordinate bottomRight;

	Wall(Coordinate& topLeftCorner, Coordinate& bottomRightCorner) { topLeft = topLeftCorner; bottomRight = bottomRightCorner; }

	// Check if a Coordinate collide with the wall.
	// Param:
	// - object (Coordinate&): the coordinate you want to check.
	// Return type: bool.
	bool isCollide(Coordinate& object) 
	{
		return (object.x >= this->topLeft.x && object.x <= this->bottomRight.x - 1 &&
				object.y >= this->topLeft.y && object.y <= this->bottomRight.y - 1);
	}
};

// A class represent a world in the snake game. 
// It is created entirely separated from Snake to make it independence to create obstacles.
class World
{
private:
	// The world itself.

	// A container for all walls in the world.
	std::vector<Wall> bounds;
	// The coordinate of the farthest point from (0, 0).
	Coordinate worldSize;
	// Whether or not to use sprite as the food or a circle.
	bool img_circle;

	// Drawing stuff.

	int gridSize;
	sf::RectangleShape wallShape;
	sf::Texture appleTexture;
	sf::Sprite appleShape;
	sf::CircleShape appleCircleShape;
public:
	World(int sizex, int sizey, int grid);
	~World();

	// Create a wall.
	// Param:
	// - topLeft (Coordinate): the top left coordinate for the rectangle wall.
	// - bottomRight (Coordinate): the bottom right coordinate for the rectangle wall.
	void createWall(Coordinate topLeft, Coordinate bottomRight);
	// Create a wall.
	// Param:
	// - topleftx (int): the top left x coord for the wall.
	// - toplefty (int): the top left y coord for the wall.
	// - bottomrightx (int): the bottom right x coord for the wall.
	// - bottomrighty (int): the bottom right y coord for the wall.
	void createWall(int topleftx, int toplefty, int bottomrightx, int bottomrighty);
	// Spawn the apple randomly in the world.
	// Return: the coordinate of the apple.
	// Return type: Coordinate.
	Coordinate spawnApple();

	// Get methods

	// Return: a deep copy vector of walls.
	// Return type: std::vector<Wall>.
	std::vector<Wall> getWalls();
	// Return: the coordinate of the farthest point from (0, 0).
	// Return type: Coordinate.
	Coordinate getSize();

	// Draw the world to the window.
	// Param:
	// - window (sf::RenderWindow&): the window you want to draw in.
	void render(sf::RenderWindow& window);
};

