from playwright.sync_api import sync_playwright
import time

class LinkedInLogin:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.browser = None
        self.page = None

    def start_browser(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()

    def login(self):
        print("Acessando LinkedIn...")
        self.page.goto("https://www.linkedin.com/login")
        self.page.fill('input[name="session_key"]', self.email)
        self.page.fill('input[name="session_password"]', self.password)
        self.page.click('button[type="submit"]')
        print("Login realizado!")

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
            print("Procurando botão de localidade pelo ID 'searchFilter_geoUrn'...")
            location_button = self.page.wait_for_selector('button#searchFilter_geoUrn', timeout=7000)
            location_button.click()
            self.page.wait_for_timeout(1200)

            for loc in locations:
                loc = loc.strip()
                print(f"Digitando localidade: {loc}")
                # O campo é um <input> com placeholder "Add a location" ou "Adicionar uma localização"
                # Vamos pegar o primeiro input visível, não hidden
                input_selectors = [
                    'input[placeholder="Add a location"]',
                    'input[placeholder="Adicionar uma localização"]',
                    'input[aria-label="Add a location"]',
                    'input[aria-label="Adicionar uma localização"]',
                ]
                location_input = None
                for sel in input_selectors:
                    try:
                        location_input = self.page.query_selector(sel)
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

                # Busca opções de autocomplete
                options = self.page.query_selector_all(
                    '//div[contains(@class,"basic-typeahead__selectable")]//span[contains(@class,"search-typeahead-v2__hit-text")]'
                )

                found = False
                for opt in options:
                    option_text = opt.inner_text().strip()
                    if option_text.lower() == loc.lower():
                        print(f"Selecionando local: {option_text}")
                        opt.click()
                        found = True
                        self.page.wait_for_timeout(800)
                        break
                if not found:
                    if options:
                        print(f"Localização '{loc}' não encontrada exatamente. Selecionando primeira opção: {options[0].inner_text().strip()}")
                        options[0].click()
                        self.page.wait_for_timeout(800)
                    else:
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
            try:
                company_button = self.page.wait_for_selector('button#searchFilter_currentCompany', timeout=5000)
            except Exception:
                try:
                    company_button = self.page.wait_for_selector('//button[contains(.,"Empresas atuais") or contains(.,"Current companies") or contains(.,"Empresas") or contains(.,"Companies")]', timeout=5000)
                except Exception:
                    print("Botão de filtro de empresa não encontrado.")
                    return
            company_button.click()
            self.page.wait_for_timeout(1500)

            for company in companies:
                company = company.strip()
                print(f"Digitando empresa: {company}")
                input_xpath = '//input[contains(@placeholder, "Adicionar uma empresa") or contains(@placeholder, "Add a company")]'
                company_input = self.page.wait_for_selector(input_xpath, timeout=4000)
                company_input.fill("")
                company_input.fill(company)
                self.page.wait_for_timeout(1500)

                option_xpath = f'//li//span[text()="{company}"]'
                try:
                    company_option = self.page.wait_for_selector(option_xpath, timeout=4000)
                    company_option.click()
                    print(f"Empresa '{company}' aplicada.")
                except Exception:
                    print(f"Não encontrou sugestão para a empresa: {company}")
                    continue
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
