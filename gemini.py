from secret import apikey, safety_settings
import fileinput
import google.generativeai as genai
import io
import linecache

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
    with io.open(arquivo_respostas_name, 'w', encoding='utf-8') as arquivo_respostas:
        arquivo_respostas.close()

    with open(arquivo_perguntas_name, 'r', encoding='utf-8') as arquivo_perguntas:
            total_linhas = len(arquivo_perguntas.readlines())

    with io.open(arquivo_perguntas_name, 'r', encoding='utf-8') as arquivo_perguntas:
        for indice, pergunta in enumerate(arquivo_perguntas, start=1):
            print(f"Gerando pergunta {indice} de {total_linhas}: {pergunta}")
            with io.open(arquivo_respostas_name, 'a', encoding='utf-8') as arquivo_respostas:
                #prompt_parts[0] = f"input: resuma {pergunta.strip()} em tres parágrafos. Se houver fórmulas, cite-as."
                prompt_parts[0] = f"input: Discorra de forma concisa mas abrangente sobre {pergunta.strip()}. Se houver fórmulas, cite-as."
                #prompt_parts[0] = f"input: você é especialista em provas do concurso da banca cesgranrio. Então resuma {pergunta.strip()} em um parágrafo."
                #prompt_parts[0] = f"input: você é especialista. Então resuma {pergunta.strip()} em um parágrafo."
                response = model.generate_content(prompt_parts)            
                arquivo_respostas.write(f"Item do edital: {pergunta}\n\n{response.text.strip()}\n\n")            

arquivo_respostas_name = "respostas.txt"
arquivo_perguntas_name = "perguntas.txt"
gerar_respostas (arquivo_perguntas_name, arquivo_respostas_name)