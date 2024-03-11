from secret import apikey, safety_settings
import fileinput
import google.generativeai as genai
import io
from datetime import datetime

genai.configure(api_key=apikey)

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def gerar_respostas(arquivo_perguntas_name, arquivo_respostas_name):
    prompt_parts = [
    "input: ",
    "output: "
    ]

    with open(arquivo_perguntas_name, 'r', encoding='utf-8') as arquivo_perguntas:
            total_linhas = len(arquivo_perguntas.readlines())
    arquivo_perguntas.close()

    timestamp = datetime.now()
    string_format = timestamp.strftime("%Y-%m-%d-%H-%M-%S_")
    dir = arquivo_respostas_name.split("/")[0] + "/"    
    arquivo_para_gravar = dir + string_format + arquivo_respostas_name.split("/")[1] 
    with io.open(arquivo_perguntas_name, 'r', encoding='utf-8') as arquivo_perguntas:
        for indice, pergunta in enumerate(arquivo_perguntas, start=1):
            print(f"Gerando pergunta {indice} de {total_linhas}: {pergunta}")
    
            with io.open(arquivo_para_gravar, 'a', encoding='utf-8') as arquivo_respostas:
                prompt_parts[0] = f"input: Elabore 20 afirmativas verdadeiras conforme padrão de provas do CESPE/CEBRASPE sobre {pergunta.strip()}."
                response = model.generate_content(prompt_parts)            
                arquivo_respostas.write(f"Item do edital: {pergunta.strip()}::\n{response.text.strip()}\n\n")            
                #arquivo_respostas.write(f"Item do edital: {pergunta}\n response.text.strip()\n\n")            


arquivo_respostas_name = "saida/respostas.txt"
arquivo_perguntas_name = "entrada/perguntas.txt"
gerar_respostas (arquivo_perguntas_name, arquivo_respostas_name)



                #prompt_parts[0] = f"input: você é especialista em provas do concurso da banca cesgranrio. Então resuma {pergunta.strip()} em um parágrafo."
                #prompt_parts[0] = f"input: você é especialista. Então resuma {pergunta.strip()} em um parágrafo."
                #prompt_parts[0] = f"input: resuma {pergunta.strip()} em tres parágrafos. Se houver fórmulas, cite-as."