# hyperparam_helpers.py

def str_to_bool(s: str) -> bool:
    return s.lower() in {"1", "true", "yes", "on"}

ollama_option_schema = {
        "temperature": float,
        "top_p": float,
        "top_k": int,
        "typical_p": float,
        "repeat_penalty": float,
        "presence_penalty": float,
        "frequency_penalty": float,
        "seed": int,
        "stop": lambda x: [s.strip() for s in x.split(",")],
        "num_predict": int,
        "num_keep": int,
        "num_ctx": int,
        "num_batch": int,
        "num_gpu": int,
        "main_gpu": int,
        "use_mmap": str_to_bool,
        "num_thread": int,
        "penalize_newline": str_to_bool,
        "mirostat": int,
        "mirostat_tau": float,
        "mirostat_eta": float,
    }

def cast_to_type(option_schema=dict, hyperparams=dict):
    """given the option schema casts the values of hyperparams into their respective types"""
    options = {}
    for key, value in hyperparams.items():
        try:
            if key in option_schema:
                options[key] = option_schema[key](value)
            else:
                options[key] = value
        except Exception as e:
            print(f"Warning: Failed to cast hyperparameter '{key}' with value '{value}': {e}")
    return options