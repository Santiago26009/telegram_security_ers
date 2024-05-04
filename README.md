# ERS Project

# Analysis and Vulnerabilities of Telegram

This project, titled "Analysis and Vulnerabilities of Telegram," aims to leverage the Telegram API to pinpoint the exact coordinates of nearby users by utilizing the `near_me` feature present in Telegram. This capability raises significant security concerns, as it potentially exposes a vulnerability in Telegram's privacy safeguards.

## Project Overview

The essence of the project is to systematically compile lists of users based on their location data. These lists are then utilized to generate visual representations on maps, highlighting the proximity of users. Furthermore, we integrate the use of ChatGPT to provide recommendations for notable places in the vicinity of these coordinates. 

An additional facet of the project involves the capability to send messages to users for whom we have a phone number, thereby demonstrating the potential outreach and implications of this feature.

## Execution

To execute this project, the following steps are necessary:

1. Creation of a virtual environment is essential to maintain an isolated and controlled workspace

    `python -m venv .venv`

2. Activation of the virtual environment should be done prior to any installations

    `.venv/Scripts/activate`

3. The required libraries need to be installed from the provided requirement document

    `pip install -r requirements.txt`

4. Launch the application by running the command

    `python -m main`

## Interactive Notebook

For a more visual, graphic, and interactive experience, a Jupyter Notebook `.ipynb` is available. This notebook provides a user-friendly interface to engage with the code and its functionalities.

## Security Implications

The project serves to underscore a potential flaw in Telegram's location-sharing capabilities, which could be exploited to infringe on user privacy. By demonstrating the ease with which user coordinates can be obtained and utilized, we aim to raise awareness about the importance of digital security and privacy measures.