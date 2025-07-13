from playwright.sync_api import sync_playwright
import time
import os
import json
from cryptography.fernet import Fernet
from pathlib import Path

class LinkedInLogin:
    def __init__(self, email=None, password=None):
        if email is None or password is None:
            self.email, self.password = self.get_credentials()
        else:
            self.email = email
            self.password = password
        self.browser = None
        self.page = None

    def start_browser(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()

    def login(self):
        while True:
            try:
                print("Acessando LinkedIn...")
                self.page.goto("https://www.linkedin.com/login")
                self.page.fill('input[name="session_key"]', self.email)
                self.page.fill('input[name="session_password"]', self.password)
                self.page.click('button[type="submit"]')
                
                # Aguarda 5 segundos para verificar se há erro de login
                try:
                    error = self.page.wait_for_selector('//div[contains(@class, "alert") or contains(@class, "error")]', timeout=5000)
                    if error:
                        error_text = error.inner_text()
                        print(f"Erro no login: {error_text}")
                        retry = input("Login falhou. Deseja tentar novamente? (s/n): ").lower()
                        if retry != 's':
                            print("Abortando o script...")
                            self.close()
                            exit()
                        continue
                except Exception:
                    # Se não encontrou erro, assume que o login foi bem sucedido
                    pass
                
                # Verifica se chegou na página inicial do LinkedIn procurando o elemento main do feed
                try:
                    self.page.wait_for_selector('main[aria-label="Main Feed"]', timeout=5000)
                    print("Login realizado com sucesso!")
                    break
                except Exception:
                    # Tenta outras variações do seletor (para diferentes idiomas)
                    try:
                        self.page.wait_for_selector('main[aria-label="Feed principal"]', timeout=2000)
                        print("Login realizado com sucesso!")
                        break
                    except Exception:
                        retry = input("Possível falha no login. Deseja tentar novamente? (s/n): ").lower()
                        if retry != 's':
                            print("Abortando o script...")
                            self.close()
                            exit()
                    
            except Exception as e:
                print(f"Erro inesperado durante o login: {str(e)}")
                retry = input("Ocorreu um erro. Deseja tentar novamente? (s/n): ").lower()
                if retry != 's':
                    print("Abortando o script...")
                    self.close()
                    exit()

    def close(self):
        self.browser.close()
        self.playwright.stop()
    
    def open_all_filters(self):
        try:
            self.page.wait_for_selector('//button[contains(.,"Todos os filtros")]', timeout=5000)
            self.page.click('//button[contains(.,"Todos os filtros")]')
        except Exception:
            self.page.wait_for_selector('//button[contains(.,"All filters")]', timeout=5000)
            self.page.click('//button[contains(.,"All filters")]')
        self.page.wait_for_timeout(1000)
    
    def apply_connection_filter(self, connection_levels):
        """
        Aplica filtros de nível de conexão (1st, 2nd, 3rd+) usando o aria-label do botão.
        connection_levels deve ser uma lista, exemplo: ['1st', '2nd']
        """
        try:
            print(f"Aplicando filtro de conexão: {connection_levels}")
            for lvl in connection_levels:
                button_xpath = f"//button[@aria-label='{lvl}']"
                print(f"Procurando botão para nível de conexão: {lvl}")
                try:
                    conn_button = self.page.wait_for_selector(button_xpath, timeout=4000)
                    aria_pressed = conn_button.get_attribute('aria-pressed')
                    if aria_pressed == 'false':
                        conn_button.click()
                        self.page.wait_for_timeout(700)
                        print(f"Nível de conexão '{lvl}' selecionado.")
                    else:
                        print(f"Nível de conexão '{lvl}' já está selecionado.")
                except Exception:
                    print(f"Botão de conexão '{lvl}' não encontrado.")
        except Exception as e:
            print(f"Erro ao definir níveis de conexão: {e}")

    def apply_location_filter(self, locations):
        try:
            print("Procurando botão de localidade...")
            location_button = None
            selectors = [
                'button#searchFilter_geoUrn',
                'button.search-reusables__filter-pill-button[aria-label*="Locations filter"]',
                'button.artdeco-pill.artdeco-pill--slate.search-reusables__filter-pill-button',
                'button[aria-label*="Locations filter"]',
                'button.reusable-search-filter-trigger-and-dropdown__trigger[id="searchFilter_geoUrn"]',
                '//button[contains(@class, "search-reusables__filter-pill-button") and contains(@aria-label, "Location")]',
                '//button[contains(@class, "artdeco-pill") and @id="searchFilter_geoUrn"]'
            ]
            
            for selector in selectors:
                try:
                    if selector.startswith('//'):
                        location_button = self.page.wait_for_selector(selector, timeout=2000)
                    else:
                        location_button = self.page.wait_for_selector(selector, timeout=2000)
                    if location_button and location_button.is_visible():
                        break
                except Exception:
                    continue
                    
            if not location_button:
                print("Botão de filtro de localidade não encontrado.")
                return

            location_button.click()
            self.page.wait_for_timeout(1200)

            for loc in locations:
                loc = loc.strip()
                print(f"Digitando localidade: {loc}")
                # O campo é um <input> com placeholder "Add a location" ou "Adicionar uma localização"
                # Vamos pegar o primeiro input visível, não hidden
                input_selectors = [
                    'input.basic-input[placeholder="Add a location"]',
                    'input.basic-input[aria-label="Add a location"]',
                    'input[role="combobox"][placeholder="Add a location"]',
                    'input.basic-input[placeholder="Adicionar uma localização"]',
                    'input[role="combobox"][aria-label="Add a location"]',
                    'input.basic-input[dir="auto"][role="combobox"]',
                    '//input[@class="basic-input" and @placeholder="Add a location"]',
                    '//input[@role="combobox" and contains(@class, "basic-input")]'
                ]
                location_input = None
                for sel in input_selectors:
                    try:
                        if sel.startswith('//'):
                            location_input = self.page.wait_for_selector(sel, timeout=2000)
                        else:
                            location_input = self.page.wait_for_selector(sel, timeout=2000)
                        if location_input and location_input.is_visible():
                            break
                    except Exception:
                        continue
                if not location_input:
                    print("Campo de localidade não encontrado/visível.")
                    continue

                location_input.click()
                location_input.fill("")  # Limpa
                location_input.type(loc, delay=50)  # Digita como humano
                self.page.wait_for_timeout(1400)  # Aguarda o autocomplete carregar

                # Busca opções de autocomplete usando vários seletores
                option_selectors = [
                    '//div[contains(@class,"basic-typeahead__selectable")]//span[contains(@class,"search-typeahead-v2__hit-text")]',
                    '//div[contains(@class,"basic-typeahead__selectable")]//span[contains(@class,"search-typeahead-v2__hit-info")]',
                    '//div[contains(@class,"basic-typeahead__selectable")]//span',
                    f'//div[contains(@class,"basic-typeahead__selectable")]//span[contains(text(),"{loc}")]'
                ]
                
                found = False
                for selector in option_selectors:
                    if found:
                        break
                    try:
                        options = self.page.query_selector_all(selector)
                        if not options:
                            continue
                            
                        for opt in options:
                            try:
                                option_text = opt.inner_text().strip()
                                if option_text.lower() == loc.lower() or loc.lower() in option_text.lower():
                                    print(f"Selecionando local: {option_text}")
                                    opt.click()
                                    found = True
                                    self.page.wait_for_timeout(800)
                                    break
                            except Exception:
                                continue
                            
                        if not found and options:
                            # Se não encontrou correspondência exata, usa a primeira opção
                            first_option_text = options[0].inner_text().strip()
                            print(f"Localização '{loc}' não encontrada exatamente. Selecionando primeira opção: {first_option_text}")
                            options[0].click()
                            found = True
                            self.page.wait_for_timeout(800)
                    except Exception:
                        continue
                        
                if not found:
                    print(f"Nenhuma opção encontrada para '{loc}'.")
            # Botão "Show results"/"Mostrar resultados"
            print("Procurando botão para aplicar filtro de localidade...")
            try:
                apply_btn = self.page.wait_for_selector(
                    '//button[contains(.,"Show results") or contains(.,"Mostrar resultados") or @aria-label="Apply current filter to show results"]',
                    timeout=5000
                )
                apply_btn.click()
                self.page.wait_for_timeout(2000)
                print("Filtro de localidade aplicado com sucesso!\n")
            except Exception:
                print("Botão 'Show results'/'Mostrar resultados' não encontrado ou não clicável.")

        except Exception as e:
            print(f"Erro ao definir localidade: {e}")


    def apply_company_filter(self, companies):
        try:
            print("Tentando localizar o botão de filtro de empresa...")
            company_button = None
            selectors = [
                'button#searchFilter_currentCompany',
                'button[aria-controls="advanced-filter-currentCompany-reloaded"]',
                '//button[contains(@aria-label, "Current company") or contains(@aria-label, "Empresa atual")]',
                '//button[contains(.,"Empresas atuais") or contains(.,"Current companies") or contains(.,"Empresas") or contains(.,"Companies")]'
            ]
            
            for selector in selectors:
                try:
                    if selector.startswith('//'):
                        company_button = self.page.wait_for_selector(selector, timeout=2000)
                    else:
                        company_button = self.page.wait_for_selector(selector, timeout=2000)
                    if company_button:
                        break
                except Exception:
                    continue
                    
            if not company_button:
                print("Botão de filtro de empresa não encontrado.")
                return
            company_button.click()
            self.page.wait_for_timeout(1500)

            for company in companies:
                company = company.strip()
                print(f"Digitando empresa: {company}")
                input_selectors = [
                    '//input[contains(@placeholder, "Adicionar uma empresa") or contains(@placeholder, "Add a company")]',
                    '//input[@aria-label="Adicionar uma empresa" or @aria-label="Add a company"]',
                    'input.search-basic-typeahead__input'
                ]
                
                company_input = None
                for selector in input_selectors:
                    try:
                        company_input = self.page.wait_for_selector(selector, timeout=2000)
                        if company_input and company_input.is_visible():
                            break
                    except Exception:
                        continue
                
                if not company_input:
                    print("Campo de empresa não encontrado.")
                    continue
                
                company_input.fill("")
                company_input.fill(company)
                self.page.wait_for_timeout(1500)

                option_selectors = [
                    f'//li//span[text()="{company}"]',
                    f'//div[contains(@class,"basic-typeahead__selectable")]//span[contains(text(),"{company}")]',
                    f'//div[contains(@class,"search-typeahead-v2__hit-info")]//span[contains(text(),"{company}")]'
                ]
                
                found = False
                for selector in option_selectors:
                    try:
                        company_option = self.page.wait_for_selector(selector, timeout=2000)
                        if company_option and company_option.is_visible():
                            company_option.click()
                            print(f"Empresa '{company}' aplicada.")
                            found = True
                            break
                    except Exception:
                        continue
                
                if not found:
                    print(f"Não encontrou sugestão para a empresa: {company}")
                self.page.wait_for_timeout(1000)

            print("Tentando localizar botão 'Cancelar filtro de empresas'...")
            cancel_button = None
            try:
                cancel_button = self.page.wait_for_selector(
                    '//button[@aria-label="Cancelar filtro de empresas atuais" or @aria-label="Cancelar filtro de empresas" or @aria-label="Cancel Current companies filter" or @aria-label="Cancel Companies filter"]', timeout=4000)
            except Exception:
                print("Botão de cancelar filtro não encontrado.")
                return

            apply_button = cancel_button.evaluate_handle('node => node.nextElementSibling')
            button_text = apply_button.evaluate('node => node.textContent').strip()
            if 'Mostrar resultados' in button_text or 'Show results' in button_text:
                print("Encontrou botão 'Mostrar resultados'. Clicando...")
                apply_button.click()
                self.page.wait_for_timeout(2000)
                print("Filtro de empresa aplicado com sucesso!\n")
            else:
                print("O botão após o cancelar não é o esperado ('Mostrar resultados'). Não será clicado.")

        except Exception as e:
            print(f"Erro ao definir empresa: {e}")
    
    def search_people_with_filters(self, search_term, connection_levels, locations, companies):
        print(f"Pesquisando por: {search_term}")
        self.page.goto("https://www.linkedin.com/feed/")
        try:
            self.page.wait_for_selector('//input[@placeholder="Pesquisar"]', timeout=5000)
            self.page.fill('//input[@placeholder="Pesquisar"]', search_term)
            self.page.keyboard.press("Enter")
        except Exception:
            self.page.wait_for_selector('//input[@placeholder="Search"]', timeout=5000)
            self.page.fill('//input[@placeholder="Search"]', search_term)
            self.page.keyboard.press("Enter")
        print("Filtrando por Pessoas...")
        try:
            self.page.wait_for_selector('//button[contains(.,"Pessoas")]', timeout=5000)
            self.page.click('//button[contains(.,"Pessoas")]')
        except Exception:
            self.page.wait_for_selector('//button[contains(.,"People")]', timeout=5000)
            self.page.click('//button[contains(.,"People")]')
        time.sleep(5)
        self.open_all_filters()

        if connection_levels:
            self.apply_connection_filter(connection_levels)
        else:
            print("Exibindo todos os níveis de conexão (sem filtro).")

        if locations:
            print(f"Aplicando filtro de localidade: {locations}")
            self.apply_location_filter(locations)
        if companies:
            print(f"Aplicando filtro de empresa: {companies}")
            self.apply_company_filter(companies)

        self.show_results()

        print(f"URL dos resultados filtrados: {self.page.url}")
        time.sleep(2)

    def show_results(self):
        try:
            self.page.wait_for_timeout(1000)
            try:
                self.page.wait_for_selector('//button[contains(.,"Mostrar resultados")]', timeout=3000)
                self.page.click('//button[contains(.,"Mostrar resultados")]')
            except Exception:
                try:
                    self.page.wait_for_selector('//button[contains(.,"Show results")]', timeout=3000)
                    self.page.click('//button[contains(.,"Show results")]')
                except Exception:
                    print("Não foi possível clicar em Mostrar resultados. Prosseguindo assim mesmo.")
            self.page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Erro ao tentar clicar em Mostrar resultados: {e}")

    def send_connection_requests(self, max_requests=10, delay=2):
        print("\nIniciando envio de convites de conexão (scroll e envio seguro)...")
        sent = 0
        try:
            # Scroll até o final da página para carregar todos os resultados
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.5)

            # Encontra todos os botões de conexão
            connect_buttons = self.page.query_selector_all(
                "//button[.//span[text()='Conectar'] or .//span[text()='Connect']]"
            )
            if not connect_buttons:
                print("Nenhum botão de conexão encontrado.")
                return

            print(f"Encontrado(s) {len(connect_buttons)} botão(ões) de conexão.")

            for idx, button in enumerate(connect_buttons):
                if sent >= max_requests:
                    print(f"Limite de {max_requests} convites atingido nesta página.")
                    break
                try:
                    print(f"Enviando convite {idx + 1} de {len(connect_buttons)}...")
                    button.scroll_into_view_if_needed()
                    time.sleep(0.7)
                    button.click()
                    time.sleep(1.5)

                    # Tenta clicar no botão de enviar sem nota, "Enviar agora", "Send now" ou "Send without a note"
                    send_now_xpath = (
                        "//button[span[text()='Enviar agora'] or span[text()='Send now'] or span[text()='Send without a note']]"
                    )
                    try:
                        send_now_btn = self.page.wait_for_selector(send_now_xpath, timeout=3000)
                        send_now_btn.click()
                        print("Clique em 'Enviar agora/Send now/Send without a note'")
                        time.sleep(1.5)
                    except Exception:
                        print("Botão 'Enviar agora/Send now/Send without a note' não encontrado ou não necessário.")

                    print("Convite enviado com sucesso.")
                    sent += 1
                    time.sleep(delay)
                except Exception as e:
                    print(f"Erro ao tentar enviar convite: {e}")
                    # Tenta fechar o popup se estiver aberto
                    try:
                        close_btn = self.page.query_selector(
                            "//button[@aria-label='Dispensar' or @aria-label='Dismiss']"
                        )
                        if close_btn:
                            close_btn.click()
                            time.sleep(1)
                    except Exception:
                        pass
                    continue
            print(f"\nTotal de convites enviados nesta página: {sent}")
            return sent
        except Exception as e:
            print(f"Erro ao enviar convites de conexão: {e}")

    def send_connection_requests_paged(self, max_requests_per_page=10, delay=2, num_pages=3):
        total_sent = 0
        for current_page in range(1, num_pages+1):
            print(f"\n===== Página {current_page} de {num_pages} =====")
            sent = self.send_connection_requests(max_requests=max_requests_per_page, delay=delay)
            total_sent += sent
            if current_page < num_pages:
                next_selector = '//button[contains(@aria-label,"Próxima") or contains(@aria-label,"Next")]'
                try:
                    next_button = self.page.wait_for_selector(next_selector, timeout=5000)
                    if next_button.is_enabled():
                        print("Indo para a próxima página de resultados...")
                        next_button.click()
                        self.page.wait_for_timeout(2000)
                    else:
                        print("Botão de próxima página está desabilitado. Fim da navegação.")
                        break
                except Exception:
                    print("Não encontrou botão de próxima página. Fim da navegação.")
                    break
        print(f"\nTotal de convites enviados em {current_page} página(s): {total_sent}")

    @staticmethod
    def _get_key_path():
        return os.path.join(str(Path.home()), '.linkedin_key')

    @staticmethod
    def _get_credentials_path():
        return os.path.join(str(Path.home()), '.linkedin_credentials')

    @staticmethod
    def _create_key():
        key = Fernet.generate_key()
        with open(LinkedInLogin._get_key_path(), 'wb') as key_file:
            key_file.write(key)
        return key

    @staticmethod
    def _load_key():
        try:
            with open(LinkedInLogin._get_key_path(), 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            return LinkedInLogin._create_key()

    def _encrypt_credentials(self, email, password):
        key = self._load_key()
        f = Fernet(key)
        credentials = {
            'email': email,
            'password': password
        }
        encrypted_data = f.encrypt(json.dumps(credentials).encode())
        with open(self._get_credentials_path(), 'wb') as file:
            file.write(encrypted_data)

    def _decrypt_credentials(self):
        try:
            key = self._load_key()
            f = Fernet(key)
            with open(self._get_credentials_path(), 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = f.decrypt(encrypted_data)
            credentials = json.loads(decrypted_data.decode())
            return credentials['email'], credentials['password']
        except Exception:
            return None, None

    def _has_saved_credentials(self):
        return os.path.exists(self._get_credentials_path())

    @staticmethod
    def get_credentials():
        from getpass import getpass
        instance = LinkedInLogin("", "")  # Instância temporária para acessar os métodos
        
        if instance._has_saved_credentials():
            use_saved = input("Credenciais salvas encontradas. Deseja utilizá-las? (s/n): ").lower()
            if use_saved == 's':
                email, password = instance._decrypt_credentials()
                if email and password:
                    print("Credenciais recuperadas com sucesso!")
                    return email, password
                print("Erro ao recuperar credenciais salvas.")

        email = input("Digite seu email do LinkedIn: ")
        password = getpass("Digite sua senha do LinkedIn: ")
        save_credentials = input("Deseja salvar estas credenciais para uso futuro? (s/n): ").lower()
        
        if save_credentials == 's':
            instance._encrypt_credentials(email, password)
            print("Credenciais salvas com sucesso!")
            
        return email, password
