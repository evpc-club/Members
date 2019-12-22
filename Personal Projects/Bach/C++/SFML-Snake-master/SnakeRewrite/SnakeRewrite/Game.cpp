#include "Game.h"
#include <iostream>


Game::Game(int grid, float snakeSpeed, Coordinate snakeSpawn, Coordinate bottomRightMapSize) : m_window("Snake", sf::Vector2u(800, 600))
{
	snake = new Snake(snakeSpawn.x, snakeSpawn.y, snakeSpeed, grid);
	world = new World(bottomRightMapSize.x, bottomRightMapSize.y, grid);
	gridSize = grid;
	m_clock.restart();
	m_elapsed = 0.0f;

	// Debug purpose
	//world->createWall(Coordinate(0, 0), Coordinate(bottomRightMapSize.x / grid, 1));
	//world->createWall(Coordinate(0, 1), Coordinate(1, bottomRightMapSize.y / grid));
	//world->createWall(Coordinate(1, bottomRightMapSize.y / grid - 1), Coordinate(bottomRightMapSize.x / grid, bottomRightMapSize.y / grid));
	//world->createWall(Coordinate(bottomRightMapSize.x / grid - 1, 1), Coordinate(bottomRightMapSize.x / grid, bottomRightMapSize.y / grid - 1));

	apple = world->spawnApple();
}

Game::~Game()
{
	delete snake;
	delete world;
}

void Game::getInput()
{
	if (sf::Keyboard::isKeyPressed(sf::Keyboard::Up) && snake->getActualDirection() != Direction::Down)
		snake->setDirection(Direction::Up);
	else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right) && snake->getActualDirection() != Direction::Left)
		snake->setDirection(Direction::Right);
	else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Down) && snake->getActualDirection() != Direction::Up)
		snake->setDirection(Direction::Down);
	else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left) && snake->getActualDirection() != Direction::Right)
		snake->setDirection(Direction::Left);
}

void Game::checkCollision()
{
	Coordinate head = snake->getPos();
	for (unsigned int i = 0; i < world->getWalls().size(); i++)
	{
		if (world->getWalls()[i].isCollide(head)) { isLost = true; break; }
	}

	for (unsigned int i = 1; i < snake->getSnake().size(); i++)
		if (head == snake->getSnake()[i]) { isLost = true; break; }

	if (isLost)
	{
		lose();
		resetGame();
	}
}

void Game::lose()
{
	std::cout << "You lost!" << std::endl;
}
void Game::resetGame()
{
	Coordinate spawn = snake->getPreSpawn();
	int speed = snake->getSpeed();
	delete snake;
	snake = new Snake(spawn.x, spawn.y, speed, gridSize);
	apple = world->spawnApple();
	isLost = false;
}

void Game::eat()
{
	Coordinate head = snake->getPos();
	if (head == apple)
	{
		snake->extend();
		apple = world->spawnApple();
	}
}

void Game::mapbound()
{
	Coordinate head = snake->getPos();
	Coordinate worldSize = world->getSize();
	if (!isLost)
	{
		if (head.x < 0)
		{
			snake->setPos(Coordinate(worldSize.x - 1, head.y));
		}
		if (head.x >= worldSize.x)
		{
			snake->setPos(Coordinate(0, head.y));
		}

		if (head.y < 0)
		{
			snake->setPos(Coordinate(head.x, worldSize.y - 1));
		}
		if (head.y >= worldSize.y)
		{
			snake->setPos(Coordinate(head.x, 0));
		}
	}
}

void Game::Update()
{
	m_window.Update();
	float timestep = 1.0f / snake->getSpeed();
	if (m_elapsed >= timestep)
	{
		snake->move();
		checkCollision();
		mapbound();
		checkCollision();
		eat();
		if (snake->getSnake().size() == (world->getSize().x * world->getSize().y))
		{
			std::cout << "You won!" << std::endl;
			resetGame();
		}
		m_elapsed -= timestep;
	}
}

void Game::Render()
{
	m_window.BeginDraw();
	world->render(m_window.getRenderWindow());
	snake->render(m_window.getRenderWindow());
	m_window.EndDraw();
}

Window* Game::GetWindow() { return &m_window; }