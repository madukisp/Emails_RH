import streamlit as st
import smtplib
from email.message import EmailMessage

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="RH - Processo de Admissão", page_icon="🦷", layout="wide")

st.title("🦷 Disparador de Admissão SBCD")
st.markdown("Preencha os dados abaixo para gerar e enviar o e-mail de aprovação.")

# --- BANCO DE DADOS (Listas para os Dropdowns) ---
# Você pode adicionar mais cargos aqui
LISTA_CARGOS = [
    "Auxiliar de Saúde Bucal",
    "Cirurgião Dentista",
    "Técnico de Enfermagem",
    "Recepcionista",
    "Auxiliar Administrativo",
    "Gerente de Unidade"
]

# Dicionário que liga o NOME DA UNIDADE ao ENDEREÇO DELA
# Adicione novas unidades seguindo o modelo: "Nome": "Endereço Completo"
LISTA_UNIDADES = {
    "UBS Jaçanã": "Rua São Geraldino, 222 - Jaçanã, São Paulo - SP, cep 02258-220",
    "UBS Vila Nova": "Rua Exemplo, 100 - Vila Nova, São Paulo - SP, cep 00000-000",
    "UBS Centro": "Av. Principal, 500 - Centro, São Paulo - SP, cep 11111-111",
    "Matriz Administrativa": "Av. Paulista, 1000 - Bela Vista, São Paulo - SP"
}

# --- BARRA LATERAL (Login) ---
with st.sidebar:
    st.header("🔐 Configuração de Envio")
    st.info("Para Gmail, lembre-se de usar a Senha de App.")
    sender_email = st.text_input("Seu E-mail", placeholder="exemplo@gmail.com")
    sender_password = st.text_input("Sua Senha de App", type="password")
    smtp_server = "smtp.gmail.com" # Altere para smtp.office365.com se for Outlook
    smtp_port = 587

# --- FORMULÁRIO ---
st.subheader("📝 Dados do Candidato e Vaga")

col1, col2 = st.columns(2)

with col1:
    nome_candidato = st.text_input("Nome Completo do Candidato", value="Evelyn Santos de Oliveira")
    email_candidato = st.text_input("E-mail do Candidato")
    cargo_selecionado = st.selectbox("Selecione o Cargo", LISTA_CARGOS)
    salario = st.text_input("Salário Bruto", value="R$ 3.429,74")

with col2:
    # O usuário escolhe o nome da unidade
    unidade_nome = st.selectbox("Selecione a Unidade", list(LISTA_UNIDADES.keys()))
    # O sistema busca o endereço automaticamente baseado na escolha acima
    endereco_automatico = LISTA_UNIDADES[unidade_nome]
    st.info(f"📍 Endereço vinculado: {endereco_automatico}")
    
    horario = st.text_input("Horário de Trabalho", value="07h00 às 16h00 - Segunda a Sexta-feira - 40 horas semanais")
    data_inicio = st.date_input("Data de Início")

# --- LÓGICA DO TEXTO ---
# Pega apenas o primeiro nome para a saudação (ex: Evelyn)
primeiro_nome = nome_candidato.split()[0] if nome_candidato else ""

assunto = f"Processo de Admissão SBCD – {nome_candidato}"

corpo_email = f"""
{primeiro_nome}, boa tarde! Espero que esteja bem.

Parabéns! Você foi aprovado para a vaga de {cargo_selecionado} na unidade {unidade_nome}. Detalhes da vaga:

• Salário Bruto: {salario}
• Benefícios: Vale Alimentação R$200,00/mês, Vale Refeição R$ 33,70/dia, Seguro de Vida e Vale Transporte
• Horário: {horario}
• Endereço: {endereco_automatico}
• Data de início: {data_inicio.strftime('%d/%m/%Y')}
 
Além disso, o setor de medicina entrará em contato com você ainda esta semana para agendar o exame médico. Fique atenta ao seu WhatsApp.
 
Para que a sua admissão seja efetuada, é imprescindível que você tenha recebido as vacinas obrigatórias.
 
Para a realização do seu exame admissional você deverá apresentar Documento original com foto + Comprovante Vacinal (original e atualizado);
Obrigatória apresentação do comprovante vacinal com as doses conforme esquema abaixo:
* 3 doses da Hepatite B ou se tiver anti-HBS (reagente);
* 3 doses da Dupla Adulto (DA) - difteria e tétano + Reforço a cada década;
* 2 doses da SCR (sarampo, caxumba, rubéola);
* Vacina contra o COVID-19 (Mínimo 3 doses).
 
Na ausência do comprovante vacinal ou caso estejam desatualizadas com as doses acima, dirija-se a UBS mais próxima antes de comparecer a SBCD sob a condição de retenção do ASO até a devida regularização vacinal (Em atendimento à NR-7 e NR-32).
 
Cronograma de Envio de Documentos:
Os documentos obrigatórios deverão ser enviados por meio do sistema (online), através de um link que você receberá em breve.
 
Para que possamos melhorar os processos de Recrutamento e Seleção pedimos que preencha a Pesquisa de Satisfação no link https://forms.office.com/r/EVb3ZQhe7C.
 
Atenciosamente,
Recursos Humanos SBCD
"""

# --- VISUALIZAÇÃO E ENVIO ---
st.divider()
st.subheader("👁️ Pré-visualização do E-mail")

# Mostra o texto exato que será enviado
st.text_area("Conteúdo:", value=corpo_email, height=400)

col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    enviar = st.button("🚀 Enviar E-mail", type="primary")

if enviar:
    if not sender_email or not sender_password:
        st.error("⚠️ Configure seu e-mail e senha na barra lateral!")
    elif not email_candidato:
        st.error("⚠️ Preencha o e-mail do candidato!")
    else:
        msg = EmailMessage()
        msg.set_content(corpo_email)
        msg['Subject'] = assunto
        msg['From'] = sender_email
        msg['To'] = email_candidato

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            st.success(f"✅ E-mail enviado com sucesso para {nome_candidato}!")
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao enviar: {e}")