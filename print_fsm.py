from transitions import Machine
from transitions.extensions import GraphMachine
from flask import Flask, jsonify, request, abort, send_file
try:
    import pygraphviz as pgv
except ImportError:
    raise
import requests
machine = GraphMachine(
    states=["user", "main_menu", "twitter_menu", "input_user", "SA","mostLike","mostRe","show_fsm","pos_rate","neu_rate", "neg_rate"],
    transitions=[
        {"trigger": "advance", "source": "user", "dest": "main_menu",
            "conditions": "is_going_to_main_menu"},
        {"trigger": "advance", "source": "main_menu", "dest": "main_menu",
            "conditions": "is_going_to_main_menu"},
        {"trigger": "advance", "source": "main_menu",
            "dest": "input_user", "conditions": "is_going_to_input_user"},
        {"trigger": "advance", "source": "input_user",
            "dest": "twitter_menu", "conditions": "is_going_to_twitter_menu"},
        {"trigger": "advance", "source": "twitter_menu",
            "dest": "SA", "conditions": "is_going_to_SA"},
        {"trigger": "advance", "source": "twitter_menu", "dest": "mostLike",
            "conditions": "is_going_to_mostLike"},
        {"trigger": "advance", "source": "twitter_menu",
            "dest": "mostRe", "conditions": "is_going_to_mostRe"},
        {"trigger": "advance", "source": "main_menu", "dest": "show_fsm",
            "conditions": "is_going_to_show_fsm", },
        {"trigger": "advance", "source": ["SA", "mostLike", "mostRe"],
            "dest": "twitter_menu","conditions": "is_going_back"},
        {"trigger": "advance", "source": "twitter_menu",
            "dest": "main_menu", "conditions": "is_going_back"},
        {"trigger": "advance", "source": "input_user",
            "dest": "main_menu", "conditions": "is_going_back"},
        {"trigger": "advance", "source": "show_fsm",
            "dest": "main_menu", "conditions": "is_going_back"},
        {"trigger": "advance", "source": "show_fsm",
            "dest": "input_user", "conditions": "is_going_to_input_user"},
        {"trigger": "advance", "source": "SA",
            "dest": "pos_rate", "conditions": "is_going_to_pos_rate"},
        {"trigger": "advance", "source": "SA",
            "dest": "neu_rate", "conditions": "is_going_to_neu_rate"},
        {"trigger": "advance", "source": "SA",
            "dest": "neg_rate", "conditions": "is_going_to_neg_rate"},
        {"trigger": "advance", "source": ["pos_rate", "neu_rate", "neg_rate"],
            "dest": "SA","conditions": "is_going_back"},
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)
machine.get_graph().draw("fsm.png", prog="dot", format="png")