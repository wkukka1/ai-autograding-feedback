class Model:
    def __init__(self):
        """
        Intialize the model. 
        """
        pass

    def generate_response(self, prompt, **kwargs):
        """
        Generate a response based on the prompt. This method should be overridden by subclasses.
        
        Args:
            prompt (str): The prompt that will be used to generate a response.
            **kwargs: Any additional arguments that might be needed for generating the response.
        
        Returns:
            tuple: A tuple containing:
                - str: The full prompt that was used to generate the response.
                - str: The generated response.
        """
        raise NotImplementedError("Subclasses must implement the `generate_response` method.")
