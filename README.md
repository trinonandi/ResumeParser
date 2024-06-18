## Resume Parser Backend
Generative AI project aimed at parsing resumes to extract interactive information, streamlining the hiring process for both job seekers and recruiters.

**Deployed App** - [Link](https://resume-parser-angular.vercel.app/)  <br>
**Frontend** - [Github Link](https://github.com/trinonandi/ResumeParserAngular)

### How it works:
**Following steps will be performed by the application:**
- First, the resume will be uploaded to our server
- The server will extract critical information from the resume using a Python library called PyMuPDF [Ref]
- Using NLP based scoring system, the extracted data will be then assigned with text styles and tags. This is to emphasize the heading, subheading and other important information from the resume
- This styled data will be displayed to the user in an editable Markdown format
- The parsed data may contain errors and hence the user will be provided with an opportunity to edit the content before feeding it to the LLM
- Additionally, the user might be asked to provide an OpenAI API key to activate the LLM. Please follow this link to create an API key
- Once the user feeds the data to the LLM, an interactive chat window will be activated
- The LLM will use the context provided by the parsed resume data to answer questions from the user

### Tech Stack:
- Flask
- LangChain
- FAISS
- OpenAI
- PyMuPDF
