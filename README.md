<img src="https://github.com/DouglasTaylorSupportGroup/EinsteinBot/blob/master/banner.png" alt="EinsteinBot Logo" width="410" />

# 🤖 A Discord bot that displays homework solutions from Chegg.com in a text channel.

> **Disclamer**: We are not responsible for any problems that may occur with this bot. This includes but is not limited to: support for building/making the bot or banned accounts. We will however respond to any **bugs/problems with the bot itself sending Chegg solutions**.

EinsteinBot is a service that creates a super easy way to share Chegg answers with others using a Discord Bot. It only requires one Chegg account and everyone can use Chegg's service using the account. You only need the Chegg link, and EinsteinBot will send the solution provided by Chegg in the text channel.

EinsteinBot is pretty easy to deploy. Everything is open-source and free to use (except for the Chegg service itself, you will need your own account).

## 📝 Commands

- `help`: Displays all commands of the bot.
- `ping`: Pong! Displays the ping of the bot.
- `source`: Displays the bot's GitHub repository.
- `search <url>` : Searches for the solution of a problem from Chegg.

## 🔨 Setup

### Requirements

- A Discord account.
- A Chegg account that has a paid subscription.
- A computer that has Python 3.8 or higher (from [python.org](https://www.python.org/), not from Windows Store) installed.

### Main Setup

> **Note**: You will need to do all of these setup steps (Preferably in order).

#### Discord Bot Creation Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications/) website and create a new application by clicking on **New Application**.
2. After creating the application, click the application and copy the `Application ID` by clicking on **Copy** and save it for later.
2. Then on the left sidebar, click **Bot**.
3. Create a new bot by clicking on **Add Bot**.
4. Copy the `token` of the bot by clicking on **Copy** and save it for later.

#### Chegg Setup

1. Download a web browser extension that allows you to download cookies.
    - Chrome: [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)
    - Firefox: [Cookie-Editor](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
2. Go to [Chegg.com](https://www.chegg.com/) and sign in.
3. At the home page, click the browser extension downloaded in Step 1. Then click the button that says **Export**. Copy the cookies and paste them into a .txt file named `cookie.txt`. 
4. Get your user agent by going to a website called [WhatMyUserAgent](https://whatmyuseragent.com/). We will only need the user agent from this site. Save this user agent somewhere as it is going to be used later.

#### Bot Setup

1. Clone this repository.
2. Go into the folder that you cloned and create a new file called `config.json`.
3. Copy the following into the file:
```json
{
    "prefix": "THE BOTS PREFIX GOES HERE (ANYTHING YOU WANT)",
    "token": "THE BOTS TOKEN GOES HERE (NOT THE CLIENT ID)",
    "userAgent": "YOUR USER AGENT GOES HERE (REFER TO STEP 4 FROM CHEGG SETUP)"
}
```
4. Copy the `cookie.txt` file from step 3 of Chegg Setup into the folder that you cloned.
5. Thats it! Run the bot in your command line from the folder you cloned using:
```bash
python -u bot.py
```
6. You can invite the bot by putting your client id/application id in this link where it says `YOURAPPIDHERE` (this link already has all the permissions needed for the bot): https://discord.com/oauth2/authorize?client_id=YOURAPPIDHERE&scope=applications.commands%20bot&permissions=139586751552