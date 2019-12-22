#pragma once

#include <SFML/Graphics.hpp>
#include <vector>

#include "Util.h"

// A class representing a snake in the snake game. Only create once.
class Snake
{
private:
	// The snake itself.

	// A container of (x, y) for the snake.
	std::vector<Coordinate> snakeBody;
	// The spawn coordinate of the snake. Can be set during initialization.
	Coordinate spawn;
	// The speed the snake should run. Can be set during initialization.
	int snakeSpeed;
	// The current Direction the snake is running.
	Direction currentDirection;

	// Drawing stuff.
	sf::RectangleShape snakePen;
	int gridSize;
public:
	Snake(int x = 5, int y = 3, float speed = 15.0f, int grid = 16);
	~Snake();

	// Get methods.

	// Return: a deep copy of snakeBody.
	// Return type: std::vector<Coordinate>.
	std::vector<Coordinate> getSnake();
	// Return: a deep copy of the current direction of the snake.
	// Return type: Direction.
	Direction getDirection(); // This return this->currentDirection
	// This method is used because there may be times the game hasn't update the snake yet, and someone change the state of the snake again,
	// resulting in missing several pieces.
	// Return: a Direction that is based on the current position of the head and neck, rather than the current direction of the snake.
	// Return type: Direction.
	Direction getActualDirection(); // This return Direction based on the position of the head and the neck of the snake.
	// Return: a deep copy of the current position of the head.
	// Return type: Coordinate.
	Coordinate getPos();
	// Return: a deep copy of the current speed of the snake.
	// Return type: int.
	float getSpeed();
	// Return: a deep copy of the snake respawn location.
	// Return type: Coordinate.
	Coordinate getPreSpawn();

	// Modify methods.

	// Set the direction of the snake.
	// Param:
	// - dir (const Direction&): the direction you want to set.
	void setDirection(const Direction& dir);
	// Set the position of the head.
	// Note: this method should be only called to deal with the snake-return-to-the-other-side issue.
	// Param:
	// - pos (const Coordinate&): the position you want to set.
	void setPos(const Coordinate& pos);

	// Extend the length of the snake.
	void extend();
	// Move the snake to the current direction.
	void move();

	// Draw the snake to window.
	// Param:
	// - window (sf::RenderWindow&): the window you want to draw in.
	void render(sf::RenderWindow& window);
};

