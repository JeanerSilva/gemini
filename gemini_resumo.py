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
        temas = arquivo_perguntas.read().split("Item do edital:")    
        for conteudo in temas:
            print(f"conteudo {conteudo}")
            with io.open(arquivo_respostas_name, 'a', encoding='utf-8') as arquivo_respostas:
                prompt_parts[0] = f"input: resuma {conteudo} em um parágrafo. Se houver fórmulas, cite-as. See houver subtópicos, liste-os"
                response = model.generate_content(prompt_parts)            
                arquivo_respostas.write(f"{response.text.strip()}\n\n")            

arquivo_respostas_name = "completo_resumo.txt"
arquivo_perguntas_name = "saida/completo2.txt"
gerar_respostas (arquivo_perguntas_name, arquivo_respostas_name)