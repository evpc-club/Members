#include "Piece.h"
#include <iostream>

Piece::Piece()
{
}

Piece::~Piece()
{
}

void Piece::createPiece(sf::Vector2i position, bool isCenter, sf::Color color, unsigned int grid)
{
	this->position = position;
	this->isCenter = isCenter;
	this->renderColor = color;
	this->grid = grid;
	isDrawing = false;
	isPlaced = false;
}

void Piece::setPosition(sf::Vector2i position) { this->position = position; }
void Piece::setPosition(unsigned int x, unsigned y) { this->position = sf::Vector2i(x, y); }

void Piece::render(sf::RenderWindow& window, bool enableOutline)
{
	isDrawing = true;
	renderShape.setSize(sf::Vector2f((float) grid - 1, (float) grid - 1));
	renderShape.setPosition((float) position.x * grid, (float) position.y * grid);
	renderShape.setFillColor(renderColor);
	if (enableOutline) { renderShape.setOutlineThickness(0.5f); renderShape.setOutlineColor(sf::Color(52, 73, 94)); }

	window.draw(renderShape);
	isDrawing = false;
}