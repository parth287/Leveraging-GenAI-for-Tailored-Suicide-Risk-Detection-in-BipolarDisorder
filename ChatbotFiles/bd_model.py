import os
from llama_index.core.response.pprint_utils import pprint_response
from llama_index.core import VectorStoreIndex,SimpleDirectoryReader
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import StorageContext, load_index_from_storage

def read_api_key(file_path):
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()  # Read the key and strip any extra whitespace
        return api_key
    except FileNotFoundError:
        print("API key file not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

OPENAPI_API_KEY='./GMU_HAP_OPENAI_API_KEY.txt'
OPENAPI_API_KEY = read_api_key(OPENAPI_API_KEY)
os.environ['OPENAI_API_KEY'] = OPENAPI_API_KEY

def indexingData(dataPath, storagePath):
    # check if storage already exists
    PERSIST_DIR = storagePath
    if not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        filename_fn = lambda filename: {"file_name": filename}
        documents = SimpleDirectoryReader(dataPath).load_data()
        index = VectorStoreIndex.from_documents(documents,show_progress=True)
        # store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
    return index

def QueryEngine_Setup(index,similarity_cutoff, similarity_top_k):
    retriever=VectorIndexRetriever(index=index,similarity_top_k=similarity_top_k)
    postprocessor=SimilarityPostprocessor(similarity_cutoff=similarity_cutoff)
    query_engine=RetrieverQueryEngine(retriever=retriever,
                                    node_postprocessors=[postprocessor])
    return query_engine

def get_response(prompt):
    dataPath = "./Data/CT_PMID"
    storagePath = "./storage"
    index = indexingData(dataPath=dataPath, storagePath=storagePath)
    postproc_cutoff, top_k = 0, 2
    query_engine = QueryEngine_Setup(index, postproc_cutoff,top_k)
    response = query_engine.query(prompt)
    response_source = pprint_response(response, show_source=True)
    return response,response_source