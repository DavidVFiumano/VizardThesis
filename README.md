# Vizard Coin Collection Game

To run this game, you must first install Vizard 7, 64-bit on your computer. See the instructions below.

## Vizard 7 Installation Instructions

This guide will help you install Vizard 7 on your system. You can download the installer from the following link: [Vizard 7 Installer](https://app.worldviz.com/download/vizard7_64)

### Prerequisites

- Windows 7, 8, 10 or 11 (64-bit)
- Graphics card with DirectX 11 support
- Microsoft Visual C++ 2015 Redistributable (x64) - [Download Link](https://www.microsoft.com/en-us/download/details.aspx?id=48145)
- Git Bash - [Download Link](https://git-scm.com/downloads)
- Git Large File Storage - [Download Link](https://git-lfs.com/)

### Installation Steps

1. **Download the installer:** Click the following link to download the Vizard 7 installer: [Vizard 7 Installer](https://app.worldviz.com/download/vizard7_64)

2. **Run the installer:** Once the download is complete, locate the downloaded file (usually in your Downloads folder) and double-click on it to start the installation process.

   ```
   vizard7_64.exe
   ```

3. **Accept the license agreement:** Read the license agreement, check the "I accept the agreement" checkbox, and click "Next".

4. **Choose the installation folder:** Select the destination folder where you want to install Vizard 7. By default, it will be installed in `C:\Program Files\WorldViz\Vizard`. You can change this by clicking "Browse" and selecting a different folder. Click "Next" to continue.

5. **Select components:** Choose the components you want to install. By default, all components will be selected. You can deselect any components you do not need. Click "Next" to continue.

6. **Create a desktop shortcut (optional):** Check the "Create a desktop shortcut" checkbox if you want to create a shortcut on your desktop for easier access. Click "Next" to continue.

7. **Start the installation:** Review your installation settings, and click "Install" to begin the installation process.

8. **Wait for the installation to complete:** The installation process may take a few minutes. Once it's complete, click "Finish" to close the installer.

9. **Launch Vizard 7:** Double-click on the Vizard 7 desktop shortcut or find Vizard 7 in your Start menu to launch the application.

You have now successfully installed Vizard 7 on your system.

## Running the Coin Collection Game

After you have installed Vizard 7, follow these steps to run the Coin Collection Game:

1. **Download or clone the repository:** Open git bash where you want to download the game and use `git clone` to clone the repository onto your local system.

   ```
   git clone https://github.com/DavidVFiumano/VizardThesis.git
   ```

2. **Download the Assets Folder:** We use git lfs to store the asset files. To download them, make sure git lfs is accessible from git bash. If you haven't done this before, you can run the following command from the git bash window you opened earlier.

   ```
   git lfs install
   ```

   After ensuring git lfs is installed, you can fetch the assets by running git lfs fetch.

  ```
  git lfs fetch --all
  ```

3. **Open the Vizard IDE:** Launch the Vizard IDE by double-clicking the Vizard 7 desktop shortcut or finding it in your Start menu.

4. **Open the game project:** In the Vizard IDE, click on `File` > `Open` from the top menu. Navigate to the folder where you downloaded or cloned the game repository, and open the `main.py` file.

5. **Run the game:** Press the `F5` key or click on the `Run` button in the Vizard IDE to start the game. The game window should open.

6. **Select a save directory:** The game will prompt you to select a save directory. You can create a new directory or choose any empty directory on your system. This is where the game will save data for analysis later. Pressing cancel at this stage will close the game window.

7. **Start the game:** Press `F` to begin playing the Coin Collection Game. Collect coins and enjoy!

8. **Ending the game:** The game ends if the player runs out of time, the player collects all the coins, or the player is caught by a robot. When the game ends, press 'Esc' to close the window.

The game will automatically save data into the selected directory for later analysis.

## How to Play the Coin Collection Game

The goal of the Coin Collection Game is to collect as many coins as possible within the given time limit while avoiding being caught by robots.

### Game Rules

1. **Collect coins:** Navigate through the game environment and collect coins to increase your score.
2. **Timer:** The game features a timer, which adds an element of urgency. Try to collect coins as fast as possible before the timer runs out.
3. **Robots:** Beware of the robots! If a robot catches you, the game ends.
4. **Game over:** The game ends when you collect all the coins, the timer runs out, or a robot catches you.

### Controls

Use the following controls to navigate the game environment:

- **Move forward:** Press `W`
- **Move left:** Press `A`
- **Move right:** Press `D`
- **Move backward:** Press `S`

Use the left and right arrow keys to look left and right:

- **Look left:** Press the `Left Arrow` key
- **Look right:** Press the `Right Arrow` key

After the data is over, analyze the game results.

## Analyzing Game Results

After playing the Coin Collection Game, you can analyze the results using the data saved in three different CSV files. Each file provides specific information about different aspects of the game. These files are saved in the save directory you selected.

### 1. FrameLog.csv

The `FrameLog.csv` file records player position and movement information for every frame during the game. This data can be used to analyze player movement patterns, for example: analyzing when players start to flee from the robots.

### 2. CollectiblesLog.csv

The `CollectiblesLog.csv` file logs when players collect coins during the game. This data helps you track coin collection progress, analyze the order in which coins were collected, and determine how much time it took for the player to collect each coin.

### 3. PathfollowerBotsLog.csv

The `PathfollowerBotsLog.csv` file provides information about the robots' interactions with the player. This file logs when the robots see the players, chase the players, lose sight of the players, and the reasons behind those events. The reasons can include losing sight of the player, hearing the player, etc. Comparing this data with the data in FrameLog.csv can help you understand how the robots' behavior affects the player's behavior.

### Custom Logging

More loggers with more file formats (not just CSV) can be added as needed.