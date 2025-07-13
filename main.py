from linkedin_login import LinkedInLogin
from getpass import getpass

def conn_level_input():
    """Prompts the user for desired connection levels."""
    level_list = []
    while not level_list:
        lvl_input = input("Digite os níveis de conexão para pesquisar, separados por vírgula (1, 2, 3): ")
        lvl_input = lvl_input.replace(" ", "")
        valid_levels = {'1': '1st', '2': '2nd', '3': '3rd+'}
        levels = lvl_input.split(",")
        for level in levels:
            if level in valid_levels:
                level_list.append(valid_levels[level])
            else:
                print(f"Nível inválido: {level}. Digite apenas 1, 2 ou 3.")
                level_list = []
                break
    print(f"Níveis de conexão a serem buscados: {level_list}\n")
    return level_list

def main():
    print("=== LinkedIn Connection Automation ===\n")
    search_term = input("Digite o termo de pesquisa no LinkedIn: ")
    
    # Coleta múltiplos níveis de conexão
    connection_levels = conn_level_input()

    print("\nDigite um ou mais locais para filtrar (separe por vírgula), ou deixe vazio para todos os locais.")
    locations_input = input("Exemplo: São Paulo, Brasil ou United States: ")
    locations = [l.strip() for l in locations_input.split(",")] if locations_input.strip() else []
    
    print("\nDigite uma ou mais empresas para filtrar (separe por vírgula), ou deixe vazio para todas as empresas.")
    companies_input = input("Exemplo: Google, Itaú Unibanco, Microsoft: ")
    companies = [c.strip() for c in companies_input.split(",")] if companies_input.strip() else []

    print("\nQuantas páginas de resultados deseja navegar? (aperte Enter para usar o padrão de 3 páginas)")
    pages_input = input("Páginas: ").strip()
    num_pages = int(pages_input) if pages_input.isdigit() and int(pages_input) > 0 else 3

    linkedin = LinkedInLogin()
    try:
        linkedin.start_browser(headless=False)
        linkedin.login()
        linkedin.search_people_with_filters(
            search_term, connection_levels, locations, companies
        )
        send = input("\nDeseja enviar convites de conexão para os resultados dessas páginas? (s/n): ").strip().lower()
        if send == 's':
            max_invites = input("Quantos convites (máx) enviar por página? [padrão=10]: ").strip()
            max_invites = int(max_invites) if max_invites.isdigit() else 10
            linkedin.send_connection_requests_paged(
                max_requests_per_page=max_invites,
                delay=2,
                num_pages=num_pages
            )
        input("Pressione Enter para sair...")
    finally:
        linkedin.close()

if __name__ == "__main__":
    main()
