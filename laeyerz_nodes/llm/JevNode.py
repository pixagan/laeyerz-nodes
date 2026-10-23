# Copyright 2025 Pixagan Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
JevNode module for Jev LLM integration
in the Laeyerz framework.
"""
from dotenv import load_dotenv
import os
import json
import io
from laeyerz.flow.Node import Node
from laeyerz.nodes.apis.APICall import APICallNode


class JevNode(Node):

    def __init__(self, node_name='JevNode', config={}):
        super().__init__(node_name=node_name, description='JevAI  Node')

        self.name = node_name
        self.api = APICallNode("JevAPI")
        self.api_key = None

        self.method = "POST"
        self.url = "https://api.typesafe.ai/v1/systemone"
        self.auth = "Bearer "

        if(config.get('api_key')):
            self.api_key = config.get('api_key')
            self.auth = "Bearer "+ self.api_key
        else:
            print("No API key provided")
            raise ValueError("No API key provided")

        self.timeout = 10
    

    def setup(self):
        print(f"Setting up node {self.name}")


    def call_model(self, state, questions):

        headers = {
            "Content-Type": "application/json", 
            "Authorization": self.auth 
        }

        body = {
            "model": "jev-latest",
            "state": state,
            "questions": questions
        }

        response = self.api.call( method=self.method, url=self.url, headers=headers, params={}, body=body, timeout=self.timeout)

        output = self.response_parser(response)
        return output



    def response_parser(self, response):

        status_code      = response['status_code']
        headers          = response['headers']
        response_content = response['response']

        answers = response_content['answers']
        usage  = response_content['usage']

        print("Answers Parsed : ", answers)

        output = {
            "status_code": status_code,
            "content":response_content,
            "answers": answers,
            "usage": usage
        }
        
        return output


    def setup(self):

        #adding llm actions
        node_inputs = [
            {
                "name":"state",
                "type":"list",
                "description":"The input messages to the model",
                "inputType":"input",
                "source":"",
                "value":None
            },
            {
                "name":"questions",
                "type":"str",
                "description":"Input to the model",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]
        node_outputs = [
            {
                "name":"status_code",
                "type":"string",
                "description":"Status Code"
            },
            {
                "name":"content",
                "type":"dict",
                "description":"Output from the llm model"
            },
            {
                "name":"answers",
                "type":"object",
                "description":"The answers extracted"
            },
            {
                "name":"usage",
                "type":"object",
                "description":"Token usage"
            }
        ]
        self.add_action(action_name="call_model", function=self.call_model, parameters=["model"], inputs=node_inputs, outputs=node_outputs, isDefault=True, description="Call the Jev Model")






# Return the configured node
if __name__ == "__main__":
    # For testing the node

    llm_node = JevNode(node_name="LLM", model="gpt-4o-mini")

    state = ""
    questions = {}
    llm_node.call_model(state, questions)
  






