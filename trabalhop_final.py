import tkinter as tk
import pyautogui
import time

# Inicializa o canvas da segunda página
optativa_canvas = None

class Materias:
    def __init__(self, nome, creditos, codigo, prerequisitos):
        """
        Inicializa os parametros do objeto

        Args:
            nome (string): nome da materia
            creditos (int): quantidade de credito
            codigo (string): codigo da materia
            prerequisitos (tuple): pre-requesitos da materia
        """
        self.nome = nome
        self.creditos = creditos
        self.codigo = codigo
        self.prerequisitos = prerequisitos
        self.rect_id = None  # Armazena o ID do retângulo desenhado no canvas

    def set_rect_id(self, rect_id):
        """
        Cria uma identificacao para o retangulo

        Args:
            rect_id (string): identificacao do retangulo
        """
        self.rect_id = rect_id

    def get_nome(self):
        """
        Acessar o parametro nome

        Returns:
            string: nome da materia
        """
        return self.nome
    
    def get_prerequisitos(self):
        """
        Acessar o parametro pre-requesitos

        Returns:
            string: pre-requesitos da materia
        """
        return self.prerequisitos

    def get_rect_id(self):
        """
        Acessar o parametro de identificacao do retangulo

        Returns:
            string: identificacao do retangulo
        """
        return self.rect_id
    
    def get_codigo(self):
        """
        Acessar o parametro codigo

        Returns:
            string: codigo da materia
        """
        return self.codigo


    def all_prerequisites_yellow(self, canvas, lista):
        """
        Percorre os pre-requesitos do objeto, comparando com os itens dentro do parametro lista.
        Se algum dos itens nao estiver pintado de amarelo, retorna Falso.
        Se percorrer a lista até o final, retorna True.

        Args:
            canvas (object): interface onde ocorrera a verificacao
            lista (tuple): objeto que sera verificado

        Returns:
            bool: retorna True se todos os pre-requesitos do objeto atual estiverem amarelos
        """
        for prereq in self.prerequisitos:
            for materia in lista:
                if materia.codigo == prereq and canvas.itemcget(materia.rect_id, "fill") != "lightyellow":
                    return False
        return True

    def paint_dependents_green_materias(self, canvas1, canvas2):
        """
        Percorre as tuplas de materiais e de optativas, verificando se o objeto atual é pre-requesito de algum item.
        Se for pre-requesito e todos os pre-requesitos do item estiverem amarelo, o item é pintado de verde.

        Args:
            canvas1 (object): interface de materiais
            canvas2 (object): interface de optativas
        """
        for materia in materias:
            if self.codigo in materia.prerequisitos and materia.all_prerequisites_yellow(canvas1, materias):
                canvas1.itemconfig(materia.rect_id, fill="lightgreen")
        for optativa in optativas:
            if self.codigo in optativa.prerequisitos and optativa.all_prerequisites_yellow(canvas2, optativas) and optativa.all_prerequisites_yellow(canvas1, materias):
                canvas2.itemconfig(optativa.rect_id, fill="lightgreen")

    def paint_dependents_gray_materias(self, canvas1, canvas2, visited=None):
        """
        Percorre as tuplas de materiais e de optativas, verificando se o objeto atual é pre-requesito de algum item.
        Se for pré-requisito e o item ainda não tiver sido visitado, pinta o item de cinza e realiza a mesma verificação para esse item.

        Args:
            canvas1 (object): interface de materiais
            canvas2 (object): interface de optativas
            visited (set, optional): conjunto de itens visitados. Defaults to None.
        """
        if visited is None:
            visited = set()
        visited.add(self.rect_id)
        for materia in materias:
            if self.codigo in materia.prerequisitos and materia.rect_id not in visited:
                canvas1.itemconfig(materia.rect_id, fill="lightgray")
                materia.paint_dependents_gray_materias(canvas1, canvas2, visited)
        for optativa in optativas:
            if self.codigo in optativa.prerequisitos and optativa.rect_id not in visited:
                canvas2.itemconfig(optativa.rect_id, fill="lightgray")
                optativa.paint_dependents_gray_materias(canvas1, canvas2, visited)

