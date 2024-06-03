# 10 Man Teams Discord Bot

## Description

The 10 Man Teams Discord Bot is a versatile Python-based application designed to streamline the organization and management of 10-man team games within Discord communities. Tailored for competitive gaming environments, this bot automates the creation of balanced teams, facilitates real-time communication, and enhances overall gaming experience.

## Key Features

- **Automated Team Assignment**: The bot intelligently assigns players to teams based on predefined criteria, ensuring fairness and balance.
- **Command Interface**: With intuitive commands, users can easily initiate new games, manage team members, and access helpful information.
- **Real-Time Status Updates**: The bot provides timely updates and actively manages activity within Discord servers, fostering smooth communication and coordination among players.

## Technologies Used

- **Python**: The project is built using the Python programming language, leveraging its flexibility and robustness.
- **discord.py**: The bot is developed with the discord.py library, allowing seamless integration with Discord's API.
- **Asyncio**: Asynchronous programming techniques are utilized to handle concurrent tasks efficiently, optimizing performance.
- **ConfigParser**: The configparser library is used for parsing configuration files, facilitating easy retrieval of bot configuration settings.

## Usage

To use the 10 Man Teams Discord Bot, follow these steps:

1. **Install Required Packages**: 
   - Make sure you have Python installed on your system.
   - Clone this repository to your local machine.
   - Navigate to the root directory of the cloned repository.
   - Run the following command to install the required packages:
     ```
     pip install -r requirements.txt
     ```

2. **Configure Bot Token**:
   - Create a file named `config.ini` in the root directory of the project.
   - Add the following lines to `config.ini`, replacing `your_discord_bot_token_here` with your actual Discord bot token:
     ```
     [Discord]
     TOKEN = your_discord_bot_token_here
     ```

3. **Run the Bot**:
   - Run the `10manteams.py` script to start the bot:
     ```
     python 10manteams.py
     ```

4. **Interact with the Bot**:
   - Once the bot is running, you can interact with it using the specified commands in your Discord server.

## Contributing

If you'd like to contribute to the project, feel free to fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).
