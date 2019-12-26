#pragma once
#include "Block.h"
#include "SFML/Audio.hpp"
#include <string>


// Represent the tetris game.
// It has only 2 public methods: setSpeed() and loop().
// Note:
// - The coord of the screen and the coord of the array is inversed, so that's where getPiece() for.
// - Some parts have magic number; it is to save up some spaces either above the spawn point so if the player rotate the I at spawn point,
// it won't throw seg fault, or to display the hint. It is usually written in the form of (important_number <operator> magic_number)
// - If the magic number is 4, it's usually the size of the Block.block (Piece*).
class Tetris
{
public:
	Tetris(sf::Vector2i boardSize = sf::Vector2i(10, 24), int grid = 20);
	~Tetris();

	// Set the initial speed.
	void setSpeed(float speed) { this->speed = speed; }
	// Loop the game.
	void loop();
private:
	// Core

	Piece**             board;				// Represent the board.	
	sf::Vector2i        size;				// Size of the board. Warning: it is inversed to the real coord if you use for array.
	const int           nextBlockSpace = 6; // The space use to display the next block.
	float		    	speed;				// The falling speed.
	unsigned int	    point;				//

	State               gameState;			// Current game state.	
	Block               currentBlock;		// Current controlled block.
	Block		    	nextBlock;			// The next block.
	bool		    	isPaused;
	bool				isSlide;			// Allow sliding for a short moment.
	bool				canMove;			// Check if a piece can move down anymore.

	// Drawing

	int					grid;				// Grid size.
	sf::RenderWindow    window;
	sf::RectangleShape  boardShape;
	sf::Clock           clock;
	float				elapsed;

	sf::Music			music;				// Background music.
	sf::SoundBuffer		buffer;				// Buffer for sound.
	sf::Sound			sound;				// Sound.

	// Handle player input.
	void getInput();
	// Update the Block to the board.
	// Param:
	// block (Block&): the block you want to update.
	void integrate(Block& block);
	// Rotate the Block. This method should only be called in move().
	// This is act as a pseudo rotate. If it fails to rotate, it'll return true. If it success, then it'll update currentBlock and return false.
	// Param:
	// block (Block): the block you want to rotate.
	bool rotate(Block block);
	// Handle block movement.
	// Param:
	// block (Block): the block you want to move. Typically this->currentBlock.
	void move(Block block);
	// Clear the full lines.
	void clearLines();
	// Handle most action in the game.
	void update();
	// Draw the stuffs.
	void render();

	void playMusic(std::string musicName);

	// Utility

	// Return the corresponding Piece on the array according to the plane coordinate.
	// Avoid confusion when accessing and rendering and other stuffs.
	inline Piece& getPiece(int winColumn, int winRow) 
	{ 
		//if (winColumn < 0 || winColumn > size.y)
		return board[winRow][winColumn]; 
	}
};

