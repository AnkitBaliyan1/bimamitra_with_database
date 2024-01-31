from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
#from langchain.vectorstores import Pinecone
from langchain_community.llms import OpenAI
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import os
from pinecone import Pinecone
from pathlib import Path


#os.environ['OPENAI_API_KEY'] = "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"
#os.environ['HUGGINGFACEHUB_API_TOKEN']="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"


def load_docs(dir):
  loader = PyPDFDirectoryLoader(dir)
  documents = loader.load()
  print("length of documents is: ", len(documents))
  return documents



# transform documents
def split_docs(documents, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs


BASE_DIR = Path(__file__).resolve().parent.parent
print("base_dir:",BASE_DIR)

def get_similar_doc(query, k=2):

    dir = os.path.join(BASE_DIR, "code/doc")
    documents = load_docs(dir)
    

    docs = split_docs(documents)
    # text embedding
    embedding = OpenAIEmbeddings()
    
    index_name=os.environ.get("index_name")
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

    index = pc.Index(index_name)


    query_embed = embedding.embed_query(query)
    similar_doc_vector = index.query(
                            namespace="ns1",
                            vector=query_embed,
                            top_k=k,
                            include_values=True,
                            include_metadata=True
                        )
    similar_doc=[]
    for i in range(k):
        id = similar_doc_vector.matches[i]["id"]
        print("id:", id)
        similar_doc.append(docs[int(id)])
    
    #return "\n".join(doc.page_content for doc in similar_doc)
    return similar_doc


from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import HuggingFaceHub
from langchain_openai import ChatOpenAI


def get_answer(query, llm=ChatOpenAI(temperature=0.5), k=2):
    relavent_doc = get_similar_doc(query, k=k)
    print("Relavant Doc found:")
    print("\n".join(doc.page_content for doc in relavent_doc))

    

    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents = relavent_doc, question=query)
    return response

def main_fun(query,k=3):

    #model = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
    #model = OpenAI(temperature=0.5)
    model=ChatOpenAI(temperature=0.5)

    #our_query="What is Mediclaim Policy?"
    k=4
    final_answer = get_answer(query, llm=model, k=k)

    print("\n\nQuestion:", query)
    print("\nAnswer is: ", final_answer)
    return final_answer

#main_fun(query="What is Mediclaim Policy?")

