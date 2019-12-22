#pragma once
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>

class Window
{
public:
	Window();
	Window(const std::string& title, const sf::Vector2u& size);
	~Window();

	void BeginDraw(); // Clear window
	void EndDraw(); // Display the changes

	void Update();

	bool IsDone();
	bool IsFullScreen();
	sf::Vector2u GetWindowSize();
	sf::RenderWindow& getRenderWindow();

	void ToggleFullScreen();

	void Draw(sf::Drawable& drawable);

private:
	void SetupWinInfo(const std::string& title, const sf::Vector2u& size);
	void DestroyWindow();
	void CreateWindow();

	sf::RenderWindow m_window;
	sf::Vector2u m_windowSize;
	std::string m_windowTitle;
	bool m_isDone;
	bool m_isFullScreen;
};