class Optativas(Materias):
    def paint_dependents_green(self, canvas):
        """
        Percorre a tupla optativas, verificando se o objeto atual é pre-requesito de algum item.
        Se for pre-requesito e todos os pre-requesitos do item estiverem amarelo, o item é pintado de verde.

        Args:
            canvas (object): interface onde ocorre a verificacao e as mudancas
        """
        for optativa in optativas:
            if self.codigo in optativa.prerequisitos and optativa.all_prerequisites_yellow(canvas, optativas):
                canvas.itemconfig(optativa.rect_id, fill="lightgreen")

    def paint_dependents_gray(self, canvas, visited=None):
        """
        Percorre a tuplas optativas, verificando se o objeto atual é pre-requesito de algum item.
        Se for pré-requisito e o item ainda não tiver sido visitado, pinta o item de cinza e realiza a mesma verificação para esse item.

        Args:
            canvas (object): _description_
            visited (set, optional): conjunto de itens visitados. Defaults to None.
        """
        if visited is None:
            visited = set()
        visited.add(self.rect_id)
        for optativa in optativas:
            if self.codigo in optativa.prerequisitos and optativa.rect_id not in visited:
                canvas.itemconfig(optativa.rect_id, fill="lightgray")
                optativa.paint_dependents_gray(canvas, visited)

# Definindo as matérias como objetos da classe Materias
materias = [


    # Lista que recebe os dados das diciplinas no objeto, tem a seguinte estrutura de dados:
    # Materias("Nome da diciplina",Numero de creditos,"codigo da diciplina",["pré-requisitos"])
    # Nome da diciplina     -> string
    # Numero de cretos      -> int
    # Codigo da diciplina   -> string
    # ["pré-requisitos"]    -> lista




    Materias("Introdução à Informática para Automação", 4, "DAS5334", []),
    Materias("Desenho Técnico para Automação", 4, "EGR5606", []),
    Materias("Conservação de Recursos Naturais", 4, "ECZ5102", []),
    Materias("Introdução à Engenharia de Controle e Automação", 4, "DAS5412", []),
    Materias("Física I", 4, "FSC5101", []),
    Materias("Cálculo 1", 4, "MTM3110", []),

    Materias("Fundamentos da Estrutura da Informação", 4, "DAS5102", ["DAS5334"]),
    Materias("Física Experimental I", 3, "FSC5122", ["FSC5101"]),
    Materias("Física II", 4, "FSC5002", ["FSC5101","MTM3110"]),
    Materias("Álgebra Linear", 4, "MTM3121", []),
    Materias("Cálculo 2", 4, "MTM3120", ["MTM3110"]),
    Materias("Circuitos e Técnicas Digitais", 5, "EEL5105", ["DAS5334"]),

    Materias("Arquitetura e Programação de Sistemas Microcontrolados", 4, "DAS5332", ["EEL5105"]),
    Materias("Física III", 4, "FSC5113", ["FSC5002"]),
    Materias("Introdução ao Controle de Processos", 3, "DAS5210", ["DAS5412","FSC5101","MTM3110"]),
    Materias("Equações Diferenciais Ordinárias", 4, "MTM3131", ["MTM3121","MTM3120"]),
    Materias("Cálculo 3", 4, "MTM3103", ["MTM3120"]),
    Materias("Mecânica dos Sólidos I", 5, "ECV5215", ["FSC5002","MTM3120"]),

    Materias("Programação de Sistemas Automatizados", 4, "DAS5308", ["DAS5102","DAS5332"]),
    Materias("Sistemas de Automação Discreta", 4, "DAS5307", ["DAS5412","EEL5105"]),
    Materias("Sinais e Sistemas Lineares", 4, "DAS5214", ["DAS5210","MTM3131"]),
    Materias("Cálculo Numérico para Controle e Automação", 4, "DAS5103", ["DAS5102","MTM3121","MTM3110"]),
    Materias("Estatística e Probabilidade para Ciências Exatas", 3, "INE5108", ["MTM3110"]),
    Materias("Circuitos Elétricos para Automação", 4, "EEL7540", ["FSC5113","MTM3131"]),

    Materias("Metodologia para Desenvolvimento de Sistemas", 4, "DAS5320", ["DAS5308"]),
    Materias("Modelagem e Controle de Sistemas a Eventos Discretos", 5, "DAS5203", ["DAS5307"]),
    Materias("Modelagem e Simulação de Processos", 4, "DAS5109", ["DAS5214","EEL7540"]),
    Materias("Fenômenos de Transporte", 4, "EMC5425", ["FSC5002","MTM3103"]),
    Materias("Metrologia Industrial", 3, "EMC5235", ["EEL7540"]),
    Materias("Eletrônica Aplicada", 4, "EEL7550", ["EEL7540"]),

    Materias("Redes de Computadores para Automação", 4, "DAS5314", ["DAS5308","DAS5307"]),
    Materias("Gerenciamento de Projetos", 3, "EPS2351", ["ECZ5102","INE5108"]),
    Materias("Aspectos Econômicos e Sociais para Automação", 4, "CNM7820", []),
    Materias("Instrumentação em Controle", 4, "DAS5151", ["DAS5109","EMC5425","EEL7550"]),
    Materias("Sistemas de Controle", 4, "DAS5120", ["DAS5109"]),
    Materias("Acionamentos Hidráulicos e Pneumáticos para Automação", 4, "EMC5467", ["EMC5425","DAS5307","DAS5214"]),
    Materias("Máquinas e Acionamentos Elétricos para Automação", 3, "EEL5193", ["EEL7540"]),

    Materias("Introdução à Automação da Manufatura", 6, "EMC5258", ["DAS5307"]),
    Materias("Introdução à Robótica Industrial", 4, "EMC5251", ["DAS5214"]),
    Materias("Avaliação de Desempenho de Processos de Sistemas Organizacionais", 4, "DAS5318", ["DAS5203","INE5108"]),
    Materias("Projeto Integrador", 6, "DAS5105", ["DAS5314","DAS5320","EPS2351","DAS5203","DAS5151","DAS5120"]),
    Materias("Sistemas Dinâmicos", 4, "DAS5142", ["DAS5120"]),

    Materias("Ética e Aspectos de Segurança em Sistemas de Controle e Automação", 2, "DAS5402", []),
    Materias("Gestão Econômica de Investimentos", 3, "EPS7076", []),
    Materias("Estágio em Controle e Automação", 12, "DAS5502", []),

    Materias("Projeto de Fim de Curso", 19, "DAS5512", ["DAS5502"])
]

