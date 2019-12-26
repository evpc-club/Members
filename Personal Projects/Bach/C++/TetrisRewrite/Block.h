#pragma once
#include "Piece.h"

enum BlockType {N, L, reverse_N, reverse_L, T, I, O, None};

// A class represent a tetris block.
// In reality, this class only serve to organize and create block and has nothing related to the board.
// To implement the change of the block to the board, iterate through the getBlock().
class Block
{
public:
	Block();
	~Block();

	// The block type.
	BlockType type;

	// Create a block. This is used instead of the constructor for multiple uses.
	// Param:
	// type (BlockType): the block type.
	// lenX (unsigned int): the horizontal length of the place you want to spawn. Internally the spawnX will be at lenX / 2.
	// color (sf::Color): render color. Default as sf::Color::Blue.
	// grid (unsigned int): the grid size. Default as 15.
	void createBlock(BlockType type, unsigned int lenX, sf::Color color = sf::Color::Blue, unsigned int grid = 15);
	// Return: the internal array of Piece.
	// Return type: Piece*(size = 4).
	Piece* getBlock() { return block; }
private:
	Piece block[4];
};

