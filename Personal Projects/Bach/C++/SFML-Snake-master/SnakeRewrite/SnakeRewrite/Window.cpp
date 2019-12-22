#include "Window.h"

Window::Window() { SetupWinInfo("Window", sf::Vector2u(1920, 1000)); }
Window::Window(const std::string& title, const sf::Vector2u& size)
{
	SetupWinInfo(title, size);
}
Window::~Window() { DestroyWindow(); }

void Window::SetupWinInfo(const std::string& title, const sf::Vector2u& size)
{
	m_windowTitle = title;
	m_windowSize = size;
	m_isFullScreen = false;
	m_isDone = false;
	CreateWindow();
}

void Window::CreateWindow()
{
	sf::Uint32 style;
	if (m_isFullScreen) style = sf::Style::Fullscreen;
	else style = sf::Style::Default;
	m_window.create(sf::VideoMode(m_windowSize.x, m_windowSize.y), m_windowTitle, style);
}

void Window::DestroyWindow()
{
	m_window.close();
}

void Window::Update()
{
	sf::Event event;
	while (m_window.pollEvent(event))
	{
		switch (event.type)
		{
		case sf::Event::Closed:
		{
			m_isDone = true;
			break;
		}
		case sf::Event::KeyPressed:
		{
			switch (event.key.code) 
			{
				case sf::Keyboard::F5:
				{
					ToggleFullScreen();
					break;
				}
				case sf::Keyboard::Escape:
				{
					m_isDone = true;
					break;
				}
			}
		}
		}
	}
}

void Window::ToggleFullScreen()
{
	m_isFullScreen = !m_isFullScreen;
	DestroyWindow();
	CreateWindow();
}

void Window::BeginDraw() { m_window.clear(sf::Color::Black); }
void Window::EndDraw() { m_window.display(); }

bool Window::IsDone() { return m_isDone; }
bool Window::IsFullScreen() { return m_isFullScreen; }
sf::Vector2u Window::GetWindowSize() { return m_windowSize; }
void Window::Draw(sf::Drawable& drawable) { m_window.draw(drawable); }
sf::RenderWindow& Window::getRenderWindow() { return m_window; }