optativas = [


    # Lista que recebe os dados das diciplinas no objeto, tem a seguinte estrutura de dados:
    # Optativas("Nome da diciplina",Numero de creditos,"codigo da diciplina",["pré-requisitos"])
    # Nome da diciplina     -> string
    # Numero de cretos      -> int
    # Codigo da diciplina   -> string
    # ["pré-requisitos"]    -> lista
        
    Optativas("Controle Multivariável", 4, "DAS5131", ["DAS5120"]),
    Optativas("Programação Concorrente e Sistemas de Tempo Real", 4, "DAS5306", ["DAS5308"]),
    Optativas("Sistemas Distribuídos para Automação", 3, "DAS5315", ["DAS5314"]),
    Optativas("Integração de Sistemas Industriais e Empresariais", 4, "DAS5319", ["DAS5314", "DAS5320"]),
    Optativas("Inteligência Artificial Aplicada a Controle e Automação", 4, "DAS5341", []),
    Optativas("Processamento de Sinais", 4, "DAS5520", ["DAS5214"]),
    Optativas("Tópicos especiais em Controle: Introdução à Identificação e ao Controle Adaptativo", 3, "DAS5901", ["DAS5120"]),
    Optativas("Tópicos Especiais em Informática Industrial", 3, "DAS5921", ["DAS5214","DAS5314"]),
    Optativas("Tópicos Especiais em Controle: Instrumentação Aplicada à Industria de Petróleo e Gás", 3, "DAS5944", ["DAS5214","EEL7550"]),
    Optativas("Tópicos Especiais em Controle: Técnicas de Controle Aplicadas à Indústria de Petróleo e Gás", 3, "DAS5945", ["DAS5120"]),
    Optativas("Tópicos Especiais em Controle e Automação: Introdução à Engenharia do Petróleo e Gás", 3, "DAS5946", ["DAS5214"]),
    Optativas("Tópicos Especiais em Controle e Automação:  Introdução ao Controle para Indústria do Petróleo e Gás", 3, "DAS5947", ["DAS5214"]),
    Optativas("Tópicos Especiais em Controle: Seminário para à Industria do Petróleo e Gás", 3, "DAS5948", ["DAS5214"]),
    Optativas("Instrumentação Biomédica", 4, "EEL7125", []),
    Optativas("Introdução a Informática Médica", 4, "EEL7307", []),
    Optativas("Engenharia Clínica para Uso Médico", 4, "EEL7324", []),
    Optativas("Fundamentos de Engenharia Biomédica", 4, "EEL7885", []),
    Optativas("Felicidade e Bem-Estar no Ambiente Acadêmico", 4, "EGC5037", []),
    Optativas("Mecanismos", 3, "EMC5123", ["MTM3120","MTM3121"]),
    Optativas("Tecnologia de Comando Numérico", 4, "EMC5219", []),
    Optativas("Automação de Processos de Soldagem", 3, "EMC5227", []),
    Optativas("Administração de Operações de Manufatura", 3, "EMC5246", ["EMC5258"]),
    Optativas("Introdução ao Projeto Manufatura-computador", 4, "EMC5301", []),
    Optativas("Trocadores de Calor", 3, "EMC5415", []),
    Optativas("Projeto de Sistemas Térmicos", 3, "EMC5444", []),
    Optativas("Computação Quântica I", 4, "FSC7152", ["MTM3121"]),
    Optativas("Grafos", 4, "INE5413", []),
    Optativas("Banco de Dados I", 4, "INE5423", ["DAS5102"]),
    Optativas("Bancos de Dados II", 4, "INE5616", []),
    Optativas("Bancos de Dados III", 2, "INE5600", []),
    Optativas("Reconhecimentos de Padrões", 4, "INE5443", ["DAS5102"]),
    Optativas("Tópicos Especiais em Aplicações Tecnológicas I", 4, "INE5448", []),
    Optativas("Testes de Software", 4, "INE5455", ["DAS5320"]),
    Optativas("Sistemas Inteligentes", 4, "INE5633", []),
    Optativas("Data Warehouse", 4, "INE5642", []),
    Optativas("Data Mining", 4, "INE5644", []),
    Optativas("Técnicas Estatísticas de Predição", 4, "INE5649", []),
    Optativas("Modelagem e Automação de Processos de Negócios", 4, "INE5681", ["DAS5320"]),
    Optativas("Relações Inter-étnicas", 4, "ANT7003", []),
    Optativas("Felicidade e Bem-Estar no Ambiente Acadêmico", 3, "EGC5037", []),
    Optativas("História e Evolução do Design", 3, "EGR5037", []),
    Optativas("Língua Brasileira de Sinais - Libras I (PCC18h-a)", 4, "LSB7244", []),
    Optativas("H-Cálculo 1", 6, "MTM5801", []),
    Optativas("H-Cálculo 2", 6, "MTM5802", ["MTM5801"]),
    Optativas("H-Cálculo 3", 6, "MTM5803", ["MTM5802"]),
    Optativas("H-Cálculo 4", 6, "MTM5804", ["MTM5803"]),
    Optativas("H-Álgebra Linear II", 6, "MTM5812", ["MTM5801"]),
    Optativas("H-Álgebra Linear III", 6, "MTM5813", ["MTM5812"]),
    Optativas("H-Análise Linear", 6, "MTM5814", ["MTM5813"])
]



