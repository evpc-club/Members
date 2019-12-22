#pragma once
#include "Window.h"
#include "World.h"
#include "Util.h"

class Game
{
public:
	Game(int grid, float snakeSpeed, Coordinate snakeSpawn, Coordinate bottomRightMapSize);
	~Game();

	// Receive input from player.
	void getInput();
	// Update the state of the game.
	void Update();
	// Render the game.
	void Render();
	// Restart the clock for fps.
	void RestartClock() { m_elapsed += m_clock.restart().asSeconds(); }
	// Return: the rendered window.
	// Return type: Window*
	Window* GetWindow();

private:
	// Window management.

	Window m_window;
	sf::Clock m_clock;
	float m_elapsed;

	sf::Time GetElapsed() { return m_clock.getElapsedTime(); }

	// The game element.

	Snake* snake = nullptr;
	World* world = nullptr;

	bool isLost;
	int gridSize;
	Coordinate apple;

	// Make the snake eat the apple.
	void eat();
	// Check if the snake collide with the wall or itself. Call resetGame() and lose() if so. Also set isLost to true.
	void checkCollision();
	// Deal when the snake is out of bound.
	void mapbound();
	// Reset the game.
	void resetGame();
	// Simply print "You lost!".
	void lose();
};

