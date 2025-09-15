# GroupMe Fantasy Football Bot

## Overview
This is a Python Flask web application that serves as a GroupMe bot for fantasy football leagues. The bot responds to commands in GroupMe chats to provide fantasy football data and statistics.

## Project Architecture
- **Language**: Python 3.11
- **Framework**: Flask web framework
- **Dependencies**: flask, requests, espn_api, schedule
- **Configuration**: Environment variables for security
- **Deployment**: VM deployment target (always running)

## Recent Changes (Sep 8, 2025)
- Migrated from GitHub import to Replit environment
- Updated Flask configuration for Replit (host=0.0.0.0, port=5000)
- Created config.py using environment variables instead of hardcoded values
- Set up workflow for the backend service
- Configured VM deployment for production

## Key Features
- Responds to !weekly# commands to show weekly fantasy achievements
- Survival bowl tracking (!survival command)
- Current week information (!week command)
- Interactive bot responses to "good bot"/"bad bot"
- Connects to ESPN Fantasy API for real-time data
- Posts responses back to GroupMe via webhook

## Configuration
The bot requires three environment variables:
- GROUPME_BOT_ID: Bot identifier from GroupMe developer portal
- ESPN_LEAGUE_ID: Your ESPN fantasy league ID from the URL
- ESPN_SEASON_YEAR: Fantasy season year (e.g., 2024)

## Webhook Endpoint
The bot listens for POST requests at the root endpoint (/) from GroupMe's webhook system.