# Definindo a posição das matérias na tela
positions = {

    # dicionário que relaciona o codigo da diciplina com a posição grafica impressa no tkinters:
    # Chave:(x,y)
    #
    # Chave -> string
    # x     -> int
    # y     -> int
        
    # 1ª Fase
    "DAS5334": (35, 50),
    "EGR5606": (35, 160),
    "ECZ5102": (35, 270),
    "DAS5412": (35, 380),
    "FSC5101": (35, 490),
    "MTM3110": (35, 600),

    # 2ª Fase
    "DAS5102": (185, 50),
    "FSC5122": (185, 160),
    "FSC5002": (185, 270),
    "MTM3121": (185, 380),
    "MTM3120": (185, 490),
    "EEL5105": (185, 600),

    # 3ª Fase
    "DAS5332": (335, 50),
    "FSC5113": (335, 160),
    "DAS5210": (335, 270),
    "MTM3131": (335, 380),
    "MTM3103": (335, 490),
    "ECV5215": (335, 600),

    # 4ª Fase
    "DAS5308": (485, 50),
    "DAS5307": (485, 160),
    "DAS5214": (485, 270),
    "DAS5103": (485, 380),
    "INE5108": (485, 490),
    "EEL7540": (485, 600),

    # 5ª Fase
    "DAS5320": (635, 50),
    "DAS5203": (635, 160),
    "DAS5109": (635, 270),
    "EMC5425": (635, 380),
    "EMC5235": (635, 490),
    "EEL7550": (635, 600),

    # 6ª Fase
    "DAS5314": (785, 50),
    "EPS2351": (785, 160),
    "CNM7820": (785, 270),
    "DAS5151": (785, 380),
    "DAS5120": (785, 490),
    "EMC5467": (785, 600),
    "EEL5193": (785, 710),

    # 7ª Fase
    "EMC5258": (935, 50),
    "EMC5251": (935, 160),
    "DAS5318": (935, 270),
    "DAS5105": (935, 380),
    "DAS5142": (935, 490),
    "EEL5354": (935, 600),

    # 8ª Fase
    "DAS5402": (1085, 50),
    "EPS7076": (1085, 160),
    "OPT0003": (1085, 270),
    "DAS5502": (1085, 380),

    # 10ª Fase
    "DAS5512": (1385, 50),

    # Títulos
    "1ª Fase": (35, 25),
    "2ª Fase": (185, 25),
    "3ª Fase": (335, 25),
    "4ª Fase": (485, 25),
    "5ª Fase": (635, 25),
    "6ª Fase": (785, 25),
    "7ª Fase": (935, 25),
    "8ª Fase": (1085, 25),
    "9ª Fase": (1235, 25),
    "10ª Fase": (1385, 25),

    # Optativas Profissionalizantes
    "DAS5131": (20, 25),
    "DAS5306": (20, 75),
    "DAS5315": (20, 125),
    "DAS5319": (20, 175),
    "DAS5341": (20, 225),
    "DAS5520": (20, 275),
    "DAS5901": (20, 325),
    "DAS5921": (20, 375),
    "DAS5944": (20, 425),
    "DAS5945": (20, 475),
    "DAS5946": (20, 525),
    "DAS5947": (20, 575),
    
    "DAS5948": (415, 25),
    "EEL7125": (415, 75),
    "EEL7307": (415, 125),
    "EEL7324": (415, 175),
    "EEL7885": (415, 225),
    "EGC5037": (415, 275),
    "EMC5123": (415, 325),
    "EMC5219": (415, 375),
    "EMC5227": (415, 425),
    "EMC5246": (415, 475),
    "EMC5301": (415, 525),
    "EMC5415": (415, 575),
    
    "EMC5444": (810, 25),
    "FSC7152": (810, 75),
    "INE5413": (810, 125),
    "INE5423": (810, 175),
    "INE5616": (810, 225),
    "INE5600": (810, 275),
    "INE5443": (810, 325),
    "INE5448": (810, 375),
    "INE5455": (810, 425),
    "INE5633": (810, 475),
    "INE5642": (810, 525),
    "INE5644": (810, 575),
    
    "INE5649": (1205, 25),
    "INE5681": (1205, 75),
    
    # Optativas livres
    "ANT7003": (1205, 125),
    "EGR5037": (1205, 175),
    "LSB7244": (1205, 225),
    "MTM5801": (1205, 275),
    "MTM5802": (1205, 325),
    "MTM5803": (1205, 375),
    "MTM5804": (1205, 425),
    "MTM5812": (1205, 475),
    "MTM5813": (1205, 525),
    "MTM5814": (1205, 575)   
}

