import time
import requests
import pandas as pd
from dotenv import load_dotenv
import os
import argparse


load_dotenv()

class RepoData:
    def __init__(self, owner):
        self.owner = owner
        self.api_base_url = 'https://api.github.com'
        self.auth_token = os.getenv('GITHUB_AUTH_TOKEN')
        self.headers = {'Authorization': 'Bearer ' + self.auth_token,
                        'X-GitHub-Api-Version': '2022-11-28'}

    def show(self):
        print(self.auth_token)

    def repo_list(self):
        repos_list = []
        page_num = 1

        while True:
            try:
                url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}&per_page=50'
                print(f"Consultando página {page_num}...")
                start_time = time.time()  

                response = requests.get(url, headers=self.headers)
                response.raise_for_status()  

                data = response.json()

                # Verificar o tempo de resposta
                end_time = time.time()
                print(f"Tempo de resposta para a página {page_num}: {end_time - start_time:.2f} segundos")

                if not data:
                    break

                repos_list.append(data)
                page_num += 1

            except Exception as e:
                print(f"Erro na página {page_num}: {e}")
                break

        return repos_list

    def repo_name(self, repos_list):
        name_repo = []

        for list in repos_list:
            for sublist in list:
                found_name = sublist.get('name')

                if found_name is None:
                    found_name = ''

                name_repo.append(found_name)
        return name_repo

    def repo_language(self, repos_list):
        language_repo = []

        for repo_page in repos_list:
            for repo in repo_page:
                found_language = repo.get('language')  

                if found_language is None:
                    found_language = ''  

                language_repo.append(found_language)

        return language_repo

    def create_df_language(self):
        repositories = self.repo_list()

        data = pd.DataFrame({
            'repository_name': self.repo_name(repositories),
            'language': self.repo_language(repositories)
        })

        return data


def main():
   
    parser = argparse.ArgumentParser(description="Extraia informações de repositórios do GitHub e salve como CSV")
    parser.add_argument('owners', type=str, nargs='+', help="Lista de nomes de usuários ou organizações no GitHub")  
    
   
    args = parser.parse_args()

    
    for owner in args.owners:
        print(f"Processando dados para o repositório: {owner}")

       
        repo_data = RepoData(owner)

       
        most_used_lang = repo_data.create_df_language()

        
        file_name = f"data_processed/languages_{owner}.csv"
        most_used_lang.to_csv(file_name, index=False)
        print(f"Dados salvos em: {file_name}")


if __name__ == '__main__':
    main()