#include "Block.h"

Block::Block()
{
	this->type = BlockType::None;
}

void Block::createBlock(BlockType type, unsigned int lenX, sf::Color color, unsigned int grid)
{
	for (int i = 0; i < 4; i++)
	{
		if (i == 0)
			block[i].createPiece(sf::Vector2i(0, 0), true, color, grid);
		else
			block[i].createPiece(sf::Vector2i(0, 0), false, color, grid);
	}
	this->type = type;
	switch (type)
	{
	case BlockType::I:
	{
		block[0].setPosition(lenX / 2, 0 + 2);
		block[1].setPosition(lenX / 2 - 1, 0 + 2);
		block[2].setPosition(lenX / 2 + 1, 0 + 2);

		block[3].setPosition(lenX / 2 + 2, 0 + 2);
		break;
	}
	case BlockType::L:
	{
		block[0].setPosition(lenX / 2, 0 + 2);
		block[1].setPosition(lenX / 2 - 1, 0 + 2);
		block[2].setPosition(lenX / 2 + 1, 0 + 2);

		block[3].setPosition(lenX / 2 - 1, 1 + 2);
		break;
	}
	case BlockType::reverse_L:
	{
		block[0].setPosition(lenX / 2, 0 + 2);
		block[1].setPosition(lenX / 2 - 1, 0 + 2);
		block[2].setPosition(lenX / 2 + 1, 0 + 2);

		block[3].setPosition(lenX / 2 + 1, 1 + 2);
		break;
	}
	case BlockType::T:
	{
		block[0].setPosition(lenX / 2, 0 + 2);
		block[1].setPosition(lenX / 2 - 1, 0 + 2);
		block[2].setPosition(lenX / 2 + 1, 0 + 2);

		block[3].setPosition(lenX / 2, 1 + 2);
		break;
	}
	case BlockType::N:
	{
		block[0].setPosition(lenX / 2, 0 + 2);
		block[1].setPosition(lenX / 2 - 1, 0 + 2);

		block[2].setPosition(lenX / 2, 1 + 2);
		block[3].setPosition(lenX / 2 + 1, 1 + 2);
		break;
	}
	case BlockType::reverse_N:
	{
		block[0].setPosition(lenX / 2, 0 + 2);
		block[1].setPosition(lenX / 2 + 1, 0 + 2);

		block[2].setPosition(lenX / 2, 1 + 2);
		block[3].setPosition(lenX / 2 - 1, 1 + 2);
		break;
	}
	case BlockType::O:
	{
		block[0].setPosition(lenX / 2, 0 + 2);
		block[1].setPosition(lenX / 2 - 1, 0 + 2);

		block[2].setPosition(lenX / 2, 1 + 2);
		block[3].setPosition(lenX / 2 - 1, 1 + 2);
		break;
	}
	}
	
	for (unsigned int i = 0; i < 4; i++)
	{
		block[i].setColor(color);
	}
}

Block::~Block()
{
}
