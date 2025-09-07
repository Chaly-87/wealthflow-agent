# WealthFlow Agent - Manual do Usuário

**Versão:** 1.0  
**Data:** 7 de Setembro de 2025  

---

## Bem-vindo ao WealthFlow Agent

O WealthFlow Agent é seu CFO pessoal automatizado - um sistema inteligente que monitora mercados 24/7, identifica oportunidades de investimento e executa estratégias automaticamente. Este manual irá guiá-lo através de todas as funcionalidades da plataforma.

---

## Primeiros Passos

### 1. Acesso ao Sistema

Acesse o dashboard através do seu navegador web:
- **URL:** http://localhost:5173 (desenvolvimento) ou seu domínio personalizado
- **Navegadores suportados:** Chrome, Firefox, Safari, Edge (versões recentes)

### 2. Interface Principal

O dashboard é organizado em 5 seções principais:

**🏠 Dashboard:** Visão geral do seu portfólio e métricas principais  
**📈 Opportunities:** Oportunidades de investimento identificadas pela IA  
**🚨 Alerts:** Alertas e notificações em tempo real  
**⚙️ Strategies:** Configuração e monitoramento de estratégias  
**📊 Reports:** Relatórios e análises detalhadas  

### 3. Controles Principais

**Botão Start/Pause Monitoring:** Liga ou desliga o monitoramento automático  
**Configurações:** Acesso a preferências e configurações avançadas  
**Notificações:** Centro de alertas e mensagens importantes  

---

## Dashboard Principal

### Visão Geral do Portfólio

**Valor Total:** Exibe o valor atual do seu portfólio com variação diária  
**Alertas Ativos:** Número de alertas pendentes por prioridade  
**Ativos Monitorados:** Quantidade de ativos sendo acompanhados  

### Gráficos Interativos

**Performance do Portfólio:** Gráfico de linha mostrando evolução dos últimos 7 meses  
**Distribuição de Ativos:** Gráfico de pizza com alocação atual (Ações, Crypto, Cash)  

### Métricas em Tempo Real

- Valor do portfólio atualizado automaticamente a cada 5 segundos
- Variação percentual diária com indicadores visuais (verde/vermelho)
- Status do sistema (Live/Pausado) claramente identificado

---

## Oportunidades de Investimento

### Como Funciona

O sistema analisa continuamente:
- **Dados técnicos:** Preços, volumes, indicadores
- **Sentimentos:** Análise de redes sociais e notícias
- **Padrões:** Identificação de tendências emergentes

### Interpretando Oportunidades

Cada oportunidade mostra:

**Symbol:** Código do ativo (ex: AAPL, BTC)  
**Type:** Tipo de ativo (stock, crypto)  
**Score:** Pontuação de confiança (0-100%)  
**Price:** Preço atual e variação  
**Reason:** Motivo da recomendação  

### Scores de Confiança

- **90-100%:** Oportunidade excepcional, alta confiança
- **80-89%:** Boa oportunidade, confiança moderada-alta
- **70-79%:** Oportunidade interessante, confiança moderada
- **Abaixo de 70%:** Monitorar, mas aguardar confirmação

### Ações Recomendadas

**View Details:** Clique para análise detalhada  
**Monitor:** Adicionar à lista de observação  
**Execute:** Executar operação (se estratégias estiverem ativas)  

---

## Sistema de Alertas

### Tipos de Alertas

**🔴 High Priority (Vermelho):**
- Volume anômalo (3x+ do normal)
- Breakouts técnicos confirmados
- Mudanças súbitas de sentimento

**🟡 Medium Priority (Amarelo):**
- Spikes de sentimento positivo
- Aproximação de resistências/suportes
- Notícias relevantes

**🔵 Low Priority (Azul):**
- Metas de preço atingidas
- Atualizações de estratégias
- Relatórios disponíveis

### Gerenciando Alertas

**Marcar como Lido:** Clique no alerta para marcá-lo como visualizado  
**Filtros:** Use filtros para ver apenas alertas específicos  
**Configurações:** Personalize tipos de alertas que deseja receber  

### Notificações

Configure notificações por:
- Email
- SMS (planos premium)
- Webhook (integração com outros sistemas)

---

## Estratégias de Trading

### Estratégias Disponíveis

#### 1. RSI Momentum
**O que faz:** Identifica oportunidades baseadas em momentum de preços  
**Melhor para:** Mercados em tendência, ações de alta liquidez  
**Risco:** Moderado  
**Configurações principais:**
- Período RSI: 14 (padrão)
- Limite oversold: 30
- Limite overbought: 70
- Stop loss: 3%

#### 2. Mean Reversion
**O que faz:** Identifica ativos que se desviaram da média histórica  
**Melhor para:** Mercados laterais, correções temporárias  
**Risco:** Baixo-Moderado  
**Configurações principais:**
- Período de média: 20 dias
- Desvio padrão: 2.0
- Stop loss: 4%

#### 3. Sentiment Analysis
**O que faz:** Opera baseado em mudanças de sentimento nas redes sociais  
**Melhor para:** Criptomoedas, ações de alta volatilidade  
**Risco:** Alto  
**Configurações principais:**
- Threshold de sentimento: 0.3
- Janela de análise: 7 dias
- Delay de confirmação: 15 minutos

