import streamlit as st
import json
from datetime import date
from pathlib import Path

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="RH - Processo de Admissão", page_icon="🦷", layout="wide"
)


# --- FUNÇÕES AUXILIARES ---
def carregar_json(arquivo):
    """Carrega dados de um arquivo JSON"""
    caminho = Path("data") / arquivo
    if caminho.exists():
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return [] if arquivo == "candidatos.json" else {}


def candidato_ja_existe(email):
    """Verifica se o candidato já foi salvo anteriormente"""
    candidatos = carregar_json("candidatos.json")
    return any(c.get("email") == email for c in candidatos)


def salvar_candidato(dados):
    """Salva dados do candidato no JSON (apenas se não existir)"""
    if candidato_ja_existe(dados["email"]):
        return False  # Já existe, não salva novamente

    caminho = Path("data") / "candidatos.json"
    candidatos = carregar_json("candidatos.json")
    candidatos.append(dados)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(candidatos, f, ensure_ascii=False, indent=2)

    return True  # Salvou com sucesso


# --- CARREGAR DADOS ---
cargos = carregar_json("cargos.json")
unidades = carregar_json("unidades.json")

# --- INTERFACE ---
st.title("🦷 Disparador de Admissão SBCD")
st.markdown("Preencha os dados abaixo para gerar o texto do e-mail de aprovação.")

st.divider()

# --- FORMULÁRIO ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Dados do Candidato")
    nome_candidato = st.text_input(
        "Nome Completo", placeholder="Ex: Evelyn Santos de Oliveira"
    )
    email_candidato = st.text_input("E-mail", placeholder="candidato@email.com")
    cargo = st.selectbox("Cargo", cargos)

with col2:
    st.subheader("📍 Dados da Vaga")
    unidade = st.selectbox("Unidade", list(unidades.keys()))
    salario = st.text_input("Salário Bruto", value="R$ 3.429,74")
    data_inicio = st.date_input("Data de Início", value=date.today())

st.divider()

# --- BENEFÍCIOS ---
st.subheader("💰 Benefícios")
col_b1, col_b2, col_b3, col_b4 = st.columns(4)

with col_b1:
    vale_alimentacao = st.text_input("Vale Alimentação", value="R$ 200,00")
with col_b2:
    vale_refeicao = st.text_input("Vale Refeição", value="R$ 33,70/dia")
with col_b3:
    st.text_input("Seguro de Vida", value="Incluso", disabled=True)
with col_b4:
    st.text_input("Vale Transporte", value="Incluso", disabled=True)

st.divider()

# --- HORÁRIO ---
horario = st.text_input(
    "Horário de Trabalho",
    value="07h00 às 16h00 - Segunda a Sexta-feira - 40 horas semanais",
)

st.divider()

# --- CERTIFICAÇÃO SAFEWEB ---
st.subheader("🔐 Certificação Digital SafeWeb")
enviar_voucher = st.checkbox(
    "✅ Este cargo precisa de certificação SafeWeb (assinatura de prontuário)",
    value=False,
)

# --- GERAR EMAIL ---
st.divider()
st.subheader("📧 Texto do E-mail Gerado")

