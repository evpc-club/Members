#include "Tetris.h"
#include <iostream>
#include <thread>


Tetris::Tetris(sf::Vector2i boardSize, int grid)
{
	boardSize.x += 2; // Side border include.
	boardSize.x += nextBlockSpace; // Next block include.
	boardSize.y += 2; // 2 spaces above the spawn point.
	boardSize.y += 1; // Bottom border include.

	window.create(sf::VideoMode(boardSize.x * grid, boardSize.y * grid), "Tetris");
	this->grid = grid;

	size = boardSize;
	// This will create a y * x array, with y as row so it looks alike in the game.
	board = new Piece*[boardSize.y];
	for (int i = 0; i < boardSize.y; i++)
		board[i] = new Piece[boardSize.x];

	// Iterate through the row
	for (int i = 0; i < boardSize.y; i++)
	{
		// Iterate through the column
		for (int j = 0; j < boardSize.x; j++)
		{
			if (j == 0 || j == boardSize.x - (1 + nextBlockSpace) || (i == boardSize.y - 1 && j <= boardSize.x - (1 + nextBlockSpace))) // Magic number? Look at line 9.
			{
				board[i][j].createPiece(sf::Vector2i(j, i), false, sf::Color::White, grid);
				board[i][j].isPlaced = true;
			}
			else
			{
				board[i][j].createPiece(sf::Vector2i(j, i), false, sf::Color::Transparent, grid);
			}

		}
	}

	clock.restart();
	elapsed = 0.0f;
	canMove = false;
	isPaused = false;
	isSlide = false;
	gameState = State::Down;
}

Tetris::~Tetris()
{
	for (int i = 0; i < size.y; i++)
	{
		delete[] board[i];
	}
	delete[] board;
}

void Tetris::getInput()
{
	sf::Event event;
	if (window.pollEvent(event))
	{
		if (event.type == sf::Event::Closed || (event.type == sf::Event::KeyPressed && event.key.code == sf::Keyboard::Escape))
		{
			window.close();
		}
		else if (event.type == sf::Event::KeyPressed)
		{
			switch (event.key.code) {
			case sf::Keyboard::A:
			{
				gameState = State::Left;
				break;
			}
			case sf::Keyboard::D:
			{
				gameState = State::Right;
				break;
			}
			case sf::Keyboard::Left:
			{
				gameState = State::LeftTurn;
				break;
			}
			case sf::Keyboard::Right:
			{
				gameState = State::RightTurn;
				break;
			}
			case sf::Keyboard::Space:
			{
				gameState = State::DownFast;
				break;
			}
			case sf::Keyboard::P:
			{
				gameState = State::None;
				isPaused = !isPaused;
				if (isPaused) music.pause();
				else music.play();
				break;
			}

			}
		}
	}
}

void Tetris::integrate(Block& block)
{
	for (int i = 0; i < 4; i++)
	{
		int aX = block.getBlock()[i].getPosition().y;
		int aY = block.getBlock()[i].getPosition().x;
		board[aX][aY] = block.getBlock()[i];
	}
}

bool Tetris::rotate(Block block)
{
	Piece* pieces = block.getBlock();

	// No need to rotate a square.
	if (block.type == BlockType::O) return false;

	bool fail = false;

	if (gameState == State::LeftTurn)
	{

		for (unsigned int i = 1; i < 4; i++) // The first one is the center so it does not move anywhere.
		{
			int x0 = pieces[0].getPosition().x;
			int y0 = pieces[0].getPosition().y;

			int x1 = pieces[i].getPosition().x;
			int y1 = pieces[i].getPosition().y;

			// Math stuffs
			int x2 = x1 + ((x0 - x1) - (y0 - y1)); // Short form: x2 = x0 - y0 + y1
			int y2 = y1 + ((y0 - y1) - (x1 - x0)); // Short form: y2 = y0 - x1 + x0

			if (y2 < 0 || y2 > size.y - 2) fail = true; // - 2 because size.y count from 1 (which minus 1), and then exclude the bottom border (another 1).
			else if (x2 < 1 || x2 > size.x - (1 + nextBlockSpace)) fail = true;
			else if (board[y2][x2].isPlaced) fail = true;
			else
			{
				// We need to save the color information. These should not be altered.
				sf::Color color = pieces[i].getColor();
				pieces[i] = board[y2][x2];
				pieces[i].setColor(color);
				continue;
			}

			if (fail)
			{
				return fail;
			}
		}
	}
	else
	{
		for (unsigned int i = 1; i < 4; i++) // The first one is the center so it does not move anywhere.
		{
			int x0 = pieces[0].getPosition().x;
			int y0 = pieces[0].getPosition().y;

			int x1 = pieces[i].getPosition().x;
			int y1 = pieces[i].getPosition().y;

			// Math stuffs
			int x2 = x1 + ((y0 - y1) - (x1 - x0));
			int y2 = y1 + ((x1 - x0) - (y1 - y0));

			bool fail = false;
			if (y2 < 0 || y2 > size.y - 2) fail = true; // - 2 because size.y count from 1 (which minus 1), and then exclude the bottom border (another 1).
			else if (x2 < 1 || x2 > size.x - (1 + nextBlockSpace)) fail = true;
			else if (board[y2][x2].isPlaced) fail = true;
			else
			{
				// We need to save the color information. These should not be altered.
				sf::Color color = pieces[i].getColor();
				pieces[i] = board[y2][x2];
				pieces[i].setColor(color);
				continue;
			}

			if (fail)
			{
				return fail;
			}
		}
	}

	if (!fail)
	{
		currentBlock = block;
		return fail;
	}
}

