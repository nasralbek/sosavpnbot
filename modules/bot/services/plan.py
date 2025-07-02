import json
import logging
import os

from modules.bot.models import Plan
from config import DEFAULT_PLANS_DIR

logger = logging.getLogger(__name__)

class PlanService():
    def __init__(self):
        file_path = DEFAULT_PLANS_DIR 
        

        if not os.path.isfile(file_path):
            logger.error(f"File '{file_path}' does not exist.")
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
       
        try:
            with open(file_path, "r") as f:
                self.data = json.load(f)
            logger.info(f"Loaded plans data from '{file_path}'.")
        except json.JSONDecodeError:
            logger.error(f"Failed to parse file '{file_path}'. Invalid JSON format.")
            raise ValueError(f"File {file_path} is not a valid JSON file.")
        

        if "plans" not in self.data or not isinstance(self.data["plans"],list):
            logger.error(f"'plans' key is missing or not a list in '{file_path}'.")
            raise ValueError(f"'plans' key is missing or not a list in '{file_path}'.")

        self.plans: list[Plan] = []
        for planjson in self.data["plans"]:
             self.plans.append(Plan.from_dict(planjson))
        logger.info("plans loaded succes")

    def get_plans(self):
        return self.plans




