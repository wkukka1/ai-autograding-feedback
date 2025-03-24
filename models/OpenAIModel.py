import os
from dotenv import load_dotenv
import openai
from models.Model import Model
from helpers.constants import INSTRUCTIONS

# Load environment variables from .env file
load_dotenv()

class OpenAIModel(Model):
    def __init__(self):
        super().__init__()
        
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize the vector store
        self.vector_store = self.client.vector_stores.create(name="Markus LLM Vector Store")
        
        # Create the model
        self.model = self.client.beta.assistants.create(
            name="Markus LLM model",
            model="gpt-4-turbo",
            instructions=(
               INSTRUCTIONS
            ),
            tools=[{"type": "file_search"}],  # Allow model to use file search tool
            tool_resources={
                "file_search": {
                    "vector_store_ids": [self.vector_store.id]
                }
            }
        )

    """Generate a response based on the given prompt and assignment"""
    def generate_response(self, prompt, assignment_files, question_num=None):
        if not self.model:
            raise RuntimeError("model was not created successfully")
        
        request = 'Uploaded Files: '
        # Upload files to model's vector store
        file_ids = []
        for file_path in assignment_files:
            base, ext = os.path.splitext(file_path)
            if ext.lower() == '.txt':  # Only upload the text files in each folder
                file_id = self._upload_file(file_path)
                file_ids.append(file_id)
                request += base

        # Modify prompt for a specific question if provided
        if question_num: 
            prompt = prompt + f' Identify and generate a response for the mistakes **only** in task ${question_num}. '
            response = self._call_openai(prompt)
        else:
            response = self._call_openai(prompt)
        
        # Cleanup resources after use
        self._cleanup_resources(file_ids)
        
        request = "\n" + INSTRUCTIONS + "\n" + prompt
        return request, response
    
    """Upload a file to OpenAI storage and link it to the vector store"""
    def _upload_file(self, file_path):
        #print("Uploading file: " + file_path)
        with open(file_path, 'rb') as f:
            response = self.client.files.create(file=f, purpose='assistants')
            self.client.vector_stores.files.create(
                vector_store_id=self.vector_store.id,
                file_id=response.id
            )
        return response.id

    """Send prompt to OpenAI and retrieve the response"""
    def _call_openai(self, prompt):
        thread = self.client.beta.threads.create()

        # Send user prompt as message in the thread
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )

        # Start run that processes user input
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.model.id
        )

        while run.status not in ["completed", "failed"]:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        
        if run.status == "failed":
            print("Error details:", run.last_error)
        
        messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        
        return response
    
    """Cleanup uploaded files and models"""
    def _cleanup_resources(self, file_ids):
        self._cleanup_files(file_ids)
        self._delete_all_models()

    """Delete the uploaded files and vector store files"""
    def _cleanup_files(self, file_ids):
        for file_id in file_ids:
            self.client.files.delete(file_id)
            self.client.vector_stores.files.delete(
                vector_store_id=self.vector_store.id,
                file_id=file_id
            )

    """Delete all models"""
    def _delete_all_models(self):
        models = self.client.beta.assistants.list().data
        for model in models:
            model_id = model.id
            # print(f"Deleting model: {model_id}")
            self.client.beta.assistants.delete(model_id)

    """Delete all files from OpenAI storage"""
    def _delete_all_files(self):
        files = self.client.files.list()
        for file in files:
            file_id = file.id
            # print(f"Deleting file: {file_id}")
            self.client.files.delete(file_id)
            self.client.vector_stores.files.delete(
                vector_store_id=self.vector_store.id,
                file_id=file_id
            )
