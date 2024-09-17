import os
import subprocess
import requests
import logging


############################# init variable ##################################### 

HOSTNAME = os.getenv('HOSTNAME') or 'ogma.lti.cs.cmu.edu'
GITLAB_PORT = os.getenv('GITLAB_PORT') or '8929'
GITLAB_USER = "root"
GITLAB_URL = f"http://{HOSTNAME}:{GITLAB_PORT}/{GITLAB_USER}"
TEST_REPO_NAME="api-server"
WIKI_REPO_NAME="wiki-test"

############################# util function #####################################  
# Set up logging
logging.basicConfig(level=logging.INFO,    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        # logging.FileHandler("app.log"),  # Log messages to a file
        logging.StreamHandler()  # Log messages to the console
    ])
logger = logging.getLogger("Functionality Test")

def execute_command(command):
    process = subprocess.run(command, shell=True, check=True)
    logger.info(process.stdout)
    return

############################# Test function ##################################### 
################### Please delete the test you don't need #######################

# test pull repository from the gitlab server
def test_pull_repository():
    execute_command(f"rm -rf {TEST_REPO_NAME}")
    execute_command(f"git clone {GITLAB_URL}/{TEST_REPO_NAME}.git")
    return

# test access wiki document
def test_wiki():
    response = requests.get(f"{GITLAB_URL}/{WIKI_REPO_NAME}/-/wikis/home")
    logger.debug(response.content)
    if "Welcome to Bridges-2" not in str(response.content):
        logger.Error("cannot get correct wiki")
    return

# test access specific internet
def test_black_white_list():
    white_list = ['https://www.google.com', 'https://www.github.com']
    black_list = ['https://www.youtube.com', 'https://www.reddit.com']
    for url in white_list:
        if not can_access_website(url):
            logger.error(f"should can access {url}")
    for url in black_list:
        if can_access_website(url):
            logger.error(f"should not access {url}")
    return


# test block specific internet
def can_access_website(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            logger.info(f"can visit {url}")
            return True
        else:
            logger.error(f"cannot access {url}")
            return False
    except requests.RequestException as e:
        logger.error(f"cannot access {url}")
        return False

# test mock local API
# test prepared file

# if __name__ == "__main__":
    # TODO: polish this file so that people could use it to testify the prerequisite
    # The function mainly test 2 parts:
    #     1. Local environment: not very important, because we always can quickly restart the task image to fresh
    #     2. Sever environment: important, if the test fails, that means user need to reset the server image
    # This file should write by benchmark developer and optionally used by benchmark user
    # test_pull_repository()
    # test_wiki()
    # test_black_white_list()
    