if nome_candidato and email_candidato:
    # Dados da unidade
    endereco = unidades[unidade]["endereco"]
    voucher = unidades[unidade]["voucher"]

    # Primeiro nome para saudação
    primeiro_nome = nome_candidato.split()[0]

    # --- CORPO DO EMAIL BASE ---
    corpo_email = f"""{primeiro_nome}, boa tarde! Espero que esteja bem.

Parabéns! Você foi aprovado(a) para a vaga de {cargo} na unidade {unidade}.

Detalhes da vaga:

- Salário Bruto: {salario}
- Benefícios: Vale Alimentação {vale_alimentacao}/mês, Vale Refeição {vale_refeicao}, Seguro de Vida e Vale Transporte
- Horário: {horario}
- Endereço: {endereco}
- Data de início: {data_inicio.strftime('%d/%m/%Y')}

Além disso, o setor de medicina entrará em contato com você ainda esta semana para agendar o exame médico. Fique atento(a) ao seu WhatsApp.

---

📋 VACINAÇÃO OBRIGATÓRIA

Para que a sua admissão seja efetuada, é imprescindível que você tenha recebido as vacinas obrigatórias.

Para a realização do seu exame admissional você deverá apresentar:
- Documento original com foto
- Comprovante Vacinal (original e atualizado)

Obrigatória apresentação do comprovante vacinal com as doses conforme esquema abaixo:
- 3 doses da Hepatite B ou se tiver anti-HBS (reagente)
- 3 doses da Dupla Adulto (DA) - difteria e tétano + Reforço a cada década
- 2 doses da SCR (sarampo, caxumba, rubéola)
- Vacina contra o COVID-19 (Mínimo 3 doses)

⚠️ Na ausência do comprovante vacinal ou caso estejam desatualizadas, dirija-se à UBS mais próxima antes de comparecer à SBCD sob a condição de retenção do ASO até a devida regularização vacinal (Em atendimento à NR-7 e NR-32).

---

📎 CRONOGRAMA DE ENVIO DE DOCUMENTOS

Os documentos obrigatórios deverão ser enviados por meio do sistema (online), através de um link que você receberá em breve.
"""

    # --- SEÇÃO SAFEWEB (SE NECESSÁRIO) ---
    if enviar_voucher:
        corpo_email += f"""
---

🔐 CADASTRO SAFE WEB - ASSINATURA DIGITAL

Para darmos continuidade ao seu processo admissional, é necessário realizar o seu cadastro no Safe Web, assinatura eletrônica necessária para as demandas diárias de sua função {cargo}.

Como realizar o cadastro:
1. Acesse o site: https://safeweb.gestaoar.com.br/Projetos/certificado/projetos?codrev=ProjetoSP
2. Utilize o seguinte voucher: {voucher}

⚠️ IMPORTANTE: 
- Para pessoas que possuem CNH Digital, o atendimento para a criação da assinatura será ONLINE.
- Para os que não possuem, o atendimento deverá ser presencial.

Após o cadastro:
Assim que você concluir o agendamento e a efetivação do seu cadastro na plataforma, solicitamos que envie as evidências (comprovantes) para o e-mail do RH.

Essas informações são essenciais para suas ações diárias na unidade de trabalho.
"""

    # --- RODAPÉ ---
    corpo_email += """
---

Para que possamos melhorar os processos de Recrutamento e Seleção, pedimos que preencha a Pesquisa de Satisfação no link: https://forms.office.com/r/EVb3ZQhe7C

Atenciosamente,
Recursos Humanos SBCD - Recrutamento e Seleção
"""

    # --- EXIBIR EMAIL ---
    st.text_area("Preview do E-mail:", value=corpo_email, height=400)

    # --- BOTÃO ÚNICO: COPIAR E SALVAR ---
    if st.button("📋 Copiar Texto do E-mail", type="primary", use_container_width=True):
        # Preparar dados para salvar
        dados_candidato = {
            "nome": nome_candidato,
            "email": email_candidato,
            "cargo": cargo,
            "unidade": unidade,
            "salario": salario,
            "data_inicio": data_inicio.strftime("%Y-%m-%d"),
            "beneficios": {
                "vale_alimentacao": vale_alimentacao,
                "vale_refeicao": vale_refeicao,
            },
            "certificacao_safeweb": enviar_voucher,
        }

        # Tentar salvar (só salva se não existir)
        foi_salvo = salvar_candidato(dados_candidato)

        # Feedback visual
        if foi_salvo:
            st.success(f"✅ Candidato {nome_candidato} salvo com sucesso!")

        st.info("📋 Texto copiado! Cole no corpo do e-mail.")

        # Copiar para área de transferência (via download)
        st.download_button(
            label="💾 Baixar como arquivo .txt",
            data=corpo_email,
            file_name=f"email_admissao_{nome_candidato.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

else:
    st.warning("⚠️ Preencha o nome e e-mail do candidato para gerar o texto do e-mail.")

# --- RODAPÉ ---
st.divider()
st.caption("💙 RH - Recrutamento e Seleção | SBCD")