### Ativando Estratégias

1. Vá para a aba **Strategies**
2. Clique no botão de play/pause ao lado da estratégia
3. Ajuste parâmetros se necessário
4. Confirme a ativação

### Monitorando Performance

**Performance (%):** Retorno acumulado da estratégia  
**Trades:** Número de operações executadas  
**Status:** Ativo, pausado ou erro  
**Win Rate:** Percentual de trades lucrativos  

---

## Gestão de Risco

### Limites Automáticos

O sistema implementa proteções automáticas:

**Por Posição:** Máximo 2% do capital por operação  
**Perda Diária:** Máximo 5% de perda em um dia  
**Exposição Total:** Máximo 20% do capital exposto simultaneamente  

### Stop Loss Dinâmico

- Ajusta automaticamente baseado na volatilidade
- Protege contra gaps de mercado
- Pode ser personalizado por estratégia

### Alertas de Risco

O sistema alerta quando:
- Limites se aproximam (80% do limite)
- Perdas excedem parâmetros normais
- Volatilidade aumenta significativamente

---

## Relatórios

### Relatório Diário

Enviado automaticamente às 8:00 AM, inclui:

**Resumo de Performance:** Como seu portfólio performou  
**Top 3 Oportunidades:** Melhores oportunidades identificadas  
**Alertas de Bolha:** Setores que podem estar sobrevalorizados  
**Notícias Relevantes:** Notícias que podem impactar seus investimentos  

### Relatórios Personalizados

Configure relatórios com:
- Frequência personalizada (diário, semanal, mensal)
- Seções específicas de interesse
- Formato preferido (HTML, PDF, texto)
- Entrega por email ou download

### Métricas Importantes

**Sharpe Ratio:** Retorno ajustado ao risco  
**Maximum Drawdown:** Maior perda consecutiva  
**Win Rate:** Percentual de trades lucrativos  
**Profit Factor:** Relação lucro/prejuízo  

---

## Configurações Avançadas

### Preferências de Usuário

**Tolerância ao Risco:**
- Conservador: Foco em preservação de capital
- Moderado: Equilíbrio entre risco e retorno
- Agressivo: Foco em maximização de retornos

**Horários de Operação:**
- Definir quando estratégias podem operar
- Pausar durante eventos específicos
- Configurar fuso horário

### Integrações

**Corretoras Suportadas:**
- Alpaca Markets (ações americanas)
- Binance (criptomoedas)
- Interactive Brokers (global)

**Notificações:**
- Email: Configure SMTP personalizado
- Webhook: Integre com Slack, Discord, etc.
- SMS: Disponível em planos premium

### Backup e Segurança

**Backup Automático:** Dados salvos diariamente  
**Autenticação:** Use senhas fortes e 2FA quando disponível  
**Logs:** Todas as operações são registradas para auditoria  

---

## Solução de Problemas

### Problemas Comuns

**Sistema não está coletando dados:**
1. Verifique conexão com internet
2. Confirme se APIs estão configuradas
3. Verifique logs de erro

**Estratégias não estão executando:**
1. Confirme se estão ativadas
2. Verifique limites de risco
3. Confirme saldo disponível

**Dashboard não atualiza:**
1. Atualize a página (F5)
2. Verifique se backend está rodando
3. Limpe cache do navegador

### Logs e Diagnósticos

**Localização dos logs:** `~/wealthflow-system/logs/`  
**Comando para visualizar:** `tail -f wealthflow.log`  
**Filtrar erros:** `grep "ERROR" wealthflow.log`  

### Suporte

**Email:** suporte@wealthflow.com  
**Discord:** Comunidade WealthFlow  
**Documentação:** Manual técnico completo disponível  

---

## Dicas de Uso

### Para Iniciantes

1. **Comece com Paper Trading:** Teste estratégias sem risco real
2. **Use Limites Conservadores:** Comece com 1% por posição
3. **Monitore Diariamente:** Acompanhe performance e ajuste conforme necessário
4. **Leia os Relatórios:** Entenda o que o sistema está identificando

### Para Usuários Avançados

1. **Combine Estratégias:** Use múltiplas estratégias para diversificação
2. **Ajuste Parâmetros:** Otimize baseado em condições de mercado
3. **Use APIs:** Integre com seus próprios sistemas
4. **Analise Backtests:** Teste estratégias em dados históricos

### Melhores Práticas

**Diversificação:** Não concentre em um único ativo ou estratégia  
**Gestão de Risco:** Nunca arrisque mais do que pode perder  
**Educação Contínua:** Mantenha-se atualizado sobre mercados  
**Paciência:** Estratégias algorítmicas requerem tempo para mostrar resultados  

---

## Glossário

**RSI:** Relative Strength Index - indicador de momentum  
**Breakout:** Rompimento de resistência ou suporte  
**Sentiment:** Sentimento do mercado baseado em análise textual  
**Stop Loss:** Ordem automática para limitar perdas  
**Take Profit:** Ordem automática para realizar lucros  
**Slippage:** Diferença entre preço esperado e executado  
**Volatilidade:** Medida de variação de preços  
**Drawdown:** Perda máxima de um pico até um vale  

---

**Manual do Usuário - WealthFlow Agent v1.0**  
**Para suporte técnico, consulte a documentação completa ou entre em contato conosco.**

