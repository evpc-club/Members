#include "Game.h"
#include <iostream>

int main()
{
	Game game(15, 10.5f, Coordinate(5, 5), Coordinate(300, 300)); // grid, speed, spawn, map size.
	while (!game.GetWindow()->IsDone())
	{
		game.getInput();
		game.Update();
		game.Render();
		game.RestartClock();
	}
}