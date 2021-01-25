import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

schema = {
    "email-general": {
        "browser_notification": {
            "required": True,
            "field_type": bool,
            "rules": lambda i: type(i) is bool
        },
        "auto_refresh_every": {
            "required": True,
            "field_type": str,
            "rules": lambda i: (type(i) is str and i in ["1m" ,"5m", "10m", "30m", "1h"])
        }
    },
    "email-vocation": {
        "subject": {
            "required": True,
            "field_type": str,
            "rules": lambda i: (type(i) is str and len(i) > 1 and len(i) < 128)
        },
        "days_beetwen_response": {
            "required": True,
            "field_type": int,
            "rules": lambda i: (type(i) is int and i > 0 and i < 8)
        },
        "message": {
            "required": True,
            "field_type": str,
            "rules": lambda i: (type(i) is str and len(i) > 1 and len(i) < 1024)
        },
        "dont_send_respnses": {
            "required": False,
            "field_type": bool,
            "rules": lambda i: type(i) is bool
        },
        "enable_reply_on": {
            "required": False,
            "field_type": "str",
            "rules": lambda i: (type(i) is str and len(i) == 12)
        },
        "disable_reply_on": {
            "required": False,
            "field_type": "str",
            "rules": lambda i: (type(i) is str and len(i) == 12)
        },
        "always_vocation_message_response": {
            "required": False,
            "field_type": bool,
            "rules": lambda i: type(i) is bool
        },
        "discard_incoming_mails": {
            "required": False,
            "field_type": bool,
            "rules": lambda i: type(i) is bool
        }
    },
    "email-forward": {
        "keep_a_copy": {
            "required": False,
            "field_type": bool,
            "rules": lambda i: type(i) is bool
        }
    },
    "email-filters": {
        "order": {
            "required": True,
            "field_type": int,
            "rules": lambda i: (type(i) is int and i > 0)
        },
        "name": {
            "required": True,
            "field_type": str,
            "rules": lambda i: (type(i) is str and len(i) > 1 and len(i) < 128)
        },
        "incoming_messages": {
            "required": True,
            "field_type": str,
            "rules": lambda i: (type(i) is str and i in ["match_all_flowing_rules", "match_any_flowing_rules", "match_all"])
        },
        "conditions": {
            "required": False,
            "field_type": list,
            "rules": lambda i : type(i) is list,
            "sub": {
                "field_type": dict, # dict: dict list | int: int list ..etc
                # "rules" # Just use withour dict list
                "section": {
                    "field_type": str,
                    "rules": lambda i : (type(i) is str and i in ["subject", "from"])
                },
                "condidation": {
                    "field_type": str,
                    "rules": lambda i : (type(i) is str and i in ["is", "is_not"])
                },
                "value": {
                    "field_type": str,
                    "rules": lambda i : (type(i) is str and len(i) > 0 and len(i) < 256)
                },
               "header": {
                    "field_type": str,
                    "rules": lambda i : (type(i) is str and len(i) > 0 and len(i) < 256)
                }
            }
        },
        "actions": {
            "required": False,
            "field_type": list,
            "rules": lambda i : type(i) is list,
            "sub": {
                "field_type": dict, # dict: dict list | int: int list ..etc
                # "rules" # Just use withour dict list
                "type": {
                    "field_type": str,
                    "rules": lambda i: (type(i) is str and i in ["discard_message", "keep_message"])
                },
                "to_email": {
                    "field_type": str,
                    "rules": lambda i: (type(i) is str and EMAIL_REGEX.match(i))
                },
                "folder": {
                    "field_type": str,
                    "rules": lambda i: (type(i) is str and i in ["discard_message", "keep_message"])
                },
                "file_width": {
                    "field_type": str,
                    "rules": lambda i: (type(i) is str and i in ["seen", "deleted"])
                },
                "message": {
                    "field_type": str,
                    "rules": lambda i: (type(i) is str and len(i) > 0 and len(i) < 1024)
                }
            }
        }
    }
}