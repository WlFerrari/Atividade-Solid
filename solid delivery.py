"""
Sistema de Delivery — Aplicando os Princípios SOLID
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


# =============================================================================
# 1. SINGLE RESPONSIBILITY PRINCIPLE (SRP)
#    Cada classe tem uma única responsabilidade bem definida.
# =============================================================================

@dataclass
class Pedido:
    """Representa um pedido — apenas armazena os dados."""
    id: int
    cliente: str
    itens: List[str]
    total: float
    data: datetime = field(default_factory=datetime.now)


class PedidoRepository:
    """Responsável por salvar e recuperar pedidos (persistência)."""

    def __init__(self):
        self._pedidos: List[Pedido] = []

    def salvar(self, pedido: Pedido) -> None:
        self._pedidos.append(pedido)
        print(f"[Repository] Pedido #{pedido.id} salvo com sucesso.")

    def buscar_por_id(self, id: int) -> Pedido | None:
        return next((p for p in self._pedidos if p.id == id), None)


class PedidoDisplay:
    """Responsável por exibir as informações de um pedido (apresentação)."""

    def exibir(self, pedido: Pedido) -> None:
        print("\n===== INFORMAÇÕES DO PEDIDO =====")
        print(f"  ID      : #{pedido.id}")
        print(f"  Cliente : {pedido.cliente}")
        print(f"  Itens   : {', '.join(pedido.itens)}")
        print(f"  Total   : R$ {pedido.total:.2f}")
        print(f"  Data    : {pedido.data.strftime('%d/%m/%Y %H:%M')}")
        print("=================================\n")


# =============================================================================
# 2. OPEN/CLOSED PRINCIPLE (OCP)
#    Novas formas de pagamento podem ser adicionadas sem alterar o código
#    existente — basta criar uma nova subclasse de MetodoPagamento.
# =============================================================================

class MetodoPagamento(ABC):
    """Abstração base para formas de pagamento."""

    @abstractmethod
    def processar(self, valor: float) -> None:
        pass


class PagamentoCartao(MetodoPagamento):
    def processar(self, valor: float) -> None:
        print(f"[Pagamento] Cartão processado: R$ {valor:.2f}")


class PagamentoPix(MetodoPagamento):
    def processar(self, valor: float) -> None:
        print(f"[Pagamento] PIX enviado: R$ {valor:.2f}")


class PagamentoDinheiro(MetodoPagamento):
    def processar(self, valor: float) -> None:
        print(f"[Pagamento] Dinheiro recebido: R$ {valor:.2f}")


# Exemplo de extensão FUTURA — não altera nada acima:
class PagamentoCriptomoeda(MetodoPagamento):
    def processar(self, valor: float) -> None:
        print(f"[Pagamento] Criptomoeda transferida: R$ {valor:.2f}")


class ProcessadorPagamento:
    """Usa qualquer MetodoPagamento sem conhecer a implementação concreta."""

    def pagar(self, metodo: MetodoPagamento, valor: float) -> None:
        metodo.processar(valor)


# =============================================================================
# 3. LISKOV SUBSTITUTION PRINCIPLE (LSP)
#    Subclasses podem substituir a classe base sem comportamentos incorretos.
# =============================================================================

class Produto:
    """Classe base de produto."""

    def __init__(self, nome: str, preco: float):
        self.nome = nome
        self.preco = preco

    def descricao(self) -> str:
        return f"{self.nome} — R$ {self.preco:.2f}"

    def esta_disponivel(self) -> bool:
        return True


class Pizza(Produto):
    def __init__(self, nome: str, preco: float, tamanho: str):
        super().__init__(nome, preco)
        self.tamanho = tamanho

    def descricao(self) -> str:
        return f"Pizza {self.nome} ({self.tamanho}) — R$ {self.preco:.2f}"


class Hamburguer(Produto):
    def __init__(self, nome: str, preco: float, ingredientes: List[str]):
        super().__init__(nome, preco)
        self.ingredientes = ingredientes

    def descricao(self) -> str:
        return (f"Hamburguer {self.nome} "
                f"[{', '.join(self.ingredientes)}] — R$ {self.preco:.2f}")


class Bebida(Produto):
    def __init__(self, nome: str, preco: float, volume_ml: int):
        super().__init__(nome, preco)
        self.volume_ml = volume_ml

    def descricao(self) -> str:
        return f"Bebida {self.nome} ({self.volume_ml}ml) — R$ {self.preco:.2f}"


def exibir_produto(produto: Produto) -> None:
    """Funciona com qualquer subclasse de Produto — LSP garantido."""
    print(f"  - {produto.descricao()} | Disponível: {produto.esta_disponivel()}")


# =============================================================================
# 4. INTERFACE SEGREGATION PRINCIPLE (ISP)
#    Interfaces pequenas e específicas — nenhuma classe implementa métodos
#    que não utiliza.
# =============================================================================

class INotificavel(ABC):
    @abstractmethod
    def enviar_notificacao(self, mensagem: str) -> None:
        pass


class IRelatorio(ABC):
    @abstractmethod
    def gerar_relatorio(self) -> str:
        pass


class IGerenciadorPedido(ABC):
    @abstractmethod
    def criar_pedido(self, pedido: Pedido) -> None:
        pass

    @abstractmethod
    def cancelar_pedido(self, pedido_id: int) -> None:
        pass


class IGerenciadorEntrega(ABC):
    @abstractmethod
    def despachar_entrega(self, pedido: Pedido) -> None:
        pass

    @abstractmethod
    def rastrear_entrega(self, pedido_id: int) -> str:
        pass


# Classes implementam apenas as interfaces que realmente precisam:

class ServicoNotificacao(INotificavel):
    def enviar_notificacao(self, mensagem: str) -> None:
        print(f"[Notificação] {mensagem}")


class ServicoRelatorio(IRelatorio):
    def gerar_relatorio(self) -> str:
        relatorio = "[Relatório] Resumo diário de pedidos gerado."
        print(relatorio)
        return relatorio


class GerenciadorPedido(IGerenciadorPedido):
    def criar_pedido(self, pedido: Pedido) -> None:
        print(f"[Gerenciador] Pedido #{pedido.id} criado para {pedido.cliente}.")

    def cancelar_pedido(self, pedido_id: int) -> None:
        print(f"[Gerenciador] Pedido #{pedido_id} cancelado.")


class GerenciadorEntrega(IGerenciadorEntrega):
    def despachar_entrega(self, pedido: Pedido) -> None:
        print(f"[Entrega] Pedido #{pedido.id} despachado.")

    def rastrear_entrega(self, pedido_id: int) -> str:
        status = f"[Entrega] Pedido #{pedido_id} — Em rota de entrega."
        print(status)
        return status


# =============================================================================
# 5. DEPENDENCY INVERSION PRINCIPLE (DIP)
#    A classe principal depende de abstrações, não de implementações concretas.
# =============================================================================

class ICanal(ABC):
    """Abstração para qualquer canal de notificação."""

    @abstractmethod
    def enviar(self, destinatario: str, mensagem: str) -> None:
        pass


class CanalEmail(ICanal):
    def enviar(self, destinatario: str, mensagem: str) -> None:
        print(f"[E-mail] Para: {destinatario} | Mensagem: {mensagem}")


class CanalSMS(ICanal):
    def enviar(self, destinatario: str, mensagem: str) -> None:
        print(f"[SMS] Para: {destinatario} | Mensagem: {mensagem}")


class CanalWhatsApp(ICanal):
    def enviar(self, destinatario: str, mensagem: str) -> None:
        print(f"[WhatsApp] Para: {destinatario} | Mensagem: {mensagem}")


class SistemaNotificacao:
    """Depende apenas da abstração ICanal — DIP garantido."""

    def __init__(self, canal: ICanal):
        self._canal = canal

    def notificar(self, destinatario: str, mensagem: str) -> None:
        self._canal.enviar(destinatario, mensagem)


# =============================================================================
# DEMONSTRAÇÃO
# =============================================================================

if __name__ == "__main__":

    print("=" * 60)
    print("  1. SRP — Single Responsibility Principle")
    print("=" * 60)

    pedido = Pedido(id=1, cliente="Ana Lima",
                    itens=["Pizza Margherita", "Coca-Cola"], total=62.90)
    repo = PedidoRepository()
    display = PedidoDisplay()

    repo.salvar(pedido)
    display.exibir(pedido)

    print("=" * 60)
    print("  2. OCP — Open/Closed Principle")
    print("=" * 60)

    processador = ProcessadorPagamento()
    processador.pagar(PagamentoCartao(), pedido.total)
    processador.pagar(PagamentoPix(), pedido.total)
    processador.pagar(PagamentoDinheiro(), pedido.total)
    processador.pagar(PagamentoCriptomoeda(), pedido.total)  # extensão futura

    print("=" * 60)
    print("  3. LSP — Liskov Substitution Principle")
    print("=" * 60)

    produtos: List[Produto] = [
        Pizza("Margherita", 45.00, "Grande"),
        Hamburguer("Clássico", 28.00, ["Carne", "Queijo", "Alface"]),
        Bebida("Coca-Cola", 8.00, 350),
    ]

    print("Cardápio:")
    for p in produtos:
        exibir_produto(p)

    print()
    print("=" * 60)
    print("  4. ISP — Interface Segregation Principle")
    print("=" * 60)

    ServicoNotificacao().enviar_notificacao("Pedido #1 confirmado!")
    ServicoRelatorio().gerar_relatorio()
    GerenciadorPedido().criar_pedido(pedido)
    GerenciadorPedido().cancelar_pedido(99)
    GerenciadorEntrega().despachar_entrega(pedido)
    GerenciadorEntrega().rastrear_entrega(pedido.id)

    print()
    print("=" * 60)
    print("  5. DIP — Dependency Inversion Principle")
    print("=" * 60)

    canais: List[ICanal] = [CanalEmail(), CanalSMS(), CanalWhatsApp()]
    for canal in canais:
        sistema = SistemaNotificacao(canal)
        sistema.notificar("ana@email.com", "Seu pedido está a caminho!")
