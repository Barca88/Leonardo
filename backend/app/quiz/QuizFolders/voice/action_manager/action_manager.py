import logging
from typing import Dict

from app.voice.action_manager.action_calculator import ActionCalculator
from app.voice.action_manager.action_executor import ActionExecutor
from app.voice.actions.action import Action
from app.voice.actions.actions import Actions


class ActionManager:
    actions: Dict[str, Dict[str, Action]]

    def __init__(self):
        self.actions = Actions().actions

    def select_action(self, transcript, lang):
        if self.actions[lang] is None:
            logging.error("Idioma não suportada.")
            raise ValueError('Idioma não suportada.')

        action = ActionCalculator(self.actions[lang]).select_action_to_execute(transcript)

        if action is None:
            logging.error("Não consigo executar a ação pedida.")
            raise ValueError('Não consigo executar a ação pedida.')

        logging.info("Ação Detetada: {}".format(action.name))
        executor = ActionExecutor(action, transcript)
        return executor.action_callback()
