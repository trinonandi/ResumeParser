from langchain_community.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS


def create_vector_db(parsed_text, api_key) -> FAISS:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    text = text_splitter.split_text(parsed_text)
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    db = FAISS.from_texts(text, embedding=embeddings)
    return db


def get_response_from_query(context, query, api_key, k=4):
    llm = OpenAI(api_key=api_key, temperature=0.5, max_tokens=-1)
    db = create_vector_db(context, api_key)

    chunks = db.similarity_search(query, k=k)
    docs_page_content = " ".join([c.page_content for c in chunks])

    prompt = PromptTemplate(
        input_variables=["query", "docs"],
        template="""
        You are an AI Resume assistant and your task is to answer questions based on the resume transcript.
        
        Answer the following question: {question}
        By searching the following resume transcript: {docs}
        
        Only use information from the transcript to answer the question.
        If you feel like you do not have enough information to answer the question, say "I am not sure".
        
        Your answer should be logically sound.
        """
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(question=query, docs=docs_page_content)
    return response
