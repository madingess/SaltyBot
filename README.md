# SaltyBot

A bot for automated betting at saltybet.com.

I am not responsible if your account gets banned.

## Setup
Run the following commands to start the bot. The first line only needs to be run once.
```commandline
pip3 install -r requirements.txt
python3 main.py
```

## Configuration
Replace the following with your account information.
```yaml
# User Credentials
email: email@domain.com
username: user
password: pass
```

Choose a wager strategy and make configurations related to the chosen strategy
```yaml
# Strategy to use when wagering. Options are as follows.
#  constant : Wager a constant value. All-in if balance is lower than constant value.
#  all-in : Wager full account balance.
#  percentage : Wager a percentage of the account balance.
wager_strategy: percentage

# Constant amount to wager when using the constant wager strategy.
# This must be a whole number greater than 0.
constant_wager: 200

# Percent of account balance to wager when using the constant wager strategy.
# This must be a decimal value greater than 0 and less than 1
percentage_wager: 0.2
```