#----------------------------------------------
# Função para criar o botão OPTATIVAS no canvas
def create_button_optativas(x, y, canva_materias):
    """
    Cria um botão de materias optativas, que lista as matérias optativas de interesse.

    Args:
        x (int): Coordenada x da posição do botão Print
        y (int): Coordenada y da posição do botão Print
        canva_materias (tk.Canvas): Canvas onde o botão será desenhado
    Returns:
                rect_optativa: codigo da diciplina
                text_optativa: nome da optativa
                optativa_canvas: canvas das optativas
    """
    text = f"OPTATIVAS"
    fill_color = "orange" 
    rect_optativa = canva_materias.create_rectangle(x, y, x + 130, y + 100, fill=fill_color, outline="black")
    text_optativa = canva_materias.create_text(x + 65, y + 50, text=text, fill="white", font=("Arial", 12), width=120)

    # Criando uma nova janela quando clicado o botão OPTATIVAS
    def create_window_optativas(event):
        """
        Cria uma nova janela listando as matérias que foram selecionadas como de interesse.

        Args:
            event (tk.Event): Evento que acionou a função
        Returns:
            tk.Tk: Uma janela secundária que lista as matérias que foram selecionadas como de interesse na janela de optativas
        """
        global optativa_canvas
        optativa_window = tk.Tk()
        optativa_window.title("Matérias Optativas")

        # Frame para segurar o canvas
        optativa_frame = tk.Frame(optativa_window)
        optativa_frame.pack(fill=tk.BOTH, expand=1)

        # Canvas para desenhar o fluxograma
        optativa_canvas = tk.Canvas(optativa_frame, width=1600, height=650, bg="white", scrollregion=(0, 0, 1900, 1575))
        optativa_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Função para lidar com cliques nos blocos das matérias
        def on_block_click_optativas(event):
            """
            Função para lidar com cliques nos blocos das matérias no canvas das optativas.
            Analisa cada cor de cada matéria e no momento do click atualiza para a nova cor de acordo com o os pré-requisitos da materia.

            Args:
                event (event): click do mouse no bloco
            """
            item = optativa_canvas.find_withtag("current")[0]
            tags = optativa_canvas.gettags(item)
            rect_id = None
            for tag in tags:
                if tag.startswith("rect_"):
                    rect_id = tag.split("_")[1]
                    break
            if rect_id:
                current_color = optativa_canvas.itemcget(rect_id, "fill")
                new_color = ""
                if current_color == "lightgray":
                    new_color = "lightgray"
                elif current_color == "lightyellow":
                    new_color = "lightblue"
                elif current_color == "lightblue":
                    new_color = "lightgreen"
                elif current_color == "lightgreen":
                    new_color = "lightyellow"

                # Se o bloco foi pintado de azul
                if new_color == "lightblue":       
                    for optativa in optativas:
                        if optativa.get_rect_id() == int(rect_id):
                            optativa.paint_dependents_gray(optativa_canvas)
                            optativa.paint_dependents_green(optativa_canvas)
                        
                # Se o bloco está mudando de amarelo para outra cor, pintar dependentes de cinza
                if current_color == "lightyellow" and new_color != "lightyellow":     
                    for optativa in optativas:
                        if optativa.get_rect_id() == int(rect_id):
                            optativa.paint_dependents_gray(optativa_canvas)

                optativa_canvas.itemconfig(rect_id, fill=new_color)

                # Verificar e pintar os blocos dependentes de verde se o bloco foi pintado de amarelo
                if new_color == "lightyellow":        
                    for optativa in optativas:
                        if optativa.get_rect_id() == int(rect_id):
                            optativa.paint_dependents_green(optativa_canvas)

        # Função para desenhar uma disciplina optativa no canvas
        def draw_course_optativas(x, y, optativa):
            """
            Função que desenha uma matéria no canvas.

        Args:
            x (int): Coordenada x da posição do retângulo
            y (int): Coordenada y da posição do retângulo
            optativas (Optativas): Parâmetro da classe Optativas representando o curso atual

        Returns:
            Tupla: Uma tupla contendo o ID do retângulo e o ID do texto criados no canvas.
            """
            text_optativa = f"{optativa.get_codigo()}: {optativa.get_nome()}"
            fill_color_optativa = "lightgreen" if not optativa.get_prerequisitos() else "lightgray"
            rect_optativa = optativa_canvas.create_rectangle(x, y, x + 375, y + 40, fill=fill_color_optativa, outline="black")
            text_id_optativa = optativa_canvas.create_text(x + 185, y + 20, text=text_optativa, fill="black", font=("Arial", 8), width=365)
            optativa.set_rect_id(rect_optativa)
            return rect_optativa, text_id_optativa

        # Desenhando todas as optativas profissionalizantes
        for optativa in optativas:
            x, y = positions[optativa.get_codigo()]
            rect_optativa, text_id_optativa = draw_course_optativas(x, y, optativa)
            optativa_canvas.addtag_withtag(f"rect_{rect_optativa}", rect_optativa)
            optativa_canvas.addtag_withtag(f"rect_{rect_optativa}", text_id_optativa)
            optativa_canvas.tag_bind(rect_optativa, "<Button-1>", on_block_click_optativas)
            optativa_canvas.tag_bind(text_id_optativa, "<Button-1>", on_block_click_optativas)
            
        return optativa_canvas
            
    # Adicionando uma tag para identificar o botão OPTATIVAS
    canva_materias.addtag_withtag("button_optativa", rect_optativa)
    canva_materias.addtag_withtag("button_optativa", text_optativa)

    # Ligando o evento de clique ao botão OPTATIVAS
    canva_materias.tag_bind("button_optativa", "<Button-1>", create_window_optativas)

    return rect_optativa, text_optativa, optativa_canvas


