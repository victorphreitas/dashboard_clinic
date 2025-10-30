"""
Modelos de banco de dados para o sistema de dashboard de clínicas estéticas.
Define as tabelas e estruturas de dados necessárias.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Cliente(Base):
    """Modelo para a tabela de clientes (clínicas)"""
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=True)
    nome_da_clinica = Column(String(150), nullable=False)
    telefone = Column(String(20), nullable=True)
    endereco = Column(String(200), nullable=True)
    link_empresa = Column(String(500), nullable=True)
    is_admin = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com dados do dashboard
    dados_dashboard = relationship("DadosDashboard", back_populates="cliente")
    # Relacionamento com procedimentos
    procedimentos = relationship("Procedimento", back_populates="cliente")

class DadosDashboard(Base):
    """Modelo para a tabela de dados do dashboard"""
    __tablename__ = 'dados_dashboard'
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    mes = Column(String(20), nullable=False)  # Janeiro, Fevereiro, etc.
    ano = Column(Integer, nullable=False, default=2024)
    
    # Dados de Leads
    leads_totais = Column(Integer, default=0)
    leads_google_ads = Column(Integer, default=0)
    leads_meta_ads = Column(Integer, default=0)
    leads_instagram_organico = Column(Integer, default=0)
    leads_indicacao = Column(Integer, default=0)
    leads_origem_desconhecida = Column(Integer, default=0)
    
    # Dados de Consultas Marcadas
    consultas_marcadas_totais = Column(Integer, default=0)
    consultas_marcadas_google_ads = Column(Integer, default=0)
    consultas_marcadas_meta_ads = Column(Integer, default=0)
    consultas_marcadas_ig_organico = Column(Integer, default=0)
    consultas_marcadas_indicacao = Column(Integer, default=0)
    consultas_marcadas_outros = Column(Integer, default=0)
    
    # Dados de Consultas Comparecidas
    consultas_comparecidas = Column(Integer, default=0)
    
    # Dados de Fechamentos
    fechamentos_totais = Column(Integer, default=0)
    fechamentos_google_ads = Column(Integer, default=0)
    fechamentos_meta_ads = Column(Integer, default=0)
    fechamentos_ig_organico = Column(Integer, default=0)
    fechamentos_indicacao = Column(Integer, default=0)
    fechamentos_outros = Column(Integer, default=0)
    
    # Dados Financeiros
    faturamento = Column(Float, default=0.0)
    valor_investido_total = Column(Float, default=0.0)  # Valor Investido Total (Realizado)
    orcamento_previsto_total = Column(Float, default=0.0)  # Orçamento Previsto Total
    orcamento_realizado_facebook = Column(Float, default=0.0)  # Orçamento Realizado Facebook Ads
    orcamento_previsto_facebook = Column(Float, default=0.0)  # Orçamento Previsto Facebook Ads
    orcamento_realizado_google = Column(Float, default=0.0)  # Orçamento Realizado Google Ads
    orcamento_previsto_google = Column(Float, default=0.0)  # Orçamento Previsto Google Ads
    
    # KPIs calculados (podem ser calculados dinamicamente ou armazenados)
    conversao_csm_leads = Column(Float, default=0.0)  # % de conversão Csm./leads
    conversao_csc_csm = Column(Float, default=0.0)  # % de conversão Csc./Csm.
    conversao_fechamento_csc = Column(Float, default=0.0)  # % de conversão fechamento/Csc.
    conversao_fechamento_leads = Column(Float, default=0.0)  # % de conversão fechamento/leads
    custo_por_compra_cirurgias = Column(Float, default=0.0)  # Custo por Compra (Cirurgias)
    roas = Column(Float, default=0.0)  # Retorno Sobre Investimento (ROAS)
    custo_por_lead_total = Column(Float, default=0.0)  # Custo por Lead Total
    custo_por_consulta_marcada = Column(Float, default=0.0)  # Custo por Consulta Marcada
    custo_por_consulta_comparecida = Column(Float, default=0.0)  # Custo por Consulta Comparecida
    ticket_medio = Column(Float, default=0.0)  # Ticket Médio
    
    # Taxas Ideais (thresholds)
    taxa_ideal_csm = Column(Float, default=10.0)  # Csm. = Consultas Marcadas >10%
    taxa_ideal_csc = Column(Float, default=50.0)  # Csc. = Consultas Comparecidas >50%
    taxa_ideal_fechamentos = Column(Float, default=40.0)  # Fechamentos >40%
    
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com cliente
    cliente = relationship("Cliente", back_populates="dados_dashboard")

class Procedimento(Base):
    """Modelo para a tabela de procedimentos"""
    __tablename__ = 'procedimentos'
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    
    # Datas do processo
    data_primeiro_contato = Column(DateTime, nullable=True)
    data_compareceu_consulta = Column(DateTime, nullable=True)
    data_fechou_cirurgia = Column(DateTime, nullable=True)
    
    # Dados do procedimento
    procedimento = Column(String(500), nullable=False)
    tipo = Column(String(100), nullable=True)  # Cosmiatria, Cirúrgico, etc.
    quantidade_na_mesma_venda = Column(Integer, default=1)
    
    # Dados financeiros
    forma_pagamento = Column(String(100), nullable=True)
    valor_da_venda = Column(Float, default=0.0)
    valor_parcelado = Column(Float, default=0.0)
    
    # Metadados
    mes_referencia = Column(String(20), nullable=False)  # Outubro, Novembro, etc.
    ano_referencia = Column(Integer, nullable=False, default=2024)
    
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com cliente
    cliente = relationship("Cliente", back_populates="procedimentos")

