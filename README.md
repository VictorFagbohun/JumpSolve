# JumpSolve - Math Platformer

A fun platformer game where you solve math problems to upgrade your jump power! Built with Python and Pygame, now ready for web deployment with pygbag.

## Game Features

- **Three Difficulty Levels**: Easy, Medium, and Hard
- **Math Integration**: Solve problems to upgrade your jump power
- **Progressive Difficulty**: Gaps increase as you progress
- **Beautiful Graphics**: Animated sprites and smooth gameplay
- **Music & Sound**: Background music for immersive experience

## Controls

- **A/D**: Move left/right
- **SPACE**: Jump
- **R**: Restart (when game over)
- **Mouse**: Select difficulty in menu

## Local Development

1. Install Python 3.8+ and pip
2. Install dependencies:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Web Deployment with pygbag

### Prerequisites

1. Install pygbag:
   ```bash
   pip install pygbag
   ```

### Building for Web

1. Navigate to the JumpSolve directory
2. Build the web version:
   ```bash
   pygbag .
   ```

3. For production build:
   ```bash
   pygbag . --build
   ```

### Testing Locally

After building, you can test the web version locally:
```bash
pygbag . --serve
```

The game will be available at `http://localhost:8000`

## Deploying to itch.io

### Method 1: Using itch.io Butler (Recommended)

1. Install [itch.io Butler](https://itch.io/docs/butler/)
2. Create a new project on itch.io
3. Build your game:
   ```bash
   pygbag . --build
   ```
4. Upload using Butler:
   ```bash
   butler push build/ your-username/your-game-name:html5
   ```

### Method 2: Manual Upload

1. Build the game:
   ```bash
   pygbag . --build
   ```
2. Zip the contents of the `build/` directory
3. Upload the zip file to itch.io as an HTML5 game

### itch.io Project Settings

When creating your itch.io project:

- **Kind**: HTML
- **Uploads**: Upload the built files or use Butler
- **Embed**: Use the provided embed code
- **Platforms**: HTML5

## File Structure

```
JumpSolve/
├── main.py              # Main game loop (async-ready)
├── menu.py              # Menu system (async-ready)
├── question.py          # Question system (async-ready)
├── settings.py          # Game settings
├── pygbag.toml         # pygbag configuration
├── index.html           # Custom HTML template
├── assets/              # Game assets (sprites, backgrounds)
├── json/                # Question data
├── music/               # Audio files
└── QuestionBank/        # Question images
```

## Troubleshooting

### Common Issues

1. **Game not loading**: Check browser console for errors
2. **Assets not loading**: Ensure all files are included in pygbag.toml
3. **Performance issues**: Try reducing game resolution in settings.py

### Browser Compatibility

The game works best in:
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

### Mobile Support

The game is designed for desktop but can work on mobile with touch controls (may need additional development).

## Development Notes

- The game has been converted to use asyncio for web compatibility
- All game loops now yield control to the event loop
- Audio and input handling are web-compatible
- File loading uses relative paths compatible with web deployment

## License

This project is open source. Feel free to modify and distribute according to your needs. 