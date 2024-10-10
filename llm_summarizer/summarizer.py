from langchain.chains.summarize import load_summarize_chain
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

from llm_summarizer.summarizer_interface import SummarizerInterface


class Summarizer(SummarizerInterface):
    def summarize(self, text: str, language: str) -> str:
        llm = Ollama(model='phi3')

        text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "\t"], chunk_size=1000,
                                                       chunk_overlap=250)
        docs = text_splitter.create_documents([text])

        template = f'''
        Please provide a summary of the given text in {language}, including all key points and supporting details. 
        The summary should be comprehensive and accurately reflect the main message and arguments presented in the original text, while also being concise and easy to understand.
        Provide the summary in bullet points, covering the key points. 
        Also create a small and appropriate title for the text at the begin (do not include the word "Title").
        Text: '{{text}}'
        '''

        prompt = PromptTemplate(
            input_variables=['text'],
            template=template
        )

        summary_chain = load_summarize_chain(
            llm=llm,
            chain_type="stuff",
            prompt=prompt,
            verbose=False
        )

        output = summary_chain.invoke({"input_documents": docs})

        return output['output_text']
