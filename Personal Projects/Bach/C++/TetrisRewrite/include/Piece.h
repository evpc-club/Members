#pragma once
#include <SFML/Graphics.hpp>
#include "Util.h"

// Represent a piece in the tetris block.
class Piece
{
public:
	Piece();
	~Piece();
	bool isCenter;
	bool isPlaced;


	// Create a piece. This is used instead of the constructor for multiple uses.
	// Param:
	// position (sf::Vector2i): the position of the piece. Default at (0, 0).
	// isCenter (bool): whether or not this is the center of the block. Default as false.
	// color (sf::Color): the color of the piece. Default as sf::Color::Blue.
	// grid (unsigned int): the grid size. Default as 15.
	void createPiece(sf::Vector2i position = sf::Vector2i(0, 0), bool isCenter = false, sf::Color color = sf::Color::Blue, unsigned int grid = 15);

	// Return: the position of the piece.
	// Return type: sf::Vector2i.
	sf::Vector2i getPosition() { return position; }

	// Set the position of the piece.
	// Param:
	// position (sf::Vector2i): the position you want to set.
	void setPosition(sf::Vector2i position);
	// Set the position of the piece.
	// Param:
	// x (unsigned int): the x-pos you want to set.
	// y (unsigned int): the y-pos you want to set.
	void setPosition(unsigned int x, unsigned int y);


	// A check if the piece is still drawing.
	bool isDrawing;

	// Return: the color of the piece.
	// Return type: sf::Color.
	sf::Color getColor() { return renderColor; }

	// Set the color for the piece.
	// Param:
	// color (sf::Color): the color you want to set.
	void setColor(sf::Color color) { renderColor = color; }

	// Render the piece.
	// Param:
	// window (sf::RenderWindow&): the window you want to render in.
	// enableOutline (bool): whether or not to draw the outline.
	void render(sf::RenderWindow& window, bool enableOutline);

private:
	// Core

	// Position of the piece.
	sf::Vector2i position;

	// Drawing
	
	unsigned int grid;
	sf::Color renderColor;
	sf::RectangleShape renderShape;
};

