import os
import html

def gerar_html():
    # Pega o nome da pasta atual para nomear o projeto e o arquivo
    nome_do_projeto = os.path.basename(os.getcwd())
    nome_arquivo_saida = f"{nome_do_projeto}.html"

    projeto_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Documentação: {nome_do_projeto}</title>
        <style>
            body {{ font-family: sans-serif; background: #f4f4f4; padding: 20px; }}
            .file {{ background: white; border: 1px solid #ccc; margin: 15px 0; padding: 15px; border-radius: 5px; }}
            h2 {{ color: #2c3e50; font-size: 16px; border-bottom: 2px solid #3498db; padding-bottom: 5px; }}
            pre {{ background: #2d3436; color: #dfe6e9; padding: 15px; overflow-x: auto; border-radius: 5px; font-size: 13px; }}
        </style>
    </head>
    <body>
        <h1>Estrutura do Projeto: {nome_do_projeto}</h1>
    """

    # Lista de pastas a ignorar (você pode adicionar mais conforme precisar)
    ignore = [
        '.git', '__pycache__', '.venv', 'env', 'node_modules',
        '.pytest_cache', '.vscode', '.idea', 'dist', 'build', '.DS_Store', 'site'
    ]

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ignore]
        for file in files:
            # Extensões que serão incluídas na documentação
            if file.endswith(('.py', '.yml', '.yaml', '.Dockerfile', '.sql', '.txt', '.md', '.sh')):
                path = os.path.join(root, file)
                projeto_html += f"<div class='file'><h2>{path}</h2><pre>"

                try:
                    with open(path, 'r', encoding='utf-8', errors='replace') as f:
                        projeto_html += html.escape(f.read())
                except Exception as e:
                    projeto_html += f"Erro ao ler arquivo: {e}"

                projeto_html += "</pre></div>"

    projeto_html += "</body></html>"

    with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        f.write(projeto_html)

    print(f"Documentação gerada com sucesso: {nome_arquivo_saida}")

if __name__ == "__main__":
    gerar_html()
