#include "World.h"
#include <iostream>


World::World(int sizex, int sizey, int grid)
{
	gridSize = grid;
	worldSize = Coordinate(sizex / grid, sizey / grid);
	std::cout << "World size: " << worldSize.x << ", " << worldSize.y << std::endl;

	if (!appleTexture.loadFromFile("apple.jpg"))
	{
		img_circle = false;
		std::cout << "Failed to load apple.jpg. Using circle shape instead." << std::endl;
		appleCircleShape.setFillColor(sf::Color::Red);
		appleCircleShape.setRadius(gridSize / 2);
	}
	else
	{
		img_circle = false; // Currently set to false because I can't find a way to shrink the texture to fit the grid.
		appleShape.setTexture(appleTexture);

		// Comment the next 2 lines if you find a way to fix the above issue.
		appleCircleShape.setFillColor(sf::Color::Red);
		appleCircleShape.setRadius(gridSize / 2);
	}
}

World::~World()
{
}

void World::createWall(Coordinate topLeft, Coordinate bottomRight)
{
	bounds.push_back(Wall(topLeft, bottomRight));
}
void World::createWall(int topleftx, int toplefty, int bottomrightx, int bottomrighty)
{
	createWall(Coordinate(topleftx, toplefty), Coordinate(bottomrightx, bottomrighty));
}

std::vector<Wall> World::getWalls() { return bounds; }
Coordinate World::getSize() { return worldSize; }

Coordinate World::spawnApple()
{
	srand(time(nullptr));

	int maxX = worldSize.x;
	int maxY = worldSize.y;
	Coordinate spawn(rand() % maxX, rand() % maxY);
	
	int flag = 0;
	while (!flag)
	{
		for (unsigned int i = 0; i < bounds.size(); i++)
		{
			if (bounds[i].isCollide(spawn)) { flag = 1; break; }
		}

		if (!flag) break;

		spawn.x = rand() % maxX + 1;
		spawn.y = rand() % maxY + 1;
	}
	std::cout << "Food spawn at: " << spawn.x << " " << spawn.y << std::endl;

	if (img_circle) appleShape.setPosition(spawn.x * gridSize, spawn.y * gridSize);
	else appleCircleShape.setPosition(spawn.x * gridSize, spawn.y * gridSize);

	return spawn;
}

void World::render(sf::RenderWindow& window)
{
	sf::RectangleShape worldShape;

	worldShape.setSize(sf::Vector2f(gridSize, gridSize));
	worldShape.setFillColor(sf::Color::Black);
	worldShape.setOutlineColor(sf::Color(52, 73, 94));
	worldShape.setOutlineThickness(0.5f);

	for (int i = 0; i < worldSize.x; i++)
		for (int j = 0; j < worldSize.y; j++)
		{
			worldShape.setPosition(gridSize * i, gridSize * j);
			
			window.draw(worldShape);
		}
	for (unsigned int i = 0; i < bounds.size(); i++)
	{
		wallShape.setFillColor(sf::Color::Red);
		wallShape.setSize(sf::Vector2f((bounds[i].bottomRight.x - bounds[i].topLeft.x) * gridSize, (bounds[i].bottomRight.y - bounds[i].topLeft.y) * gridSize));
		wallShape.setPosition(bounds[i].topLeft.x * gridSize, bounds[i].topLeft.y * gridSize);

		window.draw(wallShape);
	}
	if (img_circle) window.draw(appleShape);
	else window.draw(appleCircleShape);
}