#------------------------------------------
# Função para criar o botão PRINT no canvas
def create_button_print(x, y, canva_materias):
    """
    Cria um botão de impressão, que lista as matérias selecionadas como de interesse.

    Args:
        x (int): Coordenada x da posição do botão Print
        y (int): Coordenada y da posição do botão Print
        canva_materias (tk.Canvas): Canvas onde o botão será desenhado

    Returns:
        tupla: Uma tupla contendo os IDs do retângulo e do texto criados no canvas.
    """
    text = f"PRINT"
    fill_color = "red" 
    rect_print = canva_materias.create_rectangle(x, y, x + 130, y + 100, fill=fill_color, outline="black")
    text_print = canva_materias.create_text(x + 65, y + 50, text=text, fill="white", font=("Arial", 12), width=110)

    # Criando uma nova janela quando clicado o botão PRINT
    def create_window_print(event):
        """
        Cria uma nova janela listando as matérias que foram selecionadas como de interesse.

        Args:
            event (tk.Event): Evento que acionou a função
        Returns:
            tk.Tk: Uma janela secundária que lista as matérias que foram selecionadas como de interesse na janela principal
        """
        data = []
        print_window = tk.Tk()
        print_window.title("Matérias desejadas")

        # Frame para segurar o canvas
        print_frame = tk.Frame(print_window)
        print_frame.pack(fill=tk.BOTH, expand=1)

        # Canvas para desenhar o fluxograma
        print_canvas = tk.Canvas(print_frame, bg="white", scrollregion=(0, 0, 1900, 1575))
        print_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Adiciona um texto na nova janela
        y_position = 20  # Posição inicial para o texto
        for materia in materias:
            if canva_materias.itemcget(materia.rect_id, "fill") == "lightblue":
                print_canvas.create_text(50, y_position, text=f"{materia.get_codigo()}", fill="black", font=("Arial", 12), width=110)
                y_position += 23  # Incrementa a posição y para o próximo texto
                data.append(materia.get_codigo())
        
        if (optativa_canvas != None):    
            for materia in optativas:
                if optativa_canvas.itemcget(materia.rect_id, "fill") == "lightblue":
                    print_canvas.create_text(50, y_position, text=f"{materia.get_codigo()}", fill="black", font=("Arial", 12), width=110)
                    y_position += 23  # Incrementa a posição y para o próximo texto
                    data.append(materia.get_codigo())
        
        #-----------------------------------------------------BOT PARA PLOTAR NO SITE MATRUFSC----------------------------------------------------

        def locate(icon):
            """
            Essa função retorna a posição onde esta uma determinada imagem na tela, dado uma imagem em png.

            Args:
                icon (.png): "imagem" em (.png) a ser procurada.

            Returns:
                (cordenadada): (x,y) posição x e y da imagem na tela em pixels
            """
            time.sleep(1)
            while True:
                coord = pyautogui.locateOnScreen(icon,10)

                if coord == None:
                    continue
                else:
                    break
                
            return coord

        #---------------------------------------------------------abre o edge-------------------------------------------------------------------
        pyautogui.press("win")
        time.sleep(1)
        pyautogui.typewrite("edge")
        time.sleep(1)
        pyautogui.press("return")
        time.sleep(3)
        #---------------------------------------------------------entra no matrufsc-------------------------------------------------------------
        pyautogui.typewrite("https://matrufsc.caravela.club/")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(5)
        #---------------------------------------------------------procura a barra de busca------------------------------------------------------
        while True:
                st_coord = locate("barra_de_busca.png")
                if st_coord == None:
                    continue
                else:
                    break
        pyautogui.click(st_coord)
        time.sleep(1)

    #---------------------------------------------------------adiciona os codigos na barra de buscas uma por uma---------------------------------

        for i in data:
        
            print(f"Nome da diciplina: {i}")
            pyautogui.typewrite(i)
            time.sleep(1)
            pyautogui.press("enter")
            time.sleep(1)
            pyautogui.hotkey("ctrl","a")
            time.sleep(1)
            pyautogui.press("backspace")
        time.sleep(1)

    # Adicionando uma tag para identificar o botão
    canva_materias.addtag_withtag("button_print", rect_print)
    canva_materias.addtag_withtag("button_print", text_print)

    # Ligando o evento de clique ao botão
    canva_materias.tag_bind("button_print", "<Button-1>", create_window_print)

    return rect_print, text_print

