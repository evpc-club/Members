#include "Snake.h"

Snake::Snake(int x, int y, float speed, int grid)
{
	spawn = Coordinate(x, y);
	snakeBody.push_back(Coordinate(x, y));
	snakeBody.push_back(Coordinate(x - 1, y));
	gridSize = grid;
	snakeSpeed = speed;
	currentDirection = Direction::None;
}

Snake::~Snake()
{
}

std::vector<Coordinate> Snake::getSnake() { return snakeBody; }
Direction Snake::getDirection() { return currentDirection; }
Direction Snake::getActualDirection()
{
	Coordinate head = snakeBody[0];
	Coordinate neck = snakeBody[1];

	if (head.x - neck.x == 1) return Direction::Right;
	else if (head.x - neck.x == -1) return Direction::Left;
	else if (head.y - neck.y == 1) return Direction::Down;
	else if (head.y - neck.y == -1) return Direction::Up;
	else return Direction::None;
}
Coordinate Snake::getPos() { return snakeBody[0]; }
float Snake::getSpeed() { return snakeSpeed; }
Coordinate Snake::getPreSpawn() { return spawn; }

void Snake::setDirection(const Direction& dir) { currentDirection = dir; }
void Snake::setPos(const Coordinate& pos) { snakeBody[0] = pos; }

void Snake::move()
{
	if (currentDirection == Direction::None) return;

	if (snakeBody.size() > 1)
	{
		for (int i = snakeBody.size() - 1; i > 0; i--)
		{
			snakeBody[i] = snakeBody[i - 1];
		}
	}
	
	switch (currentDirection)
	{
	case Direction::Up:
	{
		snakeBody[0].y--;
		break;
	}
	case Direction::Right:
	{
		snakeBody[0].x++;
		break;
	}
	case Direction::Down:
	{
		snakeBody[0].y++;
		break;
	}
	case Direction::Left:
	{
		snakeBody[0].x--;
		break;
	}
	}
}

void Snake::extend()
{
	Coordinate tail = snakeBody[snakeBody.size() - 1];
	Coordinate neck = snakeBody[snakeBody.size() - 2];
	Coordinate new_tail;

	if (tail.x == neck.x) new_tail = Coordinate(tail.x, tail.y + (tail.y - neck.y));
	else if (tail.y == neck.y) new_tail = Coordinate(tail.x + (tail.x - neck.x), tail.y);

	snakeBody.push_back(new_tail);
}

void Snake::render(sf::RenderWindow& window)
{
	if (snakeBody.empty()) return;

	for (auto iter = snakeBody.begin(); iter != snakeBody.end(); iter++)
	{
		if (iter == snakeBody.begin()) snakePen.setFillColor(sf::Color::Yellow);
		else snakePen.setFillColor(sf::Color::Green);

		snakePen.setPosition(iter->x * gridSize, iter->y * gridSize);
		snakePen.setSize(sf::Vector2f(gridSize - 1, gridSize - 1));
		window.draw(snakePen);
	}
}