void Tetris::move(Block block)
{
	if (isPaused) return;

	// Make a copy of block so we can clear all the old places of the old position before drawing the new one.
	Block copyBlock(block);

	// If one of the block is drawing, then we shouldn't allow to move at all.
	for (int i = 0; i < 4; i++)
		if (block.getBlock()[i].isDrawing) return;
	
	Piece* pieces = block.getBlock();

	bool fail = true;

	// State::...Turn is also included in Left and Right because if it fails to rotate (due to isPlaced or border),
	// then it can move left/right to continue to do that. A fail counter is there to prevent from trying too many times.
	// Refer to the comments in State::Left to know more.
	if (gameState == State::Left || gameState == State::RightTurn || gameState == State::LeftTurn)
	{
		// Try rotating
		if (gameState == State::RightTurn || gameState == State::LeftTurn) 
			fail = rotate(block);
		// If it fail to rotate block.
		int fail_count = 0;
		while (fail)
		{
			fail_count++;
			// If the block fail to rotate the block, then it'll try to move to a different direction.
			for (int i = 0; i < 4; i++)
			{
				int aX = pieces[i].getPosition().y;
				int aY = pieces[i].getPosition().x;
				if (board[aX][aY - 1].isPlaced == false)
				{
					// We need to save the color and the center information. These should not be altered.
					sf::Color color = pieces[i].getColor();
					bool isCenter = pieces[i].isCenter;
					pieces[i] = board[aX][aY - 1];
					pieces[i].setColor(color);
					pieces[i].isCenter = isCenter;

					fail = false;
				}
				else
				{
					fail = true;
					block = copyBlock;
				}
				// If it fails to move to a new location, then it's fail.
				if (fail) break;
			}

			// If the block fails to move to a new location, no rotation can be made.
			if (fail) break;

			if (fail_count > 4) break;

			// Try rotating again.
			if (gameState == State::RightTurn || gameState == State::LeftTurn)
				fail = rotate(block);
		}
	}
	if (gameState == State::Right || 
		((gameState == State::LeftTurn || gameState == State::RightTurn) && fail)) // This line indicate if moving left doesn't
																				   // solve the rotate, then try to move right.
	{
		if (gameState == State::LeftTurn || gameState == State::RightTurn) 
			fail = rotate(block);
		// If it fail to rotate block.
		int fail_count = 0;
		while (fail)
		{
			fail_count++;
			for (int i = 0; i < 4; i++)
			{
				int aX = pieces[i].getPosition().y;
				int aY = pieces[i].getPosition().x;
				if (board[aX][aY + 1].isPlaced == false)
				{
					// We need to save the color and the center information. These should not be altered.
					sf::Color color = pieces[i].getColor();
					bool isCenter = pieces[i].isCenter;
					pieces[i] = board[aX][aY + 1];
					pieces[i].setColor(color);
					pieces[i].isCenter = isCenter;

					fail = false;
				}
				else
				{
					fail = true;
					block = copyBlock;
				}
				if (fail) break;
			}
			if (fail) break;

			if (fail_count > 4) break;

			if (gameState == State::LeftTurn || gameState == State::RightTurn)
				fail = rotate(block);
		}
	}
	else if (gameState == State::DownFast)
	{
		bool fail = false;
		while (!fail)
		{
			for (int i = 0; i < 4; i++)
			{
				int aX = pieces[i].getPosition().y;
				int aY = pieces[i].getPosition().x;
				if (board[aX + 1][aY].isPlaced == false)
				{
					// We need to save the color and the center information. These should not be altered.
					sf::Color color = pieces[i].getColor();
					bool isCenter = pieces[i].isCenter;
					pieces[i] = board[aX + 1][aY];
					pieces[i].setColor(color);
					pieces[i].isCenter = isCenter;
					fail = false;
				}
				else
				{
					fail = true;
					for (int j = i - 1; j >= 0; j--)
					{
						int aX = pieces[j].getPosition().y;
						int aY = pieces[j].getPosition().x;

						sf::Color color = pieces[j].getColor();
						bool isCenter = pieces[j].isCenter;
						pieces[j] = board[aX - 1][aY];
						pieces[j].setColor(color);
						pieces[j].isCenter = isCenter;
					}
				}
				if (fail) break;
			}
		}
	}

	// currentBlock is updated in rotate().
	if (gameState == State::LeftTurn || gameState == State::RightTurn)
		block = currentBlock;

	gameState = State::Down;

	for (int i = 0; i < 4; i++)
	{
		bool fail = false;
		int aX = pieces[i].getPosition().y;
		int aY = pieces[i].getPosition().x;
		if (board[aX + 1][aY].isPlaced == false)
		{
			// We need to save the color and the center information. These should not be altered.
			sf::Color color = pieces[i].getColor();
			bool isCenter = pieces[i].isCenter;
			pieces[i] = board[aX + 1][aY];
			pieces[i].setColor(color);
			pieces[i].isCenter = isCenter;
		}
		else
		{
			fail = true;
			for (int j = i - 1; j >= 0; j--)
			{
				int aX = pieces[j].getPosition().y;
				int aY = pieces[j].getPosition().x;

				sf::Color color = pieces[j].getColor();
				bool isCenter = pieces[j].isCenter;
				pieces[j] = board[aX - 1][aY];
				pieces[j].setColor(color);
				pieces[j].isCenter = isCenter;
			}
		}
		if (fail) break;
	}
	
	currentBlock = block;

	// First we clear the old position
	for (int i = 0; i < 4; i++)
	{
		copyBlock.getBlock()[i].setColor(sf::Color::Transparent);
		copyBlock.getBlock()[i].isCenter = false;
		integrate(copyBlock);
	}
	// Then we draw the new position
	for (int i = 0; i < 4; i++)
	{
		integrate(currentBlock);
	}
}

