import win32com.client as win32

def enviar_email(
        destinatario: str,
        assunto: str,
        corpo: str,
        arquivo: str = None
):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.to = destinatario
    mail.Subject = assunto
    mail.HTMLBody = corpo
    if arquivo:
        mail.Attachments.Add(arquivo)
    mail.Send()

if __name__ == '__main__':
    enviar_email(
        destinatario='lucas.mal2005@gmail.com',
        assunto='Dados Linkedin',
        corpo='Realizada busca de dados de pessoas no linkedin<br>Segue planilha...',
        arquivo=r'C:\RPA\LINKEDIN\assets\csv\dados_linkedin.csv'
    )