# Código para criar a janela e desenhar as matérias
def create_window():
    """
    Cria a janela principal do programa e confirgura o canvas para desenhar o flucograma de matérias.

    Returns:
        tk.Tk: A janela principal do programa contendo o fluxograma
    """
    window = tk.Tk()
    window.title("Fluxograma do Curso de Engenharia de Controle e Automação - UFSC")

    # Frame para segurar o canvas
    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=1)

    # Canvas para desenhar o fluxograma
    canvas = tk.Canvas(frame, width=1550, height=850, bg="white", scrollregion=(0, 0, 1600, 1575))
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Função para lidar com cliques nos blocos
    def on_block_click(event):
        """
        Função que interpreta os cliques nos retângulos e gera suas mudanças.

        Args:
            event (tk.Event): Evento de clique no canvas que contém informações sobre o que foi clicado

        Comportamento:
        - Identifica o retângulo clicado no canvas e determina seu ID
        - Obtém a cor atual do retângulo e, com base nessa, define sua próxima cor
        - As cores podem ser:
          CINZA: Indica que, com base em seus pre-requisitos, ainda não é possível fazer a matéria
          AMARELO: Indica que a matéria já foi concluída
          AZUL: Indica interesse de cursar a matéria
        """
        item = canvas.find_withtag("current")[0]
        tags = canvas.gettags(item)
        rect_id = None
        for tag in tags:
            if tag.startswith("rect_"):
                rect_id = tag.split("_")[1]
                break
        if rect_id:
            current_color = canvas.itemcget(rect_id, "fill")
            new_color = ""
            if current_color == "lightgray":
                new_color = "lightgray"
            elif current_color == "lightyellow":
                new_color = "lightblue"
            elif current_color == "lightblue":
                new_color = "lightgreen"
            elif current_color == "lightgreen":
                new_color = "lightyellow"

            # Se o bloco foi pintado de azul
            if new_color == "lightblue":
                for materia in materias:
                    if materia.get_rect_id() == int(rect_id):
                        materia.paint_dependents_gray_materias(canvas, optativa_canvas)
                        materia.paint_dependents_green_materias(canvas, optativa_canvas)


            # Se o bloco está mudando de amarelo para outra cor, pintar dependentes de cinza
            if current_color == "lightyellow" and new_color != "lightyellow":
                for materia in materias:
                    if materia.get_rect_id() == int(rect_id):
                        materia.paint_dependents_gray_materias(canvas, optativa_canvas)

            canvas.itemconfig(rect_id, fill=new_color)

            # Verificar e pintar os blocos dependentes de verde se o bloco foi pintado de amarelo
            if new_color == "lightyellow":
                for materia in materias:
                    if materia.get_rect_id() == int(rect_id):
                        materia.paint_dependents_green_materias(canvas, optativa_canvas)

    # Função para desenhar uma disciplina no canvas
    def draw_course(x, y, materia):
        """
        Função que desenha uma matéria no canvas.

        Args:
            x (int): Coordenada x da posição do retângulo
            y (int): Coordenada y da posição do retângulo
            materia (Materias): Parâmetro da classe Materias representando o curso atual

        Returns:https://matrufsc.caravela.club/
            Tupla: Uma tupla contendo o ID do retângulo e o ID do texto criados no canvas.
        """
        text = f"{materia.get_codigo()}\n{materia.get_nome()}"
        fill_color = "lightgreen" if not materia.get_prerequisitos() else "lightgray"
        rect = canvas.create_rectangle(x, y, x + 130, y + 100, fill=fill_color, outline="black")
        text_id = canvas.create_text(x + 65, y + 50, text=text, fill="black", font=("Arial", 8), width=110)
        materia.set_rect_id(rect)
        return rect, text_id

    # Desenhando os títulos das fases
    for title, (x, y) in positions.items():
        if title.endswith("ª Fase"):
            canvas.create_text(x + 60, y, text=title, fill="black", font=("Arial", 10, "bold"))

    # Desenhando todas as disciplinas
    for materia in materias:
        x, y = positions[materia.get_codigo()]
        rect, text_id = draw_course(x, y, materia)
        canvas.addtag_withtag(f"rect_{rect}", rect)
        canvas.addtag_withtag(f"rect_{rect}", text_id)
        canvas.tag_bind(rect, "<Button-1>", on_block_click)
        canvas.tag_bind(text_id, "<Button-1>", on_block_click)

    create_button_optativas(1235,50,canvas)
    create_button_print(1235,575, canvas)

    window.mainloop()

# Criando a janela com
create_window()