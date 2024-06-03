# 10 Man Teams Discord Bot

## Description

The 10 Man Teams Discord Bot is a Python-based application developed to automate the creation and management of 10-man team games on Discord, a popular communication platform. It is specifically designed for competitive gaming scenarios where organizing and managing teams efficiently is crucial.

## Key Features

- **Automated Team Assignment**: The bot automatically assigns players to teams based on predefined criteria, facilitating fair and balanced team compositions.
- **Command Interface**: Users can interact with the bot through commands to start new games, manage team members, and access help information.
- **Real-Time Status Updates**: The bot provides real-time updates and manages activity within the Discord server, ensuring smooth communication and coordination among players.
  
## Technologies Used

- **Python**: The project is developed using the Python programming language.
- **discord.py**: The bot is built using the discord.py library, which provides an interface for interacting with the Discord API.
- **asyncio**: Asynchronous programming is utilized to handle concurrent tasks efficiently.

## Usage

To use the 10 Man Teams Discord Bot, follow these steps:

1. **Create a Config File**: Create a file named `config.ini` in the root directory of the project.

2. **Add Your Discord Token**: In the `config.ini` file, add the following lines:

    ```ini
    [Discord]
    TOKEN = your_discord_bot_token_here
    ```

    Replace `your_discord_bot_token_here` with your actual Discord bot token.

3. **Save the Config File**: Save the `config.ini` file.

## Contributing

If you'd like to contribute to the project, feel free to fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).