void Tetris::clearLines()
{
	int* fullLines = new int[4]; // The largest row someone can delete in a row is 4.
	int index = 0;
	for (int aX = 0; aX < size.y - 1; aX++) // Bottom border excluded.
	{
		bool isFull = true;
		for (int aY = 0; aY < size.x - nextBlockSpace; aY++)
		{
			if (!board[aX][aY].isPlaced) 
			{ 
				isFull = false; break; 
			}
		}
		if (isFull)
		{
			fullLines[index] = aX;
			index++;
		}
	}

	if (index > 0)
	{ 
		for (int i = 0; i < index; i++)
		{
			for (int aY = 1; aY < size.x - (1 + nextBlockSpace); aY++) // Side borders excluded.
			{
				for (int aX = fullLines[i]; aX > 1; aX--)
				{
					board[aX][aY].createPiece(
						board[aX][aY].getPosition(), 
						board[aX - 1][aY].isCenter, 
						board[aX - 1][aY].getColor(), 
						grid
					);
					board[aX][aY].isPlaced = board[aX - 1][aY].isPlaced;
				}
			}
			point += 100;
		}

		if (index == 4)
		{
			if (!buffer.loadFromFile("./Music/line4.wav"))
			{
				std::cout << "Tetris sound not found" << std::endl;
			}
			else
			{
				sound.setBuffer(buffer);
				sound.play();
			}
		}
		else
		{
			if (!buffer.loadFromFile("./Music/line.wav"))
			{
				std::cout << "Line sound not found" << std::endl;
			}
			else
			{
				sound.setBuffer(buffer);
				sound.play();
			}
		}
	}
}

