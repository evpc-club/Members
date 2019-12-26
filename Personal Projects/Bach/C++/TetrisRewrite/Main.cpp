#include "Tetris.h"

int main()
{
	Tetris game (sf::Vector2i(10, 24), 20);
	game.setSpeed(5.0f);
	game.loop();
	return 0;
}