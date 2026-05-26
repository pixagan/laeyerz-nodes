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
BM25Node module for BM25 vector store operations
in the Laeyerz framework.
"""
# BM25 Adapter

from laeyerz.flow.Node import Node
from rank_bm25 import BM25Okapi
import re

class BM25Node(Node):
    def __init__(self, name: str, config:dict={}):
        super().__init__(name, config)
        self.chunks = []
        self.tokenized_chunks = []
        self.bm25 = None
        self.add_actions()

    def tokenize(self, text: str):
        text = text.lower()
        return re.findall(r"\b\w+\b", text)

    def add_documents(self, chunks: list[str]):
        self.chunks = chunks
        self.tokenized_chunks = [self.tokenize(chunk) for chunk in chunks]
        self.bm25 = BM25Okapi(self.tokenized_chunks)

    def search(self, query: str, k: int = 3):
        tokenized_query = self.tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []
        for idx, score in ranked[:k]:
            results.append({
                "chunk": self.chunks[idx],
                "score": float(score)
            })

        return {
            "results":results
        }

    def add_actions(self):

        store_inputs = [
            {
                "name":"chunks",
                "type":"list",
                "description":"The chunks to add",
                "inputType":"input",
                "source":"",
                "value":None

            }
        ]
        store_outputs = []
        self.add_action(action_name="store", function=self.add_documents, parameters=[], inputs=store_inputs, outputs=store_outputs, isDefault=True, description="Add chunks to the BM25 index")


        search_inputs = [
            {
                "name":"query",
                "type":"string",
                "description":"The query to search for",
                "inputType":"input",
                "source":"",
                "value":None
            },
            {
                "name":"k",
                "type":"int",
                "description":"The number of results to return",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]
        search_outputs = [
            {
                "name":"results",
                "type":"list",
                "description":"The search results",
                "outputType":"output",
                "source":"",
                "value":None
            }
        ]
        self.add_action(action_name="search", function=self.search, parameters=[], inputs=search_inputs, outputs=search_outputs, isDefault=True, description="Search the BM25 index")



        