void Tetris::update()
{
	if (gameState == State::Lose) return;

	float timestep = 1.0f / speed;
	elapsed += clock.restart().asSeconds();

	if (elapsed >= timestep)
	{
		if (!canMove)
		{
			srand(time(NULL));
			for (int i = 0; i < 2; i++)
			{
				BlockType blocktype;
				sf::Color blockcolor;

				switch (rand() % 7)
				{
				case 0:
					blocktype = BlockType::I;
					blockcolor = sf::Color(19, 141, 117);
					break;
				case 1:
					blocktype = BlockType::L;
					blockcolor = sf::Color(243, 156, 18);
					break;
				case 2:
					blocktype = BlockType::N;
					blockcolor = sf::Color::Red;
					break;
				case 3:
					blocktype = BlockType::O;
					blockcolor = sf::Color::Yellow;
					break;
				case 4:
					blocktype = BlockType::reverse_L;
					blockcolor = sf::Color::Blue;
					break;
				case 5:
					blocktype = BlockType::reverse_N;
					blockcolor = sf::Color::Green;
					break;
				case 6:
					blocktype = BlockType::T;
					blockcolor = sf::Color(142, 68, 173);
					break;
				}

				if (i == 0)
				{
					if (nextBlock.type == BlockType::None)
					{
						currentBlock.createBlock(blocktype, size.x - nextBlockSpace, blockcolor, grid);
						gameState = State::None;
						isPaused = true;
					}
					else
					{
						currentBlock.createBlock(
							nextBlock.type,
							size.x - nextBlockSpace,
							nextBlock.getBlock()[i].getColor(),
							grid
						);

						// Check if lost.
						for (int i = 0; i < 4; i++)
						{
							if (board[currentBlock.getBlock()[i].getPosition().y][currentBlock.getBlock()[i].getPosition().x].isPlaced)
							{
								music.stop();
								if (!buffer.loadFromFile("./Music/gameover.wav"))
								{
									std::cout << "Can't load game over sound." << std::endl;
								}
								else
								{
									sound.setBuffer(buffer);
									sound.play();
								}
								std::cout << "You lose!" << std::endl;
								std::cout << "Press ESC or close the window." << std::endl;
								gameState = State::Lose;
								return;
							}
						}
					}
				}
				else
				{
					// Clear the old next block.
					for (int i = 0; i < 4; i++)
					{
						board[nextBlock.getBlock()[i].getPosition().y][nextBlock.getBlock()[i].getPosition().x].setColor(sf::Color::Transparent);
						board[nextBlock.getBlock()[i].getPosition().y][nextBlock.getBlock()[i].getPosition().x].isCenter = false;
					}

					nextBlock.createBlock(blocktype, size.x - (size.x - nextBlockSpace), blockcolor, grid);
					for (int i = 0; i < 4; i++)
					{
						nextBlock.getBlock()[i].setPosition(
							nextBlock.getBlock()[i].getPosition().x + (size.x - nextBlockSpace), 
							nextBlock.getBlock()[i].getPosition().y + 2
						);
					}
				}

			}

			integrate(currentBlock);
			integrate(nextBlock);
			canMove = true;
		}
		else
		{
			move(currentBlock);

			for (int i = 0; i < 4; i++)
			{
				int aX = currentBlock.getBlock()[i].getPosition().y;
				int aY = currentBlock.getBlock()[i].getPosition().x;
				if (board[aX + 1][aY].isPlaced)
				{
					if (isSlide) { canMove = false; isSlide = false; break; }
					else { isSlide = true; break; }
				}
			}

			if (!canMove)
			{
				for (int i = 0; i < 4; i++)
				{
					currentBlock.getBlock()[i].isPlaced = true;
				}

				integrate(currentBlock);

				if (!buffer.loadFromFile("./Music/fall.wav"))
				{
					std::cout << "Failed to load fall.wav" << std::endl;
				}
				else
				{
					sound.setBuffer(buffer);
					sound.play();
				}

				int prepoint = point;

				clearLines();
				
				// If there's a change in the point then increase the speed.
				// This encourage people to snap more 4 rows at a time to gain more points before it gets harder.
				if (point != prepoint)
				{
					speed += 0.01f;
					std::cout << "Point: " << point << std::endl;
				}
			}

		}

		elapsed -= timestep;
	}
}

void Tetris::render()
{
	window.clear(sf::Color::Black);
	for (int i = 2; i < size.y; i++) // Ignore the first 2 spaces.
	{
		for (int j = 0; j < size.x; j++)
		{
			board[i][j].render(window, true);
		}
	}
	window.display();
}

void Tetris::playMusic(std::string musicName)
{
	if (!music.openFromFile("./Music/" + musicName + ".ogg"))
	{
		std::cout << "Music not found" << std::endl;
		return;
	}
	music.setVolume(50.0f);
	music.setLoop(true);
	music.play();
}

void Tetris::loop()
{
	std::cout << "Introduction:" << std::endl;
	std::cout << "Welcome to the good old Tetris game but rewritten by SFML." << std::endl;
	std::cout << std::endl;
	std::cout << "Instruction:" << std::endl;
	std::cout << "- A key: move left" << std::endl;
	std::cout << "- D key: move right" << std::endl;
	std::cout << "- Left Arrow key: rotate left" << std::endl;
	std::cout << "- Right Arrow key: rotate right" << std::endl;
	std::cout << "- P key: pause/resume" << std::endl;
	std::cout << "The game is pausing. Press P to start!" << std::endl;
	std::cout << "Enjoy!" << std::endl;

	playMusic("Tetris"); // Available music: 1UP, Tetris.

	while (window.isOpen())
	{
		getInput();
		update();
		render();
	}
}